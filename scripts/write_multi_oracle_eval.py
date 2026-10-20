#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Multi-oracle O-Eval: average the oracle-normalised score over every O-award paper.

Why
---
The benchmark originally anchored each task to ONE reproduced O-award paper. But a
modeling problem has many defensible solutions, and different human teams report
different numbers. Anchoring on one paper rewards "matching that paper" rather than
"modeling well". This module lets every human O-award paper be a reference.

Definition
----------
For task t let the scored metrics be M(t), and let P(t) be the set of O-award papers.
Paper p reports a subset S_p subset M(t). Write R(m, S) for the weighted panel score
of submission m restricted to the metrics in S (weights renormalised over S).

  O-Eval(m, t) = mean over { p in P(t) : S_p non-empty } of  R(m, S_p)

Because a paper matches its own reported values exactly, R(p, S_p) = 1, so each
paper contributes "how close is the model to THIS human answer, on the fields that
human actually reported". Papers are weighted equally: one human solution, one vote.
A paper that reports only one field therefore acts as a single-field check, which is
the honest treatment of an incomplete report -- excluding such a paper outright would
throw away the only human evidence for that field.

Fallback
--------
If no O-award paper reports any scored field (it happens: the MCM answers are often
prose or figures), the task keeps the original reproduced anchor. Those tasks are
flagged in the output so a reader knows the score rests on a single reproduction.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
MULTI = ROOT / "oracle-multi"
OUT = ROOT / "jobs" / "multi-oracle-eval.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def paper_panels(
    task_slug: str,
    config: dict[str, Any],
    exclusion_reason=None,
) -> list[dict[str, Any]]:
    """Every O-award paper for this task that reports at least one active metric."""
    scored = {
        m["path"]: m
        for m in config["metrics"]
        if float(m.get("score_weight", m.get("weight", 1.0)) or 0.0) > 0.0
        and (exclusion_reason is None or exclusion_reason(m, config) is None)
    }
    panels: list[dict[str, Any]] = []
    for path in sorted((MULTI / task_slug).glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        fields = data.get("fields") or {}
        subset = {p: v for p, v in fields.items() if p in scored and v is not None}
        if not subset:
            continue
        # Build a score_config restricted to the fields this paper reports, with the
        # paper's own value as the anchor. Weights keep their configured ratio.
        metrics = []
        for p, value in subset.items():
            metric = dict(scored[p])
            metric["oracle_value"] = float(value)
            metric["outstanding_value"] = float(value)
            metric["baseline_value"] = None
            metric["normalization_mode"] = metric.get(
                "normalization_mode", "legacy_target_distance_to_outstanding"
            )
            if metric["normalization_mode"] == "baseline_to_outstanding_target_minmax":
                # A paper is not a baseline/outstanding pair; score by target distance.
                metric["normalization_mode"] = "legacy_target_distance_to_outstanding"
            metrics.append(metric)
        panel_config = dict(config)
        panel_config["metrics"] = metrics
        panels.append(
            {
                "paper_id": data.get("paper_id", path.stem),
                "source": data.get("source"),
                "n_fields": len(subset),
                "n_scored_in_task": len(scored),
                "coverage": len(subset) / max(len(scored), 1),
                "config": panel_config,
                "notes": data.get("notes", ""),
            }
        )
    return panels


def evaluate(base, builder, models: dict[str, Any], model_artifact) -> dict[str, Any]:
    """O-Eval averaged over human papers, per task, for each registered model."""
    out: dict[str, Any] = {"tasks": {}, "models": {}}
    for case in builder.CASES:
        if case.year not in (2023, 2024, 2025):
            continue
        config = base._score_config(case)
        panels = paper_panels(case.slug, config, base._metric_exclusion_reason)
        record: dict[str, Any] = {
            "n_papers_total": len(list((MULTI / case.slug).glob("*.json"))),
            "n_oracles_used": len(panels),
            "oracles": [
                {"paper_id": p["paper_id"], "n_fields": p["n_fields"],
                 "coverage": round(p["coverage"], 3), "notes": p["notes"][:200]}
                for p in panels
            ],
            "per_model": {},
        }
        if not panels:
            # Fallback: the original reproduced anchor, as a single-paper panel.
            oracle_details = base.score_artifact_direction_aware(
                base._expected_result(case), config
            )
            fallback = {"paper_id": "REPRODUCTION", "n_fields": len(config["metrics"]),
                        "coverage": 1.0, "config": config, "notes": "reproduced anchor"}
            panels = [fallback]
            record["fallback_to_reproduction"] = True

        for model in models:
            det = model_artifact(model, case, config)
            if det is None:
                # Match the single-anchor board's protocol: a missing or non-scoreable
                # artifact scores 0 on this task and STAYS in the denominator. Dropping
                # it would let a model that failed three tasks average over only its
                # best ones.
                record["per_model"][model] = {
                    "o_eval": 0.0,
                    "n_oracles_scored": 0,
                    "per_paper": [],
                    "missing_artifact": True,
                }
                continue
            # Re-score the model on each paper's field subset.
            values = {}
            for item in det.get("metrics", []):
                if item.get("found") and item.get("actual") is not None:
                    values[item["path"]] = item["actual"]
            per_paper = []
            for panel in panels:
                # Keep the paper in the denominator even when the model omits one
                # of the paper's reported fields. The scorer gives a missing metric
                # reward of 0; dropping the whole paper here would let a model avoid
                # difficult fields by omission and would violate the one-paper-one-vote
                # definition.
                sub = dict(panel["config"])
                sub["metrics"] = list(panel["config"]["metrics"])
                details = base.score_artifact_direction_aware(_nest(values), sub)
                raw = base._raw(details)
                per_paper.append({
                    "paper_id": panel["paper_id"],
                    "score": max(0.0, min(1.0, raw)),
                    "n": len(sub["metrics"]),
                    "found": sum(1 for item in details["metrics"] if item.get("found")),
                })
            used = [p for p in per_paper if p["n"] > 0]
            mean_o = sum(p["score"] for p in used) / len(used) if used else 0.0
            record["per_model"][model] = {
                "o_eval": mean_o,
                "n_oracles_scored": len(used),
                "per_paper": per_paper,
            }
        out["tasks"][case.slug] = record
    return out


def _nest(values: dict[str, float]) -> dict[str, Any]:
    """Rebuild a nested artifact dict from {dotted.path: value}."""
    import re
    root: dict[str, Any] = {}
    for path, value in values.items():
        tokens = re.findall(r"[^.\[\]]+|\[\d+\]", path)
        cur: Any = root
        for i, tok in enumerate(tokens[:-1]):
            nxt = tokens[i + 1]
            if tok.startswith("["):
                idx = int(tok[1:-1])
                while len(cur) <= idx:
                    cur.append(None)
                if cur[idx] is None:
                    cur[idx] = [] if nxt.startswith("[") else {}
                cur = cur[idx]
            else:
                if tok not in cur or cur[tok] is None:
                    cur[tok] = [] if nxt.startswith("[") else {}
                cur = cur[tok]
        last = tokens[-1]
        if last.startswith("["):
            idx = int(last[1:-1])
            while len(cur) <= idx:
                cur.append(None)
            cur[idx] = value
        else:
            cur[last] = value
    return root


def main() -> int:
    base = _load("base", SCRIPTS / "write_direction_aware_flash_baseline_eval_2024_2025.py")
    board = _load("board", SCRIPTS / "write_all_models_boeval_2023_2025.py")
    builder = base._load_builder()
    models = board.model_config(builder)
    board.MODELS = models
    base.MODELS = models

    def artifact(model, case, config):
        return base._score_model_artifact_direction_aware(
            model, case, case.output_name, config
        )

    result = evaluate(base, builder, models, artifact)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{'task':34s} {'papers':>7s} {'used':>5s} {'fallback':>9s}")
    for slug, rec in result["tasks"].items():
        print(f"{slug:34s} {rec['n_papers_total']:>7d} {rec['n_oracles_used']:>5d} "
              f"{'YES' if rec.get('fallback_to_reproduction') else '-':>9s}")

    print()
    print(f"{'model':34s} {'mean O-Eval (multi-oracle)':>28s}")
    names = [k for k in models]
    for model in names:
        vals = [rec["per_model"].get(model)["o_eval"]
                for rec in result["tasks"].values()
                if rec["per_model"].get(model)]
        if vals:
            print(f"{model:34s} {100*sum(vals)/len(vals):>27.2f}%  (n={len(vals)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
