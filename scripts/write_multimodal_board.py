#!/usr/bin/env python3
"""Emit the multimodal leaderboard's figures using the existing AA renderers.

The site's visuals are AA-style, so this deliberately contains no drawing code of
its own. It drives the two established generators:

* ``write_all_models_boeval_2023_2025.py`` — O-Eval year/suite splits
* ``write_aa_style_eval_figures.py`` — O-Eval bar, O-Eval vs. cost, Robust bar,
  Robust vs. cost, token usage, cost

Both are re-run with the multimodal figure prefix, a narrowed model set and USD
costs, so the multimodal board renders exactly like the text-only board and the
two cannot drift apart.
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SITE_FIGURES = ROOT / "jobs" / "github-pages-site" / "assets" / "figures"

#: Report row labels of the multimodal entries, in the order they are drawn.
MULTIMODAL_MODELS = (
    "codex + gpt-5.5 xhigh",
    "opencode + deepseek-flash",
    "opencode + deepseek-flash (max)",
)

#: Filenames produced into <site>/assets/figures by this driver.
FIGURE_NAMES = (
    "o-eval-bar",
    "o-eval-cost-scatter",
    "effect-bar",
    "effect-cost-scatter",
    "token-usage",
    "cost",
    "o-eval-year-split",
    "o-eval-suite-split",
)


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", default="mm", help="Figure filename prefix.")
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=ROOT / "jobs" / "figures",
        help="Where the generators write; files are copied to the site afterwards.",
    )
    parser.add_argument("--report-path", type=Path, default=None)
    parser.add_argument(
        "--skip-splits",
        action="store_true",
        help="Only refresh the AA-style charts, not the year/suite splits.",
    )
    args = parser.parse_args()

    # Both generators read the 2023-2025 report: that is the one covering all 18
    # tasks and every registered model (the AA script's own default is the
    # narrower 2024-2025 report used by an earlier board).
    board_path = ROOT / "jobs" / "terminus2-direction-aware-flash-baseline-bbo-2023-2025.md"
    report_path = args.report_path or board_path

    generated: list[Path] = []

    if not args.skip_splits:
        board = _load("all_models_boeval", "write_all_models_boeval_2023_2025.py")
        board.FIGURE_PREFIX = args.prefix
        board.FIGURES = args.figures_dir
        board.SUMMARY_FILTER = set(MULTIMODAL_MODELS)
        _, _, records, summaries = board.compute()
        for split in ("year", "suite"):
            svg = board.write_split_bars(records, summaries, split=split, metric="o")
            generated.append(svg)
            generated.append(board.convert_svg(svg))

    # The AA renderer is driven as a subprocess because it parses argv itself.
    command = [
        sys.executable,
        str(SCRIPTS / "write_aa_style_eval_figures.py"),
        "--report-path",
        str(report_path),
        "--output-prefix",
        args.prefix,
        "--currency",
        "usd",
        "--models",
        *MULTIMODAL_MODELS,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"AA figure generation failed:\n{result.stdout}\n{result.stderr}")
    for line in result.stdout.splitlines():
        path = Path(line.strip())
        if path.suffix in {".svg", ".png"} and path.exists():
            generated.append(path)

    SITE_FIGURES.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for name in FIGURE_NAMES:
        for suffix in (".svg", ".png"):
            src = args.figures_dir / f"{args.prefix}-{name}{suffix}"
            if not src.exists():
                continue
            dst = SITE_FIGURES / src.name
            shutil.copy2(src, dst)
            copied.append(dst)

    for path in sorted(set(copied)):
        print(path)
    print(f"copied {len(set(copied))} files into {SITE_FIGURES}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
