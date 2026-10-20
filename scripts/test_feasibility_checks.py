#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract tests for the programmatic feasibility gate.

Run with the repo venv:

    .venv/bin/python scripts/test_feasibility_checks.py

These are not unit tests of individual bounds. They enforce the two contracts
that keep the gate trustworthy when it runs unattended:

1. COVERAGE -- every task under tasks/ has a registered check, so a new task
   cannot ship ungated (this is the failure that let CUMCM 2024 C through).
1. COVERAGE -- every task under tasks/ has a registered check, so a new task
   cannot ship ungated (this is the failure that let CUMCM 2024 C through).
2. ORACLE SELF-CONSISTENCY -- the O-award reference artifact for every task must
   PASS its own check. A gate that rejects the human outstanding solution is
   wrong by construction, so a red oracle means the bounds or the schema path
   are broken, not that the reference is bad.
   The reference is `tasks/<contest>/<slug>/tests/expected_result.json`: it is the
   reproduction the task's own scoring is anchored to, and (unlike the saved model
   artifacts under `jobs/`, which are gitignored) it is present in CI. An earlier
   version of this suite globbed `solution/oracle/**/result.json`, which matches
   nothing in the repo, so it passed forever without checking anything; the
   oracle-coverage suite below makes that regression impossible to reintroduce.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = REPO_ROOT / "tasks"
JOBS_ROOT = REPO_ROOT / "jobs"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from feasibility_checks import CHECKS, validate_artifact  # noqa: E402


def task_slugs() -> list[str]:
    return sorted(path.name for path in TASKS_ROOT.glob("*/*") if path.is_dir())


def oracle_artifacts() -> dict[str, Path]:
    """Map task slug -> the committed O-award reference result JSON."""
    found: dict[str, Path] = {}
    for slug in task_slugs():
        candidates = sorted(TASKS_ROOT.glob(f"*/{slug}/tests/expected_result.json"))
        if candidates:
            found[slug] = candidates[0]
    return found


def check_oracle_coverage() -> list[str]:
    """Every task must have a reference artifact on disk.

    Without this, a path change silently empties `oracle_artifacts()` and the
    self-consistency suite passes vacuously -- the exact bug this file shipped with.
    """
    missing = [slug for slug in task_slugs() if slug not in oracle_artifacts()]
    return [
        f"ORACLE-COVERAGE: no reference artifact at tasks/*/{slug}/tests/expected_result.json"
        for slug in missing
    ]


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


#: Real saved model artifacts to discriminate on. Each entry is
#: (task slug, JSON path, replacement value, substring the error must contain).
#: These use the actual field paths and scales agents emit, so they exercise the
#: gate on real data rather than on a hand-built minimal object. Skipped (not
#: failed) when the `jobs/` tree is absent, as it is in CI.
SAVED_ARTIFACT_MUTATIONS: tuple[tuple[str, str, Any, str], ...] = (
    ("mcm-2024-c-tennis-momentum",
     "experiment_result.dual_temporal_bayes.final_match_warning_rate", 1.4, "warning rate"),
    ("cumcm-2023-c-vegetable-pricing",
     "reproduced.correlation_comparison.0.actual_sales_markup_corr", -3.2, "correlation coefficient"),
    ("cumcm-2025-b-sic-thickness",
     "experiment_result.sic_recommended_thickness_um", -1.0, "positive"),
    ("mcm-2025-c-olympic-medals",
     "monte_carlo_summary_top_total.0.total_interval95_low", 500.0, "interval is reversed"),
    ("mcm-2025-b-juneau-tourism",
     "experiment_result.resident_acceptance_index", -2.0, "negative"),
    ("mcm-2023-a-plant-community",
     "reproduced.species_count_summary.0.pielou_evenness", 1.4, "Pielou evenness"),
)


def _has_path(data: Any, path: str) -> bool:
    """True when `path` (dotted, with [i] indices) resolves inside `data`."""
    import re as _re
    tokens = _re.findall(r"[^.\[\]]+|\[\d+\]", path)
    cur = data
    for tok in tokens:
        if tok.startswith("["):
            idx = int(tok[1:-1])
            if not isinstance(cur, list) or idx >= len(cur):
                return False
            cur = cur[idx]
        else:
            if not isinstance(cur, dict) or tok not in cur:
                return False
            cur = cur[tok]
    return True


def _newest_saved_artifact(slug: str, required_path: str | None = None) -> Path | None:
    """The most recent saved result JSON for `slug` that carries `required_path`.

    Some saved artifacts are partial by design (a submission that only reports the
    scored fields). Those cannot exercise a mutation of a field they do not have, so
    we pick the newest artifact that actually contains the target path.
    """
    hits: list[Path] = []
    for tree in JOBS_ROOT.glob("*"):
        if not tree.is_dir():
            continue
        hits.extend(tree.glob(f"{slug}__*/artifacts/root/results/{slug}_result.json"))
    if not hits:
        return None
    hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if required_path is None:
        return hits[0]
    for candidate in hits:
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if _has_path(data, required_path):
            return candidate
    return None


def _set_path(data: Any, path: str, value: Any) -> None:
    keys = path.split(".")
    cursor = data
    for key in keys[:-1]:
        cursor = cursor[int(key)] if isinstance(cursor, list) else cursor[key]
    last = keys[-1]
    if isinstance(cursor, list):
        cursor[int(last)] = value
    else:
        cursor[last] = value


def check_saved_artifact_rejections() -> list[str]:
    """Mutate one field of a real saved artifact and require a hard rejection.

    This is the same discrimination contract as the synthetic suite, but run
    against actual agent output: real paths, real scales, real surrounding data.
    """
    failures: list[str] = []
    exercised = 0
    for slug, path, value, needle in SAVED_ARTIFACT_MUTATIONS:
        source = _newest_saved_artifact(slug, path)
        if source is None:
            continue
        exercised += 1
        data = json.loads(source.read_text(encoding="utf-8"))
        try:
            _set_path(data, path, value)
        except (KeyError, IndexError, TypeError):
            failures.append(f"SAVED: '{slug}' has no field at {path} in {source}")
            continue
        result = validate_artifact(data, slug)
        errors = result.get("hard_errors") or []
        if not errors:
            failures.append(f"SAVED: '{slug}' accepted {path}={value!r} in {source}")
        elif not any(needle in message for message in errors):
            failures.append(
                f"SAVED: '{slug}' rejected {path}={value!r} but for the wrong reason; "
                f"expected '{needle}' in {errors}"
            )
    if exercised == 0:
        print("     (no saved artifacts under jobs/; suite skipped)")
    return failures


def main() -> int:
    suites = (
        ("coverage", check_coverage()),
        ("oracle coverage", check_oracle_coverage()),
        ("oracle self-consistency", check_oracles()),
        ("no-always-hard-fail", check_no_always_hard_fail()),
        ("result shape", check_status_shape()),
        ("synthetic rejections", check_synthetic_rejections()),
        ("saved-artifact rejections", check_saved_artifact_rejections()),
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
