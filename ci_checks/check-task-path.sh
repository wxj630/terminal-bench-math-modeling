#!/usr/bin/env bash
#
# Validate a task folder path: tasks/<contest>/<task>/
#
# - 3-segment path (tasks/CUMCM/<task>/ or tasks/MCM/<task>/)
# - <contest> is one of CUMCM or MCM
# - If task.toml exists, its [metadata].domain matches the contest folder and
#   [metadata].field is math-modeling
#
# Usage: check-task-path.sh [task-dir ...]

set -e

if [ $# -eq 0 ]; then
    TASK_DIRS=$(find tasks -type f -name "task.toml" -exec dirname {} \; | sort)
else
    TASK_DIRS=""
    for task_dir in "$@"; do
        TASK_DIRS="$TASK_DIRS ${task_dir%/}"
    done
fi

FAILED=0
for TASK_DIR in $TASK_DIRS; do
python3 - "$TASK_DIR" <<'PYEOF' || FAILED=1
import os, sys

task_dir = sys.argv[1]

CONTESTS = {"CUMCM", "MCM"}

parts = task_dir.split("/")

if not parts or parts[0] != "tasks":
    print(f"FAIL {task_dir}: not under tasks/")
    sys.exit(1)

if len(parts) != 3:
    print(f"FAIL {task_dir}: path must match tasks/<contest>/<task>/ (got {len(parts)} segments).")
    sys.exit(1)

contest, _ = parts[1], parts[2]

if contest not in CONTESTS:
    print(f"FAIL {task_dir}: '{contest}' is not a valid contest directory.")
    print(f"     Valid: {', '.join(sorted(CONTESTS))}")
    sys.exit(1)

# Validate task.toml [metadata].domain / [metadata].field match the first-class contest layout.
toml_path = os.path.join(task_dir, "task.toml")
if os.path.isfile(toml_path):
    try:
        import tomllib
        with open(toml_path, "rb") as f:
            tdata = tomllib.load(f)
        def slug(s):
            # Normalize: lowercase + collapse whitespace + replace spaces with hyphens.
            return "-".join((s or "").lower().split())

        meta = tdata.get("metadata", {})
        toml_domain = (meta.get("domain") or "").strip()
        toml_field = (meta.get("field") or "").strip()

        errs = []
        if toml_domain and toml_domain.upper() != contest:
            errs.append(f"task.toml [metadata].domain = '{toml_domain}' but folder is under '{contest}'")
        if toml_field and slug(toml_field) != "math-modeling":
            errs.append(f"task.toml [metadata].field = '{toml_field}' but TB-MathModeling expects 'math-modeling'")
        if errs:
            for e in errs:
                print(f"FAIL {task_dir}: {e}")
            sys.exit(1)
    except Exception:
        # task.toml parsing failures are check-task-fields' problem, not ours.
        pass

sys.exit(0)
PYEOF
done

exit "$FAILED"
