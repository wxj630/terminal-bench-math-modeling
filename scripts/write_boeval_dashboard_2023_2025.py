#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write a clickable local HTML dashboard for the 2023-2025 BO-Eval report."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "jobs"
REPORT_PATH = JOBS / "terminus2-direction-aware-flash-baseline-bbo-2023-2025.md"
ARTICLE_PATH = JOBS / "terminus2-bo-eval-plain-language-article-2023-2025.md"
AUDIT_PATH = JOBS / "terminus2-all-model-feasibility-audit-2023-2025.md"
HTML_PATH = JOBS / "terminus2-bo-eval-aa-dashboard-2023-2025.html"


FIGURE_TABS = [
    ("hard-gated-o-effect", "HardGate O效果", "aa-style-2023-2025-hard-gated-o-eval-bar.png"),
    ("hard-gated-o-score-cost", "HardGate O分数-cost", "aa-style-2023-2025-hard-gated-o-eval-cost-scatter.png"),
    ("o-effect", "O效果", "aa-style-2023-2025-o-eval-bar.png"),
    ("o-score-cost", "O分数-cost", "aa-style-2023-2025-o-eval-cost-scatter.png"),
    ("effect", "Robust效果", "aa-style-2023-2025-boeval-effect-bar.png"),
    ("score-cost", "Robust分数-cost", "aa-style-2023-2025-boeval-score-cost.png"),
    ("tokens", "Token", "aa-style-2023-2025-token-usage.png"),
    ("cost", "成本", "aa-style-2023-2025-cost.png"),
    ("year", "O年份", "aa-style-2023-2025-o-eval-year-split.png"),
    ("suite", "O赛制", "aa-style-2023-2025-o-eval-suite-split.png"),
]


@dataclass
class ModelRow:
    model: str
    artifacts: str
    raw: str
    o_eval: str
    effect: str
    tokens: str
    cost: str


@dataclass
class HardGatedRow:
    model: str
    hard_o_eval: str
    hard_effect: str
    original_o_eval: str
    gates: str
    cost: str


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table(lines: list[str]) -> str:
    header = split_table_row(lines[0])
    body_lines = lines[2:]
    out = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    out.extend(f"<th>{inline_md(cell)}</th>" for cell in header)
    out.append("</tr></thead><tbody>")
    for line in body_lines:
        cells = split_table_row(line)
        out.append("<tr>")
        out.extend(f"<td>{inline_md(cell)}</td>" for cell in cells)
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    in_code = False
    code_lines: list[str] = []
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append("<p>" + inline_md(" ".join(paragraph)) + "</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            out.append("<ul>" + "".join(f"<li>{inline_md(item)}</li>" for item in list_items) + "</ul>")
            list_items = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not stripped:
            flush_paragraph()
            flush_list()
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
            flush_paragraph()
            flush_list()
            table_lines = [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            out.append(render_table(table_lines))
            continue
        if stripped.startswith("### "):
            flush_paragraph()
            flush_list()
            out.append(f"<h3>{inline_md(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            flush_paragraph()
            flush_list()
            out.append(f"<h2>{inline_md(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            flush_paragraph()
            flush_list()
            out.append(f"<h1>{inline_md(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            flush_paragraph()
            list_items.append(stripped[2:])
        elif stripped.startswith("!["):
            flush_paragraph()
            flush_list()
            out.append("<figure class=\"inline-figure\">" + inline_md(stripped) + "</figure>")
        else:
            paragraph.append(stripped)
        i += 1
    flush_paragraph()
    flush_list()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(out)


def section_between(markdown: str, heading: str, next_heading: str | None = None) -> str:
    lines = markdown.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    end = len(lines)
    if next_heading is not None:
        for i in range(start + 1, len(lines)):
            if lines[i].strip() == next_heading:
                end = i
                break
    elif heading.startswith("## "):
        for i in range(start + 1, len(lines)):
            if lines[i].startswith("## "):
                end = i
                break
    return "\n".join(lines[start:end])


def parse_overall_rows(report_md: str) -> list[ModelRow]:
    table_md = section_between(report_md, "## Overall Mean").splitlines()
    table_lines = [line for line in table_md if line.startswith("|")]
    headers = split_table_row(table_lines[0])
    idx = {name: i for i, name in enumerate(headers)}
    o_header = "Mean O-Eval on all 18 (%)"
    effect_header = "Mean Robust BO-Eval on all 18 (%)"
    if effect_header not in idx:
        effect_header = "Mean B/BO fallback effect on all 18 (%)"
    rows: list[ModelRow] = []
    for line in table_lines[2:]:
        cells = split_table_row(line)
        if len(cells) < len(headers):
            continue
        rows.append(
            ModelRow(
                model=cells[idx["Model"]],
                artifacts=cells[idx["Artifacts"]],
                raw=cells[idx["Mean direction-aware raw"]],
                o_eval=cells[idx[o_header]] if o_header in idx else "N/A",
                effect=cells[idx[effect_header]],
                tokens=cells[idx["Tokens input/cache/output"]],
                cost=cells[idx["Est. cost RMB"]],
            )
        )
    return rows


def parse_hard_gated_rows(report_md: str) -> list[HardGatedRow]:
    try:
        table_md = section_between(report_md, "## Tempered Hard-Gated Leaderboard").splitlines()
    except StopIteration:
        return []
    table_lines = [line for line in table_md if line.startswith("|")]
    if len(table_lines) < 3:
        return []
    headers = split_table_row(table_lines[0])
    idx = {name: i for i, name in enumerate(headers)}
    rows: list[HardGatedRow] = []
    for line in table_lines[2:]:
        cells = split_table_row(line)
        if len(cells) < len(headers):
            continue
        rows.append(
            HardGatedRow(
                model=cells[idx["Model"]],
                hard_o_eval=cells[idx["Hard-gated O-Eval"]],
                hard_effect=cells[idx["Hard-gated Robust BO-Eval"]],
                original_o_eval=cells[idx["Original O-Eval"]],
                gates=cells[idx["Hard gates"]],
                cost=cells[idx["Est. cost RMB"]],
            )
        )
    return rows


def top_card(rows: list[ModelRow], model_name: str) -> ModelRow | None:
    return next((row for row in rows if row.model == model_name), None)


def percent_value(text: str) -> float:
    try:
        return float(text.replace("%", "").replace("+", "").strip())
    except ValueError:
        return float("-inf")


def render_overview(report_md: str, article_md: str) -> str:
    rows = parse_overall_rows(report_md)
    hard_rows = parse_hard_gated_rows(report_md)
    best_o = max((row for row in rows if row.model != "v4 flash baseline"), key=lambda row: percent_value(row.o_eval), default=None)
    best_robust = max((row for row in rows if row.model != "v4 flash baseline"), key=lambda row: percent_value(row.effect), default=None)
    best_hard_gated = max((row for row in hard_rows if row.model != "v4 flash baseline"), key=lambda row: percent_value(row.hard_o_eval), default=None)
    qwen = top_card(rows, "Qwen3.8-27B-FP8 thinking")
    kimi = top_card(rows, "Kimi K3")
    gemini = top_card(rows, "Gemini 3.7 Flash high primary+retry")
    report_intro = "\n".join(report_md.splitlines()[:40])
    article_intro = section_between(article_md, "## 先说结论", "## 图怎么读")

    cards = [
        ("最佳 O-Eval", best_o.o_eval if best_o else "N/A", (best_o.model + " · 主榜") if best_o else ""),
        ("最佳 HardGate O", best_hard_gated.hard_o_eval if best_hard_gated else "N/A", (best_hard_gated.model + " · 谨慎榜") if best_hard_gated else ""),
        ("最佳 Robust", best_robust.effect if best_robust else "N/A", (best_robust.model + " · 辅助口径，冲突时让位 O-Eval") if best_robust else "辅助口径"),
        ("Qwen O-Eval", qwen.o_eval if qwen else "N/A", (qwen.cost + " · OpenRouter价/原始cache计数") if qwen else ""),
        ("Kimi O-Eval", kimi.o_eval if kimi else "N/A", kimi.cost if kimi else ""),
        ("Gemini 覆盖", f"{gemini.artifacts}/18" if gemini else "N/A", "缺失 artifact 按 raw 0"),
    ]
    card_html = "\n".join(
        f"<article class=\"metric\"><span>{inline_md(label)}</span><strong>{inline_md(value)}</strong><small>{inline_md(note)}</small></article>"
        for label, value, note in cards
    )
    return (
        "<div class=\"metrics\">"
        + card_html
        + "</div>"
        + "<div class=\"two-col\">"
        + "<section class=\"prose mini\">"
        + markdown_to_html(article_intro)
        + "</section>"
        + "<section class=\"prose mini\">"
        + markdown_to_html(report_intro)
        + "</section>"
        + "</div>"
    )


def figure_panel(tab_id: str, title: str, filename: str) -> str:
    source = f"figures/{filename}"
    return (
        f"<figure class=\"chart-frame\">"
        f"<img src=\"{source}\" alt=\"{html.escape(title)}\" loading=\"lazy\">"
        f"<figcaption><a href=\"{source}\">{html.escape(filename)}</a></figcaption>"
        f"</figure>"
    )


def render_html() -> str:
    report_md = REPORT_PATH.read_text(encoding="utf-8")
    article_md = ARTICLE_PATH.read_text(encoding="utf-8")
    audit_md = AUDIT_PATH.read_text(encoding="utf-8") if AUDIT_PATH.exists() else "# Qwen 可行性\n\n审计文件尚未生成。"
    report_html = markdown_to_html(report_md)
    article_html = markdown_to_html(article_md)
    audit_html = markdown_to_html(audit_md)
    overview_html = render_overview(report_md, article_md)

    tabs = [
        ("overview", "总览"),
        *[(tab_id, label) for tab_id, label, _ in FIGURE_TABS],
        ("qwen-audit", "Qwen可行性"),
        ("report", "正式报告"),
        ("article", "大白话"),
    ]
    nav = "\n".join(
        f'<button type="button" class="tab{" active" if tab_id == "overview" else ""}" data-target="{tab_id}" aria-controls="{tab_id}" aria-selected="{"true" if tab_id == "overview" else "false"}">{label}</button>'
        for tab_id, label in tabs
    )
    panels = [
        f'<section id="overview" class="panel active">{overview_html}</section>',
        *[
            f'<section id="{tab_id}" class="panel">{figure_panel(tab_id, label, filename)}</section>'
            for tab_id, label, filename in FIGURE_TABS
        ],
        f'<section id="qwen-audit" class="panel prose">{audit_html}</section>',
        f'<section id="report" class="panel prose">{report_html}</section>',
        f'<section id="article" class="panel prose">{article_html}</section>',
    ]
    css = """
    :root {
      color-scheme: light;
      --bg: #f7f7f5;
      --surface: #ffffff;
      --ink: #141414;
      --muted: #747474;
      --line: #deded8;
      --soft: #eceae4;
      --accent: #7c3aed;
      --green: #dff6e4;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(247, 247, 245, 0.94);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(10px);
    }
    .shell { max-width: 1440px; margin: 0 auto; padding: 22px 28px; }
    .topline { display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; margin-bottom: 16px; }
    h1 { margin: 0; font-family: Georgia, "Times New Roman", serif; font-size: 34px; line-height: 1.12; letter-spacing: 0; }
    .meta { color: var(--muted); font-size: 14px; font-weight: 650; }
    nav { display: flex; flex-wrap: wrap; gap: 8px; }
    .tab {
      border: 1px solid var(--line);
      background: var(--surface);
      color: #343434;
      font: inherit;
      font-weight: 750;
      min-height: 38px;
      padding: 7px 13px;
      border-radius: 8px;
      cursor: pointer;
    }
    .tab:hover { border-color: #bdbdb7; }
    .tab.active { background: #141414; color: #ffffff; border-color: #141414; }
    main.shell { padding-top: 24px; }
    .panel { display: none; }
    .panel.active { display: block; }
    .metrics { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 12px; margin-bottom: 18px; }
    .metric { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 15px 16px; }
    .metric span { display: block; color: var(--muted); font-size: 13px; font-weight: 800; }
    .metric strong { display: block; margin-top: 6px; font-size: 28px; line-height: 1.05; }
    .metric small { display: block; margin-top: 8px; color: var(--muted); font-size: 12px; font-weight: 650; overflow-wrap: anywhere; }
    .two-col { display: grid; grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr); gap: 16px; }
    .chart-frame, .prose, .mini {
      margin: 0;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }
    .chart-frame img { display: block; width: 100%; height: auto; border: 1px solid var(--soft); border-radius: 6px; background: #fff; }
    figcaption { margin-top: 10px; color: var(--muted); font-size: 12px; font-weight: 700; }
    a { color: #3f2fc4; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    .prose { max-width: none; overflow: hidden; }
    .prose h1, .prose h2, .prose h3 { font-family: Georgia, "Times New Roman", serif; letter-spacing: 0; }
    .prose h1 { font-size: 30px; margin: 0 0 18px; }
    .prose h2 { font-size: 24px; margin: 28px 0 12px; }
    .prose h3 { font-size: 19px; margin: 26px 0 8px; }
    .prose p { margin: 0 0 12px; }
    .prose ul { margin: 0 0 16px; padding-left: 20px; }
    .prose code { background: var(--soft); border-radius: 4px; padding: 1px 5px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.92em; }
    pre { background: #171717; color: #f2f2f2; border-radius: 8px; padding: 14px; overflow: auto; }
    pre code { background: transparent; padding: 0; }
    .table-wrap { overflow: auto; border: 1px solid var(--line); border-radius: 8px; margin: 14px 0 20px; }
    table { width: 100%; border-collapse: collapse; min-width: 860px; background: #fff; }
    th, td { border-bottom: 1px solid var(--line); padding: 9px 10px; text-align: left; vertical-align: top; font-size: 13px; }
    th { position: sticky; top: 0; background: #f4f3ef; font-weight: 850; }
    tr:last-child td { border-bottom: 0; }
    td:not(:first-child), th:not(:first-child) { text-align: right; }
    .inline-figure img { max-width: 100%; height: auto; border: 1px solid var(--line); border-radius: 6px; }
    @media (max-width: 900px) {
      .shell { padding: 16px; }
      .topline { align-items: flex-start; flex-direction: column; }
      h1 { font-size: 27px; }
      .metrics, .two-col { grid-template-columns: 1fr; }
      .tab { flex: 1 1 auto; }
    }
    """
    js = """
    const tabs = Array.from(document.querySelectorAll('.tab'));
    const panels = Array.from(document.querySelectorAll('.panel'));
    function activate(id, push = true) {
      tabs.forEach(tab => {
        const active = tab.dataset.target === id;
        tab.classList.toggle('active', active);
        tab.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      panels.forEach(panel => panel.classList.toggle('active', panel.id === id));
      if (push) history.replaceState(null, '', '#' + id);
    }
    tabs.forEach(tab => tab.addEventListener('click', () => activate(tab.dataset.target)));
    const initial = location.hash.slice(1);
    if (initial && document.getElementById(initial)) activate(initial, false);
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Terminal-Bench Math Modeling O-Eval / Robust BO-Eval 2023-2025</title>
  <style>{css}</style>
</head>
<body>
  <header>
    <div class="shell">
      <div class="topline">
        <div>
          <h1>18 题 O-Eval / Robust BO-Eval Dashboard</h1>
          <div class="meta">2023-2025 · generated {date.today().isoformat()} · AA-style</div>
        </div>
        <div class="meta"><a href="{REPORT_PATH.name}">正式报告</a> · <a href="{ARTICLE_PATH.name}">大白话</a> · <a href="{AUDIT_PATH.name}">全模型可行性复核</a></div>
      </div>
      <nav aria-label="Views">{nav}</nav>
    </div>
  </header>
  <main class="shell">
    {"".join(panels)}
  </main>
  <script>{js}</script>
</body>
</html>
"""


def main() -> None:
    HTML_PATH.write_text(render_html(), encoding="utf-8")
    print(HTML_PATH)


if __name__ == "__main__":
    main()
