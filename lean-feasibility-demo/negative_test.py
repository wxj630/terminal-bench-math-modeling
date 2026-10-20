#!/usr/bin/env python3
"""Negative tests: mutate one artifact value at a time and require the build to FAIL.

A gate that cannot fail is not a gate. For each mutation we copy the whole artifact
tree to a scratch dir, patch exactly one numeric leaf, regenerate, and assert that
`lake build` now breaks AND that the broken obligation mentions the mutated field.

This is the discrimination contract, run end-to-end against the same generator the
real check uses -- not a synthetic unit test of an isolated predicate.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

DEMO = Path(__file__).resolve().parent
REPO = DEMO.parent
LAKE = Path.home() / ".elan" / "bin" / "lake"

# (task slug, json path, new value, what the failure must mention)
MUTATIONS: list[tuple[str, str, object, str]] = [
    # 1. range bound: probability out of [0,1]
    ("mcm-2024-c-tennis-momentum", "experiment_result.dual_temporal_bayes.final_match_warning_rate", 1.4,
     "final_match_warning_rate"),
    # 2. range bound: correlation out of [-1,1]
    ("cumcm-2023-c-vegetable-pricing", "reproduced.correlation_comparison.0.actual_sales_markup_corr", -3.2,
     "sales/markup correlation"),
    # 3. ordering: discount profit below waste profit
    ("cumcm-2024-c-crop-planting", "experiment_result.q1.discount_profit_yuan", 1000.0,
     "discount profit"),
    # 4. exact identity: head speed x ratio must equal the 2 m/s cap
    ("cumcm-2024-a-dragon-dance", "experiment_result.q5.max_head_speed_mps", 5.0,
     "head*ratio"),
    # 5. rate bound: sic thickness non-positive
    ("cumcm-2025-b-sic-thickness", "experiment_result.sic_recommended_thickness_um", -1.0,
     "sic_recommended_thickness_um"),
    # 6. ordering: interval reversed
    ("mcm-2025-c-olympic-medals", "monte_carlo_summary_top_total.0.total_interval95_low", 500.0,
     "interval low"),
    # 7. binary/domain: q3 decision bit not 0/1
    ("cumcm-2024-b-production-decision", "experiment_result.q3.decision_bits.0", 7,
     "decision_bits"),
    # 8. nonnegativity: negative acceptance index
    ("mcm-2025-b-juneau-tourism", "experiment_result.resident_acceptance_index", -2.0,
     "acceptance_index"),
    # 9. ordering: q95 below mean
    ("cumcm-2024-b-production-decision", "experiment_result.q4.posterior_rows.0.posterior_q95_defect_rate", 0.001,
     "q95"),
    # 10. partition/identity: single-scenario sum still equal, so mutate a species count to 0
    ("mcm-2023-a-plant-community", "reproduced.species_count_summary.0.species_count", 0,
     "count"),
]


def find_artifact(slug: str) -> Path:
    import glob
    for tree in ("jobs/ua-union-alpha-cumcm", "jobs/ua-union-alpha-mcm",
                 "jobs/opencode-deepseek-flash-cumcm-retry", "jobs/opencode-deepseek-flash-helio-retry3"):
        hits = sorted(glob.glob(f"{REPO / tree}/*{slug}__*/artifacts/root/results/{slug}_result.json"))
        if hits:
            return Path(hits[0])
    raise FileNotFoundError(slug)


def patch(data, path, value):
    keys = path.split(".")
    cur = data
    for k in keys[:-1]:
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    last = keys[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value


def stage(slug: str, mutation) -> Path:
    """Copy the repo's artifact tree to a scratch root, patched at one leaf."""
    scratch = Path("/tmp/lean-negtest-root")
    if scratch.exists():
        shutil.rmtree(scratch)
    for tree in ("jobs/ua-union-alpha-cumcm", "jobs/ua-union-alpha-mcm",
                 "jobs/opencode-deepseek-flash-cumcm-retry", "jobs/opencode-deepseek-flash-helio-retry3"):
        src = REPO / tree
        if src.is_dir():
            shutil.copytree(src, scratch / tree, symlinks=False,
                            ignore=shutil.ignore_patterns("*.txt", "trajectory.json"))
    if mutation:
        path, value, _ = mutation
        target = scratch / find_artifact(slug).relative_to(REPO)
        data = json.loads(target.read_text())
        patch(data, path, value)
        target.write_text(json.dumps(data, ensure_ascii=False))
    return scratch


def run_gen(root: Path):
    proc = subprocess.run([sys.executable, str(DEMO / "generate_check.py"), str(root)],
                          cwd=DEMO, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def failing_notes(out: str, cases: Path) -> list[str]:
    """The `-- note` comment immediately preceding each failing obligation line.

    Lean echoes the proposition but not our annotation, so we recover the traceable
    field name from the generated source at the reported line number.
    """
    import re
    notes = []
    lines = cases.read_text(encoding="utf-8").splitlines()
    for m in re.finditer(r"Cases\.lean:(\d+):", out):
        idx = int(m.group(1)) - 1
        # walk back to the nearest preceding comment line
        for j in range(idx, max(-1, idx - 4), -1):
            if lines[j].lstrip().startswith("--"):
                notes.append(lines[j])
                break
    return notes


def main() -> int:
    failures = []
    # baseline: unmutated scratch root must build
    code, out = run_gen(stage(None, None))
    if code != 0:
        print("BASELINE FAILED (clean copy did not build)")
        print(out[-2000:])
        return 1
    print("baseline: clean artifact copy builds OK\n")
    for i, (slug, path, value, needle) in enumerate(MUTATIONS, 1):
        code, out = run_gen(stage(slug, (path, value, needle)))
        broke = code != 0
        notes = failing_notes(out, DEMO / "FeasibilityDemo" / "Cases.lean")
        mentioned = any(needle in n for n in notes) or needle in out
        status = "ok  " if (broke and mentioned) else "FAIL"
        if not (broke and mentioned):
            failures.append((slug, path, broke, mentioned))
        print(f"{status} [{i:2d}] {slug:32s} {path} -> {value!r}  "
              f"build_failed={broke} error_cites_field={mentioned}")
        if broke and not mentioned:
            for n in notes[:3]:
                print(f"      cited: {n.strip()[:120]}")
        if not broke:
            print("      (build unexpectedly succeeded)")
    print()
    if failures:
        print(f"{len(failures)} negative test(s) did not behave as required")
        return 1
    print(f"all {len(MUTATIONS)} mutations rejected by the kernel, each citing its field")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
