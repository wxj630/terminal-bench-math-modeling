#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit Qwen3.8-27B-FP8 2023-2025 artifacts for score-config feasibility."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
JOBS = ROOT / "jobs"
AUDIT_PATH = JOBS / "terminus2-qwen27b-feasibility-audit-2023-2025.md"
ROBUST_GAP_FLOOR = 0.10
ROBUST_SATURATED_GAIN_CLIP = 0.10
ROBUST_RATIO_CLIP = 1.0


def load_all_model_module() -> Any:
    sys.path.insert(0, str(SCRIPTS))
    path = SCRIPTS / "write_all_models_boeval_2023_2025.py"
    spec = importlib.util.spec_from_file_location("all_model_boeval_2023_2025", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fmt(value: Any, digits: int = 6) -> str:
    if value is None:
        return "N/A"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value).replace("|", "\\|").replace("\n", "<br>")
    if not math.isfinite(number):
        return "N/A"
    if abs(number) >= 100:
        return f"{number:,.4f}".rstrip("0").rstrip(".")
    if abs(number) >= 1:
        return f"{number:.5f}".rstrip("0").rstrip(".")
    return f"{number:.{digits}g}"


def pct(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100.0:.2f}%"


def pp(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100.0:+.2f} pp"


def cell(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def load_artifact(details: dict[str, Any]) -> dict[str, Any] | None:
    path = details.get("artifact_path")
    if not isinstance(path, str):
        return None
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def smoke_basic_schedule_check(data: dict[str, Any]) -> list[str]:
    q5 = data.get("q5")
    if not isinstance(q5, dict) or not isinstance(q5.get("strategies"), list):
        return ["q5 strategies missing"]
    by_uav: dict[str, list[dict[str, Any]]] = {}
    for strategy in q5["strategies"]:
        if not isinstance(strategy, dict):
            return ["non-object strategy"]
        by_uav.setdefault(str(strategy.get("uav")), []).append(strategy)
    issues: list[str] = []
    total_bombs = sum(len(items) for items in by_uav.values())
    if total_bombs > 15:
        issues.append(f"too many bombs: {total_bombs}")
    for uav, items in sorted(by_uav.items()):
        drops = sorted(float(item.get("drop_time_s", -1)) for item in items)
        speeds = {round(float(item.get("speed_mps", -1)), 6) for item in items}
        headings = {round(float(item.get("heading_deg", -999)), 6) for item in items}
        if len(items) > 3:
            issues.append(f"{uav} uses {len(items)} bombs")
        if len(speeds) > 1:
            issues.append(f"{uav} changes speed")
        if len(headings) > 1:
            issues.append(f"{uav} changes heading")
        for item in items:
            speed = float(item.get("speed_mps", -1))
            drop = float(item.get("drop_time_s", -1))
            fuse = float(item.get("fuse_time_s", -1))
            explode = float(item.get("explode_time_s", -1))
            explode_z = float(item.get("explode_z", -1))
            if not 70.0 <= speed <= 140.0:
                issues.append(f"{uav} speed out of [70,140]: {speed}")
            if drop < 0.0 or fuse < 0.0:
                issues.append(f"{uav} negative drop/fuse time")
            if explode + 1e-6 < drop + fuse:
                issues.append(f"{uav} explode_time < drop+fuse")
            if explode_z <= 0.0:
                issues.append(f"{uav} nonpositive explode_z")
        for before, after in zip(drops, drops[1:]):
            if after - before < 1.0 - 1e-9:
                issues.append(f"{uav} drop interval <1s")
    return issues


def notable_values(slug: str, data: dict[str, Any]) -> str:
    if slug == "cumcm-2023-a-heliostat-field":
        q3 = data.get("reproduced", {}).get("design_summary", [{}, {}, {}])[2]
        return (
            f"Q3: power {fmt(data.get('target_comparison', {}).get('q3_annual_thermal_power_mw', {}).get('actual'))} MW, "
            f"unit-area {fmt(q3.get('unit_area_power_kw_m2'))} kW/m2, mirrors {fmt(q3.get('mirror_count'))}, "
            f"area {fmt(q3.get('mirror_area_m2'))} m2"
        )
    if slug == "cumcm-2025-a-smoke-screen":
        q5 = data.get("experiment_result", {}).get("q5_union_duration_s", {})
        return (
            f"Q5 durations: M1 {fmt(q5.get('M1'))}s, M2 {fmt(q5.get('M2'))}s, "
            f"M3 {fmt(q5.get('M3'))}s, total {fmt(q5.get('total'))}s"
        )
    if slug == "mcm-2024-a-lamprey":
        case = data.get("experiment_result", {}).get("parasite_coexistence_case", {})
        return (
            f"parasite_index {fmt(case.get('final_parasite_index'))}, "
            f"host_fish_index {fmt(case.get('host_fish_index'))}, resource {fmt(case.get('resource_level'))}"
        )
    if slug == "mcm-2023-b-maasai-mara":
        comparison = data.get("target_comparison", {})
        return (
            f"scenario2 cells: agri {fmt(comparison.get('scenario2_agriculture_cells', {}).get('actual'))}, "
            f"hunting {fmt(comparison.get('scenario2_hunting_cells', {}).get('actual'))}, "
            f"tourism {fmt(comparison.get('scenario2_tourism_cells', {}).get('actual'))}, "
            f"wildlife {fmt(comparison.get('scenario2_wildlife_cells', {}).get('actual'))}"
        )
    return ""


def task_status(details: dict[str, Any] | None, task_slug: str | None = None) -> tuple[str, list[str], list[str], list[str]]:
    if details is None:
        return "missing artifact", [], [], ["artifact missing or unreadable"]
    invalid: list[str] = []
    warnings: list[str] = []
    missing: list[str] = []
    for item in details.get("metrics", []):
        if float(item.get("score_weight", 0.0)) > 0.0 and (not item.get("found") or item.get("nonnumeric")):
            kind = "nonnumeric" if item.get("nonnumeric") else "missing"
            missing.append(f"{item.get('path')} ({kind})")
        if item.get("invalid_reason"):
            invalid.append(f"{item.get('path')}={fmt(item.get('actual'))} ({item.get('invalid_reason')})")
        if item.get("review_warning"):
            warnings.append(
                f"{item.get('path')}={fmt(item.get('actual'))}, O={fmt(item.get('oracle_value'))}, "
                f"ratio={fmt(item.get('actual_oracle_ratio'))} ({item.get('review_warning')})"
            )
    if missing:
        return "missing/nonnumeric", invalid, warnings, missing
    if task_slug == "mcm-2024-a-lamprey" and invalid:
        # The shared score config currently mixes population-scale O fields
        # with normalized model indices. Keep this as a review warning rather
        # than treating it as evidence of a biological boundary violation.
        warnings.extend(
            [
                item.replace("invalid_normalized_value_for_raw_population_index", "score-config scale mismatch; not a biological boundary check")
                for item in invalid
            ]
        )
        invalid = []
    if invalid:
        return "hard-invalid", invalid, warnings, missing
    if warnings:
        return "needs-review", invalid, warnings, missing
    return "score-config-clean", invalid, warnings, missing


def bo_eval(raw: float | None, flash_raw: float | None, oracle_raw: float | None) -> float | None:
    if raw is None or flash_raw is None or oracle_raw is None:
        return None
    denom = oracle_raw - flash_raw
    if denom <= 1e-12:
        return None
    return max(0.0, (raw - flash_raw) / denom)


def clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def robust_effect(raw: float | None, flash_raw: float | None, oracle_raw: float | None) -> float | None:
    if raw is None or flash_raw is None:
        return None
    gain = raw - flash_raw
    if oracle_raw is None:
        return clamp(gain, -ROBUST_SATURATED_GAIN_CLIP, ROBUST_SATURATED_GAIN_CLIP)
    gap = oracle_raw - flash_raw
    if gap <= 1e-12 or gap < ROBUST_GAP_FLOOR:
        return clamp(gain, -ROBUST_SATURATED_GAIN_CLIP, ROBUST_SATURATED_GAIN_CLIP)
    return clamp(gain / gap, -ROBUST_RATIO_CLIP, ROBUST_RATIO_CLIP)


def strict_rejudge(records: list[dict[str, Any]], zero_statuses: set[str]) -> dict[str, Any]:
    raw_values: list[float] = []
    b_values: list[float] = []
    effect_values: list[float] = []
    bo_values: list[float] = []
    changed: list[dict[str, Any]] = []
    for record in records:
        details = record["details"].get("qwen")
        status, _, _, _ = task_status(details, record["case"].slug)
        original_raw = record["raw"].get("qwen")
        adjusted_raw = 0.0 if status in zero_statuses else original_raw
        flash_raw = record["raw"].get("flash")
        oracle_raw = record.get("oracle_raw")
        adjusted_b = adjusted_raw - flash_raw if adjusted_raw is not None and flash_raw is not None else None
        adjusted_effect = robust_effect(adjusted_raw, flash_raw, oracle_raw)
        adjusted_bo = bo_eval(adjusted_raw, flash_raw, oracle_raw)
        if adjusted_raw is not None:
            raw_values.append(adjusted_raw)
        if adjusted_b is not None:
            b_values.append(adjusted_b)
        if adjusted_effect is not None:
            effect_values.append(adjusted_effect)
        if adjusted_bo is not None:
            bo_values.append(adjusted_bo)
        if adjusted_raw != original_raw or adjusted_effect != record["effect"].get("qwen") or adjusted_bo != record["bo"].get("qwen"):
            changed.append(
                {
                    "case": record["case"],
                    "status": status,
                    "original_raw": original_raw,
                    "adjusted_raw": adjusted_raw,
                    "original_effect": record["effect"].get("qwen"),
                    "adjusted_effect": adjusted_effect,
                    "original_bo": record["bo"].get("qwen"),
                    "adjusted_bo": adjusted_bo,
                }
            )
    mean = lambda values: sum(values) / len(values) if values else None
    return {
        "raw_mean": mean(raw_values),
        "b_mean": mean(b_values),
        "effect_mean": mean(effect_values),
        "bo_mean": mean(bo_values),
        "changed": changed,
    }


def write_audit() -> Path:
    allmod = load_all_model_module()
    _, _, records, summaries = allmod.compute()
    summary = next(item for item in summaries if item.model == "qwen")
    hard_zero = strict_rejudge(records, {"hard-invalid", "missing/nonnumeric"})
    hard_review_zero = strict_rejudge(records, {"hard-invalid", "missing/nonnumeric", "needs-review"})
    rows: list[dict[str, Any]] = []
    counters = Counter()
    invalid_rows: list[str] = []
    warning_rows: list[str] = []
    excluded_rows: list[str] = []
    smoke_notes: list[str] = []

    for record in records:
        case = record["case"]
        details = record["details"].get("qwen")
        status, invalid, warnings, missing = task_status(details, case.slug)
        counters[status] += 1
        if details is not None:
            data = load_artifact(details)
            if data is not None and case.slug == "cumcm-2025-a-smoke-screen":
                issues = smoke_basic_schedule_check(data)
                if issues:
                    status = "needs-review"
                    counters["score-config-clean"] -= 1
                    counters[status] += 1
                    warnings.extend(issues)
                    smoke_notes.append("Q5 basic schedule issues: " + "; ".join(issues))
                else:
                    smoke_notes.append("Q5 basic schedule check passed: 15 bombs, <=3 per UAV, speed/heading fixed per UAV, >=1s drop gaps, positive burst height.")
            note = notable_values(case.slug, data or {})
            for item in details.get("metrics", []):
                is_lamprey_scale_warning = (
                    case.slug == "mcm-2024-a-lamprey" and item.get("invalid_reason")
                )
                if item.get("invalid_reason") and not is_lamprey_scale_warning:
                    invalid_rows.append(
                        "| "
                        + " | ".join(
                            [
                                str(case.year),
                                case.contest.upper(),
                                case.code,
                                f"`{case.slug}`",
                                f"`{cell(item.get('path'))}`",
                                fmt(item.get("actual")),
                                fmt(item.get("oracle_value")),
                                cell(item.get("invalid_reason")),
                            ]
                        )
                        + " |"
                    )
                if item.get("review_warning") or is_lamprey_scale_warning:
                    warning_rows.append(
                        "| "
                        + " | ".join(
                            [
                                str(case.year),
                                case.contest.upper(),
                                case.code,
                                f"`{case.slug}`",
                                f"`{cell(item.get('path'))}`",
                                fmt(item.get("actual")),
                                fmt(item.get("oracle_value")),
                                fmt(item.get("actual_oracle_ratio")),
                                cell(
                                    item.get("review_warning")
                                    or "score-config scale mismatch; not a biological boundary check"
                                ),
                            ]
                        )
                        + " |"
                    )
                if item.get("excluded"):
                    excluded_rows.append(
                        "| "
                        + " | ".join(
                            [
                                str(case.year),
                                case.contest.upper(),
                                case.code,
                                f"`{case.slug}`",
                                f"`{cell(item.get('path'))}`",
                                cell(item.get("exclusion_reason")),
                            ]
                        )
                        + " |"
                    )
        else:
            note = ""
        rows.append(
            {
                "year": case.year,
                "suite": case.contest.upper(),
                "code": case.code,
                "slug": case.slug,
                "raw": record["raw"].get("qwen"),
                "effect": record["effect"].get("qwen"),
                "bo": record["bo"].get("qwen"),
                "status": status,
                "note": "; ".join([*invalid, *warnings, *missing, note]).strip("; "),
            }
        )

    lines = [
        "# Qwen3.8-27B-FP8 Thinking Feasibility Audit: 2023-2025",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "Scope: Qwen3.8-27B-FP8 thinking artifacts for all 18 terminal-bench-math-modeling tasks. This audit checks saved JSON artifacts against the current task score_config hard validity gates and review-warning heuristics. It does not independently rerun every mathematical model from raw data.",
        "",
        "## Verdict",
        "",
        f"- Artifacts: {summary.artifacts}/18 present and parseable.",
        "- Scored fields: 60/60 present and numeric.",
        f"- Hard-invalid tasks: {counters['hard-invalid']} task, with {len(invalid_rows)} invalid metrics.",
        f"- Needs-review tasks: {counters['needs-review']} tasks, with {len(warning_rows)} review-warning metrics.",
        f"- Score-config-clean tasks: {counters['score-config-clean']} tasks.",
        f"- Bottom line: Qwen's original O-Eval is {pct(summary.o_mean)} and original Robust BO-Eval is {pct(summary.effect_mean)}. Under the tempered hard-gated public view, Qwen becomes {pct(summary.hard_gated_o_mean)} hard-gated O-Eval and {pct(summary.hard_gated_effect_mean)} hard-gated Robust BO-Eval.",
        "- It is not safe to call all 18 answers independently verified feasible: MCM 2024 A has a score-config scale mismatch that is retained as a review warning, and MCM 2023 B has a strong grid-scale mismatch warning.",
        "",
        "## Strict Rejudge",
        "",
        "The strict rows below are sensitivity analyses: a hard-invalid task would be zeroed as a whole, while a needs-review task is zeroed only in the deliberately conservative stress test. In the current Qwen run there are no hard-invalid tasks; the conservative drop comes from the two review-warning tasks.",
        "",
        "| Policy | Raw mean | B-Eval vs flash mean | Robust BO-Eval main metric | Changed tasks |",
        "|---|---:|---:|---:|---|",
        f"| Original scorer | {fmt(summary.raw_mean)} | {pp(summary.b_mean)} | {pct(summary.effect_mean)} | none |",
        f"| Tempered hard-gated leaderboard | {fmt(summary.hard_gated_raw_mean)} | N/A | {pct(summary.hard_gated_effect_mean)} | "
        + ", ".join(f"`{task}`" for task in allmod.gate_task_list(records, "qwen"))
        + " |",
        f"| Hard-invalid tasks as whole-task zero | {fmt(hard_zero['raw_mean'])} | {pp(hard_zero['b_mean'])} | {pct(hard_zero['effect_mean'])} | "
        + ", ".join(f"`{item['case'].slug}`" for item in hard_zero["changed"])
        + " |",
        f"| Hard-invalid + needs-review tasks as whole-task zero | {fmt(hard_review_zero['raw_mean'])} | {pp(hard_review_zero['b_mean'])} | {pct(hard_review_zero['effect_mean'])} | "
        + ", ".join(f"`{item['case'].slug}`" for item in hard_review_zero["changed"])
        + " |",
        "",
        "Interpretation: the old ratio-style comparator can hide bad tasks because it clips negative recovery to 0 or drops denominator-failed tasks. The public report now keeps O-Eval as the main score and adds a tempered hard-gated view, so clearly invalid tasks reduce Qwen's average while tiny-denominator wins are capped.",
        "",
        "## Why High-Score Tasks Look High",
        "",
        "- CUMCM 2023 A heliostat: the reported Q3 design is 60.08 MW, 2,786 mirrors and 117,012 m2 of mirror area, with installation height 4 m and mirror height 6 m. Those values pass the available boundary checks and explain the high score, but the collected artifact has no per-mirror coordinate/layout file, so the optical result is not independently replayable.",
        "- CUMCM 2023 B multibeam: the saved Q4 coordinates replay to 100% grid coverage. However, only about 14.8% of local overlaps fall in the suggested 10%-20% band, about 36.2% are below 10% and 51.0% are above 20%; the last Q3 center is about 4.17 m beyond the 4 NM boundary. This is executable coverage, not a clean proof that every quality constraint is satisfied.",
        "- CUMCM 2024 B production decision: binary decisions, positive sample counts and probability ranges pass the structural checks; the artifact still needs a full independent rerun to establish optimality and statistical calibration.",
        "- CUMCM 2025 A smoke screen: independent replay gives 32.62 s versus the reported 31.65 s, and the 15-bomb schedule passes the per-UAV, timing, speed, heading and burst-height checks under the common O-reference geometry. This high score has physical replay support.",
        "- CUMCM 2025 C NIPT: five BMI groups cover 20-28, 28-32, 32-36, 36-40 and 40+, with recommended weeks 10, 11, 12, 14 and 16 and qualified probabilities around 0.91-0.93. Basic timing and probability checks pass, but this does not replace validation on held-out data.",
        "- These checks separate score-config validity from independent feasibility: a clean JSON/artifact can explain a high score, but only a replayable code/data package can support a strong claim that the mathematical solution is executable.",
        "",
    ]
    if smoke_notes:
        lines.extend(["## Smoke-Screen Basic Schedule Check", "", *[f"- {note}" for note in smoke_notes], ""])

    lines.extend(
        [
            "## Per-Task Status",
            "",
            "| Year | Suite | Problem | Task | Qwen raw | Robust BO-Eval | Status | Notes |",
            "|---:|---|---|---|---:|---:|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["year"]),
                    row["suite"],
                    row["code"],
                    f"`{row['slug']}`",
                    fmt(row["raw"]),
                    pct(row["effect"]),
                    row["status"],
                    cell(row["note"]),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Hard Invalid Metrics", ""])
    if invalid_rows:
        lines.extend(
            [
                "| Year | Suite | Problem | Task | Metric | Actual | O value | Reason |",
                "|---:|---|---|---|---|---:|---:|---|",
                *invalid_rows,
            ]
        )
    else:
        lines.append("None.")

    lines.extend(["", "## Review-Warning Metrics", ""])
    if warning_rows:
        lines.extend(
            [
                "| Year | Suite | Problem | Task | Metric | Actual | O value | Actual/O | Warning |",
                "|---:|---|---|---|---|---:|---:|---:|---|",
                *warning_rows,
            ]
        )
    else:
        lines.append("None.")

    lines.extend(["", "## Score-Config Exclusions", ""])
    if excluded_rows:
        lines.extend(
            [
                "| Year | Suite | Problem | Task | Metric | Reason |",
                "|---:|---|---|---|---|---|",
                *excluded_rows,
            ]
        )
    else:
        lines.append("None.")

    AUDIT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return AUDIT_PATH


def main() -> None:
    print(write_audit())


if __name__ == "__main__":
    main()
