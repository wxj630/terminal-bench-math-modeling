#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit saved 2023-2025 model answers for physical and structural feasibility.

This report deliberately separates score-config validity from independent
replay.  A final JSON artifact can be schema-complete without containing the
layout, code, or intermediate values needed to reproduce its claims.
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
import zipfile
from collections import defaultdict
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any

import xml.etree.ElementTree as ET

from feasibility_checks import validate_artifact


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
JOBS = ROOT / "jobs"
AUDIT_PATH = JOBS / "terminus2-all-model-feasibility-audit-2023-2025.md"
BATHYMETRY_XLSX = (
    ROOT
    / "tasks/CUMCM/cumcm-2023-b-multibeam-lines/environment/data/repo/cumcm/source_materials/extracted"
    / "2023_Y20WPner9fa62862794e6dc82731a5561ce1132f/B题/附件.xlsx"
)
VEGETABLE_DATA_DIR = (
    ROOT
    / "tasks/CUMCM/cumcm-2023-c-vegetable-pricing/environment/data/repo"
    / "cumcm/source_materials/extracted/2023_Y20WPner9fa62862794e6dc82731a5561ce1132f/C题"
)
XLSX_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NM_TO_M = 1852.0


def load_all_model_module() -> Any:
    sys.path.insert(0, str(SCRIPTS))
    path = SCRIPTS / "write_all_models_boeval_2023_2025.py"
    spec = importlib.util.spec_from_file_location("all_model_boeval_for_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


MISSILES = {
    "M1": (20000.0, 0.0, 2000.0),
    "M2": (19000.0, 600.0, 2100.0),
    "M3": (18000.0, -600.0, 1900.0),
}
UAVS = {
    "FY1": (17800.0, 0.0, 1800.0),
    "FY2": (12000.0, 1400.0, 1400.0),
    "FY3": (6000.0, -3000.0, 700.0),
    "FY4": (11000.0, 2000.0, 1800.0),
    "FY5": (13000.0, -2000.0, 1300.0),
}
TARGET_SAMPLES = [
    (0.0, 200.0, 5.0),
    (0.0, 200.0, 0.0),
    (0.0, 200.0, 10.0),
]
for z in (0.0, 10.0, 5.0):
    for i in range(8):
        theta = 2.0 * math.pi * i / 8.0
        TARGET_SAMPLES.append((7.0 * math.cos(theta), 200.0 + 7.0 * math.sin(theta), z))
MISSILE_SPEED = 300.0
SMOKE_RADIUS = 10.0
SMOKE_LIFETIME = 20.0
SMOKE_SINK_SPEED = 3.0
GRAVITY = 9.8


def fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "N/A"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value).replace("|", "\\|").replace("\n", "<br>")
    if not math.isfinite(number):
        return "N/A"
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def pct(value: float | None) -> str:
    return "N/A" if value is None else f"{value * 100.0:.2f}%"


def cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def sub(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale(a: tuple[float, float, float], factor: float) -> tuple[float, float, float]:
    return (a[0] * factor, a[1] * factor, a[2] * factor)


def norm(a: tuple[float, float, float]) -> float:
    return math.sqrt(sum(value * value for value in a))


def point_segment_distance(
    point: tuple[float, float, float],
    start: tuple[float, float, float],
    end: tuple[float, float, float],
) -> float:
    direction = sub(end, start)
    denominator = sum(value * value for value in direction)
    if denominator <= 1e-12:
        return norm(sub(point, start))
    fraction = sum((point[i] - start[i]) * direction[i] for i in range(3)) / denominator
    fraction = min(1.0, max(0.0, fraction))
    projection = add(start, scale(direction, fraction))
    return norm(sub(point, projection))


def missile_position(missile: str, time_s: float) -> tuple[float, float, float]:
    initial = MISSILES[missile]
    direction = scale(initial, -1.0 / norm(initial))
    return add(initial, scale(direction, MISSILE_SPEED * time_s))


def impact_time(missile: str) -> float:
    return norm(MISSILES[missile]) / MISSILE_SPEED


def bomb_points(row: dict[str, Any]) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    uav = UAVS[str(row["uav"])]
    heading = math.radians(float(row["heading_deg"]))
    speed = float(row["speed_mps"])
    drop_time = float(row["drop_time_s"])
    fuse_time = float(row["fuse_time_s"])
    velocity = (speed * math.cos(heading), speed * math.sin(heading), 0.0)
    drop = add(uav, scale(velocity, drop_time))
    explode = add(drop, (velocity[0] * fuse_time, velocity[1] * fuse_time, -0.5 * GRAVITY * fuse_time * fuse_time))
    return drop, explode


def smoke_replay(data: dict[str, Any]) -> dict[str, Any]:
    """Recompute Q5 using the common 27-point O-reference geometry."""
    rows = data.get("q5", {}).get("strategies", [])
    if not isinstance(rows, list):
        return {"status": "invalid", "errors": ["q5 strategies is not a list"]}
    # Several agents preserve the fixed 15-row output template and leave its
    # unused slots blank/all-zero. They are not releases and must not count
    # toward bomb limits or enter the kinematic replay.
    def is_unused_template_slot(row: Any) -> bool:
        if not isinstance(row, dict) or str(row.get("target_missile", "")).strip():
            return False
        for key in ("speed_mps", "drop_time_s", "fuse_time_s", "explode_time_s"):
            value = row.get(key, 0)
            try:
                if float(value or 0) != 0.0:
                    return False
            except (TypeError, ValueError):
                return False
        return True

    active_rows = [row for row in rows if not is_unused_template_slot(row)]
    errors: list[str] = []
    by_uav: dict[str, list[float]] = defaultdict(list)
    masks: dict[str, list[bool]] = {missile: [] for missile in MISSILES}
    step = 0.02
    max_time = max(impact_time(missile) for missile in MISSILES) + SMOKE_LIFETIME
    times = [i * step for i in range(int(max_time / step) + 1)]
    for index, row in enumerate(active_rows):
        if not isinstance(row, dict):
            errors.append(f"row {index} is not an object")
            continue
        uav = str(row.get("uav", ""))
        missile = str(row.get("target_missile", ""))
        if uav not in UAVS or missile not in MISSILES:
            errors.append(f"row {index} has unknown UAV/missile ({uav}/{missile})")
            continue
        try:
            speed = float(row["speed_mps"])
            drop_time = float(row["drop_time_s"])
            fuse_time = float(row["fuse_time_s"])
            explode_time = float(row["explode_time_s"])
            drop, explode = bomb_points(row)
        except (KeyError, TypeError, ValueError):
            errors.append(f"row {index} has nonnumeric kinematic fields")
            continue
        by_uav[uav].append(drop_time)
        if not 70.0 <= speed <= 140.0:
            errors.append(f"{uav} speed {speed} outside [70,140] m/s")
        if drop_time < 0.0 or fuse_time < 0.0:
            errors.append(f"row {index} has negative drop/fuse time")
        if abs(explode_time - drop_time - fuse_time) > 0.02:
            errors.append(f"row {index} has inconsistent explode time")
        if explode[2] <= 0.0 or explode_time > impact_time(missile):
            errors.append(f"row {index} explodes below ground or after missile impact")
        given_drop = tuple(float(row.get(key, float("nan"))) for key in ("drop_x", "drop_y", "drop_z"))
        given_explode = tuple(float(row.get(key, float("nan"))) for key in ("explode_x", "explode_y", "explode_z"))
        if max(abs(drop[i] - given_drop[i]) for i in range(3)) > 0.02:
            errors.append(f"row {index} drop point disagrees with kinematics")
        if max(abs(explode[i] - given_explode[i]) for i in range(3)) > 0.02:
            errors.append(f"row {index} explode point disagrees with kinematics")
        for time_s in times:
            active = explode_time <= time_s <= explode_time + SMOKE_LIFETIME and time_s <= impact_time(missile)
            if not active:
                masks[missile].append(False)
                continue
            cloud = (explode[0], explode[1], explode[2] - SMOKE_SINK_SPEED * (time_s - explode_time))
            missile_point = missile_position(missile, time_s)
            covered = sum(
                point_segment_distance(cloud, missile_point, sample) <= SMOKE_RADIUS
                for sample in TARGET_SAMPLES
            )
            masks[missile].append(covered / len(TARGET_SAMPLES) >= 0.25)
    if len(active_rows) > 15:
        errors.append(f"Q5 uses {len(active_rows)} bombs, above the 15-bomb limit")
    for uav, drops in by_uav.items():
        if len(drops) > 3:
            errors.append(f"{uav} uses {len(drops)} bombs, above the per-UAV limit")
        drops.sort()
        if any(after - before < 1.0 - 1e-9 for before, after in zip(drops, drops[1:])):
            errors.append(f"{uav} has two drops less than 1 s apart")
    durations: dict[str, float] = {}
    # Every missile mask is built on the same time grid, so the union is a
    # simple OR across bombs assigned to that missile.
    for missile in MISSILES:
        assigned = [
            row for row in active_rows
            if isinstance(row, dict) and str(row.get("target_missile", "")) == missile
        ]
        union = [False] * len(times)
        for row in assigned:
            # Re-evaluate this row rather than relying on any claimed duration.
            try:
                _, explode = bomb_points(row)
                explode_time = float(row["explode_time_s"])
            except (KeyError, TypeError, ValueError):
                continue
            for index, time_s in enumerate(times):
                if not (explode_time <= time_s <= explode_time + SMOKE_LIFETIME and time_s <= impact_time(missile)):
                    continue
                cloud = (explode[0], explode[1], explode[2] - SMOKE_SINK_SPEED * (time_s - explode_time))
                missile_point = missile_position(missile, time_s)
                covered = sum(
                    point_segment_distance(cloud, missile_point, sample) <= SMOKE_RADIUS
                    for sample in TARGET_SAMPLES
                )
                union[index] = union[index] or covered / len(TARGET_SAMPLES) >= 0.25
        durations[missile] = sum(union) * step
    durations["total"] = sum(durations.values())
    if not active_rows:
        errors.append("Q5 strategies missing")
    status = "hard-invalid/replay-constraint" if errors else (
        "hard-invalid/replay-zero-coverage" if durations["total"] <= 1e-9 else "replay-feasible-under-O-geometry"
    )
    return {
        "status": status,
        "errors": errors,
        "durations": durations,
        "reported": data.get("q5", {}).get("union_duration_s", {}),
        "active_bombs": len(active_rows),
        "ignored_template_slots": len(rows) - len(active_rows),
    }


def load_artifact(details: dict[str, Any] | None) -> dict[str, Any] | None:
    if not details or not isinstance(details.get("artifact_path"), str):
        return None
    try:
        data = json.loads(Path(details["artifact_path"]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def trajectory_evidence(details: dict[str, Any] | None) -> str:
    if not details or not isinstance(details.get("artifact_path"), str):
        return "no artifact"
    trial = Path(details["artifact_path"]).parents[3]
    path = trial / "agent" / "trajectory.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "no trajectory"
    steps = data.get("steps") if isinstance(data, dict) else None
    metrics = data.get("final_metrics") if isinstance(data, dict) else None
    return f"trajectory steps={len(steps) if isinstance(steps, list) else 'N/A'}, final_metrics={'yes' if metrics else 'no'}"


def _excel_column(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref.upper())
    if not match:
        raise ValueError(f"invalid Excel cell reference: {cell_ref}")
    value = 0
    for char in match.group(1):
        value = value * 26 + ord(char) - ord("A") + 1
    return value


def _read_official_bathymetry() -> tuple[list[float], list[float], list[list[float]]] | None:
    """Read the small official XLSX with stdlib only, avoiding a pandas dependency."""
    if not BATHYMETRY_XLSX.is_file():
        return None
    try:
        with zipfile.ZipFile(BATHYMETRY_XLSX) as archive:
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = [
                "".join(text.text or "" for text in item.iter(XLSX_NS + "t"))
                for item in shared_root.findall(XLSX_NS + "si")
            ]
            sheet_root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError):
        return None

    cells: dict[tuple[int, int], Any] = {}
    for element in sheet_root.iter(XLSX_NS + "c"):
        value_node = element.find(XLSX_NS + "v")
        if value_node is None or value_node.text is None:
            continue
        try:
            value: Any = float(value_node.text)
        except ValueError:
            value = value_node.text
        if element.attrib.get("t") == "s":
            try:
                value = shared[int(value)]
            except (IndexError, TypeError, ValueError):
                continue
        ref = element.attrib.get("r", "")
        row_match = re.search(r"[0-9]+", ref)
        if not row_match:
            continue
        cells[(int(row_match.group()), _excel_column(ref))] = value

    xs = [
        cells[(2, column)]
        for column in range(3, 300)
        if isinstance(cells.get((2, column)), (int, float))
    ]
    ys = [
        cells[(row, 2)]
        for row in range(3, 400)
        if isinstance(cells.get((row, 2)), (int, float))
    ]
    if len(xs) < 2 or len(ys) < 2:
        return None
    depth = [
        [cells.get((row, column)) for column in range(3, 3 + len(xs))]
        for row in range(3, 3 + len(ys))
    ]
    if any(not isinstance(value, (int, float)) for row in depth for value in row):
        return None
    return [float(value) for value in xs], [float(value) for value in ys], [
        [float(value) for value in row] for row in depth
    ]


def _linear_interpolate(xs: list[float], values: list[float], x: float) -> float:
    if x <= xs[0]:
        return values[0]
    if x >= xs[-1]:
        return values[-1]
    for index in range(len(xs) - 1):
        if xs[index] <= x <= xs[index + 1]:
            fraction = (x - xs[index]) / (xs[index + 1] - xs[index])
            return values[index] * (1.0 - fraction) + values[index + 1] * fraction
    return values[-1]


def multibeam_replay(data: dict[str, Any]) -> dict[str, Any] | None:
    """Replay a saved line layout against the official bathymetry grid.

    This is intentionally a geometric feasibility check, not a claim that the
    model's complete optimization objective has been independently reproduced.
    """
    # Agents used several result schemas for the same Q4 witness. Normalize
    # all known coordinate paths to nautical miles before one common replay.
    sources = [
        (("problem4", "positions_nm"), 1.0, data.get("problem4")),
        (("questions", "problem4", "positions_nm"), 1.0, None),
        (("problem4_results", "final_design", "positions_m"), 1.0 / NM_TO_M, None),
        (("question_4", "lines_x_from_west_nm"), 1.0, None),
    ]
    positions: Any = None
    source_path: tuple[str, ...] | None = None
    source_block: dict[str, Any] | None = None
    for path, unit_scale, fallback_block in sources:
        current: Any = data
        for key in path:
            if not isinstance(current, dict) or key not in current:
                current = None
                break
            current = current[key]
        if not isinstance(current, list) or not current:
            continue
        positions = current
        source_path = path
        if isinstance(fallback_block, dict):
            source_block = fallback_block
        else:
            source_block = data
            for key in path[:-1]:
                if not isinstance(source_block, dict):
                    source_block = None
                    break
                source_block = source_block.get(key)
        break
    if not isinstance(positions, list) or not positions or source_path is None:
        return None
    try:
        lines = [float(value) * unit_scale for value in positions]
    except (TypeError, ValueError):
        return {"status": "invalid", "errors": [f"{'.'.join(source_path)} contains nonnumeric values"]}
    grid = _read_official_bathymetry()
    if grid is None:
        return {"status": "unavailable", "errors": ["official bathymetry XLSX is unavailable or unreadable"]}
    xs, ys, depths = grid
    errors: list[str] = []
    reported_line_count = None
    reported_length = None
    if isinstance(source_block, dict):
        reported_line_count = source_block.get("line_count", source_block.get("n"))
        reported_length = source_block.get("total_length_nm", source_block.get("total_length_nautical_miles"))
    if isinstance(reported_line_count, (int, float)) and int(reported_line_count) != len(lines):
        errors.append(f"reported line_count={reported_line_count} disagrees with {len(lines)} saved positions")
    if isinstance(reported_length, (int, float)) and abs(float(reported_length) - len(lines) * 5.0) > 0.05:
        errors.append(
            f"reported total_length_nm={reported_length} disagrees with {len(lines)} lines x 5 NM"
        )
    if any(after <= before for before, after in zip(lines, lines[1:])):
        errors.append("line positions are not strictly increasing")
    if any(line < xs[0] - 1e-9 or line > xs[-1] + 1e-9 for line in lines):
        errors.append(f"line position outside [{xs[0]}, {xs[-1]}] NM")
    theta = math.radians(120.0)
    denominator_constant = math.cos(theta / 2.0) ** 2
    slope_factor = math.sin(theta / 2.0) ** 2
    widths: list[list[float]] = []
    for row_index, row in enumerate(depths):
        row_widths: list[float] = []
        for column_index, depth in enumerate(row):
            if column_index == 0:
                slope = (row[1] - depth) / ((xs[1] - xs[0]) * NM_TO_M)
            elif column_index == len(row) - 1:
                slope = (depth - row[-2]) / ((xs[-1] - xs[-2]) * NM_TO_M)
            else:
                slope = (row[column_index + 1] - row[column_index - 1]) / (
                    (xs[column_index + 1] - xs[column_index - 1]) * NM_TO_M
                )
            denominator = denominator_constant - slope_factor * slope * slope
            if denominator <= 0.0 or depth <= 0.0:
                errors.append(f"invalid local swath geometry at grid row {row_index}, column {column_index}")
                row_widths.append(0.0)
            else:
                # beta=90 degrees for north-south lines crossing the E-W slope.
                row_widths.append(depth * math.sin(theta) / denominator / NM_TO_M)
        widths.append(row_widths)

    covered_count = 0
    missing_length_by_row: list[float] = []
    overlap_values: list[float] = []
    overlap_over20_length_nm = 0.0
    grid_dy = ys[1] - ys[0]
    for row_index, y in enumerate(ys):
        row_widths = widths[row_index]
        covered_row = 0
        intervals: list[tuple[float, float]] = []
        line_widths = []
        for line in lines:
            width = _linear_interpolate(xs, row_widths, line)
            line_widths.append(width)
            intervals.append((line - width / 2.0, line + width / 2.0))
        for x, width in zip(xs, row_widths):
            if any(abs(x - line) <= width_at_line / 2.0 for line, width_at_line in zip(lines, line_widths)):
                covered_count += 1
                covered_row += 1
        intervals.sort()
        union_end = 0.0
        gap = 0.0
        for left, right in intervals:
            left = max(xs[0], left)
            right = min(xs[-1], right)
            if right <= left:
                continue
            if left > union_end:
                gap += left - union_end
            union_end = max(union_end, right)
        if union_end < xs[-1]:
            gap += xs[-1] - union_end
        missing_length_by_row.append(gap)
        for left_width, right_width, left, right in zip(line_widths, line_widths[1:], lines, lines[1:]):
            mean_width = (left_width + right_width) / 2.0
            overlap = 1.0 - (right - left) / mean_width if mean_width > 0.0 else -1.0
            overlap_values.append(overlap)
            if overlap > 0.20:
                overlap_over20_length_nm += grid_dy

    overlap_count = len(overlap_values)
    below10_count = sum(value < 0.10 for value in overlap_values)
    within10_20_count = sum(0.10 <= value <= 0.20 for value in overlap_values)
    above20_count = sum(value > 0.20 for value in overlap_values)
    overlap_quality_warning = below10_count > 0 or above20_count > 0

    total_points = len(xs) * len(ys)
    coverage_rate = covered_count / total_points if total_points else 0.0
    q3 = data.get("problem3")
    q3_warning = None
    if isinstance(q3, dict) and isinstance(q3.get("positions_m"), list) and q3["positions_m"]:
        try:
            q3_last = max(float(value) for value in q3["positions_m"])
            q3_boundary_over_m = q3_last - (xs[-1] * NM_TO_M)
            if q3_boundary_over_m > 1.0:
                q3_warning = f"Q3 last line center is {q3_boundary_over_m:.2f} m beyond the 4 NM east boundary"
        except (TypeError, ValueError):
            q3_warning = "Q3 positions_m contains nonnumeric values"
    if errors:
        status = "invalid"
    elif coverage_rate < 1.0 - 1e-6:
        status = "needs-review/replay-gaps"
    elif overlap_quality_warning:
        status = "needs-review/overlap-quality-warning"
    else:
        status = "replay-feasible-under-official-bathymetry"
    return {
        "status": status,
        "errors": errors,
        "x_count": len(xs),
        "y_count": len(ys),
        "line_count": len(lines),
        "line_min_nm": min(lines),
        "line_max_nm": max(lines),
        "coverage_rate": coverage_rate,
        "missed_area_pct": (1.0 - coverage_rate) * 100.0,
        "overlap_over20_length_nm": overlap_over20_length_nm,
        "mean_overlap_pct": (sum(overlap_values) / len(overlap_values) * 100.0) if overlap_values else None,
        "overlap_sample_count": overlap_count,
        "overlap_below10_pct": below10_count / overlap_count * 100.0 if overlap_count else None,
        "overlap_within10_20_pct": within10_20_count / overlap_count * 100.0 if overlap_count else None,
        "overlap_above20_pct": above20_count / overlap_count * 100.0 if overlap_count else None,
        "max_row_gap_nm": max(missing_length_by_row) if missing_length_by_row else None,
        "q3_warning": q3_warning,
    }


def _normalise_code(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    text = str(value).strip()
    return text or None


@lru_cache(maxsize=1)
def vegetable_reference_sets() -> tuple[set[str], dict[str, str]] | None:
    """Load the official June 24-30 candidate SKU set and category map."""
    try:
        import openpyxl
    except ImportError:
        return None
    try:
        workbook = openpyxl.load_workbook(VEGETABLE_DATA_DIR / "附件1.xlsx", read_only=True, data_only=True)
        catalog: dict[str, str] = {}
        for row in workbook.active.iter_rows(min_row=2, values_only=True):
            code = _normalise_code(row[0] if len(row) > 0 else None)
            category = str(row[3]).strip() if len(row) > 3 and row[3] is not None else ""
            if code:
                catalog[code] = category
        workbook.close()
        workbook = openpyxl.load_workbook(VEGETABLE_DATA_DIR / "附件2.xlsx", read_only=True, data_only=True)
        candidates: set[str] = set()
        for row in workbook.active.iter_rows(min_row=2, values_only=True):
            value = row[0] if row else None
            day = value.date() if hasattr(value, "date") else str(value)[:10]
            if str(day) >= "2023-06-24" and str(day) <= "2023-06-30":
                code = _normalise_code(row[2] if len(row) > 2 else None)
                if code:
                    candidates.add(code)
        workbook.close()
    except (OSError, ValueError, TypeError):
        return None
    return candidates, catalog


def vegetable_plan(data: dict[str, Any]) -> list[dict[str, Any]] | None:
    """Find a concrete July 1 SKU plan, if the artifact actually saved one."""
    paths = [
        ("problem3", "item_plan"),
        ("problem3_analysis", "item_plan"),
        ("q3_results", "sku_plan"),
        ("questions", "question3", "full_recommended_plan"),
        ("problem3", "items"),
    ]
    for path in paths:
        current: Any = data
        for key in path:
            if not isinstance(current, dict) or key not in current:
                current = None
                break
            current = current[key]
        if isinstance(current, list) and current and all(isinstance(row, dict) for row in current):
            return current
    return None


def vegetable_schedule_replay(data: dict[str, Any]) -> dict[str, Any] | None:
    """Check hard operational constraints; this is not an optimality proof."""
    plan = vegetable_plan(data)
    if plan is None:
        return None
    code_keys = ("item_id", "item", "单品编码", "code", "item_code")
    order_keys = ("replenishment_kg", "补货量kg", "recommended_gross_order_kg", "order_kg", "replenish_kg")
    price_keys = ("price_yuan_per_kg", "price", "定价元每kg", "recommended_retail_price_yuan_per_kg")
    errors: list[str] = []
    soft_warnings: list[str] = []
    codes: list[str] = []
    categories: set[str] = set()
    references = vegetable_reference_sets()
    candidate_codes = references[0] if references else None
    catalog = references[1] if references else {}
    for index, row in enumerate(plan):
        code_value = next((row.get(key) for key in code_keys if row.get(key) is not None), None)
        code = _normalise_code(code_value)
        if code is None:
            errors.append(f"row {index} has no SKU code")
            continue
        codes.append(code)
        if candidate_codes is not None and code not in candidate_codes:
            errors.append(f"row {index} SKU {code} was not sold during the official June 24-30 candidate window")
        category = next((row.get(key) for key in ("category", "品类", "category_name") if row.get(key)), None)
        if category:
            categories.add(str(category))
        elif catalog.get(code):
            categories.add(catalog[code])
        order_value = next((row.get(key) for key in order_keys if row.get(key) is not None), None)
        try:
            order = float(order_value)
        except (TypeError, ValueError):
            soft_warnings.append(f"row {index} SKU {code} has no numeric order quantity")
        else:
            if not math.isfinite(order) or order < 2.5 - 1e-9:
                errors.append(f"row {index} SKU {code} order={order_value} kg is below the 2.5 kg minimum display quantity")
        price_value = next((row.get(key) for key in price_keys if row.get(key) is not None), None)
        try:
            price = float(price_value)
        except (TypeError, ValueError):
            soft_warnings.append(f"row {index} SKU {code} has no numeric retail price")
        else:
            if not math.isfinite(price) or price <= 0.0:
                errors.append(f"row {index} SKU {code} has non-positive retail price={price_value}")
    if not 27 <= len(plan) <= 33:
        errors.append(f"plan contains {len(plan)} SKUs, outside the required 27-33 range")
    if len(set(codes)) != len(codes):
        errors.append("plan contains duplicate SKU codes")
    if len(categories) < 6:
        soft_warnings.append(f"only {len(categories)} of 6 official categories can be recovered from the saved plan")
    return {
        "status": "hard-invalid/replenishment-constraint" if errors else (
            "needs-review/schedule-fields-missing" if soft_warnings else "needs-review/schedule-basic-check-pass"
        ),
        "errors": errors,
        "warnings": soft_warnings,
        "plan_count": len(plan),
        "unique_code_count": len(set(codes)),
        "category_count": len(categories),
        "candidate_check": "passed" if candidate_codes is not None and not any("candidate window" in error for error in errors) else "unavailable/failed",
    }


def artifact_status(allm: Any, record: dict[str, Any], model: str) -> tuple[str, str]:
    case = record["case"]
    details = record["details"].get(model)
    gate = record["hard_gate"].get(model)
    if gate:
        return "hard-invalid", gate
    data = load_artifact(details)
    if data is None:
        return "missing-artifact", "artifact missing or unreadable"
    validation = validate_artifact(data, case.slug)
    if validation.get("hard_errors"):
        return str(validation.get("status", "hard-invalid")), str(validation.get("evidence", "hard constraint violation"))
    if case.slug == "cumcm-2025-a-smoke-screen":
        replay = smoke_replay(data)
        if replay["status"].startswith("hard-invalid"):
            return replay["status"], "; ".join(replay["errors"][:3]) or "independent replay found zero coverage"
        return replay["status"], (
            "reported total=" + fmt(replay["reported"].get("total")) + " s; "
            "independent total=" + fmt(replay["durations"].get("total")) + " s"
        )
    if case.slug == "cumcm-2023-a-heliostat-field" and model == "qwen":
        return "needs-review/model-scale-mismatch", "Q1 fixed-field optical scale is about 14.9% above O; Q3 power is not independently replayable from saved coordinates"
    if case.slug == "cumcm-2023-a-heliostat-field":
        return "needs-review/model-layout-missing", "summary JSON reports Q3 design values, but no per-mirror coordinates, dimensions, heights, spacing, shadow, or optical replay files are present in the artifact"
    if case.slug == "cumcm-2023-b-multibeam-lines":
        replay = multibeam_replay(data)
        if replay is not None:
            if replay["status"] == "invalid":
                return "hard-invalid/replay-geometry", "; ".join(replay["errors"][:3])
            if replay["status"] == "unavailable":
                return "artifact-only/official-grid-unavailable", "; ".join(replay["errors"])
            warning = f"; warning: {replay['q3_warning']}" if replay.get("q3_warning") else ""
            quality = (
                f"; overlap below10/within10-20/above20="
                f"{fmt(replay['overlap_below10_pct'], 1)}/{fmt(replay['overlap_within10_20_pct'], 1)}/{fmt(replay['overlap_above20_pct'], 1)}%"
            )
            return replay["status"], (
                f"Q4 replay on official {replay['x_count']}x{replay['y_count']} grid: "
                f"{replay['line_count']} N-S lines in [{fmt(replay['line_min_nm'])},{fmt(replay['line_max_nm'])}] NM, "
                f"coverage={fmt(replay['coverage_rate'] * 100.0, 3)}%, "
                f"missed={fmt(replay['missed_area_pct'], 4)}%, "
                f">20% overlap={fmt(replay['overlap_over20_length_nm'], 2)} NM, "
                f"mean overlap={fmt(replay['mean_overlap_pct'], 2)}%{quality}{warning}"
            )
        return "artifact-only/no-layout-replay", "final JSON has summary metrics but the claimed line schedule/coverage files are not in the collected artifact"
    if case.slug == "cumcm-2023-c-vegetable-pricing":
        schedule = vegetable_schedule_replay(data)
        if schedule is None:
            return "needs-review/no-replenishment-schedule", "artifact has aggregate demand/profit numbers but no concrete July 1 SKU replenishment and pricing table"
        if schedule["status"].startswith("hard-invalid"):
            return schedule["status"], "; ".join(schedule["errors"][:3])
        note = (
            f"saved {schedule['plan_count']}-SKU plan passes candidate/minimum-quantity checks; "
            f"{schedule['category_count']}/6 categories recovered"
        )
        if schedule["warnings"]:
            note += "; " + "; ".join(schedule["warnings"][:2])
        return schedule["status"], note + "; optimization and demand-coverage claims still need replay"
    if case.slug == "mcm-2023-a-plant-community":
        return "artifact-only/calibrated-model", "the problem supplies no numerical ecology time series; reported trajectories are model assumptions, not independently verifiable observations"
    if validation.get("warnings"):
        return str(validation.get("status", "needs-review")), str(validation.get("evidence", ""))
    if validation.get("status") != "artifact-only":
        return str(validation.get("status")), str(validation.get("evidence", ""))
    return "range-clean/artifact-only", trajectory_evidence(details)


def write_report() -> Path:
    allm = load_all_model_module()
    _, _, records, summaries = allm.compute()
    rows: list[dict[str, Any]] = []
    high_rows: list[dict[str, Any]] = []
    for record in records:
        for model in allm.MODELS:
            status, evidence = artifact_status(allm, record, model)
            row = {
                "model": model,
                "label": allm.MODELS[model]["label"],
                "task": record["case"].slug,
                "raw": record["raw"].get(model),
                "o": record["o"].get(model),
                "status": status,
                "evidence": evidence,
            }
            rows.append(row)
            if model != "flash" and (float(record["raw"].get(model) or 0.0) >= 1.15 or record["hard_gate"].get(model)):
                high_rows.append(row)

    smoke_rows = [row for row in rows if row["task"] == "cumcm-2025-a-smoke-screen"]
    gates = [row for row in rows if row["status"].startswith("hard-invalid") and row["task"] != "cumcm-2025-a-smoke-screen"]
    status_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        status_counts[row["status"]] += 1
    lines = [
        "# 2023-2025 全模型答案可行性复核",
        "",
        f"生成日期：{date.today().isoformat()}",
        "",
        "## 结论",
        "",
        "这份复核不把 JSON 字段齐全、轨迹里写过代码或分数高，直接当成数学方案已经可行。可行性分成三层：题面硬约束明确违反时 hard-invalid；能用共同几何/运动学重放时报告 replay-feasible；开放题或缺少布局/代码时只能写 artifact-only，不能据此宣称方案已被独立验证。",
        "",
        f"本轮共检查 {len(rows)} 个模型-题目单元。状态计数：" + ", ".join(f"{key}={value}" for key, value in sorted(status_counts.items())) + "。",
        "",
        "新增确定性处罚：GLM-5.3 的 `cumcm-2023-a-heliostat-field` Q3 文字明确给出一面尾镜 `z=1.9024 m`，低于题面安装高度下限 2 m；v4 flash baseline 的 Q3 年平均热功率为 53.7955 MW，Gemini 3.7 Flash 的 Q2/Q3 年平均热功率为 55.460/54.966 MW，均未达到约 60 MW。这些是题面硬约束违反，进入 whole-task hard gate。此前对 Hy4 的 `cumcm-2024-b-production-decision`（SPRT 的 `c=-1` 哨兵）和 Juneau 中间年份 `sustainability_score>100` 的判断是审计误报，已撤销；它们现在分别标为结构通过和量纲需复核。",
        "多波束题补充了独立重放：GLM、ox-alpha、Kimi 和 Qwen 的 artifact 都保存了可读取的实际 Q4 测线坐标。GLM/ox-alpha 为 60 条线，在官方海深网格上覆盖率约 99.945%，存在少量漏测；Kimi 为 81 条线、覆盖率 100%，但约 79.6% 的相邻局部重叠超过 20%；Qwen 为 60 条线、覆盖率 100%，但只有约 14.8% 的局部重叠落在 10%–20%，约 36.2% 低于 10%，约 51.0% 高于 20%。这些结果说明覆盖几何可执行，但质量约束仍需复核，不能直接写成完全满足题面。Qwen 的 Q3 末条测线中心超出 4 海里边界约 4.17 m，仅作为边界约定警告。",
        "",
        "## 烟幕题独立重放",
        "",
        "统一采用题面导弹/无人机坐标、300 m/s 导弹、重力抛体、10 m 烟幕半径、20 s 有效期，以及 Outstanding 复现使用的 27 个目标采样点和 25% 覆盖阈值。重放不读取模型自报的遮蔽时长，只读取投放参数重新计算。",
        "",
        "| 模型 | 自报 Q5 总时长(s) | 独立重放总时长(s) | 状态 |",
        "|---|---:|---:|---|",
    ]
    for row in smoke_rows:
        reported = row["evidence"].split("reported total=")[-1].split(" s;")[0] if "reported total=" in row["evidence"] else "N/A"
        independent = row["evidence"].split("independent total=")[-1].split(" s")[0] if "independent total=" in row["evidence"] else "N/A"
        lines.append(f"| {row['label']} | {reported} | {independent} | {row['status']} |")
    lines.extend([
        "",
        "Qwen3.8-27B 的自报 31.65 s 在共同重放下约为 32.62 s，15 枚弹、每架不超过 3 枚、同一无人机投放间隔至少 1 s、速度和爆炸高度约束均通过。因此这个离群高分目前不能因“高于 Outstanding”而处罚；它的风险是目标模型较简化，而不是已发现的运动学不可能。",
        "",
        "ox-alpha 的 Q5 在共同重放下为 0 s，保留既有 hard gate。其余模型的重放结果也会和自报值有差异，这是采样阈值/时间步不同造成的，不自动按数值差异处罚。",
        "",
        "## 明确硬错误",
        "",
        "| 模型 | 题目 | 处理 | 证据 |",
        "|---|---|---|---|",
    ])
    for row in gates:
        lines.append(f"| {row['label']} | `{row['task']}` | {row['status']} | {row['evidence']} |")
    lines.extend([
        "",
        "其中 `mcm-2024-a-lamprey` 的 score-config invalid 是所有当前模型共用的字段量纲问题：O 奖端点给的是种群规模，若模型返回归一化指数，不能把它当成“生态边界违反”，但也不能当成同量纲精确复现；因此只保留逐指标警告，不整题 hard gate。Kimi 的 Juneau 仍因最终接受度 1.5 和可持续分数 232.2 与 unit-scale 端点不可比较而保留人工 hard gate；Kimi 的 Olympic 结构也有独立硬证据。ox-alpha 烟幕题仍以统一几何重放为准。",
        "",
        "## 高分单元复核",
        "",
        "下表列出 direction-aware raw ≥ 1.15 或已被 hard gate 的单元。`range-clean/artifact-only` 只表示基础数值范围和结构没有直接越界，不表示论文级数学模型已经被重跑。",
        "",
        "| 模型 | 题目 | raw | O-Eval | 状态 | 复核结论 |",
        "|---|---|---:|---:|---|---|",
    ])
    for row in sorted(high_rows, key=lambda item: (item["task"], item["label"])):
        lines.append(f"| {row['label']} | `{row['task']}` | {fmt(row['raw'])} | {pct(row['o'])} | {row['status']} | {row['evidence']} |")
    lines.extend([
        "",
        "## 多波束独立重放细节",
        "",
        "Qwen 的 Q4 方案使用 60 条南北测线，位置范围约 0.02141–3.99624 NM；官方附件为 201×251 网格，深度范围 20–197.2 m。按 120° 开角、局部东西向坡度和多波束覆盖宽度逐网格重算，覆盖率为 100%，漏测率为 0%，相邻条带重叠超过 20% 的长度约 151.10 NM，平均重叠约 27.08%，与自报 147.98 NM 和 26.28% 接近。但逐网格的相邻重叠只有约 14.8% 落在题面建议的 10%–20% 区间，约 36.2% 低于 10%，约 51.0% 高于 20%，所以这是一份“覆盖可执行、质量约束需复核”的方案，不应写成完全满足题面质量要求。",
        "",
        "Q3 的 33 条测线间距对应约 10% 的设计重叠，但最后一个中心位置为 7412.17 m，而 4 NM 横向边界为 7408 m。差值只有 4.17 m，可能来自端点/坐标定义或四舍五入；在没有原始测线文件和坐标约定说明前，标记为需要人工复核，不把它升级成 whole-task hard gate。",
        "",
        "## 重点开放题限制",
        "",
        "- `cumcm-2023-b-multibeam-lines`：GLM、ox-alpha、Kimi 和 Qwen 保存了可重放的 Q4 测线坐标；GLM/ox-alpha 有约 0.055% 的网格漏测，Kimi 和 Qwen 虽然覆盖率为 100%，但相邻重叠分别明显偏高或分布很散。其他模型仍只有摘要，不能仅凭自报覆盖率称为已独立验证的可行布线。",
        "- `mcm-2023-b-maasai-mara`：Qwen 的农业/旅游网格数相对 Outstanding 约大 73/120 倍，但题面允许自行建模，且最终 JSON 的 2500 格分配内部相加一致；当前标记为尺度需复核，不把 O 论文的 36 格复现直接当成题面硬约束。",
        "- `mcm-2023-a-plant-community`：这是没有数值观测数据的开放生态建模题。不同模型用不同校准参数得到 5 或 8 个物种、不同生物量和干旱缓冲，并不自动意味着不可行；必须保存并重跑模型代码、参数、随机种子后才能升级为 verified feasible。",
        "- `cumcm-2023-a-heliostat-field`：除 GLM 的高度硬错误、v4 flash/Gemini 的额定功率硬错误外，其余模型的 Q3 仍只有汇总数字，没有逐镜面坐标和光学重放包。Qwen 的 Q1 固定场光学效率比 Outstanding 约高 14.9%，Q3 的 60.08 MW 不能从已采集的镜面坐标独立复算，因此保持 needs-review，不把它当成确定的超 O 方案。",
        "- `cumcm-2023-c-vegetable-pricing`：GPT、Kimi、Qwen Flash、Hy4 保存了 33 行单品计划；这些计划的单品均来自官方 6 月 24–30 日可售集合、数量均达到 2.5 kg 且覆盖 6 个品类，但仍没有独立重跑需求预测、价格弹性和“尽量满足各品类需求”的优化约束。其他模型没有具体单品表，不能仅凭利润和单品数 claim 可执行。",
        "",
        "## 对榜单的影响",
        "",
        "本轮只有证据充分的 whole-task 错误进入 hard-gated 榜：GLM 2023 A 定日镜高度、v4 flash 2023 A 额定功率、Gemini 2023 A 额定功率、Kimi 2025 B 的 unit/scale 错误、Kimi 2025 C 的推荐结构错误，以及既有的 ox-alpha 烟幕错误。Qwen 2023 A 因布局缺失保持 needs-review 不处罚；Qwen 2023 B 因覆盖几何通过但重叠质量超标改为 needs-review/overlap-quality-warning，不直接 hard gate；Qwen 2025 A 烟幕重放通过，不处罚；Hy4 的生产决策和 Juneau 不再处罚。原始 O-Eval 仍是主榜，hard-gated O-Eval 是可行性更保守的辅助榜，Robust BO-Eval 继续使用 hard-invalid=-100% 的失败惩罚。",
        "",
        "## 复核边界",
        "",
        "模型作答时生成的 `/root/results` 代码、Excel、CSV 和中间验证文件没有完整进入当前 Harbor artifact；因此本报告不会把轨迹中自报的“运行了仿真”当成独立证据。后续若要把某个开放题标成 verified feasible，应在 artifact 中保存最小可重放包：输入数据哈希、代码、参数、随机种子、约束检查结果和最终数值。",
    ])
    AUDIT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return AUDIT_PATH


if __name__ == "__main__":
    print(write_report())
