#!/usr/bin/env bash
# End-to-end verification for the Lean feasibility layer.
#
#   1. generate the obligations from the real saved artifacts (jobs/)
#   2. kernel-check them (these must all pass)
#   3. print the trust audit (no sorryAx / no native_decide)
#   4. run the discrimination suite (mutations must make the build fail)
#   5. run the generator against the in-repo reference artifacts too
#
# Requires Lean 4 via elan on PATH:  export PATH="$HOME/.elan/bin:$PATH"
set -euo pipefail
cd "$(dirname "$0")"

REPO_ROOT="$(cd .. && pwd)"

echo "== 1/5 generate obligations from saved agent artifacts =="
python3 generate_check.py "$REPO_ROOT"

echo
echo "== 2/5 kernel check =="
lake build

echo
echo "== 3/5 trust audit (expect only propext / Quot.sound, or none) =="
lake build 2>&1 | grep -E "depends on axioms|does not depend" | sed 's/^info: //'

echo
echo "== 4/5 discrimination suite (each mutation must break the build) =="
python3 negative_test.py

echo
echo "== 5/5 generator also runs on the committed reference artifacts =="
python3 check_references.py

echo
echo "ALL GREEN"
