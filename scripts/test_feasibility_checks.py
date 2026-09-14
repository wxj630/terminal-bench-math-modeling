#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract tests for the programmatic feasibility gate.

Run with the repo venv:

    .venv/bin/python scripts/test_feasibility_checks.py

These are not unit tests of individual bounds. They enforce the two contracts
that keep the gate trustworthy when it runs unattended:

1. COVERAGE -- every task under tasks/ has a registered check, so a new task
   cannot ship ungated (this is the failure that let CUMCM 2024 C through).
2. ORACLE SELF-CONSISTENCY -- the O-award reference artifact for every task must
   PASS its own check. A gate that rejects the human outstanding solution is
   wrong by construction, so a red oracle means the bounds or the schema path
   are broken, not that the reference is bad.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = REPO_ROOT / "tasks"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from feasibility_checks import CHECKS, validate_artifact  # noqa: E402


def task_slugs() -> list[str]:
    return sorted(path.name for path in TASKS_ROOT.glob("*/*") if path.is_dir())


def oracle_artifacts() -> dict[str, Path]:
    """Map task slug -> the oracle reproduction result JSON shipped with it."""
    found: dict[str, Path] = {}
    for slug in task_slugs():
        candidates = sorted((TASKS_ROOT / "*" / slug / "solution" / "oracle").glob("**/result.json"))
        if candidates:
            found[slug] = candidates[0]
    return found


def check_coverage() -> list[str]:
    failures: list[str] = []
    for slug in task_slugs():
        if slug not in CHECKS:
            failures.append(f"COVERAGE: task '{slug}' has no registered feasibility check")
    return failures


def check_oracles() -> list[str]:
    failures: list[str] = []
    for slug, path in oracle_artifacts().items():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"ORACLE: could not read {path}: {exc}")
            continue
        result = validate_artifact(data, slug)
        if result.get("hard_errors"):
            failures.append(
                f"ORACLE: O-award reference for '{slug}' fails its own gate: "
                + "; ".join(result["hard_errors"])
            )
    return failures


def check_no_always_hard_fail() -> list[str]:
    """A check that hard-fails *every* input is a bug, not a gate."""
    failures: list[str] = []
    empty: dict[str, Any] = {}
    for slug in task_slugs():
        result = validate_artifact(empty, slug)
        if result.get("hard_errors"):
            failures.append(
                f"ROBUSTNESS: '{slug}' hard-fails an empty artifact (should warn, not error): "
                + result["hard_errors"][0]
            )
    return failures


def check_status_shape() -> list[str]:
    failures: list[str] = []
    for slug in task_slugs():
        result = validate_artifact({}, slug)
        for key in ("status", "hard_errors", "warnings", "evidence"):
            if key not in result:
                failures.append(f"SHAPE: '{slug}' result is missing the '{key}' field")
        if not isinstance(result.get("hard_errors"), list):
            failures.append(f"SHAPE: '{slug}' hard_errors is not a list")
    return failures


#: Synthetic artifacts that MUST be hard-rejected. Each entry is
#: (task slug, artifact, substring the error list must contain). This proves the
#: gate actually discriminates instead of always returning "pass", which is the
#: other way the coverage contract could be satisfied vacuously.
SYNTHETIC_VIOLATIONS: tuple[tuple[str, dict[str, Any], str], ...] = (
    (
        "cumcm-2024-a-dragon-dance",
        {"experiment_result": {"q5": {"max_head_speed_mps": 2.0, "max_speed_ratio_when_head_1mps": 1.6048}}},
        "exceeds the 2 m/s",
    ),
    (
        "cumcm-2023-c-vegetable-pricing",
        {"reproduced": {"correlation_comparison": [{"sales_markup_corr": 3.5}]}},
        "correlation coefficient",
    ),
    (
        "mcm-2024-b-submersible-search",
        {"experiment_result": {"search_strategy": {"find_probability_6h": 1.4}}},
        "search probability",
    ),
    (
        "mcm-2024-c-tennis-momentum",
        {"experiment_result": {"top_swing_features": [{"warning_correlation": -1.9}]}},
        "correlation coefficient",
    ),
    (
        "cumcm-2025-b-sic-thickness",
        {"joint_thickness_summary": [{"joint_two_beam_thickness_um": -3.0}]},
        "positive",
    ),
    (
        "mcm-2025-c-olympic-medals",
        {"monte_carlo_summary_top_total": [{"expected_total": 10.0, "expected_gold": 15.0}]},
        "gold medals exceed",
    ),
)


def check_synthetic_rejections() -> list[str]:
    failures: list[str] = []
    for slug, artifact, needle in SYNTHETIC_VIOLATIONS:
        result = validate_artifact(artifact, slug)
        errors = result.get("hard_errors") or []
        if not errors:
            failures.append(f"DISCRIMINATION: '{slug}' accepted a synthetic violation (expected an error mentioning '{needle}')")
            continue
        if not any(needle in message for message in errors):
            failures.append(
                f"DISCRIMINATION: '{slug}' rejected the artifact but for the wrong reason; "
                f"expected '{needle}' in {errors}"
            )
    return failures


def main() -> int:
    suites = (
        ("coverage", check_coverage()),
        ("oracle self-consistency", check_oracles()),
        ("no-always-hard-fail", check_no_always_hard_fail()),
        ("result shape", check_status_shape()),
        ("synthetic rejections", check_synthetic_rejections()),
    )
    failed = 0
    for name, failures in suites:
        if failures:
            failed += len(failures)
            print(f"FAIL {name}")
            for line in failures:
                print(f"  - {line}")
        else:
            print(f"ok   {name}")
    print()
    print(f"{len(task_slugs())} tasks, {failed} failure(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
