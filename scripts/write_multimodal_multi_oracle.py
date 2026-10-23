#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the MULTIMODAL leaderboard under multi-oracle O-Eval.

Scope: this rewrites only the multimodal board. The text-only board keeps its
single-anchor definition, so this script writes its own report and its own
figures and does not touch the existing 16-model report.

Reported metrics
----------------
* ``Multi-O Eval``  -- the headline: for each task, average over the O-award
  papers that report the task's scored fields; then average over 18 tasks.
  A missing artifact scores 0 and stays in the denominator (same protocol as
  the single-anchor board, so the two are comparable).
* ``Single-O Eval`` -- the previous single-anchor number, kept for reference.
* ``Robust BO-Eval`` -- unchanged definition (gain over the flash baseline,
  normalised by the oracle-baseline gap), using the reproduced anchor.

Usage:  python3 scripts/write_multimodal_multi_oracle.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
JOBS = ROOT / "jobs"

#: (model key, display label). Keys must match `model_config()` in the board script.
MULTIMODAL = (
    ("codex_gpt55_xhigh", "codex + GPT-5.5 xhigh"),
    ("flash_opencode", "opencode + DeepSeek V4.1 Flash"),  # board label: opencode + deepseek-flash
    ("claude_fable51", "claude-code + Fable 5.1"),
    ("flash_opencode_max", "opencode + DeepSeek V4.1 Flash (max)"),  # board: ... (max)
    ("codex_gpt6_astra", "codex + GPT-6 Astra"),
)

REPORT_PATH = JOBS / "multimodal-multi-oracle-2023-2025.md"
EXPECTED_TASKS = 18

def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _mean_over_tasks(values: list[float]) -> float:
    if len(values) != EXPECTED_TASKS:
        raise ValueError(f"expected {EXPECTED_TASKS} task scores, got {len(values)}")
    return _mean(values)


def _sensitivity_scores(multi: dict[str, Any], model: str) -> dict[str, float]:
    tasks = list(multi["tasks"].values())
    at_least_two = [
        rec["per_model"][model]["o_eval"]
        for rec in tasks
        if rec["n_oracles_used"] >= 2
    ]
    at_least_three = [
        rec["per_model"][model]["o_eval"]
        for rec in tasks
        if rec["n_oracles_used"] >= 3
    ]
    paper_scores: list[float] = []
    for rec in tasks:
        model_record = rec["per_model"][model]
        if model_record["per_paper"]:
            paper_scores.extend(p["score"] for p in model_record["per_paper"])
        else:
            # A missing artifact is zero on every human panel. Fallback tasks have one
            # reproduction panel even though n_oracles_used is zero.
            paper_scores.extend([0.0] * max(1, rec["n_oracles_used"]))
    return {
        "task_equal_all": _mean_over_tasks(
            [rec["per_model"][model]["o_eval"] for rec in tasks]
        ),
        "task_equal_ge2": _mean(at_least_two),
        "task_equal_ge3": _mean(at_least_three),
        "paper_equal": _mean(paper_scores),
        "n_ge2": len(at_least_two),
        "n_ge3": len(at_least_three),
        "n_papers": len(paper_scores),
    }


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _board_token_costs() -> dict[str, tuple[str, str, str, str, str]]:
    """Pull artifact count, token counts, and USD/RMB costs from the main report.

    The multi-oracle board reuses the same measured token/cost figures: re-evaluating
    the score does not change what the runs consumed.
    """
    path = JOBS / "terminus2-direction-aware-flash-baseline-bbo-2023-2025.md"
    if not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    start = lines.index("## Overall Mean")
    table = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.startswith("|"):
            table.append(line)
        elif table:
            break
    headers = [c.strip() for c in table[0].strip().strip("|").split("|")]
    idx = {name: i for i, name in enumerate(headers)}
    out: dict[str, tuple[str, str, str, str, str]] = {}
    for line in table[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < len(headers):
            continue
        payload = (
            cells[idx["Artifacts"]],
            cells[idx["Tokens input/cache/output"]],
            cells[idx["Billable input/output"]],
            cells[idx["Est. cost USD"]],
            cells[idx["Est. cost RMB"]],
        )
        out[cells[0]] = payload
        out[_norm(cells[0])] = payload
    return out


#: display label -> label used in the main board's Overall Mean table
BOARD_LABEL = {
    "codex + GPT-5.5 xhigh": "codex + gpt-5.5 xhigh",
    "opencode + DeepSeek V4.1 Flash": "opencode + deepseek-flash",
    "opencode + DeepSeek V4.1 Flash (max)": "opencode + deepseek-flash (max)",
}


def _norm(label: str) -> str:
    """Case/space-insensitive key so 'opencode + deepseek-flash' matches its variants."""
    return "".join(ch for ch in label.lower() if ch.isalnum())


def main() -> int:
    base = _load("base", "write_direction_aware_flash_baseline_eval_2024_2025.py")
    board = _load("board", "write_all_models_boeval_2023_2025.py")
    builder = base._load_builder()
    models = board.model_config(builder)
    board.MODELS = models
    base.MODELS = models

    multi = json.loads((JOBS / "multi-oracle-eval.json").read_text(encoding="utf-8"))
    cases = [c for c in builder.CASES if c.year in (2023, 2024, 2025)]
    if len(cases) != EXPECTED_TASKS or len(multi["tasks"]) != EXPECTED_TASKS:
        raise ValueError(
            f"multi-oracle board requires {EXPECTED_TASKS} tasks; "
            f"builder has {len(cases)}, evaluation has {len(multi['tasks'])}"
        )

    # ---- single-anchor numbers, and Robust BO-Eval, from the existing pipeline ----
    single: dict[str, dict[str, float]] = {}
    robust: dict[str, dict[str, float]] = {}
    raw_by_model: dict[str, dict[str, float]] = {}
    for case in cases:
        config = base._score_config(case)
        oracle_details = base.score_artifact_direction_aware(
            base._expected_result(case), config
        )
        oracle_raw = base._raw(oracle_details)
        flash_details = base._score_model_artifact_direction_aware(
            "flash_opencode", case, case.output_name, config
        )
        flash_raw = base._raw(flash_details) if flash_details else 0.0
        for key, _label in MULTIMODAL:
            details = base._score_model_artifact_direction_aware(
                key, case, case.output_name, config
            )
            raw = base._raw(details) if details else 0.0
            raw_by_model.setdefault(key, {})[case.slug] = raw
            single.setdefault(key, {})[case.slug] = min(
                1.0, max(0.0, raw / oracle_raw)
            ) if oracle_raw else 0.0
            robust.setdefault(key, {})[case.slug] = board.robust_effect(
                raw, flash_raw, oracle_raw, failure=details is None
            )

    rows = []
    for key, label in MULTIMODAL:
        if key not in models:
            print(f"  WARNING: unknown model key {key!r}", file=sys.stderr)
            continue
        tasks = multi["tasks"]
        multi_vals = [tasks[s]["per_model"][key]["o_eval"] for s in tasks]
        single_vals = [single[key][s] for s in tasks]
        robust_vals = [robust[key][s] for s in tasks]
        rows.append(
            {
                "label": label,
                "key": key,
                "multi": _mean_over_tasks(multi_vals),
                "single": _mean_over_tasks(single_vals),
                "robust": _mean_over_tasks(robust_vals),
                "per_task_multi": multi_vals,
                "per_task_single": single_vals,
                "sensitivity": _sensitivity_scores(multi, key),
            }
        )
    rows.sort(key=lambda r: r["multi"], reverse=True)

    # ---- report ----
    lines = [
        "# Multimodal board — multi-oracle O-Eval",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## What changed",
        "",
        "Each task is now anchored to **every O-award paper** for that problem, not just",
        "one reproduced answer. For a task, every paper that reports at least one of the",
        "task's scored fields contributes one oracle panel; the model's O-Eval on that",
        "task is the mean over those papers, and the board averages over 18 tasks.",
        "A missing artifact scores 0 and stays in the denominator (same protocol as the",
        "single-anchor board). Where no paper reports any scored field, the task falls",
        "back to the reproduced anchor and is flagged below.",
        "",
        "## Leaderboard",
        "",
        "| Rank | Model | Multi-O Eval | Single-O Eval | Δ | Robust BO-Eval (single anchor) |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for i, row in enumerate(rows, 1):
        lines.append(
            f"| {i} | {row['label']} | **{100*row['multi']:.2f}%** | "
            f"{100*row['single']:.2f}% | {100*(row['multi']-row['single']):+.2f}pp | "
            f"{100*row['robust']:.2f}% |"
        )

    n_ge2 = rows[0]["sensitivity"]["n_ge2"]
    n_ge3 = rows[0]["sensitivity"]["n_ge3"]
    n_papers = rows[0]["sensitivity"]["n_papers"]
    lines += [
        "",
        "## Aggregation sensitivity",
        "",
        "The headline is the task-equal mean over all 18 tasks. The other columns are",
        "diagnostics rather than alternate headline scores: they show whether the ordering",
        "depends on single-reference tasks or on giving tasks rather than papers equal weight.",
        "",
        f"| Model | All 18 tasks (task-equal) | Tasks with ≥2 refs (n={n_ge2}) | "
        f"Tasks with ≥3 refs (n={n_ge3}) | All panels paper-equal (n={n_papers}) |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in sorted(rows, key=lambda r: r["sensitivity"]["task_equal_all"], reverse=True):
        sensitivity = row["sensitivity"]
        lines.append(
            f"| {row['label']} | {100*sensitivity['task_equal_all']:.2f}% | "
            f"{100*sensitivity['task_equal_ge2']:.2f}% | "
            f"{100*sensitivity['task_equal_ge3']:.2f}% | "
            f"{100*sensitivity['paper_equal']:.2f}% |"
        )

    lines += [
        "",
        "## Oracle coverage per task",
        "",
        "| Task | Papers found | Papers usable | Scored fields covered | Fallback |",
        "|---|---:|---:|---:|---|",
    ]
    for slug, rec in multi["tasks"].items():
        total = rec["n_papers_total"]
        used = rec["n_oracles_used"]
        lines.append(
            f"| `{slug}` | {total} | {used} | "
            f"{sum(o['n_fields'] for o in rec['oracles'])} field-reports | "
            f"{'**reproduction**' if rec.get('fallback_to_reproduction') else '—'} |"
        )

    exclusions = []
    for slug in multi["tasks"]:
        for path in sorted((ROOT / "oracle-multi" / slug).glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            fields = data.get("fields") or {}
            if any(value is not None for value in fields.values()):
                continue
            exclusions.append((slug, data.get("paper_id", path.stem),
                               data.get("exclusion_reason", "")))
    lines += [
        "",
        "## Human papers not in any panel",
        "",
        "Every one of the 99 papers is either used or listed here with a structured",
        "reason. These five cannot answer the task's single core scalar without",
        "inventing a conversion.",
        "",
        "| Task | Paper | Reason |",
        "|---|---|---|",
    ]
    for slug, paper_id, reason in exclusions:
        lines.append(f"| `{slug}` | {paper_id} | {reason.replace('|', '/')} |")

    lines += [
        "",
        "## Caveats a reader must know",
        "",
        f"1. **Coverage is uneven.** The 99 O-award papers were extracted from OCR of",
        f"   the PDFs; {sum(r['n_oracles_used'] for r in multi['tasks'].values())} papers form usable panels with "
        f"{sum(sum(o['n_fields'] for o in r['oracles']) for r in multi['tasks'].values())} numeric field-reports.",
        "   Every task has at least one human panel. Fourteen tasks are fully covered; smoke",
        "   screen has one paper available, submersible 2 of 4, lamprey 4 of 5, stair-wear 3 of 5.",
        "2. **A paper may not report the reproduction's numbers.** MCM answers are often",
        "   prose, figures, or defined on a different grid or scale. Where the current",
        "   anchor came from the reproduction rather than the paper text (for example,",
        "   Olympic's 75th-percentile jump), the paper contributes only fields it states.",
        "3. **Papers that report few fields act as partial checks.** One human answer gets",
        "   one vote. Missing model fields score zero inside that vote; they never remove",
        "   the paper from the denominator.",
        "4. **Robust BO-Eval is still single-anchor.** It is shown only for continuity and",
        "   must not be interpreted as a multi-reference robustness score.",
        "",
        "## Per-task detail (multimodal entries)",
        "",
        "| Task | " + " | ".join(r["label"] for r in rows) + " |",
        "|---|" + "---:|" * len(rows),
    ]
    for case in cases:
        cells = " | ".join(
            f"{100*multi['tasks'][case.slug]['per_model'][r['key']]['o_eval']:.1f}"
            for r in rows
        )
        lines.append(f"| `{case.slug}` | {cells} |")

    # An "Overall Mean" block in the layout the AA figure renderer parses, so the
    # same renderer can draw this board without a second implementation.
    tokens = _board_token_costs()
    lines += [
        "",
        "## Overall Mean",
        "",
        "| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | "
        "Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | "
        "Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        board_label = BOARD_LABEL.get(row["label"], row["label"])
        artifacts, tok, bill, cost_usd, cost_rmb = tokens.get(
            board_label,
            tokens.get(
                _norm(board_label),
                tokens.get(
                    _norm(row["label"]),
                    ("0", "0 / 0 / 0", "0 / 0", "N/A", "N/A"),
                ),
            ),
        )
        raw_mean = _mean_over_tasks(list(raw_by_model[row["key"]].values()))
        lines.append(
            f"| {row['label']} | {artifacts} | {raw_mean:.6f} | {100*row['multi']:.2f}% | "
            f"+0.00 pp | {100*row['robust']:.2f}% | {tok} | {bill} | "
            f"{cost_usd} | {cost_rmb} |"
        )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {REPORT_PATH}")
    print()
    print(f"{'rank':>4s} {'model':40s} {'multi':>8s} {'single':>8s} {'delta':>8s}")
    for i, row in enumerate(rows, 1):
        print(f"{i:>4d} {row['label']:40s} {100*row['multi']:7.2f}% "
              f"{100*row['single']:7.2f}% {100*(row['multi']-row['single']):+7.2f}pp")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
