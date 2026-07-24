#!/bin/bash

# Enforce a maximum number of hyphen-separated tokens in the task folder name.
# Long slugs become unwieldy in CLI output, CI logs, and artifact paths.

MAX_TOKENS=5

if [ $# -lt 1 ]; then
    TASK_DIRS=$(find tasks -type f -name "task.toml" -exec dirname {} \; | sort)
else
    TASK_DIRS="$@"
fi

failed=0
for task_dir in $TASK_DIRS; do
    slug=$(basename "$task_dir")
    n=$(awk -F- '{print NF}' <<<"$slug")
    if [ "$n" -gt "$MAX_TOKENS" ]; then
        echo "FAIL $task_dir: slug has $n hyphen-separated tokens (max $MAX_TOKENS)"
        failed=1
    else
        echo "PASS $task_dir ($n tokens)"
    fi
done

exit $failed
