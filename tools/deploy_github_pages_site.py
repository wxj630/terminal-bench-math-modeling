#!/usr/bin/env python3
"""Deploy jobs/github-pages-site to the repository's gh-pages branch.

This keeps the local preview, main branch copy, and published GitHub Pages
branch from drifting apart.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "jobs" / "github-pages-site"
WORKTREE = Path("/tmp/tb-mathmodel-gh-pages")
REMOTE = "origin"
PAGES_BRANCH = "gh-pages"
PAGES_URL = "https://wxj630.github.io/terminal-bench-math-modeling/"


def run(command: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def ensure_clean(path: Path) -> None:
    status = run(["git", "status", "--short"], cwd=path).stdout.strip()
    if status:
        raise SystemExit(f"Refusing to deploy with dirty worktree at {path}:\n{status}")


def image_sources(index_html: str) -> list[str]:
    sources: list[str] = []
    for src in re.findall(r'<img[^>]+src="([^"]+)"', index_html):
        parsed = urlsplit(src)
        if parsed.scheme or parsed.netloc:
            continue
        sources.append(parsed.path)
    return sources


def local_href_sources(index_html: str) -> list[str]:
    sources: list[str] = []
    for href in re.findall(r'<a[^>]+href="([^"]+)"', index_html):
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or parsed.path in {"", "."}:
            continue
        if parsed.path.startswith("#"):
            continue
        sources.append(parsed.path)
    return sources


def markdown_figure_sources(markdown: str) -> list[str]:
    sources: list[str] = []
    for rel in re.findall(r"`(figures/aa-style-2023-2025-[^`]+\.(?:png|svg))`", markdown):
        sources.append(f"reports/{rel}")
    for rel in re.findall(r"!\[[^\]]*\]\((figures/aa-style-2023-2025-[^)]+\.(?:png|svg))\)", markdown):
        sources.append(f"reports/{rel}")
    return sources


def with_existing_companions(rel_paths: list[str]) -> list[str]:
    expanded: set[str] = set(rel_paths)
    for rel in rel_paths:
        path = SITE_DIR / rel
        if path.suffix.lower() == ".png":
            companion = path.with_suffix(".svg")
        elif path.suffix.lower() == ".svg":
            companion = path.with_suffix(".png")
        else:
            continue
        if companion.exists():
            expanded.add(str(companion.relative_to(SITE_DIR)))
    return sorted(expanded)


def clean_unreferenced_figures(allowed: set[str]) -> None:
    for folder in [WORKTREE / "assets" / "figures", WORKTREE / "reports" / "figures"]:
        if not folder.exists():
            continue
        for figure in folder.glob("aa-style-2023-2025-*"):
            rel = str(figure.relative_to(WORKTREE))
            if rel not in allowed:
                figure.unlink()


def copy_site() -> tuple[list[str], bool]:
    if not SITE_DIR.exists():
        raise SystemExit(f"Missing site directory: {SITE_DIR}")
    created_worktree = False
    if WORKTREE.exists():
        ensure_clean(WORKTREE)
    else:
        run(["git", "worktree", "add", str(WORKTREE), PAGES_BRANCH])
        created_worktree = True

    index_html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    sources = image_sources(index_html)
    linked_sources = local_href_sources(index_html)
    report_path = SITE_DIR / "reports" / "full-report.md"
    report_sources = markdown_figure_sources(report_path.read_text(encoding="utf-8")) if report_path.exists() else []
    report_files = [
        str(path.relative_to(SITE_DIR))
        for path in (SITE_DIR / "reports").glob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".md", ".json"}
    ]
    required = [
        "index.html",
        "reports/full-report.md",
        *linked_sources,
        *report_files,
        *with_existing_companions([*sources, *report_sources]),
    ]
    copied: list[str] = []
    for rel in required:
        src = SITE_DIR / rel
        dst = WORKTREE / rel
        if not src.exists():
            raise SystemExit(f"Missing required site file: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)
    clean_unreferenced_figures(set(copied))
    return sorted(set(copied)), created_worktree


def commit_and_push(message: str) -> bool:
    status = run(["git", "status", "--short"], cwd=WORKTREE).stdout.strip()
    if not status:
        print("gh-pages already matches local site.")
        return False
    print(status)
    run(["git", "add", "-A"], cwd=WORKTREE)
    run(["git", "commit", "-m", message], cwd=WORKTREE)
    run(["git", "push", REMOTE, PAGES_BRANCH], cwd=WORKTREE)
    return True


def verify_online(timeout_s: int = 120) -> None:
    local_html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    sources = image_sources(local_html)
    deadline = time.time() + timeout_s
    last_error = ""
    while time.time() < deadline:
        try:
            html = urlopen(
                Request(PAGES_URL + f"?deploy_check={int(time.time())}", headers={"Cache-Control": "no-cache", "User-Agent": "TB-MathModel-deploy"}),
                timeout=20,
            ).read().decode("utf-8", "replace")
            if "TB-MathModel" not in html:
                raise RuntimeError("online HTML does not look like TB-MathModel")
            mismatches: list[str] = []
            for rel in sources:
                local_bytes = (SITE_DIR / rel).read_bytes()
                remote_bytes = urlopen(
                    Request(urljoin(PAGES_URL, rel) + f"?deploy_check={int(time.time())}", headers={"Cache-Control": "no-cache", "User-Agent": "TB-MathModel-deploy"}),
                    timeout=20,
                ).read()
                if hashlib.sha256(local_bytes).digest() != hashlib.sha256(remote_bytes).digest():
                    mismatches.append(rel)
            if not mismatches:
                print("Online Pages verification passed.")
                return
            last_error = "asset mismatch: " + ", ".join(mismatches)
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
        time.sleep(10)
    raise SystemExit(f"Online Pages verification failed: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--message", default="Deploy GitHub Pages site", help="Commit message for gh-pages.")
    parser.add_argument("--skip-verify", action="store_true", help="Skip online hash verification.")
    args = parser.parse_args()

    copied, created_worktree = copy_site()
    try:
        print(f"Prepared {len(copied)} files for gh-pages.")
        commit_and_push(args.message)
        if not args.skip_verify:
            verify_online()
    finally:
        if created_worktree:
            run(["git", "worktree", "remove", str(WORKTREE)], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
