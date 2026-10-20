#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract tests for multi-reference O-Eval.

Run: python3 scripts/test_multi_oracle_contracts.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EXPECTED_TASKS = 18
EXPECTED_PAPERS = 99
EXPECTED_PANELS = 67
OLYMPIC_FOURTH = "great_coach_model.recommendations[3].estimated_medal_count_gain"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _metric(path: str, oracle: float) -> dict[str, Any]:
    return {
        "path": path,
        "oracle_value": oracle,
        "outstanding_value": oracle,
        "baseline_value": None,
        "direction": "target_value",
        "normalization_mode": "legacy_target_distance_to_outstanding",
        "rel_scale": 0.12,
        "abs_scale": 1e-6,
        "weight": 1.0,
    }


def _fake_base(real_base, config: dict[str, Any], expected: dict[str, Any]):
    return SimpleNamespace(
        _score_config=lambda case: config,
        _expected_result=lambda case: expected,
        score_artifact_direction_aware=real_base.score_artifact_direction_aware,
        _raw=real_base._raw,
        _metric_exclusion_reason=real_base._metric_exclusion_reason,
    )


def _with_multi_root(multi, root: Path, fn):
    previous = multi.MULTI
    multi.MULTI = root
    try:
        return fn()
    finally:
        multi.MULTI = previous


def check_missing_field_keeps_paper(multi, real_base) -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        task = root / "task"
        task.mkdir()
        (task / "paper-a.json").write_text(
            json.dumps({"paper_id": "paper-a", "fields": {"result.a": 10.0}}),
            encoding="utf-8",
        )
        (task / "paper-b.json").write_text(
            json.dumps({"paper_id": "paper-b", "fields": {"result.b": 20.0}}),
            encoding="utf-8",
        )
        config = {"metrics": [_metric("result.a", 10.0), _metric("result.b", 20.0)]}
        base = _fake_base(real_base, config, {"result": {"a": 10.0, "b": 20.0}})
        builder = SimpleNamespace(CASES=[SimpleNamespace(year=2024, slug="task")])

        def run():
            return multi.evaluate(
                base,
                builder,
                {"model": {}},
                lambda model, case, score_config: {
                    "metrics": [{"path": "result.a", "found": True, "actual": 10.0}]
                },
            )

        result = _with_multi_root(multi, root, run)
        record = result["tasks"]["task"]["per_model"]["model"]
        if abs(record["o_eval"] - 0.5) > 1e-12:
            failures.append(
                f"MISSING FIELD: expected mean 0.5 over both papers, got {record['o_eval']!r}"
            )
        if record["n_oracles_scored"] != 2:
            failures.append(
                "MISSING FIELD: a paper with zero overlapping model fields was dropped "
                f"(n_oracles_scored={record['n_oracles_scored']!r})"
            )
    return failures


def check_missing_artifact_is_zero(multi, real_base) -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        task = root / "task"
        task.mkdir()
        (task / "paper.json").write_text(
            json.dumps({"paper_id": "paper", "fields": {"result.a": 10.0}}),
            encoding="utf-8",
        )
        config = {"metrics": [_metric("result.a", 10.0)]}
        base = _fake_base(real_base, config, {"result": {"a": 10.0}})
        builder = SimpleNamespace(CASES=[SimpleNamespace(year=2024, slug="task")])

        def run():
            return multi.evaluate(
                base, builder, {"model": {}}, lambda model, case, score_config: None
            )

        record = _with_multi_root(multi, root, run)["tasks"]["task"]["per_model"]["model"]
        if record["o_eval"] != 0.0 or not record.get("missing_artifact"):
            failures.append(f"MISSING ARTIFACT: expected hard zero, got {record!r}")
    return failures


def check_fallback_only_without_usable_paper(multi, real_base) -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        task = root / "task"
        task.mkdir()
        (task / "paper.json").write_text(
            json.dumps({"paper_id": "paper", "fields": {"unscored.value": 99.0}}),
            encoding="utf-8",
        )
        config = {"metrics": [_metric("result.a", 10.0)]}
        base = _fake_base(real_base, config, {"result": {"a": 10.0}})
        builder = SimpleNamespace(CASES=[SimpleNamespace(year=2024, slug="task")])

        def run():
            return multi.evaluate(
                base,
                builder,
                {"model": {}},
                lambda model, case, score_config: {
                    "metrics": [{"path": "result.a", "found": True, "actual": 10.0}]
                },
            )

        task_record = _with_multi_root(multi, root, run)["tasks"]["task"]
        if not task_record.get("fallback_to_reproduction"):
            failures.append("FALLBACK: no usable human field did not trigger reproduction fallback")
        if task_record["per_model"]["model"]["o_eval"] != 1.0:
            failures.append(
                "FALLBACK: model matching the reproduction should score 1.0, got "
                f"{task_record['per_model']['model']['o_eval']!r}"
            )
    return failures


def check_real_panel_contracts(multi, base, builder) -> list[str]:
    failures: list[str] = []
    paper_count = 0
    panel_count = 0
    olympic_checked = False
    for case in builder.CASES:
        if case.year not in (2023, 2024, 2025):
            continue
        config = base._score_config(case)
        paper_count += len(list((multi.MULTI / case.slug).glob("*.json")))
        panels = multi.paper_panels(case.slug, config, base._metric_exclusion_reason)
        panel_count += len(panels)
        for panel in panels:
            values = {m["path"]: m["oracle_value"] for m in panel["config"]["metrics"]}
            raw = base._raw(
                base.score_artifact_direction_aware(multi._nest(values), panel["config"])
            )
            if abs(raw - 1.0) > 1e-12:
                failures.append(
                    f"PAPER SELF-SCORE: {case.slug}/{panel['paper_id']} scored {raw!r}"
                )
        if case.slug == "mcm-2025-c-olympic-medals":
            olympic_checked = True
            for panel in panels:
                paths = {m["path"] for m in panel["config"]["metrics"]}
                if OLYMPIC_FOURTH in paths:
                    failures.append(
                        f"OLYMPIC: excluded fourth recommendation leaked into {panel['paper_id']}"
                    )
                if panel["n_scored_in_task"] != 4:
                    failures.append(
                        "OLYMPIC: coverage denominator must contain four active metrics, got "
                        f"{panel['n_scored_in_task']!r}"
                    )
    if paper_count != EXPECTED_PAPERS:
        failures.append(f"COVERAGE: expected {EXPECTED_PAPERS} paper files, got {paper_count}")
    if panel_count != EXPECTED_PANELS:
        failures.append(f"COVERAGE: expected {EXPECTED_PANELS} usable panels, got {panel_count}")
    if not olympic_checked:
        failures.append("OLYMPIC: task was not checked")
    return failures


def check_fixed_task_denominator(board) -> list[str]:
    failures: list[str] = []
    try:
        board._mean_over_tasks([1.0] * (EXPECTED_TASKS - 1))
    except ValueError:
        pass
    except Exception as exc:
        failures.append(f"TASK DENOMINATOR: wrong exception for 17 tasks: {exc!r}")
    else:
        failures.append("TASK DENOMINATOR: 17 tasks were silently accepted")
    try:
        value = board._mean_over_tasks([1.0] * EXPECTED_TASKS)
    except Exception as exc:
        failures.append(f"TASK DENOMINATOR: 18 tasks raised {exc!r}")
    else:
        if value != 1.0:
            failures.append(f"TASK DENOMINATOR: mean of 18 ones was {value!r}")
    return failures


def check_derivation_provenance(multi) -> list[str]:
    failures: list[str] = []
    derived_fields = 0
    for path in sorted(multi.MULTI.glob("*/*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        derivations = data.get("derivations") or {}
        if "DERIVED" in str(data.get("notes", "")) and not derivations:
            failures.append(f"DERIVATION: {path.relative_to(ROOT)} marks DERIVED without metadata")
        for field, derivation in derivations.items():
            derived_fields += 1
            if field not in (data.get("fields") or {}):
                failures.append(f"DERIVATION: {path.name}/{field} is absent from fields")
                continue
            kind = derivation.get("kind")
            values = derivation.get("reported_values")
            try:
                if kind == "relative_improvement_pct_higher_is_better":
                    expected = 100.0 * (float(values["adaptive"]) - float(values["fixed"])) / float(values["fixed"])
                elif kind == "relative_improvement_pct_lower_is_better":
                    expected = 100.0 * (float(values["fixed"]) - float(values["adaptive"])) / float(values["fixed"])
                elif kind == "sum_reported_components":
                    expected = sum(float(value) for value in values)
                else:
                    failures.append(f"DERIVATION: {path.name}/{field} has unknown kind {kind!r}")
                    continue
            except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
                failures.append(f"DERIVATION: {path.name}/{field} cannot be recomputed: {exc}")
                continue
            declared = float(derivation.get("computed_value"))
            field_value = float(data["fields"][field])
            if abs(round(expected, 2) - declared) > 1e-12 or abs(declared - field_value) > 1e-12:
                failures.append(
                    f"DERIVATION: {path.name}/{field} expected {expected!r}, "
                    f"declared {declared!r}, field {field_value!r}"
                )
    if derived_fields != 6:
        failures.append(f"DERIVATION: expected 6 audited derived fields, got {derived_fields}")
    return failures


def check_recovery_manifest(multi) -> list[str]:
    failures: list[str] = []
    manifest = json.loads((multi.MULTI / "MODEL_ARTIFACT_RECOVERY.json").read_text(encoding="utf-8"))
    recoveries = manifest.get("recoveries") or []
    if len(recoveries) != 2:
        failures.append(f"RECOVERY: expected 2 recovery records, got {len(recoveries)}")
    for recovery in recoveries:
        artifact_path = ROOT / recovery["artifact_path"]
        if not artifact_path.exists():
            failures.append(f"RECOVERY: missing artifact {artifact_path.relative_to(ROOT)}")
            continue
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        provenance = artifact.get("_recovery_provenance") or {}
        if provenance.get("trajectory_sha256") != recovery.get("source_trajectory_sha256"):
            failures.append(f"RECOVERY: hash mismatch in {artifact_path.relative_to(ROOT)}")
        if provenance.get("evidence_steps") != recovery.get("evidence_steps"):
            failures.append(f"RECOVERY: evidence-step mismatch in {artifact_path.relative_to(ROOT)}")
        for field, expected in recovery["fields"].items():
            found, actual = _get_path(artifact, field)
            if not found or abs(float(actual) - float(expected)) > 1e-12:
                failures.append(
                    f"RECOVERY: {artifact_path.name}/{field} is {actual!r}, expected {expected!r}"
                )
    return failures


def _get_path(data: dict[str, Any], path: str) -> tuple[bool, Any]:
    current: Any = data
    for token in path.split("."):
        if not isinstance(current, dict) or token not in current:
            return False, None
        current = current[token]
    return True, current


def check_multimodal_renderer(figures) -> list[str]:
    failures: list[str] = []
    report = ROOT / "jobs" / "multimodal-multi-oracle-2023-2025.md"
    previous_filter = set(figures.MODEL_FILTER)
    previous_currency = figures.COST_CURRENCY
    figures.MODEL_FILTER = {
        "codex + gpt-5.5 xhigh",
        "opencode + deepseek-flash",
        "opencode + deepseek-flash (max)",
        "codex + GPT-6 Astra",
        "claude-code + Fable 5.1",
    }
    figures.set_cost_currency("usd")
    try:
        rows = figures.parse_report(report)
        actual_costs = {round(float(row.cost), 2) for row in rows if row.cost is not None}
    finally:
        figures.MODEL_FILTER = previous_filter
        figures.set_cost_currency(previous_currency)
    if len(rows) != 5:
        failures.append(f"RENDERER: expected 5 multimodal rows, got {len(rows)}")
    if {row.artifacts for row in rows} != {17, 18}:
        failures.append(f"RENDERER: artifact counts are {[row.artifacts for row in rows]!r}")
    expected_costs = {2.54, 2.78, 99.37, 246.41, 272.80}
    if actual_costs != expected_costs:
        failures.append(f"RENDERER: USD costs are {sorted(actual_costs)!r}")
    return failures


def main() -> int:
    base = _load("multi_contract_base", "write_direction_aware_flash_baseline_eval_2024_2025.py")
    multi = _load("multi_contract_eval", "write_multi_oracle_eval.py")
    board = _load("multi_contract_board", "write_multimodal_multi_oracle.py")
    figures = _load("multi_contract_figures", "write_aa_style_eval_figures.py")
    builder = base._load_builder()
    suites = (
        ("missing model field keeps paper", check_missing_field_keeps_paper(multi, base)),
        ("missing artifact is zero", check_missing_artifact_is_zero(multi, base)),
        ("fallback semantics", check_fallback_only_without_usable_paper(multi, base)),
        ("real paper panels", check_real_panel_contracts(multi, base, builder)),
        ("fixed 18-task denominator", check_fixed_task_denominator(board)),
        ("derived reference provenance", check_derivation_provenance(multi)),
        ("model artifact recovery manifest", check_recovery_manifest(multi)),
        ("five-model renderer", check_multimodal_renderer(figures)),
    )
    failed = 0
    for name, problems in suites:
        if problems:
            failed += len(problems)
            print(f"FAIL {name}")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(f"ok   {name}")
    print()
    print(f"{failed} failure(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
