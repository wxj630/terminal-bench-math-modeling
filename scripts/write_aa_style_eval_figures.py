#!/usr/bin/env python3
"""Generate Artificial Analysis-inspired SVG charts from the eval summary."""

from __future__ import annotations

import argparse
import math
import subprocess
from dataclasses import dataclass
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "jobs" / "terminus2-direction-aware-flash-baseline-bbo-2024-2025.md"
OUT_DIR = ROOT / "jobs" / "figures"
OUTPUT_PREFIX = "aa-style"
OPENROUTER_USD_TO_RMB = 6.737012

# Cost display currency. Prices are stored per Mtok in RMB (that is what the
# generated report's price table quotes); when USD is selected every cost figure
# is divided by the same rate the report used, so the boards stay consistent.
COST_CURRENCY = "rmb"


def set_cost_currency(currency: str) -> None:
    global COST_CURRENCY
    if currency not in {"rmb", "usd"}:
        raise ValueError(f"unsupported currency: {currency}")
    COST_CURRENCY = currency


def cost_symbol() -> str:
    return "¥" if COST_CURRENCY == "rmb" else "$"


def cost_label() -> str:
    return "RMB" if COST_CURRENCY == "rmb" else "USD"


def cost_divisor() -> float:
    return 1.0 if COST_CURRENCY == "rmb" else OPENROUTER_USD_TO_RMB


def openrouter_rmb_per_mtok(usd_per_token: str | float) -> float:
    return float(usd_per_token) * 1_000_000.0 * OPENROUTER_USD_TO_RMB


DISPLAY = {
    "v4 flash baseline": "DeepSeek V4 Flash",
    "v4 pro": "DeepSeek V4 Pro",
    "GLM-5.3": "GLM-5.3",
    "GPT-5.6 SOL high": "GPT-5.6 Sol",
    "GPT-5.6 SOL xhigh": "GPT-5.6 Sol XH",
    "Claude Opus 5": "Claude Opus 5",
    "Kimi K3": "Kimi K3",
    "Gemini 3.7 Flash high primary+retry": "Gemini 3.7 Flash",
    "Qwen3.8-27B-FP8 thinking": "Qwen3.8 27B",
    "OpenRouter ox-alpha": "ox-alpha",
    "Tencent Hy4 Preview": "Hy4 Preview",
    "codex + gpt-5.5 xhigh": "GPT-5.5 xhigh (codex)",
    "opencode + deepseek-flash": "V4.1 Flash (opencode)",
    "opencode + deepseek-flash (max)": "V4.1 Flash max (opencode)",
}

SHORT_LINES = {
    "v4 flash baseline": ["DeepSeek V4", "Flash"],
    "v4 pro": ["DeepSeek V4", "Pro"],
    "GLM-5.3": ["GLM-5.3"],
    "GPT-5.6 SOL high": ["GPT-5.6", "Sol"],
    "GPT-5.6 SOL xhigh": ["GPT-5.6", "Sol XH"],
    "Claude Opus 5": ["Claude", "Opus 5"],
    "Kimi K3": ["Kimi K3"],
    "Gemini 3.7 Flash high primary+retry": ["Gemini 3.7", "Flash"],
    "Qwen3.8-27B-FP8 thinking": ["Qwen3.8", "27B"],
    "OpenRouter ox-alpha": ["ox-alpha"],
    "Tencent Hy4 Preview": ["Hy4", "Preview"],
    "codex + gpt-5.5 xhigh": ["GPT-5.5", "xhigh"],
    "opencode + deepseek-flash": ["V4.1", "Flash"],
    "opencode + deepseek-flash (max)": ["V4.1", "Flash max"],
}

COLORS = {
    "v4 flash baseline": "#2f80ed",
    "v4 pro": "#2945d9",
    "GLM-5.3": "#6f6f6f",
    "GPT-5.6 SOL high": "#202020",
    "GPT-5.6 SOL xhigh": "#0f766e",
    "Claude Opus 5": "#c15f3c",
    "Kimi K3": "#1f83ff",
    "Gemini 3.7 Flash high primary+retry": "#34a853",
    "Qwen3.8-27B-FP8 thinking": "#7c3aed",
    "OpenRouter ox-alpha": "#f59e0b",
    "Tencent Hy4 Preview": "#dc2626",
    "codex + gpt-5.5 xhigh": "#111111",
    "opencode + deepseek-flash": "#00897b",
    "opencode + deepseek-flash (max)": "#00695c",
}

PRICE_RMB_PER_MTOK = {
    "v4 flash baseline": {
        "input": openrouter_rmb_per_mtok("0.00000006"),
        "cache": openrouter_rmb_per_mtok("0.000000012"),
        "output": openrouter_rmb_per_mtok("0.00000012"),
    },
    "v4 pro": {
        "input": openrouter_rmb_per_mtok("0.00000087"),
        "cache": openrouter_rmb_per_mtok("0.0000000725"),
        "output": openrouter_rmb_per_mtok("0.00000174"),
    },
    "GLM-5.3": {
        "input": openrouter_rmb_per_mtok("0.0000014"),
        "cache": openrouter_rmb_per_mtok("0.00000026"),
        "output": openrouter_rmb_per_mtok("0.0000044"),
    },
    "GPT-5.6 SOL high": {
        "input": openrouter_rmb_per_mtok("0.000002"),
        "cache": openrouter_rmb_per_mtok("0.0000002"),
        "output": openrouter_rmb_per_mtok("0.00001"),
    },
    "GPT-5.6 SOL xhigh": {
        "input": openrouter_rmb_per_mtok("0.000002"),
        "cache": openrouter_rmb_per_mtok("0.0000002"),
        "output": openrouter_rmb_per_mtok("0.00001"),
    },
    "Claude Opus 5": {"input": 36.0, "output": 180.0},
    "Kimi K3": {
        "input": openrouter_rmb_per_mtok("0.000003"),
        "cache": openrouter_rmb_per_mtok("0.0000003"),
        "output": openrouter_rmb_per_mtok("0.000015"),
    },
    "Gemini 3.7 Flash high primary+retry": {
        "input": openrouter_rmb_per_mtok("0.000000375"),
        "cache": openrouter_rmb_per_mtok("0.0000000375"),
        "output": openrouter_rmb_per_mtok("0.000001875"),
    },
    "Qwen3.8-27B-FP8 thinking": {
        "input": openrouter_rmb_per_mtok("0.000000425"),
        "cache": openrouter_rmb_per_mtok("0.000000085"),
        "output": openrouter_rmb_per_mtok("0.00000255"),
    },
}


@dataclass
class Row:
    model: str
    artifacts: int
    raw: float
    o_eval_pct: float
    b_eval_pp: float
    bo_eval_pct: float
    input_tokens: int
    cache_tokens: int
    output_tokens: int
    billable_input_tokens: int
    billable_output_tokens: int
    cost_rmb: float | None

    @property
    def cost(self) -> float | None:
        """Total estimated cost in the display currency."""
        if self.cost_rmb is None:
            return None
        return self.cost_rmb / cost_divisor()

    @property
    def label(self) -> str:
        return DISPLAY.get(self.model, self.model)

    @property
    def short_lines(self) -> list[str]:
        return SHORT_LINES.get(self.model, [self.label])

    @property
    def color(self) -> str:
        return COLORS.get(self.model, "#777777")

    @property
    def cache_hit_tokens(self) -> int:
        return max(0, self.input_tokens - self.billable_input_tokens)

    @property
    def total_usage_tokens(self) -> int:
        return self.billable_input_tokens + self.cache_hit_tokens + self.output_tokens

    @property
    def input_cost(self) -> float:
        price = PRICE_RMB_PER_MTOK.get(self.model, {}).get("input")
        if price is None:
            return 0.0
        return self.billable_input_tokens / 1_000_000.0 * price / cost_divisor()

    @property
    def output_cost(self) -> float:
        price = PRICE_RMB_PER_MTOK.get(self.model, {}).get("output")
        if price is None:
            return 0.0
        return self.output_tokens / 1_000_000.0 * price / cost_divisor()

    @property
    def cache_cost(self) -> float:
        price = PRICE_RMB_PER_MTOK.get(self.model, {}).get("cache")
        if price is None:
            return 0.0
        return self.cache_hit_tokens / 1_000_000.0 * price / cost_divisor()

    @property
    def effect_pct(self) -> float:
        return self.bo_eval_pct

    def score_pct(self, metric: str = "robust") -> float:
        return self.o_eval_pct if metric == "o" else self.effect_pct


def parse_int_triplet(cell: str) -> tuple[int, int, int]:
    parts = [p.strip().replace(",", "") for p in cell.split("/")]
    if len(parts) != 3:
        raise ValueError(f"expected token triplet, got {cell!r}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def parse_int_pair(cell: str) -> tuple[int, int]:
    parts = [p.strip().replace(",", "") for p in cell.split("/")]
    if len(parts) != 2:
        raise ValueError(f"expected token pair, got {cell!r}")
    return int(parts[0]), int(parts[1])


def parse_percent(cell: str) -> float:
    return float(cell.replace("%", "").replace("pp", "").replace("+", "").strip())


def parse_money_cell(cell: str) -> float | None:
    cleaned = cell.replace("¥", "").replace(",", "").strip()
    if cleaned.upper() == "N/A" or not cleaned:
        return None
    return float(cleaned)


def parse_price_cell(cell: str) -> float | None:
    cleaned = cell.replace("¥", "").replace("/M", "").replace(",", "").strip()
    if cleaned.upper() == "N/A" or not cleaned:
        return None
    return float(cleaned)


def parse_price_table(lines: list[str]) -> dict[str, dict[str, float]]:
    try:
        start = lines.index("## Price Table")
    except ValueError:
        return {}
    table_lines: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if line.startswith("|"):
            table_lines.append(line)
        elif table_lines:
            break
    if len(table_lines) < 3:
        return {}
    headers = [c.strip() for c in table_lines[0].strip().strip("|").split("|")]
    idx = {name: i for i, name in enumerate(headers)}
    required = {"Model", "Input", "Cached read", "Output"}
    if not required.issubset(idx):
        return {}
    parsed: dict[str, dict[str, float]] = {}
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < len(headers):
            continue
        values: dict[str, float] = {}
        input_price = parse_price_cell(cells[idx["Input"]])
        cache_price = parse_price_cell(cells[idx["Cached read"]])
        output_price = parse_price_cell(cells[idx["Output"]])
        cache_create_header = "Cache write/create"
        cache_create_price = parse_price_cell(cells[idx[cache_create_header]]) if cache_create_header in idx else None
        if input_price is not None:
            values["input"] = input_price
        if cache_price is not None:
            values["cache"] = cache_price
        if cache_create_price is not None:
            values["cache_create"] = cache_create_price
        if output_price is not None:
            values["output"] = output_price
        if values:
            parsed[cells[idx["Model"]]] = values
    return parsed


#: When non-empty, only these report row labels are drawn. The multimodal board
#: reuses this script with this set narrowed, so both boards share one renderer.
MODEL_FILTER: set[str] = set()


def parse_report(report_path: Path = REPORT_PATH) -> list[Row]:
    global PRICE_RMB_PER_MTOK
    lines = report_path.read_text(encoding="utf-8").splitlines()
    PRICE_RMB_PER_MTOK.update(parse_price_table(lines))
    start = lines.index("## Overall Mean")
    table_lines: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if line.startswith("|"):
            table_lines.append(line)
        elif table_lines:
            break
    if len(table_lines) < 3:
        return []
    headers = [c.strip() for c in table_lines[0].strip().strip("|").split("|")]
    header_index = {name: idx for idx, name in enumerate(headers)}
    token_idx = header_index.get("Tokens input/cache/output")
    billable_idx = header_index.get("Billable input/output")
    cost_idx = header_index.get("Est. cost RMB")
    raw_idx = header_index.get("Mean direction-aware raw")
    o_idx = header_index.get("Mean O-Eval on all 18 (%)")
    b_idx = header_index.get("Mean B-Eval vs flash (pp)")
    effect_idx = header_index.get(
        "Mean Robust BO-Eval on all 18 (%)",
        header_index.get(
            "Mean B/BO fallback effect on all 18 (%)",
            header_index.get("Mean BO-Eval vs flash on defined subset (%)"),
        ),
    )
    if None in {token_idx, billable_idx, cost_idx, raw_idx, b_idx, effect_idx}:
        raise ValueError(f"cannot parse overall table headers from {report_path}")
    rows: list[Row] = []
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < len(headers):
            continue
        input_tokens, cache_tokens, output_tokens = parse_int_triplet(cells[token_idx])
        billable_input_tokens, billable_output_tokens = parse_int_pair(cells[billable_idx])
        rows.append(
            Row(
                model=cells[0],
                artifacts=int(cells[1]),
                raw=float(cells[raw_idx]),
                o_eval_pct=parse_percent(cells[o_idx]) if o_idx is not None else float(cells[raw_idx]) * 100.0,
                b_eval_pp=parse_percent(cells[b_idx]),
                bo_eval_pct=parse_percent(cells[effect_idx]),
                input_tokens=input_tokens,
                cache_tokens=cache_tokens,
                output_tokens=output_tokens,
                billable_input_tokens=billable_input_tokens,
                billable_output_tokens=billable_output_tokens,
                cost_rmb=parse_money_cell(cells[cost_idx]),
            )
        )
    if MODEL_FILTER:
        rows = [row for row in rows if row.model in MODEL_FILTER]
    return rows


def fmt_num(value: float, digits: int = 2) -> str:
    text = f"{value:.{digits}f}"
    return text.rstrip("0").rstrip(".")


def fmt_tokens(value: float) -> str:
    if value >= 10:
        return f"{value:.0f}M"
    return f"{value:.1f}M"


def fmt_money(value: float | None) -> str:
    if value is None:
        return f"{cost_label()} N/A"
    return f"{cost_label()} {value:.2f}"


def text(
    x: float,
    y: float,
    content: str,
    *,
    cls: str = "",
    anchor: str = "start",
    fill: str | None = None,
    size: int | None = None,
    weight: str | None = None,
    transform: str | None = None,
) -> str:
    attrs = [f'x="{x:.2f}"', f'y="{y:.2f}"', f'text-anchor="{anchor}"']
    if cls:
        attrs.append(f'class="{cls}"')
    if fill:
        attrs.append(f'fill="{fill}"')
    if size:
        attrs.append(f'font-size="{size}"')
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if transform:
        attrs.append(f'transform="{transform}"')
    return f"<text {' '.join(attrs)}>{escape(content)}</text>"


def multiline_rotated_label(x: float, y: float, lines: list[str]) -> str:
    tspans = []
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else 17
        tspans.append(f'<tspan x="0" dy="{dy}">{escape(line)}</tspan>')
    return (
        f'<g transform="translate({x:.2f},{y:.2f}) rotate(-55)">'
        f'<text class="x-label" text-anchor="end">{"".join(tspans)}</text>'
        "</g>"
    )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str,
    stroke: str | None = None,
    rx: float = 0,
    opacity: float | None = None,
    cls: str = "",
) -> str:
    attrs = [
        f'x="{x:.2f}"',
        f'y="{y:.2f}"',
        f'width="{w:.2f}"',
        f'height="{h:.2f}"',
        f'fill="{fill}"',
    ]
    if stroke:
        attrs.append(f'stroke="{stroke}"')
    if rx:
        attrs.append(f'rx="{rx:.2f}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:.3f}"')
    if cls:
        attrs.append(f'class="{cls}"')
    return f"<rect {' '.join(attrs)} />"


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    stroke: str = "#d6d6d6",
    width: float = 1.0,
    dash: str | None = None,
    opacity: float | None = None,
) -> str:
    attrs = [
        f'x1="{x1:.2f}"',
        f'y1="{y1:.2f}"',
        f'x2="{x2:.2f}"',
        f'y2="{y2:.2f}"',
        f'stroke="{stroke}"',
        f'stroke-width="{width:.2f}"',
    ]
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:.3f}"')
    return f"<line {' '.join(attrs)} />"


def circle(
    cx: float,
    cy: float,
    r: float,
    *,
    fill: str,
    stroke: str | None = None,
    width: float = 1.0,
    opacity: float | None = None,
) -> str:
    attrs = [
        f'cx="{cx:.2f}"',
        f'cy="{cy:.2f}"',
        f'r="{r:.2f}"',
        f'fill="{fill}"',
    ]
    if stroke:
        attrs.append(f'stroke="{stroke}"')
        attrs.append(f'stroke-width="{width:.2f}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:.3f}"')
    return f"<circle {' '.join(attrs)} />"


def path(points: list[tuple[float, float]], *, stroke: str, width: float, dash: str | None = None) -> str:
    if not points:
        return ""
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width:.2f}"{dash_attr} stroke-linecap="round" />'


def svg_shell(width: int, height: int, body: str) -> str:
    style = """
    <style>
      .title { font-family: Georgia, Times, serif; font-size: 42px; fill: #050505; }
      .subtitle { font-family: Arial, Helvetica, sans-serif; font-size: 22px; fill: #8b8b8b; font-weight: 650; }
      .tab { font-family: Arial, Helvetica, sans-serif; font-size: 23px; fill: #4e4e4e; font-weight: 760; }
      .tab-active { fill: #111111; }
      .axis { font-family: Arial, Helvetica, sans-serif; font-size: 18px; fill: #767676; font-weight: 600; }
      .axis-title { font-family: Arial, Helvetica, sans-serif; font-size: 22px; fill: #101010; font-weight: 720; }
      .legend { font-family: Arial, Helvetica, sans-serif; font-size: 20px; fill: #151515; font-weight: 680; }
      .x-label { font-family: Arial, Helvetica, sans-serif; font-size: 18px; fill: #151515; font-weight: 650; }
      .bar-label { font-family: Arial, Helvetica, sans-serif; font-size: 22px; fill: #ffffff; font-weight: 800; }
      .top-label { font-family: Arial, Helvetica, sans-serif; font-size: 19px; fill: #939393; font-weight: 750; }
      .small-note { font-family: Arial, Helvetica, sans-serif; font-size: 18px; fill: #949494; font-weight: 650; }
      .point-label { font-family: Arial, Helvetica, sans-serif; font-size: 19px; fill: #4a4a4a; font-weight: 700; }
      .brand { font-family: Georgia, Times, serif; font-size: 26px; fill: #555555; }
    </style>
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">{style}{body}</svg>\n'
    )


def draw_tabs(active: str, x: float, y: float) -> str:
    tabs = [
        ("effect", "Robust"),
        ("o-effect", "O-Eval"),
        ("tokens", "Token Usage"),
        ("cost", "Cost"),
        ("scatter", "Robust vs. Cost"),
        ("o-scatter", "O vs. Cost"),
    ]
    widths = {"Robust": 140, "O-Eval": 140, "Token Usage": 210, "Cost": 110, "Robust vs. Cost": 230, "O vs. Cost": 170}
    out = []
    cur = x
    for key, label in tabs:
        w = widths[label]
        if key == active:
            out.append(rect(cur, y - 26, w, 58, fill="#efefef", rx=8))
            out.append(text(cur + 18, y + 10, label, cls="tab tab-active"))
        else:
            out.append(text(cur + 18, y + 10, label, cls="tab"))
        cur += w + 52
    return "\n".join(out)


def draw_brand(x: float, y: float) -> str:
    return "\n".join(
        [
            f'<rect x="{x:.2f}" y="{y-14:.2f}" width="9" height="9" rx="1.5" fill="#8a63ff" transform="rotate(-45 {x+4.5:.2f} {y-9.5:.2f})" />',
            f'<rect x="{x+13:.2f}" y="{y-14:.2f}" width="9" height="9" rx="1.5" fill="#8a63ff" transform="rotate(-45 {x+17.5:.2f} {y-9.5:.2f})" />',
            f'<rect x="{x:.2f}" y="{y:.2f}" width="9" height="9" rx="1.5" fill="#8a63ff" transform="rotate(-45 {x+4.5:.2f} {y+4.5:.2f})" />',
            text(x + 34, y + 10, "Terminal-Bench Math Modeling", cls="brand"),
        ]
    )


def draw_grid(
    x: float,
    y: float,
    w: float,
    h: float,
    ticks: list[float],
    domain_max: float,
    *,
    fmt=lambda value: str(value),
) -> tuple[str, callable]:
    def sy(value: float) -> float:
        return y + h - value / domain_max * h

    out = []
    for tick in ticks:
        yy = sy(tick)
        out.append(line(x, yy, x + w, yy, dash="4 8", stroke="#cfcfcf", width=1.2))
        out.append(text(x - 18, yy + 6, fmt(tick), cls="axis", anchor="end"))
    out.append(line(x, y + h, x + w, y + h, stroke="#dadada", width=1.2))
    return "\n".join(out), sy


def draw_grid_range(
    x: float,
    y: float,
    w: float,
    h: float,
    ticks: list[float],
    domain_min: float,
    domain_max: float,
    *,
    fmt=lambda value: str(value),
) -> tuple[str, callable]:
    span = domain_max - domain_min

    def sy(value: float) -> float:
        return y + h - (value - domain_min) / span * h

    out = []
    for tick in ticks:
        yy = sy(tick)
        stroke = "#9e9e9e" if abs(tick) < 1e-9 else "#cfcfcf"
        dash = None if abs(tick) < 1e-9 else "4 8"
        width = 1.5 if abs(tick) < 1e-9 else 1.2
        out.append(line(x, yy, x + w, yy, dash=dash, stroke=stroke, width=width))
        out.append(text(x - 18, yy + 6, fmt(tick), cls="axis", anchor="end"))
    return "\n".join(out), sy


def nice_max(value: float) -> float:
    if value <= 1:
        return 1.0
    magnitude = 10 ** math.floor(math.log10(value))
    normalized = value / magnitude
    if normalized <= 1:
        nice = 1
    elif normalized <= 2:
        nice = 2
    elif normalized <= 5:
        nice = 5
    else:
        nice = 10
    return nice * magnitude


def axis_ceiling(value: float, step: float) -> float:
    return math.ceil(value / step) * step


def effect_axis_step(max_abs_effect: float) -> float:
    if max_abs_effect <= 20:
        return 5.0
    if max_abs_effect <= 50:
        return 10.0
    return 20.0


def effect_axis_domain(values: list[float], *, min_span: float = 20.0) -> tuple[float, float, float]:
    values = values or [0.0]
    step = effect_axis_step(max(abs(value) for value in values))
    low = min(values)
    high = max(values)
    domain_min = math.floor(min(0.0, low * 1.20) / step) * step
    domain_max = math.ceil(max(0.0, high * 1.20) / step) * step
    if domain_max <= domain_min:
        domain_min -= step
        domain_max += step
    span = domain_max - domain_min
    if span < min_span:
        pad = (min_span - span) / 2.0
        domain_min = math.floor((domain_min - pad) / step) * step
        domain_max = math.ceil((domain_max + pad) / step) * step
    return domain_min, domain_max, step


def text_width_estimate(value: str, *, size: int = 19) -> float:
    return max(34.0, len(value) * size * 0.55)


def label_bbox(x: float, y: float, lines: list[str], *, anchor: str, sizes: list[int]) -> tuple[float, float, float, float]:
    widths = [text_width_estimate(line, size=size) for line, size in zip(lines, sizes)]
    width = max(widths) + 14.0
    height = 24.0 * len(lines) + 8.0
    if anchor == "end":
        left = x - width
        right = x
    elif anchor == "middle":
        left = x - width / 2.0
        right = x + width / 2.0
    else:
        left = x
        right = x + width
    top = y - 20.0
    return left, top, right, top + height


def overlap_area(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    x_overlap = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    y_overlap = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return x_overlap * y_overlap


def outside_penalty(box: tuple[float, float, float, float], bounds: tuple[float, float, float, float]) -> float:
    left, top, right, bottom = box
    min_x, min_y, max_x, max_y = bounds
    return (
        max(0.0, min_x - left) ** 2
        + max(0.0, right - max_x) ** 2
        + max(0.0, min_y - top) ** 2
        + max(0.0, bottom - max_y) ** 2
    )


def place_point_labels(
    points: list[tuple[str, float, float, list[str]]],
    bounds: tuple[float, float, float, float],
) -> dict[str, tuple[float, float, str]]:
    placed = [(x - 18.0, y - 18.0, x + 18.0, y + 18.0) for _, x, y, _ in points]
    result: dict[str, tuple[float, float, str]] = {}
    sizes = [19, 18]
    base_candidates = [
        (20, -24, "start"),
        (20, 38, "start"),
        (-20, -24, "end"),
        (-20, 38, "end"),
        (20, 68, "start"),
        (-20, 68, "end"),
        (20, -56, "start"),
        (-20, -56, "end"),
        (34, 96, "start"),
        (-34, 96, "end"),
        (34, -88, "start"),
        (-34, -88, "end"),
        (0, -52, "middle"),
        (0, 62, "middle"),
        (0, 102, "middle"),
        (0, -92, "middle"),
    ]
    mid_x = (bounds[0] + bounds[2]) / 2.0
    for model, point_x, point_y, lines in sorted(points, key=lambda item: (item[2], item[1])):
        candidates = list(base_candidates)
        if point_x > mid_x:
            candidates = sorted(candidates, key=lambda item: 0 if item[2] == "end" else 1)
        best: tuple[float, float, str] | None = None
        best_score = float("inf")
        for dx, dy, anchor in candidates:
            label_x = point_x + dx
            label_y = point_y + dy
            box = label_bbox(label_x, label_y, lines, anchor=anchor, sizes=sizes[: len(lines)])
            score = outside_penalty(box, bounds) * 10.0
            score += sum(overlap_area(box, other) for other in placed) * 12.0
            score += abs(dx) * 0.04 + abs(dy) * 0.04
            if score < best_score:
                best_score = score
                best = (label_x, label_y, anchor)
        assert best is not None
        result[model] = best
        placed.append(label_bbox(best[0], best[1], lines, anchor=best[2], sizes=sizes[: len(lines)]))
    return result


def scatter_label(row: Row) -> str:
    return " ".join(row.short_lines)


def write_effect_bar(rows: list[Row]) -> Path:
    width, height = 1800, 1040
    card_x, card_y, card_w, card_h = 24, 24, width - 48, height - 48
    plot_x, plot_y, plot_w, plot_h = 132, 332, 1570, 440
    rows_sorted = sorted(rows, key=lambda row: row.effect_pct, reverse=True)
    values = [row.effect_pct for row in rows_sorted]
    domain_min, domain_max, tick_step = effect_axis_domain(values)
    ticks = []
    current = domain_min
    while current <= domain_max + 1e-9:
        ticks.append(current)
        current += tick_step
    grid, sy = draw_grid_range(
        plot_x,
        plot_y,
        plot_w,
        plot_h,
        ticks,
        domain_min,
        domain_max,
        fmt=lambda v: f"{v:.0f}%",
    )
    gap = 34
    bar_w = (plot_w - gap * (len(rows_sorted) - 1)) / len(rows_sorted)
    out = [
        rect(card_x, card_y, card_w, card_h, fill="#ffffff", stroke="#dddddd", rx=16),
        rect(card_x, card_y, card_w, 88, fill="#ffffff", rx=16),
        draw_tabs("effect", card_x + 42, card_y + 50),
        line(card_x, card_y + 90, card_x + card_w, card_y + 90, stroke="#dddddd", width=1.2),
        text(card_x + 42, 170, "Robust BO-Eval", cls="title"),
        text(card_x + 42, 210, "Clipped ratio for clean gaps; clipped B-Eval for saturated or tiny-gap tasks. Bad tasks can go negative.", cls="subtitle"),
        circle(card_x + 52, 270, 8, fill="#555555"),
        text(card_x + 70, 277, "Robust score", cls="legend"),
        circle(card_x + 188, 270, 8, fill="#b0b0b0"),
        text(card_x + 206, 277, "Raw score label", cls="legend"),
        draw_brand(plot_x + plot_w - 420, plot_y - 34),
        grid,
        text(plot_x - 88, plot_y + plot_h / 2, "Robust BO-Eval (%)", cls="axis-title", anchor="middle", transform=f"rotate(-90 {plot_x - 88:.2f} {plot_y + plot_h / 2:.2f})"),
    ]
    y_zero = sy(0.0)
    for idx, row in enumerate(rows_sorted):
        x = plot_x + idx * (bar_w + gap)
        y_value = sy(row.effect_pct)
        y = min(y_value, y_zero)
        h = abs(y_zero - y_value)
        out.append(rect(x, y, bar_w, h, fill=row.color, rx=8))
        label_y = y + h * 0.56 if row.effect_pct >= 0 else y + h + 26
        if h > 30:
            fill = "#ffffff" if row.effect_pct >= 0 else row.color
            out.append(text(x + bar_w / 2, label_y, f"{row.effect_pct:.1f}%", cls="bar-label", anchor="middle", fill=fill))
        raw_label = f"raw {fmt_num(row.raw, 3)}"
        out.append(text(x + bar_w / 2, y - 14, raw_label, cls="top-label", anchor="middle"))
        out.append(multiline_rotated_label(x + bar_w / 2, plot_y + plot_h + 44, row.short_lines))
    out.extend(
        [
            text(plot_x + plot_w / 2, height - 66, "Models sorted by Robust BO-Eval over all 18 tasks. Tiny-gap tasks fall back to clipped B-Eval, so the leaderboard is not driven by ratio outliers.", cls="small-note", anchor="middle"),
        ]
    )
    path_out = OUT_DIR / f"{OUTPUT_PREFIX}-effect-bar.svg"
    path_out.write_text(svg_shell(width, height, "\n".join(out)), encoding="utf-8")
    return path_out


def write_o_eval_bar(rows: list[Row]) -> Path:
    width, height = 1800, 1040
    card_x, card_y, card_w, card_h = 24, 24, width - 48, height - 48
    plot_x, plot_y, plot_w, plot_h = 132, 332, 1570, 440
    rows_sorted = sorted(rows, key=lambda row: row.o_eval_pct, reverse=True)
    max_o = max(row.o_eval_pct for row in rows_sorted)
    domain_max = max(100.0, axis_ceiling(max_o * 1.08, 20.0))
    ticks = [domain_max * i / 5 for i in range(6)]
    grid, sy = draw_grid(
        plot_x,
        plot_y,
        plot_w,
        plot_h,
        ticks,
        domain_max,
        fmt=lambda v: f"{v:.0f}%",
    )
    gap = 34
    bar_w = (plot_w - gap * (len(rows_sorted) - 1)) / len(rows_sorted)
    out = [
        rect(card_x, card_y, card_w, card_h, fill="#ffffff", stroke="#dddddd", rx=16),
        rect(card_x, card_y, card_w, 88, fill="#ffffff", rx=16),
        draw_tabs("o-effect", card_x + 42, card_y + 50),
        line(card_x, card_y + 90, card_x + card_w, card_y + 90, stroke="#dddddd", width=1.2),
        text(card_x + 42, 170, "O-Eval", cls="title"),
        text(card_x + 42, 210, "Absolute oracle-normalized score: model direction-aware raw divided by O-award raw over all 18 tasks.", cls="subtitle"),
        circle(card_x + 52, 270, 8, fill="#555555"),
        text(card_x + 70, 277, "O-Eval score", cls="legend"),
        circle(card_x + 222, 270, 8, fill="#b0b0b0"),
        text(card_x + 240, 277, "Mean raw label", cls="legend"),
        draw_brand(plot_x + plot_w - 420, plot_y - 34),
        grid,
        line(plot_x, sy(100.0), plot_x + plot_w, sy(100.0), stroke="#777777", width=1.8, dash="6 8", opacity=0.75),
        text(plot_x + plot_w - 12, sy(100.0) - 10, "O-award = 100%", cls="small-note", anchor="end"),
        text(plot_x - 88, plot_y + plot_h / 2, "O-Eval (%)", cls="axis-title", anchor="middle", transform=f"rotate(-90 {plot_x - 88:.2f} {plot_y + plot_h / 2:.2f})"),
    ]
    for idx, row in enumerate(rows_sorted):
        x = plot_x + idx * (bar_w + gap)
        y = sy(row.o_eval_pct)
        h = plot_y + plot_h - y
        out.append(rect(x, y, bar_w, h, fill=row.color, rx=8))
        if h > 30:
            out.append(text(x + bar_w / 2, y + h * 0.56, f"{row.o_eval_pct:.1f}%", cls="bar-label", anchor="middle"))
        raw_label = f"raw {fmt_num(row.raw, 3)}"
        out.append(text(x + bar_w / 2, y - 14, raw_label, cls="top-label", anchor="middle"))
        out.append(multiline_rotated_label(x + bar_w / 2, plot_y + plot_h + 44, row.short_lines))
    out.append(text(plot_x + plot_w / 2, height - 66, "Models sorted by O-Eval over all 18 tasks. This is the primary absolute score for the report.", cls="small-note", anchor="middle"))
    path_out = OUT_DIR / f"{OUTPUT_PREFIX}-o-eval-bar.svg"
    path_out.write_text(svg_shell(width, height, "\n".join(out)), encoding="utf-8")
    return path_out


def write_token_usage(rows: list[Row]) -> Path:
    width, height = 1800, 1060
    card_x, card_y, card_w, card_h = 24, 24, width - 48, height - 48
    plot_x, plot_y, plot_w, plot_h = 132, 350, 1570, 430
    rows_sorted = sorted(rows, key=lambda row: row.total_usage_tokens)
    max_m = max(row.total_usage_tokens for row in rows_sorted) / 1_000_000
    domain_max = axis_ceiling(max_m * 1.08, 20)
    ticks = [domain_max * i / 6 for i in range(7)]
    grid, sy = draw_grid(plot_x, plot_y, plot_w, plot_h, ticks, domain_max, fmt=lambda v: fmt_tokens(v))
    gap = 34
    bar_w = (plot_w - gap * (len(rows_sorted) - 1)) / len(rows_sorted)
    out = [
        rect(card_x, card_y, card_w, card_h, fill="#ffffff", stroke="#dddddd", rx=16),
        draw_tabs("tokens", card_x + 42, card_y + 50),
        line(card_x, card_y + 90, card_x + card_w, card_y + 90, stroke="#dddddd", width=1.2),
        text(card_x + 42, 170, "Token Usage", cls="title"),
        text(card_x + 42, 210, "Run tokens split into cache-miss input, cached-read input, and output. Qwen cache is peer-average imputed.", cls="subtitle"),
        circle(card_x + 52, 278, 8, fill="#4c4c4c"),
        text(card_x + 70, 285, "Billable input", cls="legend"),
        circle(card_x + 246, 278, 8, fill="#cfcfcf"),
        text(card_x + 264, 285, "Cache hit input", cls="legend"),
        circle(card_x + 456, 278, 8, fill="#2f80ed"),
        text(card_x + 474, 285, "Output", cls="legend"),
        draw_brand(plot_x + plot_w - 420, plot_y - 34),
        grid,
        text(plot_x - 88, plot_y + plot_h / 2, "Tokens (million)", cls="axis-title", anchor="middle", transform=f"rotate(-90 {plot_x - 88:.2f} {plot_y + plot_h / 2:.2f})"),
    ]
    for idx, row in enumerate(rows_sorted):
        x = plot_x + idx * (bar_w + gap)
        segments = [
            ("Billable", row.billable_input_tokens / 1_000_000, "#4c4c4c"),
            ("Cache", row.cache_hit_tokens / 1_000_000, "#cfcfcf"),
            ("Output", row.output_tokens / 1_000_000, row.color),
        ]
        cursor_y = plot_y + plot_h
        total_m = row.total_usage_tokens / 1_000_000
        for _, value_m, fill in segments:
            seg_h = value_m / domain_max * plot_h
            cursor_y -= seg_h
            out.append(rect(x, cursor_y, bar_w, seg_h, fill=fill, rx=6 if cursor_y < plot_y + 5 else 0))
            if seg_h > 44:
                txt_fill = "#ffffff" if fill not in {"#cfcfcf"} else "#ffffff"
                out.append(text(x + bar_w / 2, cursor_y + seg_h / 2 + 7, fmt_tokens(value_m), cls="bar-label", anchor="middle", fill=txt_fill, size=19))
        out.append(text(x + bar_w / 2, sy(total_m) - 14, fmt_tokens(total_m), cls="top-label", anchor="middle"))
        out.append(multiline_rotated_label(x + bar_w / 2, plot_y + plot_h + 44, row.short_lines))
    out.append(text(plot_x + plot_w / 2, height - 66, "Cache-hit input is displayed separately and charged when the report price table provides a cached-read price.", cls="small-note", anchor="middle"))
    path_out = OUT_DIR / f"{OUTPUT_PREFIX}-token-usage.svg"
    path_out.write_text(svg_shell(width, height, "\n".join(out)), encoding="utf-8")
    return path_out


def write_cost(rows: list[Row]) -> Path:
    width, height = 1800, 1060
    card_x, card_y, card_w, card_h = 24, 24, width - 48, height - 48
    plot_x, plot_y, plot_w, plot_h = 132, 350, 1570, 430
    rows_sorted = sorted([row for row in rows if row.cost is not None], key=lambda row: row.cost or 0.0)
    if not rows_sorted:
        raise ValueError("no rows with estimated cost")
    max_cost = max(row.cost or 0.0 for row in rows_sorted)
    domain_max = axis_ceiling(max_cost * 1.12, 25)
    ticks = [domain_max * i / 5 for i in range(6)]
    grid, sy = draw_grid(plot_x, plot_y, plot_w, plot_h, ticks, domain_max, fmt=lambda v: f"{v:.0f}")
    gap = 34
    bar_w = (plot_w - gap * (len(rows_sorted) - 1)) / len(rows_sorted)
    out = [
        rect(card_x, card_y, card_w, card_h, fill="#ffffff", stroke="#dddddd", rx=16),
        draw_tabs("cost", card_x + 42, card_y + 50),
        line(card_x, card_y + 90, card_x + card_w, card_y + 90, stroke="#dddddd", width=1.2),
        text(card_x + 42, 170, "Estimated Cost", cls="title"),
        text(card_x + 42, 210, f"{cost_label()} estimate from the report price table: OpenRouter catalog when available, local fallback otherwise.", cls="subtitle"),
        circle(card_x + 52, 278, 8, fill="#d9dde4"),
        text(card_x + 70, 285, "Input cost", cls="legend"),
        circle(card_x + 218, 278, 8, fill="#cfcfcf"),
        text(card_x + 236, 285, "Cache hit cost", cls="legend"),
        circle(card_x + 424, 278, 8, fill="#2f80ed"),
        text(card_x + 442, 285, "Output cost", cls="legend"),
        draw_brand(plot_x + plot_w - 420, plot_y - 34),
        grid,
        text(plot_x - 88, plot_y + plot_h / 2, f"Estimated cost ({cost_label()})", cls="axis-title", anchor="middle", transform=f"rotate(-90 {plot_x - 88:.2f} {plot_y + plot_h / 2:.2f})"),
    ]
    for idx, row in enumerate(rows_sorted):
        x = plot_x + idx * (bar_w + gap)
        input_cost = row.input_cost
        cache_cost = row.cache_cost
        output_cost = row.output_cost
        segments = [("Input", input_cost, "#d9dde4"), ("Cache", cache_cost, "#cfcfcf"), ("Output", output_cost, row.color)]
        cursor_y = plot_y + plot_h
        for _, value, fill in segments:
            if value <= 0:
                continue
            seg_h = value / domain_max * plot_h
            cursor_y -= seg_h
            out.append(rect(x, cursor_y, bar_w, seg_h, fill=fill, rx=6 if cursor_y < plot_y + 5 else 0))
            if seg_h > 38:
                txt_fill = "#ffffff" if fill not in {"#d9dde4", "#cfcfcf"} else "#777777"
                out.append(text(x + bar_w / 2, cursor_y + seg_h / 2 + 7, f"{value:.1f}", cls="bar-label", anchor="middle", fill=txt_fill, size=18))
        out.append(text(x + bar_w / 2, sy(row.cost or 0.0) - 14, fmt_money(row.cost), cls="top-label", anchor="middle"))
        out.append(multiline_rotated_label(x + bar_w / 2, plot_y + plot_h + 44, row.short_lines))
    out.append(text(plot_x + plot_w / 2, height - 66, f"Price split is parsed from the generated report; USD/token prices use USD/CNY {OPENROUTER_USD_TO_RMB}.", cls="small-note", anchor="middle"))
    path_out = OUT_DIR / f"{OUTPUT_PREFIX}-cost.svg"
    path_out.write_text(svg_shell(width, height, "\n".join(out)), encoding="utf-8")
    return path_out


def log_scale(value: float, domain_min: float, domain_max: float, range_min: float, range_max: float) -> float:
    return range_min + (math.log(value) - math.log(domain_min)) / (math.log(domain_max) - math.log(domain_min)) * (range_max - range_min)


def pareto_front(rows: list[Row], *, metric: str = "robust") -> list[Row]:
    front = []
    priced_rows = [row for row in rows if row.cost is not None and row.cost > 0]
    for candidate in sorted(priced_rows, key=lambda row: row.cost or 0.0):
        dominated = False
        candidate_score = candidate.score_pct(metric)
        for other in priced_rows:
            if other is candidate:
                continue
            other_score = other.score_pct(metric)
            if (
                (other.cost_rmb or 0.0) <= (candidate.cost_rmb or 0.0)
                and other_score >= candidate_score
                and ((other.cost_rmb or 0.0) < (candidate.cost_rmb or 0.0) or other_score > candidate_score)
            ):
                dominated = True
                break
        if not dominated:
            front.append(candidate)
    return front


def write_effect_cost_scatter(rows: list[Row]) -> Path:
    width, height = 1800, 1100
    card_x, card_y, card_w, card_h = 24, 24, width - 48, height - 48
    plot_x, plot_y, plot_w, plot_h = 154, 330, 1520, 560
    priced_rows = [row for row in rows if row.cost is not None and row.cost > 0]
    if not priced_rows:
        raise ValueError("no rows with estimated cost")
    x_min = max(1.0, min(row.cost or 0.0 for row in priced_rows) * 0.75)
    x_max = max(row.cost or 0.0 for row in priced_rows) * 1.25
    min_effect = min(row.effect_pct for row in rows)
    max_effect = max(row.effect_pct for row in rows)
    score_threshold = max(5.0, min(10.0, max_effect * 0.75))
    y_min, y_max, y_step = effect_axis_domain([row.effect_pct for row in rows])
    if y_max <= score_threshold:
        y_max = axis_ceiling(score_threshold + y_step, y_step)
    expected_artifacts = max(row.artifacts for row in rows)

    def sx(value: float) -> float:
        return log_scale(value, x_min, x_max, plot_x, plot_x + plot_w)

    def sy(value: float) -> float:
        return plot_y + plot_h - (value - y_min) / (y_max - y_min) * plot_h

    cost_threshold = 80.0
    effect_threshold = score_threshold

    out = [
        rect(card_x, card_y, card_w, card_h, fill="#ffffff", stroke="#dddddd", rx=16),
        draw_tabs("scatter", card_x + 42, card_y + 50),
        line(card_x, card_y + 90, card_x + card_w, card_y + 90, stroke="#dddddd", width=1.2),
        text(card_x + 42, 170, "Robust BO-Eval vs. Cost", cls="title"),
        text(card_x + 42, 210, f"Robust BO-Eval vs. estimated {cost_label()} cost. Green marks the current high-value zone.", cls="subtitle"),
        rect(card_x + 42, 252, 24, 18, fill="#dff7e4", stroke="#98d9a5", rx=3),
        text(card_x + 78, 270, f"Value zone: <={cost_symbol()}{cost_threshold:.0f}, >={effect_threshold:.1f}% robust", cls="legend"),
        line(card_x + 560, 262, card_x + 620, 262, stroke="#222222", width=3, dash="1 10"),
        text(card_x + 636, 270, "Pareto line", cls="legend"),
        draw_brand(plot_x + plot_w - 420, plot_y - 30),
    ]

    green_x2 = sx(cost_threshold)
    green_y = sy(y_max)
    green_h = max(0.0, sy(effect_threshold) - sy(y_max))
    out.append(rect(plot_x, green_y, green_x2 - plot_x, green_h, fill="#dff7e4"))
    out.append(rect(green_x2, sy(effect_threshold), plot_x + plot_w - green_x2, plot_y + plot_h - sy(effect_threshold), fill="#fafafa"))

    tick = y_min
    y_ticks = []
    while tick <= y_max + 1e-9:
        y_ticks.append(tick)
        tick += y_step
    for tick in y_ticks:
        yy = sy(tick)
        out.append(line(plot_x, yy, plot_x + plot_w, yy, dash=None if abs(tick) < 1e-9 else "4 8", stroke="#9e9e9e" if abs(tick) < 1e-9 else "#cfcfcf", width=1.5 if abs(tick) < 1e-9 else 1.2))
        out.append(text(plot_x - 18, yy + 6, f"{tick}%", cls="axis", anchor="end"))
    x_ticks = [5, 10, 20, 50, 80, 100, 150, 200, 500, 800]
    for tick in x_ticks:
        if tick < x_min or tick > x_max:
            continue
        xx = sx(tick)
        out.append(line(xx, plot_y + plot_h, xx, plot_y + plot_h + 8, stroke="#777777", width=1.2))
        out.append(text(xx, plot_y + plot_h + 36, f"{tick}", cls="axis", anchor="middle"))
    out.extend(
        [
            line(plot_x, plot_y + plot_h, plot_x + plot_w, plot_y + plot_h, stroke="#9e9e9e", width=1.2),
            line(plot_x, plot_y, plot_x, plot_y + plot_h, stroke="#9e9e9e", width=1.2),
            text(plot_x + plot_w / 2, plot_y + plot_h + 82, f"Estimated cost ({cost_label()}, log scale)", cls="axis-title", anchor="middle"),
            text(plot_x - 104, plot_y + plot_h / 2, "Robust BO-Eval (%)", cls="axis-title", anchor="middle", transform=f"rotate(-90 {plot_x - 104:.2f} {plot_y + plot_h / 2:.2f})"),
            line(plot_x, sy(effect_threshold), plot_x + plot_w, sy(effect_threshold), stroke="#808080", width=1.2, dash="6 7", opacity=0.55),
            text(plot_x + plot_w - 10, sy(effect_threshold) - 10, f"{effect_threshold:.1f}% robust", cls="small-note", anchor="end"),
        ]
    )

    front = pareto_front(rows)
    out.append(path([(sx(row.cost), sy(row.effect_pct)) for row in front], stroke="#2f2f2f", width=3, dash="1 11"))

    point_specs: list[tuple[str, float, float, list[str]]] = []
    for row in priced_rows:
        x = sx(row.cost or 0.0)
        y = sy(row.effect_pct)
        label = scatter_label(row)
        if row.artifacts < expected_artifacts:
            label += f" ({row.artifacts}/{expected_artifacts})"
        point_specs.append((row.model, x, y, [label]))
    placements = place_point_labels(point_specs, (plot_x + 8, plot_y + 8, plot_x + plot_w - 8, plot_y + plot_h - 8))
    for row in priced_rows:
        x = sx(row.cost or 0.0)
        y = sy(row.effect_pct)
        out.append(circle(x, y, 11, fill=row.color, stroke="#ffffff", width=3))
        label = scatter_label(row)
        if row.artifacts < expected_artifacts:
            label += f" ({row.artifacts}/{expected_artifacts})"
        label_x, label_y, anchor = placements[row.model]
        out.append(text(label_x, label_y, label, cls="point-label", anchor=anchor))
    no_cost_rows = [row for row in rows if row.cost is None and row.model != "v4 flash baseline"]
    if no_cost_rows:
        note = "; ".join(f"{row.label}: {row.effect_pct:.1f}% robust, cost N/A" for row in no_cost_rows)
        out.append(rect(card_x + 760, 218, 900, 48, fill="#f3e8ff", rx=8))
        out.append(text(card_x + 780, 250, note, cls="legend", fill="#6d28d9"))
    out.append(text(plot_x + plot_w / 2, height - 72, "Pareto front rewards higher effect at lower cost; rows without API price estimates are not placed on the x-axis.", cls="small-note", anchor="middle"))
    path_out = OUT_DIR / f"{OUTPUT_PREFIX}-effect-cost-scatter.svg"
    path_out.write_text(svg_shell(width, height, "\n".join(out)), encoding="utf-8")
    return path_out


def write_o_eval_cost_scatter(rows: list[Row]) -> Path:
    width, height = 1800, 1100
    card_x, card_y, card_w, card_h = 24, 24, width - 48, height - 48
    plot_x, plot_y, plot_w, plot_h = 154, 330, 1520, 560
    priced_rows = [row for row in rows if row.cost is not None and row.cost > 0]
    if not priced_rows:
        raise ValueError("no rows with estimated cost")
    x_min = max(1.0, min(row.cost or 0.0 for row in priced_rows) * 0.75)
    x_max = max(row.cost or 0.0 for row in priced_rows) * 1.25
    max_o = max(row.o_eval_pct for row in rows)
    y_min = 0.0
    y_max = max(100.0, axis_ceiling(max_o * 1.08, 20.0))
    expected_artifacts = max(row.artifacts for row in rows)

    def sx(value: float) -> float:
        return log_scale(value, x_min, x_max, plot_x, plot_x + plot_w)

    def sy(value: float) -> float:
        return plot_y + plot_h - (value - y_min) / (y_max - y_min) * plot_h

    cost_threshold = 80.0
    score_threshold = 80.0

    out = [
        rect(card_x, card_y, card_w, card_h, fill="#ffffff", stroke="#dddddd", rx=16),
        draw_tabs("o-scatter", card_x + 42, card_y + 50),
        line(card_x, card_y + 90, card_x + card_w, card_y + 90, stroke="#dddddd", width=1.2),
        text(card_x + 42, 170, "O-Eval vs. Cost", cls="title"),
        text(card_x + 42, 210, f"Primary absolute O-normalized score against estimated {cost_label()} cost. Green marks the high-value zone.", cls="subtitle"),
        rect(card_x + 42, 252, 24, 18, fill="#dff7e4", stroke="#98d9a5", rx=3),
        text(card_x + 78, 270, f"Value zone: <={cost_symbol()}{cost_threshold:.0f}, >={score_threshold:.0f}% O-Eval", cls="legend"),
        line(card_x + 560, 262, card_x + 620, 262, stroke="#222222", width=3, dash="1 10"),
        text(card_x + 636, 270, "Pareto line", cls="legend"),
        draw_brand(plot_x + plot_w - 420, plot_y - 30),
    ]

    if x_min < cost_threshold < x_max:
        green_x2 = sx(cost_threshold)
        out.append(rect(plot_x, sy(y_max), green_x2 - plot_x, sy(score_threshold) - sy(y_max), fill="#dff7e4"))
        out.append(line(green_x2, plot_y, green_x2, plot_y + plot_h, stroke="#9ca3af", width=1.2, dash="6 7", opacity=0.55))
    out.append(rect(plot_x, sy(score_threshold), plot_x + plot_w - plot_x, plot_y + plot_h - sy(score_threshold), fill="#fafafa"))

    y_tick = y_min
    while y_tick <= y_max + 1e-9:
        yy = sy(y_tick)
        out.append(line(plot_x, yy, plot_x + plot_w, yy, dash="4 8", stroke="#cfcfcf", width=1.2))
        out.append(text(plot_x - 18, yy + 6, f"{y_tick:.0f}%", cls="axis", anchor="end"))
        y_tick += 20.0
    x_ticks = [5, 10, 20, 50, 80, 100, 150, 200, 500, 800]
    for tick in x_ticks:
        if tick < x_min or tick > x_max:
            continue
        xx = sx(tick)
        out.append(line(xx, plot_y + plot_h, xx, plot_y + plot_h + 8, stroke="#777777", width=1.2))
        out.append(text(xx, plot_y + plot_h + 36, f"{tick}", cls="axis", anchor="middle"))
    out.extend(
        [
            line(plot_x, plot_y + plot_h, plot_x + plot_w, plot_y + plot_h, stroke="#9e9e9e", width=1.2),
            line(plot_x, plot_y, plot_x, plot_y + plot_h, stroke="#9e9e9e", width=1.2),
            text(plot_x + plot_w / 2, plot_y + plot_h + 82, f"Estimated cost ({cost_label()}, log scale)", cls="axis-title", anchor="middle"),
            text(plot_x - 104, plot_y + plot_h / 2, "O-Eval (%)", cls="axis-title", anchor="middle", transform=f"rotate(-90 {plot_x - 104:.2f} {plot_y + plot_h / 2:.2f})"),
            line(plot_x, sy(score_threshold), plot_x + plot_w, sy(score_threshold), stroke="#808080", width=1.2, dash="6 7", opacity=0.55),
            line(plot_x, sy(100.0), plot_x + plot_w, sy(100.0), stroke="#777777", width=1.8, dash="6 8", opacity=0.75),
            text(plot_x + plot_w - 10, sy(100.0) - 10, "O-award = 100%", cls="small-note", anchor="end"),
            text(plot_x + plot_w - 10, sy(score_threshold) - 10, f"{score_threshold:.0f}% O-Eval", cls="small-note", anchor="end"),
        ]
    )

    front = pareto_front(rows, metric="o")
    out.append(path([(sx(row.cost), sy(row.o_eval_pct)) for row in front], stroke="#2f2f2f", width=3, dash="1 11"))

    point_specs: list[tuple[str, float, float, list[str]]] = []
    for row in priced_rows:
        x = sx(row.cost or 0.0)
        y = sy(row.o_eval_pct)
        label = scatter_label(row)
        if row.artifacts < expected_artifacts:
            label += f" ({row.artifacts}/{expected_artifacts})"
        point_specs.append((row.model, x, y, [label, f"{row.o_eval_pct:.1f}% / {fmt_money(row.cost)}"]))
    placements = place_point_labels(point_specs, (plot_x + 8, plot_y + 8, plot_x + plot_w - 8, plot_y + plot_h - 8))
    for row in priced_rows:
        x = sx(row.cost or 0.0)
        y = sy(row.o_eval_pct)
        out.append(circle(x, y, 11, fill=row.color, stroke="#ffffff", width=3))
        label = scatter_label(row)
        if row.artifacts < expected_artifacts:
            label += f" ({row.artifacts}/{expected_artifacts})"
        label_x, label_y, anchor = placements[row.model]
        out.append(text(label_x, label_y, label, cls="point-label", anchor=anchor))
        out.append(text(label_x, label_y + 24, f"{row.o_eval_pct:.1f}% / {fmt_money(row.cost)}", cls="small-note", anchor=anchor))
    no_cost_rows = [row for row in rows if row.cost is None and row.model != "v4 flash baseline"]
    if no_cost_rows:
        note = "; ".join(f"{row.label}: {row.o_eval_pct:.1f}% O-Eval, cost N/A" for row in no_cost_rows)
        out.append(rect(card_x + 760, 218, 900, 48, fill="#f3e8ff", rx=8))
        out.append(text(card_x + 780, 250, note, cls="legend", fill="#6d28d9"))
    out.append(text(plot_x + plot_w / 2, height - 72, f"This view answers: how close is each model to the O-award reproduction per {cost_label()} spent?", cls="small-note", anchor="middle"))
    path_out = OUT_DIR / f"{OUTPUT_PREFIX}-o-eval-cost-scatter.svg"
    path_out.write_text(svg_shell(width, height, "\n".join(out)), encoding="utf-8")
    return path_out


def convert_svg_to_png(path: Path) -> Path:
    png_path = path.with_suffix(".png")
    commands = [
        ["magick", str(path), str(png_path)],
        ["convert", str(path), str(png_path)],
        ["sips", "-s", "format", "png", str(path), "--out", str(png_path)],
    ]
    errors: list[str] = []
    for command in commands:
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except FileNotFoundError:
            errors.append(f"{command[0]} not found")
        except subprocess.CalledProcessError as exc:
            errors.append((exc.stderr or exc.stdout or command[0]).strip())
        else:
            return png_path
    raise RuntimeError(f"could not convert {path}: {'; '.join(errors)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-path", type=Path, default=REPORT_PATH)
    parser.add_argument("--output-prefix", default=OUTPUT_PREFIX)
    parser.add_argument(
        "--currency",
        choices=("rmb", "usd"),
        default="rmb",
        help="Currency for every cost figure (prices are stored per Mtok in RMB).",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=None,
        help="Only draw these report row labels (e.g. the multimodal subset).",
    )
    return parser.parse_args()


def main() -> None:
    global OUTPUT_PREFIX, MODEL_FILTER
    args = parse_args()
    OUTPUT_PREFIX = args.output_prefix
    set_cost_currency(args.currency)
    MODEL_FILTER = set(args.models or [])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = parse_report(args.report_path)
    if not rows:
        raise SystemExit(f"no rows parsed from {args.report_path}")
    paths = [
        write_effect_bar(rows),
        write_effect_cost_scatter(rows),
        write_o_eval_bar(rows),
        write_o_eval_cost_scatter(rows),
        write_token_usage(rows),
        write_cost(rows),
    ]
    for path_out in paths:
        print(path_out)
        print(convert_svg_to_png(path_out))


if __name__ == "__main__":
    main()
