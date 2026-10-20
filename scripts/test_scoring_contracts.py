#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract tests for the direction-aware scoring layer.

These lock in two properties that the leaderboard depends on and that are easy to
break silently:

1. ORACLE SELF-CONSISTENCY -- the outstanding reproduction must score a panel of
   exactly 1.0 on every task. If it does not, the anchors or the schema paths are
   wrong, and every downstream O-Eval is meaningless.
2. ONE-SIDED DIRECTIONAL SCORING -- on a `higher_is_better` metric, a result at or
   above the outstanding value is never a failure (it is at least as good), and
   symmetrically for `lower_is_better`. Regression here silently penalises models
   for beating the paper.

Run:  python3 scripts/test_scoring_contracts.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check_oracle_self_consistency(base, builder) -> list[str]:
    failures = []
    checked = 0
    for case in builder.CASES:
        config = base._score_config(case)
        raw = base._raw(base.score_artifact_direction_aware(base._expected_result(case), config))
        checked += 1
        if raw is None or abs(raw - 1.0) > 1e-9:
            failures.append(f"ORACLE: {case.slug} reproduction scores {raw!r}, expected 1.0")
    if checked == 0:
        failures.append("ORACLE: no tasks were checked")
    return failures


def _synthetic(actual: float, oracle: float, direction: str, baseline: float | None = None) -> dict:
    metric = {
        "path": "experiment_result.probe",
        "oracle_value": oracle,
        "outstanding_value": oracle,
        "direction": direction,
        "rel_scale": 0.12,
        "abs_scale": 1e-6,
        "weight": 1.0,
        "found": True,
    }
    if baseline is not None:
        metric["baseline_value"] = baseline
        metric["normalization_mode"] = "baseline_to_outstanding_target_minmax"
    return metric


def check_one_sided(base) -> list[str]:
    failures = []
    cases = (
        ("higher_is_better", 15.0, 10.0, None),   # above the paper -> full credit
        ("higher_is_better", 10.0, 10.0, None),   # exactly the paper
        ("lower_is_better", 5.0, 10.0, None),     # below the paper -> full credit
        ("higher_is_better", 15.0, 10.0, 8.0),    # endpoint mode, above -> full credit
        ("lower_is_better", 5.0, 10.0, 12.0),     # endpoint mode, below -> full credit
    )
    for direction, actual, oracle, baseline in cases:
        metric = _synthetic(actual, oracle, direction, baseline)
        reward = base._metric_score(actual, metric)
        label = f"{direction} actual={actual} oracle={oracle} baseline={baseline}"
        if reward < 1.0 - 1e-9:
            failures.append(
                f"ONE-SIDED: {label} scored {reward:.4f} < 1.0; meeting or beating the "
                "outstanding value must never be penalised"
            )
    return failures


def main() -> int:
    base = _load("dascore", "write_direction_aware_flash_baseline_eval_2024_2025.py")
    builder = base._load_builder()
    suites = (
        ("oracle self-consistency", check_oracle_self_consistency(base, builder)),
        ("one-sided directional scoring", check_one_sided(base)),
    )
    failed = 0
    for name, problems in suites:
        if problems:
            failed += len(problems)
            print(f"FAIL {name}")
            for line in problems:
                print(f"  - {line}")
        else:
            print(f"ok   {name}")
    print()
    print(f"{len(builder.CASES)} tasks, {failed} failure(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
