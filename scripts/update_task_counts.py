#!/usr/bin/env python3
"""Update README task-count markers for the first-class contest directories."""

import re
from pathlib import Path


def count_tasks(contest_path: str) -> int:
    path = Path(contest_path)
    if not path.exists():
        return 0
    return sum(1 for d in path.iterdir() if d.is_dir() and (d / "task.toml").exists())


def main() -> None:
    counts = {
        "CUMCM_COUNT": count_tasks("tasks/CUMCM"),
        "MCM_COUNT": count_tasks("tasks/MCM"),
    }
    counts["TOTAL_COUNT"] = sum(counts.values())

    readme_path = Path("README.md")
    content = readme_path.read_text(encoding="utf-8")

    for marker, count in counts.items():
        if marker == "TOTAL_COUNT":
            pattern = rf"(<!--{marker}-->\s*\*\*)\d+(\*\*)"
            replacement = rf"\g<1>{count}\2"
        else:
            pattern = rf"(<!--{marker}-->)\s*\d+"
            replacement = rf"\g<1> {count}"
        content = re.sub(pattern, replacement, content)

    badge_pattern = r"(\[!\[Tasks\]\(https://img\.shields\.io/badge/tasks-)\d+(-white\.svg\)\])"
    content = re.sub(badge_pattern, rf"\g<1>{counts['TOTAL_COUNT']}\2", content)

    readme_path.write_text(content, encoding="utf-8")

    print("Updated task counts in README.md")
    for marker, count in sorted(counts.items()):
        print(f"  {marker}: {count}")
