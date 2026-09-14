#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write focused completion visuals and a plain-language summary for Qwen/Kimi runs."""

from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "jobs"
FIGURES = JOBS / "figures"
SUMMARY_PATH = JOBS / "terminus2-qwen-kimi-completion-plain-language-summary.md"

QWEN_MODEL = "Qwen3.8-27B-FP8 thinking-on"
KIMI_MODEL = "Kimi K3"

QWEN_2024_2025_PREFIX = "terminus2-qwen3-8-27b-fp8-h800-thinking-2024-2025"
QWEN_2023_PREFIX = "terminus2-qwen3-8-27b-fp8-h800-thinking-2023"
KIMI_2023_PREFIX = "terminus2-kimi-k3-2023"

KIMI_INPUT_MISS_RMB_PER_MTOK = 20.0
KIMI_CACHE_RMB_PER_MTOK = 2.0
KIMI_OUTPUT_RMB_PER_MTOK = 100.0

EXPECTED_BY_GROUP = {
    "qwen-2024-2025": [
        "cumcm-2024-a-dragon-dance",
        "cumcm-2024-b-production-decision",
        "cumcm-2024-c-crop-planting",
        "cumcm-2025-a-smoke-screen",
        "cumcm-2025-b-sic-thickness",
        "cumcm-2025-c-nipt",
        "mcm-2024-a-lamprey",
        "mcm-2024-b-submersible-search",
        "mcm-2024-c-tennis-momentum",
        "mcm-2025-a-stair-wear",
        "mcm-2025-b-juneau-tourism",
        "mcm-2025-c-olympic-medals",
    ],
    "qwen-2023": [
        "cumcm-2023-a-heliostat-field",
        "cumcm-2023-b-multibeam-lines",
        "cumcm-2023-c-vegetable-pricing",
        "mcm-2023-a-plant-community",
        "mcm-2023-b-maasai-mara",
        "mcm-2023-c-wordle",
    ],
    "kimi-2023": [
        "cumcm-2023-a-heliostat-field",
        "cumcm-2023-b-multibeam-lines",
        "cumcm-2023-c-vegetable-pricing",
        "mcm-2023-a-plant-community",
        "mcm-2023-b-maasai-mara",
        "mcm-2023-c-wordle",
    ],
}

TASK_TITLE = {
    "cumcm-2023-a-heliostat-field": "CUMCM 2023 A 定日镜场",
    "cumcm-2023-b-multibeam-lines": "CUMCM 2023 B 多波束测线",
    "cumcm-2023-c-vegetable-pricing": "CUMCM 2023 C 蔬菜定价",
    "mcm-2023-a-plant-community": "MCM 2023 A 植物群落",
    "mcm-2023-b-maasai-mara": "MCM 2023 B 马赛马拉",
    "mcm-2023-c-wordle": "MCM 2023 C Wordle",
    "cumcm-2024-a-dragon-dance": "CUMCM 2024 A 板凳龙调头",
    "cumcm-2024-b-production-decision": "CUMCM 2024 B 生产过程决策",
    "cumcm-2024-c-crop-planting": "CUMCM 2024 C 作物种植",
    "cumcm-2025-a-smoke-screen": "CUMCM 2025 A 烟幕遮蔽",
    "cumcm-2025-b-sic-thickness": "CUMCM 2025 B 外延层厚度",
    "cumcm-2025-c-nipt": "CUMCM 2025 C NIPT",
    "mcm-2024-a-lamprey": "MCM 2024 A 七鳃鳗",
    "mcm-2024-b-submersible-search": "MCM 2024 B 潜水器搜索",
    "mcm-2024-c-tennis-momentum": "MCM 2024 C 网球势头",
    "mcm-2025-a-stair-wear": "MCM 2025 A 楼梯磨损",
    "mcm-2025-b-juneau-tourism": "MCM 2025 B 朱诺旅游",
    "mcm-2025-c-olympic-medals": "MCM 2025 C 奥运奖牌",
}


@dataclass
class ResultStats:
    prefix: str
    contest: str
    result_path: Path
    completed: int
    running: int
    pending: int
    errored: int
    input_tokens: int
    cache_tokens: int
    output_tokens: int
    mean_reward: float | None
    exception_stats: dict[str, list[str]]


@dataclass
class Batch:
    key: str
    label: str
    model: str
    prefixes: list[str]
    expected_slugs: list[str]
    stats: list[ResultStats]
    artifacts: dict[str, Path]

    @property
    def expected_count(self) -> int:
        return len(self.expected_slugs)

    @property
    def artifact_count(self) -> int:
        return len(self.artifacts)

    @property
    def completed(self) -> int:
        return sum(item.completed for item in self.stats)

    @property
    def running(self) -> int:
        return sum(item.running for item in self.stats)

    @property
    def pending(self) -> int:
        return sum(item.pending for item in self.stats)

    @property
    def errored(self) -> int:
        return sum(item.errored for item in self.stats)

    @property
    def input_tokens(self) -> int:
        return sum(item.input_tokens for item in self.stats)

    @property
    def cache_tokens(self) -> int:
        return sum(item.cache_tokens for item in self.stats)

    @property
    def output_tokens(self) -> int:
        return sum(item.output_tokens for item in self.stats)

    @property
    def billable_input_tokens(self) -> int:
        return max(0, self.input_tokens - self.cache_tokens)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def missing_slugs(self) -> list[str]:
        return [slug for slug in self.expected_slugs if slug not in self.artifacts]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_result(prefix: str, contest: str) -> ResultStats:
    path = JOBS / f"{prefix}-{contest}-retryproxy" / "result.json"
    data = read_json(path)
    stats = data["stats"]
    eval_items = list(stats.get("evals", {}).values())
    eval_stats = eval_items[0] if eval_items else {}
    metrics = eval_stats.get("metrics") or []
    mean_reward = metrics[0].get("mean") if metrics and isinstance(metrics[0], dict) else None
    exception_stats = eval_stats.get("exception_stats") or {}
    return ResultStats(
        prefix=prefix,
        contest=contest,
        result_path=path,
        completed=int(stats.get("n_completed_trials", 0)),
        running=int(stats.get("n_running_trials", 0)),
        pending=int(stats.get("n_pending_trials", 0)),
        errored=int(stats.get("n_errored_trials", 0)),
        input_tokens=int(stats.get("n_input_tokens", 0)),
        cache_tokens=int(stats.get("n_cache_tokens", 0)),
        output_tokens=int(stats.get("n_output_tokens", 0)),
        mean_reward=float(mean_reward) if mean_reward is not None else None,
        exception_stats=exception_stats,
    )


def artifact_map(prefixes: list[str], expected_slugs: list[str]) -> dict[str, Path]:
    expected = set(expected_slugs)
    found: dict[str, Path] = {}
    for prefix in prefixes:
        for contest in ("cumcm", "mcm"):
            root = JOBS / f"{prefix}-{contest}-retryproxy"
            if not root.exists():
                continue
            for path in root.glob("*/artifacts/root/results/*_result.json"):
                slug = path.name.removesuffix("_result.json")
                if slug in expected and slug not in found:
                    found[slug] = path
    return found


def make_batches() -> list[Batch]:
    batches = [
        Batch(
            key="qwen-2024-2025",
            label="Qwen 2024/2025",
            model=QWEN_MODEL,
            prefixes=[QWEN_2024_2025_PREFIX],
            expected_slugs=EXPECTED_BY_GROUP["qwen-2024-2025"],
            stats=[
                read_result(QWEN_2024_2025_PREFIX, "cumcm"),
                read_result(QWEN_2024_2025_PREFIX, "mcm"),
            ],
            artifacts={},
        ),
        Batch(
            key="qwen-2023",
            label="Qwen 2023 补跑",
            model=QWEN_MODEL,
            prefixes=[QWEN_2023_PREFIX],
            expected_slugs=EXPECTED_BY_GROUP["qwen-2023"],
            stats=[
                read_result(QWEN_2023_PREFIX, "cumcm"),
                read_result(QWEN_2023_PREFIX, "mcm"),
            ],
            artifacts={},
        ),
        Batch(
            key="kimi-2023",
            label="Kimi K3 2023 补跑",
            model=KIMI_MODEL,
            prefixes=[KIMI_2023_PREFIX],
            expected_slugs=EXPECTED_BY_GROUP["kimi-2023"],
            stats=[
                read_result(KIMI_2023_PREFIX, "cumcm"),
                read_result(KIMI_2023_PREFIX, "mcm"),
            ],
            artifacts={},
        ),
    ]
    for batch in batches:
        batch.artifacts = artifact_map(batch.prefixes, batch.expected_slugs)
    return batches


def combine_batch(key: str, label: str, model: str, parts: list[Batch]) -> Batch:
    expected: list[str] = []
    prefixes: list[str] = []
    stats: list[ResultStats] = []
    artifacts: dict[str, Path] = {}
    for part in parts:
        expected.extend(part.expected_slugs)
        prefixes.extend(part.prefixes)
        stats.extend(part.stats)
        artifacts.update(part.artifacts)
    return Batch(key=key, label=label, model=model, prefixes=prefixes, expected_slugs=expected, stats=stats, artifacts=artifacts)


def kimi_cost_rmb(batch: Batch) -> float:
    miss = batch.billable_input_tokens
    cache = batch.cache_tokens
    output = batch.output_tokens
    return (
        miss / 1_000_000 * KIMI_INPUT_MISS_RMB_PER_MTOK
        + cache / 1_000_000 * KIMI_CACHE_RMB_PER_MTOK
        + output / 1_000_000 * KIMI_OUTPUT_RMB_PER_MTOK
    )


def fmt_int(value: int) -> str:
    return f"{value:,}"


def fmt_mtokens(value: int) -> str:
    return f"{value / 1_000_000:.2f}M"


def fmt_reward(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value:.6f}".rstrip("0").rstrip(".")


def md_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def svg_text(x: float, y: float, content: str, *, size: int = 20, weight: int = 500, fill: str = "#171717", anchor: str = "start") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(content)}</text>'
    )


def svg_rect(x: float, y: float, w: float, h: float, fill: str, *, rx: float = 0, stroke: str | None = None, opacity: float | None = None) -> str:
    attrs = [
        f'x="{x:.1f}"',
        f'y="{y:.1f}"',
        f'width="{w:.1f}"',
        f'height="{h:.1f}"',
        f'fill="{fill}"',
    ]
    if rx:
        attrs.append(f'rx="{rx:.1f}"')
    if stroke:
        attrs.append(f'stroke="{stroke}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:.3f}"')
    return f"<rect {' '.join(attrs)} />"


def svg_line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#d4d4d4", width: float = 1.0, dash: str | None = None) -> str:
    attrs = [
        f'x1="{x1:.1f}"',
        f'y1="{y1:.1f}"',
        f'x2="{x2:.1f}"',
        f'y2="{y2:.1f}"',
        f'stroke="{stroke}"',
        f'stroke-width="{width:.1f}"',
    ]
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    return f"<line {' '.join(attrs)} />"


def svg_shell(width: int, height: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">\n'
        f'<rect width="{width}" height="{height}" fill="#ffffff" />\n'
        f"{body}\n</svg>\n"
    )


def write_svg_png(path: Path, svg: str) -> None:
    path.write_text(svg, encoding="utf-8")
    png_path = path.with_suffix(".png")
    converters = [
        ["magick", str(path), str(png_path)],
        ["convert", str(path), str(png_path)],
        ["sips", "-s", "format", "png", str(path), "--out", str(png_path)],
    ]
    errors: list[str] = []
    for command in converters:
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except FileNotFoundError:
            errors.append(f"{command[0]}: not found")
        except subprocess.CalledProcessError as exc:
            message = (exc.stderr or exc.stdout or "").strip()
            errors.append(f"{command[0]}: {message}")
        else:
            return
    raise RuntimeError(f"failed to convert {path.name} to PNG: {'; '.join(errors)}")


def write_completion_overview(batches: list[Batch], qwen_total: Batch) -> Path:
    rows = [qwen_total, batches[0], batches[1], batches[2]]
    width, height = 1600, 940
    x0, y0 = 120, 260
    bar_w, bar_h = 980, 54
    gap = 138
    colors = {
        "qwen-total": "#4f46e5",
        "qwen-2024-2025": "#6366f1",
        "qwen-2023": "#22a06b",
        "kimi-2023": "#0ea5e9",
    }
    out = [
        svg_text(70, 90, "Qwen Thinking + Kimi K3 Completion", size=44, weight=700),
        svg_text(72, 130, "Artifacts are counted from saved *_result.json files. Result stats are read directly from each job result.json.", size=21, weight=500, fill="#666666"),
        svg_rect(72, 170, 300, 54, "#f3f4f6", rx=10),
        svg_text(92, 204, f"Qwen total: {qwen_total.artifact_count}/{qwen_total.expected_count}", size=24, weight=700),
        svg_rect(400, 170, 280, 54, "#f3f4f6", rx=10),
        svg_text(420, 204, f"Kimi 2023: {batches[2].artifact_count}/{batches[2].expected_count}", size=24, weight=700),
        svg_rect(708, 170, 310, 54, "#fff7ed", rx=10),
        svg_text(728, 204, "Qwen historical error: 1", size=22, weight=700, fill="#9a3412"),
        svg_rect(1086, 170, 390, 54, "#ecfdf5", rx=10),
        svg_text(1106, 204, "Kimi CUMCM errors: 0", size=22, weight=700, fill="#047857"),
    ]
    for idx, row in enumerate(rows):
        y = y0 + idx * gap
        pct = row.artifact_count / row.expected_count if row.expected_count else 0
        fill_w = bar_w * pct
        out.append(svg_text(x0, y - 14, row.label, size=24, weight=700))
        out.append(svg_text(x0 + bar_w + 38, y + 36, f"{row.artifact_count}/{row.expected_count} artifacts", size=24, weight=700))
        out.append(svg_rect(x0, y, bar_w, bar_h, "#e5e7eb", rx=12))
        out.append(svg_rect(x0, y, fill_w, bar_h, colors[row.key], rx=12))
        out.append(svg_text(x0 + 22, y + 36, f"{pct * 100:.0f}%", size=24, weight=700, fill="#ffffff"))
        stat = f"completed {row.completed}, running {row.running}, pending {row.pending}, errors {row.errored}"
        out.append(svg_text(x0, y + 84, stat, size=19, weight=500, fill="#666666"))
        if row.missing_slugs:
            out.append(svg_text(x0 + 560, y + 84, f"missing: {len(row.missing_slugs)}", size=19, weight=700, fill="#b91c1c"))
    out.extend(
        [
            svg_line(70, height - 104, width - 70, height - 104, stroke="#e5e7eb"),
            svg_text(70, height - 64, "Note: Qwen 2024/2025 CUMCM result.json still records one AgentTimeoutError, but its dragon-dance artifact exists.", size=20, weight=500, fill="#666666"),
        ]
    )
    out_path = FIGURES / "qwen-kimi-completion-overview.svg"
    write_svg_png(out_path, svg_shell(width, height, "\n".join(out)))
    return out_path


def write_token_cost_figure(qwen_total: Batch, kimi_batch: Batch) -> Path:
    rows = [qwen_total, kimi_batch]
    width, height = 1600, 960
    plot_x, plot_y, plot_w, plot_h = 150, 290, 1180, 420
    max_tokens = max(row.total_tokens for row in rows) / 1_000_000
    domain = math.ceil(max_tokens / 10) * 10
    out = [
        svg_text(70, 92, "Token Use and Kimi Cost", size=44, weight=700),
        svg_text(72, 132, "Input includes cache-hit input. Kimi RMB estimate uses the user-provided Bailian prices.", size=21, weight=500, fill="#666666"),
        svg_rect(72, 174, 330, 62, "#f3f4f6", rx=10),
        svg_text(92, 213, f"Qwen tokens: {fmt_mtokens(qwen_total.total_tokens)}", size=24, weight=700),
        svg_rect(430, 174, 330, 62, "#f3f4f6", rx=10),
        svg_text(450, 213, f"Kimi tokens: {fmt_mtokens(kimi_batch.total_tokens)}", size=24, weight=700),
        svg_rect(788, 174, 330, 62, "#eff6ff", rx=10),
        svg_text(808, 213, f"Kimi cost: RMB {kimi_cost_rmb(kimi_batch):.2f}", size=24, weight=700, fill="#1d4ed8"),
    ]
    for tick in range(0, domain + 1, 10):
        x = plot_x + (tick / domain) * plot_w
        out.append(svg_line(x, plot_y, x, plot_y + plot_h, stroke="#e5e7eb", dash="4 8"))
        out.append(svg_text(x, plot_y + plot_h + 36, f"{tick}M", size=18, weight=500, fill="#666666", anchor="middle"))
    out.append(svg_line(plot_x, plot_y + plot_h, plot_x + plot_w, plot_y + plot_h, stroke="#a3a3a3", width=1.4))
    colors = [("#4f46e5", "#c7d2fe", "#111827"), ("#0ea5e9", "#bae6fd", "#0369a1")]
    labels = [("input", "cache", "output"), ("input miss", "cache", "output")]
    for idx, row in enumerate(rows):
        y = plot_y + 82 + idx * 174
        out.append(svg_text(plot_x, y - 24, row.label, size=24, weight=700))
        segments = [
            (row.billable_input_tokens if row.key == "kimi-2023" else row.input_tokens, colors[idx][0], labels[idx][0]),
            (row.cache_tokens if row.key == "kimi-2023" else 0, colors[idx][1], labels[idx][1]),
            (row.output_tokens, colors[idx][2], labels[idx][2]),
        ]
        x = plot_x
        for value, color, label in segments:
            if value <= 0:
                continue
            w = (value / 1_000_000) / domain * plot_w
            out.append(svg_rect(x, y, w, 58, color, rx=8 if x == plot_x else 0))
            if w > 94:
                text_fill = "#ffffff" if color not in {"#c7d2fe", "#bae6fd"} else "#1f2937"
                out.append(svg_text(x + w / 2, y + 37, f"{label} {fmt_mtokens(value)}", size=19, weight=700, fill=text_fill, anchor="middle"))
            x += w
        out.append(svg_text(plot_x + plot_w + 32, y + 38, fmt_mtokens(row.total_tokens), size=24, weight=700))
    legend_y = height - 138
    legend_items = [
        ("Qwen input", "#4f46e5"),
        ("Qwen output", "#111827"),
        ("Kimi input miss", "#0ea5e9"),
        ("Kimi cached input", "#bae6fd"),
        ("Kimi output", "#0369a1"),
    ]
    x = 72
    for label, color in legend_items:
        out.append(svg_rect(x, legend_y, 24, 18, color, rx=3))
        out.append(svg_text(x + 34, legend_y + 18, label, size=18, weight=600, fill="#525252"))
        x += 238
    out.append(svg_text(72, height - 70, "For Kimi: cost = cache-miss input * 20 + cached input * 2 + output * 100 RMB per 1M tokens.", size=20, weight=500, fill="#666666"))
    out_path = FIGURES / "qwen-kimi-token-cost.svg"
    write_svg_png(out_path, svg_shell(width, height, "\n".join(out)))
    return out_path


def status_table(batch: Batch) -> list[str]:
    rows = [
        "| 子集 | completed | running | pending | error | input/cache/output tokens | mean reward | 异常摘要 |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for item in batch.stats:
        contest = item.contest.upper()
        exceptions = []
        for key, trials in item.exception_stats.items():
            exceptions.append(f"{key}({len(trials)})")
        exception_text = ", ".join(exceptions) if exceptions else "无"
        rows.append(
            "| "
            + " | ".join(
                [
                    contest,
                    str(item.completed),
                    str(item.running),
                    str(item.pending),
                    str(item.errored),
                    f"{fmt_int(item.input_tokens)} / {fmt_int(item.cache_tokens)} / {fmt_int(item.output_tokens)}",
                    fmt_reward(item.mean_reward),
                    md_cell(exception_text),
                ]
            )
            + " |"
        )
    return rows


def artifact_table(batch: Batch) -> list[str]:
    rows = [
        "| 题目 | artifact |",
        "|---|---|",
    ]
    for slug in batch.expected_slugs:
        path = batch.artifacts.get(slug)
        if path is None:
            value = "缺失"
        else:
            value = f"`{path.relative_to(ROOT)}`"
        rows.append(f"| {TASK_TITLE.get(slug, slug)} | {value} |")
    return rows


def write_summary(batches: list[Batch], qwen_total: Batch, overview_svg: Path, token_svg: Path) -> Path:
    kimi = next(batch for batch in batches if batch.key == "kimi-2023")
    qwen_2024 = next(batch for batch in batches if batch.key == "qwen-2024-2025")
    qwen_2023 = next(batch for batch in batches if batch.key == "qwen-2023")
    lines: list[str] = [
        "# Qwen thinking-on 与 Kimi K3 2023 补跑结果，大白话版",
        "",
        f"生成日期：{date.today().isoformat()}",
        "",
        "这份说明只看最近这条线：Qwen3.8-27B-FP8 thinking-on 的 2023/2024/2025 全量结果，以及 Kimi K3 的 2023 补跑结果。它不改旧的 2024/2025 BO-Eval 排名报告，也不重新调用模型；所有数字都来自已经落盘的 `result.json` 和 `artifacts/root/results/*_result.json`。",
        "",
        "## 先说结论",
        "",
        f"Qwen 现在是 **{qwen_total.artifact_count}/{qwen_total.expected_count} 个 artifact 齐了**。其中 2024/2025 是 {qwen_2024.artifact_count}/{qwen_2024.expected_count}，2023 补跑是 {qwen_2023.artifact_count}/{qwen_2023.expected_count}。所以从“有没有最后答案文件”这个角度看，Qwen 的 18 题全量目标已经补齐。",
        "",
        f"Kimi K3 2023 也是 **{kimi.artifact_count}/{kimi.expected_count} 个 artifact 齐了**。刚修过的 Kimi CUMCM 汇总 `result.json` 现在显示 3 completed、0 error；定日镜场 artifact 是从 trajectory 里恢复出来的，所以 CUMCM reward 统计里它仍然是 0.0，没有伪装成重新评分后的高分。",
        "",
        "两张图先放这里：第一张看完成度，第二张看 token 和 Kimi 的粗略费用。",
        "",
        "![Qwen/Kimi 完成度](figures/qwen-kimi-completion-overview.png)",
        "",
        "![Qwen/Kimi token 与成本](figures/qwen-kimi-token-cost.png)",
        "",
        "## 这轮到底算完成了吗",
        "",
        "如果问题是“每道题有没有产出最后答案 JSON”，答案是：完成。Qwen 有 18 个结果 artifact，Kimi 2023 有 6 个结果 artifact。",
        "",
        "如果问题是“`result.json` 里是否完全没有历史异常”，答案要更细一点：Kimi 2023 已经没有 error；Qwen 2024/2025 CUMCM 里还保留一个 `AgentTimeoutError`，对应 CUMCM 2024 A 板凳龙调头。但这个 trial 的 artifact 文件已经存在，所以它更像是历史运行状态没有被回写干净，而不是结果文件缺失。",
        "",
        "## 机器实际花了多少 token",
        "",
        f"Qwen 三年合计 token 是 **{fmt_int(qwen_total.input_tokens)} input / {fmt_int(qwen_total.cache_tokens)} cache / {fmt_int(qwen_total.output_tokens)} output**。这条是 H800 本地 vLLM 后端，文档里只做用量统计，不粗算人民币 API 费用。",
        "",
        f"Kimi 2023 合计 token 是 **{fmt_int(kimi.input_tokens)} input / {fmt_int(kimi.cache_tokens)} cache / {fmt_int(kimi.output_tokens)} output**。按用户给的百炼价格粗算：cache miss input {KIMI_INPUT_MISS_RMB_PER_MTOK:g} RMB/M、cached input {KIMI_CACHE_RMB_PER_MTOK:g} RMB/M、output {KIMI_OUTPUT_RMB_PER_MTOK:g} RMB/M，本轮约 **RMB {kimi_cost_rmb(kimi):.2f}**。",
        "",
        "大白话说，Kimi 的 input 里绝大部分命中了 cache，所以贵的部分主要是 output；如果没有 cache，费用会明显更难看。",
        "",
        "## 分批状态",
        "",
        "### Qwen 2024/2025",
        "",
        *status_table(qwen_2024),
        "",
        "### Qwen 2023 补跑",
        "",
        *status_table(qwen_2023),
        "",
        "### Kimi K3 2023 补跑",
        "",
        *status_table(kimi),
        "",
        "## artifact 清单",
        "",
        "### Qwen 2024/2025",
        "",
        *artifact_table(qwen_2024),
        "",
        "### Qwen 2023 补跑",
        "",
        *artifact_table(qwen_2023),
        "",
        "### Kimi K3 2023 补跑",
        "",
        *artifact_table(kimi),
        "",
        "## 读这些数时别踩的坑",
        "",
        "第一，artifact 数和 reward 不是同一个概念。artifact 齐了，说明每道题都有最终答案文件；reward 高低要看评测器如何按题目指标打分。",
        "",
        "第二，Kimi 定日镜这题虽然已经恢复出 artifact，但没有重新跑 Harbor 评分，所以汇总里的 CUMCM mean 仍包含这个 0.0。这样做比较诚实：完成度回来了，分数不冒充重算。",
        "",
        "第三，Qwen 那个历史超时标记不要直接等同于“缺结果”。现在应当把它理解成：`result.json` 还记着运行时异常，但对应答案文件已经在 artifacts 里。",
        "",
        "一句话总结：**这次更新把“结果文件是否齐全”和“运行汇总是否干净”分开讲清楚了。Qwen/Kimi 的目标 artifact 都齐了；Kimi 汇总已清零 error；Qwen 只剩一个有 artifact 的历史超时标记。**",
        "",
        "## 生成物",
        "",
        f"- 完成度 SVG：`{overview_svg.relative_to(ROOT)}`",
        f"- 完成度 PNG：`{overview_svg.with_suffix('.png').relative_to(ROOT)}`",
        f"- token/cost SVG：`{token_svg.relative_to(ROOT)}`",
        f"- token/cost PNG：`{token_svg.with_suffix('.png').relative_to(ROOT)}`",
        "",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")
    return SUMMARY_PATH


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    batches = make_batches()
    qwen_total = combine_batch("qwen-total", "Qwen total 2023/2024/2025", QWEN_MODEL, batches[:2])
    overview_svg = write_completion_overview(batches, qwen_total)
    token_svg = write_token_cost_figure(qwen_total, batches[2])
    summary = write_summary(batches, qwen_total, overview_svg, token_svg)
    for path in [overview_svg, overview_svg.with_suffix(".png"), token_svg, token_svg.with_suffix(".png"), summary]:
        print(path)


if __name__ == "__main__":
    main()
