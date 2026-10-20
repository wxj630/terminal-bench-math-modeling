#!/usr/bin/env python3
"""Check the Lean obligation generator against the in-repo reference artifacts.

Two inputs matter for this layer:

  * the saved agent artifacts under `jobs/` -- what `verify.sh` audits (they carry
    rich per-row data); and
  * the committed O-award references at `tasks/<contest>/<slug>/tests/expected_result.json`
    -- the same input the Python gate's oracle suite uses.

This script runs the generator (no Lean build) against the *references* and reports
how many obligations each yields, so the two layers can be compared on identical
input. It exits non-zero if any reference is missing or crashes the generator --
including if it carries a non-finite number, which is treated as missing evidence.
"""
from __future__ import annotations

import glob
import importlib.util
import json
import sys
from pathlib import Path

DEMO = Path(__file__).resolve().parent
REPO = DEMO.parent

spec = importlib.util.spec_from_file_location("gen", DEMO / "generate_check.py")
gen = importlib.util.module_from_spec(spec)
sys.modules["gen"] = gen
spec.loader.exec_module(gen)


def main() -> int:
    total = skipped = 0
    problems: list[str] = []
    for slug, _tree, fn in gen.TASKS:
        hits = glob.glob(f"{REPO}/tasks/*/{slug}/tests/expected_result.json")
        if not hits:
            problems.append(f"{slug}: no reference artifact")
            continue
        data = json.loads(Path(hits[0]).read_text(encoding="utf-8"))
        e = gen.Emitter()
        try:
            fn(data, e)
        except Exception as exc:  # noqa: BLE001 - report any generator crash
            problems.append(f"{slug}: generator raised {type(exc).__name__}: {exc}")
            continue
        total += e.count
        skipped += len(e.skipped)
        flag = f"  [{len(e.skipped)} skipped]" if e.skipped else ""
        print(f"  {slug:38s} {e.count:3d} obligations{flag}")
    print()
    print(f"references: {total} obligations, {skipped} skipped, {len(problems)} problem(s)")
    for p in problems:
        print(f"  PROBLEM: {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
