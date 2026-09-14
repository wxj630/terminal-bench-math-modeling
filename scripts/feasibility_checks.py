#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Small, task-specific feasibility checks shared by scoring and audit reports.

These checks intentionally distinguish a hard contradiction from missing
evidence.  A summary-only artifact is not promoted to a verified solution,
but it is also not silently treated as impossible.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any


def _finite(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _number(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _integer(value: Any) -> bool:
    number = _number(value)
    return number is not None and abs(number - round(number)) <= 1e-9


def _binary(value: Any) -> bool:
    return value in (0, 1, False, True)


def _question_name(value: Any) -> str:
    return str(value or "").lower().replace(" ", "").replace("_", "")


def _summary_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = data.get("reproduced", {}).get("design_summary")
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def heliostat_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    rows = _summary_rows(data)
    if not rows:
        return {
            "status": "needs-review/model-layout-missing",
            "hard_errors": [],
            "warnings": ["no normalized per-question design summary is present"],
            "evidence": "no normalized Q1-Q3 design summary; geometry cannot be checked from this artifact",
        }

    constrained_rows = 0
    explicit_layout_witness = False
    for row in rows:
        question = _question_name(row.get("question"))
        is_constrained = question in {"q2", "question2", "q3", "question3"}
        if not is_constrained:
            continue
        constrained_rows += 1
        width = _number(row.get("mirror_width_m"))
        height = _number(row.get("mirror_height_m"))
        install = _number(row.get("installation_height_m"))
        area = _number(row.get("mirror_area_m2"))
        count = _number(row.get("mirror_count"))
        power = _number(row.get("annual_thermal_power_mw"))
        unit_power = _number(row.get("unit_area_power_kw_m2"))
        if width is not None and height is not None:
            explicit_layout_witness = True
            if not 2.0 <= width <= 8.0 or not 2.0 <= height <= 8.0:
                errors.append(f"{row.get('question', 'Q?')} mirror dimension outside [2,8] m: {width} x {height}")
            if width + 1e-9 < height:
                errors.append(f"{row.get('question', 'Q?')} violates width >= height: {width} < {height} m")
            if count is not None and area is not None:
                expected_area = count * width * height
                if abs(expected_area - area) > max(1.0, 0.01 * max(abs(area), 1.0)):
                    errors.append(
                        f"{row.get('question', 'Q?')} area mismatch: reported {area:g} m2 versus count*width*height {expected_area:g} m2"
                    )
        elif is_constrained:
            warnings.append(f"{row.get('question', 'Q?')} does not expose numeric mirror dimensions")
        if install is not None:
            explicit_layout_witness = True
            if not 2.0 <= install <= 6.0:
                errors.append(f"{row.get('question', 'Q?')} installation height {install:g} m outside [2,6] m")
        if power is not None and power < 60.0 - 1e-6:
            errors.append(
                f"{row.get('question', 'Q?')} rated-power constraint violation: {power:.6f} MW is below the required approximately 60 MW"
            )
        if area is not None and unit_power is not None and power is not None:
            implied = unit_power * area / 1000.0
            if abs(implied - power) > max(0.05, 0.03 * max(abs(power), 1.0)):
                errors.append(
                    f"{row.get('question', 'Q?')} power/area mismatch: reported {power:g} MW versus {implied:g} MW implied by unit-area power"
                )

        note = str(row.get("model_note", ""))
        for match in re.finditer(r"(?:^|[;,( ])(?:z|h)\s*=\s*(-?[0-9]+(?:\.[0-9]+)?)\s*m?\b", note, re.IGNORECASE):
            noted_height = float(match.group(1))
            explicit_layout_witness = True
            if not 2.0 <= noted_height <= 6.0:
                errors.append(
                    f"{row.get('question', 'Q?')} model note gives installation height z={noted_height:g} m outside [2,6] m"
                )
        for match in re.finditer(r"([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*m", note, re.IGNORECASE):
            note_width, note_height = (float(match.group(1)), float(match.group(2)))
            explicit_layout_witness = True
            if not 2.0 <= note_width <= 8.0 or not 2.0 <= note_height <= 8.0:
                errors.append(f"{row.get('question', 'Q?')} model-note mirror dimension outside [2,8] m")
            if note_width + 1e-9 < note_height:
                errors.append(f"{row.get('question', 'Q?')} model-note dimension violates width >= height")

    detailed = data.get("detailed_results")
    if isinstance(detailed, dict):
        for question in ("q2", "q3"):
            block = detailed.get(question)
            if not isinstance(block, dict):
                continue
            geometry = block.get("geometry")
            if isinstance(geometry, dict):
                radius = _number(geometry.get("maximum_field_radius_m"))
                tower_clearance = _number(geometry.get("minimum_tower_exclusion_distance_m"))
                spacing = _number(geometry.get("minimum_center_distance_m"))
                required_spacing = _number(geometry.get("minimum_required_distance_m"))
                corner_height = _number(geometry.get("minimum_corner_height_m"))
                if radius is not None and radius > 350.0 + 1e-6:
                    errors.append(f"{question} field radius {radius:g} m exceeds 350 m")
                if tower_clearance is not None and tower_clearance < 100.0 - 1e-6:
                    errors.append(f"{question} mirror center is within the 100 m tower exclusion zone")
                if spacing is not None and required_spacing is not None and spacing + 1e-6 < required_spacing:
                    errors.append(f"{question} minimum center spacing {spacing:g} m is below required {required_spacing:g} m")
                if corner_height is not None and corner_height < -1e-6:
                    errors.append(f"{question} mirror corner penetrates the ground by {-corner_height:g} m")

    if constrained_rows < 2:
        warnings.append("Q2/Q3 constrained-design rows are incomplete")
    if not explicit_layout_witness:
        warnings.append("artifact has summary metrics but no concrete per-mirror layout witness")

    if errors:
        status = "hard-invalid/heliostat-constraint"
    elif warnings:
        status = "needs-review/heliostat-witness-missing"
    else:
        status = "needs-review/heliostat-summary-only"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings)}


def production_decision_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    result = data.get("experiment_result")
    if not isinstance(result, dict):
        return {"status": "needs-review/decision-fields-missing", "hard_errors": [], "warnings": ["experiment_result missing"], "evidence": "experiment_result missing"}

    q1 = result.get("q1_sampling")
    if isinstance(q1, list):
        for index, plan in enumerate(q1):
            if not isinstance(plan, dict):
                errors.append(f"q1 sampling plan {index} is not an object")
                continue
            n = _number(plan.get("n"))
            c = _number(plan.get("c"))
            mode = str(plan.get("mode", "")).upper()
            if "SPRT" in mode:
                # A sequential probability ratio test has stopping boundaries,
                # not one fixed binomial acceptance number. Some artifacts use
                # -1 as the schema sentinel for this non-applicable field.
                if n is None or n <= 0:
                    errors.append(f"q1 SPRT plan {index} has invalid expected sample size n")
                if c is not None and c != -1:
                    errors.append(f"q1 SPRT plan {index} uses unexpected fixed-threshold sentinel c={c:g}")
            elif n is None or n <= 0 or c is None or not _integer(c) or c < 0 or c > n:
                errors.append(f"q1 fixed-sample plan {index} has invalid integer n/c")
            for key in ("false_alarm", "power"):
                value = _number(plan.get(key))
                if value is not None and not 0.0 <= value <= 1.0:
                    errors.append(f"q1 {key}={value:g} is outside [0,1]")
    else:
        warnings.append("q1 sampling plan is missing")

    q2 = result.get("q2")
    decisions = q2.get("best_decisions") if isinstance(q2, dict) else None
    if not isinstance(decisions, list):
        errors.append("q2 best_decisions is missing")
    else:
        case_ids: list[int] = []
        for index, decision in enumerate(decisions):
            if not isinstance(decision, dict):
                errors.append(f"q2 decision {index} is not an object")
                continue
            case = decision.get("case")
            if not _integer(case):
                errors.append(f"q2 decision {index} has non-integer case id")
            else:
                case_ids.append(int(float(case)))
            for key in ("inspect_part1", "inspect_part2", "inspect_final", "dismantle_bad_final"):
                if key in decision and not _binary(decision[key]):
                    errors.append(f"q2 case {case} has non-binary {key}")
            probability = _number(decision.get("good_probability"))
            if probability is not None and not 0.0 <= probability <= 1.0:
                errors.append(f"q2 case {case} good_probability={probability:g} is outside [0,1]")
            if "expected_profit" in decision and not _finite(decision.get("expected_profit")):
                errors.append(f"q2 case {case} expected_profit is non-finite")
        if set(case_ids) != set(range(1, 7)):
            errors.append(f"q2 does not provide exactly one decision for cases 1-6: {sorted(case_ids)}")

    q3 = result.get("q3")
    bits = q3.get("decision_bits") if isinstance(q3, dict) else None
    if not isinstance(bits, list) or len(bits) not in (16, 17):
        errors.append("q3 decision_bits must contain the 16 or 17 binary decisions required by the supplied topology")
    elif any(not _binary(bit) for bit in bits):
        errors.append("q3 decision_bits contains a non-binary value")

    q4 = result.get("q4")
    posterior = q4.get("posterior_rows") if isinstance(q4, dict) else None
    if isinstance(posterior, list):
        for index, row in enumerate(posterior):
            if not isinstance(row, dict):
                errors.append(f"q4 posterior row {index} is not an object")
                continue
            mean = _number(row.get("posterior_mean_defect_rate"))
            q95 = _number(row.get("posterior_q95_defect_rate"))
            if mean is not None and not 0.0 <= mean <= 1.0:
                errors.append(f"q4 posterior mean {mean:g} is outside [0,1]")
            if q95 is not None and not 0.0 <= q95 <= 1.0:
                errors.append(f"q4 posterior q95 {q95:g} is outside [0,1]")
            if mean is not None and q95 is not None and q95 + 1e-9 < mean:
                errors.append(f"q4 posterior q95 is below its posterior mean in row {index}")
    else:
        warnings.append("q4 posterior rows are missing")

    if errors:
        status = "hard-invalid/decision-constraint"
    else:
        status = "needs-review/decision-structure-pass"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings) or "binary decisions and probability ranges pass basic checks"}


def nipt_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    result = data.get("experiment_result") if isinstance(data.get("experiment_result"), dict) else {}
    earliest = _number(result.get("earliest_recommended_week"))
    latest = _number(result.get("latest_recommended_week"))
    if earliest is not None and not 10.0 <= earliest <= 25.0:
        errors.append(f"earliest recommended week {earliest:g} is outside the 10-25 week testing window")
    if latest is not None and not 10.0 <= latest <= 25.0:
        errors.append(f"latest recommended week {latest:g} is outside the 10-25 week testing window")
    if earliest is not None and latest is not None and latest < earliest:
        errors.append("latest recommended week is earlier than earliest recommended week")

    bmi = data.get("bmi_timing")
    groups = bmi.get("groups") if isinstance(bmi, dict) else None
    if not isinstance(groups, list) or not groups:
        warnings.append("BMI timing groups are missing")
    else:
        observed_ranges: list[tuple[float, float]] = []
        labelled_ranges: list[tuple[float, float]] = []
        for index, group in enumerate(groups):
            if not isinstance(group, dict):
                errors.append(f"BMI group {index} is not an object")
                continue
            low = _number(group.get("bmi_min"))
            high = _number(group.get("bmi_max"))
            week = _number(group.get("recommended_week"))
            sample_count = group.get("sample_count")
            if sample_count is not None and (not _integer(sample_count) or float(sample_count) <= 0):
                errors.append(f"BMI group {index} has invalid positive integer sample_count")
            if low is not None and high is not None:
                if high < low:
                    errors.append(f"BMI group {index} has upper bound below lower bound")
                observed_ranges.append((low, high))
            label = str(group.get("bmi_group", ""))
            # Prefer the interval explicitly promised to patients. The
            # bmi_min/bmi_max fields are often only observed sample extrema;
            # treating those as policy boundaries creates false gap alarms.
            match = re.search(
                r"[\[(]\s*(-?(?:\d+(?:\.\d*)?|\.\d+)|[-+]?inf(?:inity)?|[-+]?∞)\s*,\s*"
                r"(\+?(?:\d+(?:\.\d*)?|\.\d+)|\+?inf(?:inity)?|\+?∞)\s*[\])]",
                label,
                re.IGNORECASE,
            )
            if match:
                def parse_bound(value: str, upper: bool) -> float:
                    value = value.lower().replace("∞", "inf")
                    if "inf" in value:
                        return math.inf if upper else -math.inf
                    return float(value)
                labelled_ranges.append((parse_bound(match.group(1), False), parse_bound(match.group(2), True)))
            if week is not None and not 10.0 <= week <= 25.0:
                errors.append(f"BMI group {index} recommended week {week:g} is outside [10,25]")
            for key in ("qualified_probability", "failure_rate"):
                value = _number(group.get(key))
                if value is not None and not 0.0 <= value <= 1.0:
                    errors.append(f"BMI group {index} {key}={value:g} is outside [0,1]")
            qualified = _number(group.get("qualified_probability"))
            failure = _number(group.get("failure_rate"))
            if qualified is not None and failure is not None and abs(qualified + failure - 1.0) > 0.02:
                errors.append(f"BMI group {index} qualified_probability + failure_rate is not approximately 1")
            risk = _number(group.get("risk_score"))
            if risk is not None and risk < 0.0:
                errors.append(f"BMI group {index} risk_score is negative")
        ranges_to_check = labelled_ranges if len(labelled_ranges) == len(groups) else observed_ranges
        ranges_to_check = sorted(ranges_to_check)
        for before, after in zip(ranges_to_check, ranges_to_check[1:]):
            if after[0] > before[1] + 1e-6:
                warnings.append(f"observed BMI ranges have an uncovered gap ({before[1]:g}, {after[0]:g})")

    female = data.get("female_abnormality")
    if isinstance(female, dict):
        rows = _number(female.get("rows"))
        positives = _number(female.get("positive_count"))
        if rows is not None and rows < 0:
            errors.append("female abnormality row count is negative")
        if rows is not None and positives is not None and (positives < 0 or positives > rows):
            errors.append("female abnormality positive_count is outside [0, rows]")
        for key in ("leave_one_out_accuracy", "leave_one_out_f1", "leave_one_out_auc"):
            value = _number(female.get(key))
            if value is not None and not 0.0 <= value <= 1.0:
                errors.append(f"female abnormality {key}={value:g} is outside [0,1]")
        cases = female.get("top_flagged_cases")
        if isinstance(cases, list):
            for index, case in enumerate(cases):
                if not isinstance(case, dict):
                    continue
                probability = _number(case.get("abnormal_probability"))
                if probability is not None and not 0.0 <= probability <= 1.0:
                    errors.append(f"female flagged case {index} abnormal_probability is outside [0,1]")
    else:
        warnings.append("female abnormality block is missing")

    if errors:
        status = "hard-invalid/nipt-constraint"
    elif warnings:
        status = "needs-review/nipt-group-coverage"
    else:
        status = "needs-review/nipt-range-pass"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings) or "timing, probability, and classification ranges pass basic checks"}


def lamprey_check(data: dict[str, Any]) -> dict[str, Any]:
    """Check ecological state bounds without assuming O-paper population units."""
    errors: list[str] = []
    warnings: list[str] = []
    result = data.get("experiment_result") if isinstance(data.get("experiment_result"), dict) else {}
    endpoint = result.get("sex_ratio_endpoint")
    if isinstance(endpoint, dict):
        for key in ("scarce_resource_male_share", "abundant_resource_male_share"):
            value = _number(endpoint.get(key))
            if value is not None and not 0.0 <= value <= 1.0:
                errors.append(f"sex-ratio endpoint {key}={value:g} is outside [0,1]")
    rows = result.get("scenario_summary")
    if not isinstance(rows, list) or not rows:
        warnings.append("scenario_summary is missing; ecosystem trajectories cannot be checked")
    else:
        nonnegative = ("mean_biomass", "final_lamprey", "final_host_fish", "final_parasite")
        bounded = ("normalized_diversity", "species_persistence", "resistance", "resilience", "sustainability", "composite_stability")
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"scenario row {index} is not an object")
                continue
            for key in nonnegative:
                value = _number(row.get(key))
                if value is not None and value < 0.0:
                    errors.append(f"scenario row {index} has negative {key}")
            for key in bounded:
                value = _number(row.get(key))
                if value is not None and not 0.0 <= value <= 1.0:
                    errors.append(f"scenario row {index} {key}={value:g} is outside [0,1]")
    if errors:
        status = "hard-invalid/lamprey-state-boundary"
    elif warnings:
        status = "needs-review/lamprey-model-evidence"
    else:
        status = "needs-review/lamprey-state-range-pass"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings) or "population states are nonnegative and normalized stability metrics are within [0,1]; calibration remains model-specific"}


def _scenario_counts(row: Any) -> dict[str, Any] | None:
    if not isinstance(row, dict):
        return None
    keys = ("wildlife_sanctuary", "agricultural_area", "hunting_area", "tourism_area")
    return {key: row.get(key) for key in keys} if all(key in row for key in keys) else None


def maasai_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    reproduced = data.get("reproduced") if isinstance(data.get("reproduced"), dict) else {}
    target = data.get("paper_targets") if isinstance(data.get("paper_targets"), dict) else {}
    grid = _number(target.get("grid_count"))
    rows = reproduced.get("scenario_rows")
    if not isinstance(rows, list) or not rows:
        warnings.append("scenario allocation rows are missing")
    else:
        for index, row in enumerate(rows):
            counts = _scenario_counts(row)
            if counts is None:
                errors.append(f"scenario {index} does not expose all four area counts")
                continue
            total = 0.0
            for key, value in counts.items():
                number = _number(value)
                if number is None or number < 0.0 or not _integer(value):
                    errors.append(f"scenario {index} has invalid nonnegative integer count for {key}")
                else:
                    total += number
            if grid is not None and abs(total - grid) > 1e-6:
                errors.append(f"scenario {index} partitions {total:g} cells but declared grid has {grid:g}")
    scenario2 = _scenario_counts(reproduced.get("scenario2_counts"))
    if scenario2 is None:
        warnings.append("scenario2_counts is missing")
    elif grid is not None:
        total = sum(_number(value) or 0.0 for value in scenario2.values())
        if abs(total - grid) > 1e-6:
            errors.append(f"scenario2_counts partitions {total:g} cells but declared grid has {grid:g}")
    distance = _number(reproduced.get("mean_sanctuary_to_tourism_interaction_distance"))
    if distance is not None and distance < 0.0:
        errors.append("mean sanctuary-to-tourism interaction distance is negative")
    if errors:
        status = "hard-invalid/maasai-partition"
    elif warnings:
        status = "needs-review/maasai-model-evidence"
    else:
        status = "needs-review/maasai-partition-pass"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings) or "all reported scenario partitions sum to their declared grid"}


def plant_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    reproduced = data.get("reproduced") if isinstance(data.get("reproduced"), dict) else {}
    rows = reproduced.get("species_count_summary")
    if not isinstance(rows, list) or not rows:
        warnings.append("species-count trajectory summary is missing")
    else:
        species_values: set[int] = set()
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"species summary row {index} is not an object")
                continue
            species = row.get("species_count")
            if not _integer(species) or float(species) <= 0:
                errors.append(f"species summary row {index} has invalid species_count")
            else:
                species_values.add(int(float(species)))
            biomass = _number(row.get("mean_total_biomass_last20y"))
            if biomass is not None and biomass < 0.0:
                errors.append(f"species summary row {index} has negative biomass")
            evenness = _number(row.get("pielou_evenness"))
            if evenness is not None and not 0.0 <= evenness <= 1.0:
                errors.append(f"species summary row {index} Pielou evenness is outside [0,1]")
        optimum = reproduced.get("optimal_species_count")
        if optimum is not None and _integer(optimum) and int(float(optimum)) not in species_values:
            warnings.append("reported optimal species count is outside the saved evaluated species grid")
    drought = reproduced.get("drought_buffer")
    if isinstance(drought, list):
        for index, row in enumerate(drought):
            if not isinstance(row, dict):
                continue
            frequency = _number(row.get("drought_frequency_per_50y"))
            if frequency is not None and frequency < 0.0:
                errors.append(f"drought scenario {index} has negative frequency")
            for key in ("monoculture_biomass_index", "five_species_biomass_index"):
                value = _number(row.get(key))
                if value is not None and value < 0.0:
                    errors.append(f"drought scenario {index} has negative {key}")
    else:
        warnings.append("drought sensitivity scenarios are missing")
    if errors:
        status = "hard-invalid/plant-boundary"
    else:
        status = "artifact-only/calibrated-model"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings) or "biomass, species, and evenness ranges pass basic checks; empirical ecology replay is unavailable"}


def _policy_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    dp = data.get("dynamic_programming")
    if isinstance(dp, dict):
        terminal = dp.get("optimal_terminal_policy")
        if isinstance(terminal, dict):
            result.append(terminal)
        yearly = dp.get("yearly_policy")
        if isinstance(yearly, list):
            result.extend(row for row in yearly if isinstance(row, dict))
    experiment = data.get("experiment_result")
    if isinstance(experiment, dict):
        result.append(experiment)
    return result


def juneau_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    rows = _policy_rows(data)
    if not rows:
        return {"status": "needs-review/tourism-policy-missing", "hard_errors": [], "warnings": ["no dynamic policy row is present"], "evidence": "no dynamic policy row is present"}
    saw_percent_scale_acceptance = False
    saw_non_unit_sustainability = False
    for index, row in enumerate(rows):
        for key in ("daily_cap", "annual_visitors", "visitor_fee_usd", "total_revenue_usd"):
            value = _number(row.get(key))
            if value is not None and value < 0.0:
                errors.append(f"policy row {index} has negative {key}")
        share = _number(row.get("conservation_share"))
        if share is not None and not 0.0 <= share <= 1.0:
            errors.append(f"policy row {index} conservation_share={share:g} is outside [0,1]")
        acceptance = _number(row.get("resident_acceptance_index"))
        if acceptance is not None:
            if acceptance < 0.0:
                errors.append(f"policy row {index} resident_acceptance_index={acceptance:g} is negative")
            elif acceptance > 1.0:
                saw_percent_scale_acceptance = True
        sustainability = _number(row.get("sustainability_score"))
        if sustainability is not None and sustainability > 1.5:
            # The task does not prescribe a universal upper bound for a
            # composite index. Values in this range are usually percentage-
            # or points-scaled, so flag the unit mismatch without calling the
            # policy physically impossible.
            saw_non_unit_sustainability = True
        if sustainability is not None and sustainability < 0.0:
            warnings.append(f"policy row {index} sustainability_score={sustainability:g} is negative; inspect the model's score definition")
    if saw_percent_scale_acceptance:
        warnings.append("resident_acceptance_index is reported above 1.0, suggesting a percentage/points scale; the Outstanding reference uses a unit scale")
    if saw_non_unit_sustainability:
        warnings.append("sustainability_score exceeds 1.5 for at least one policy; its composite-index scale is incompatible with the Outstanding unit-scale endpoint until explicitly converted")
    if errors:
        status = "hard-invalid/tourism-policy-range"
    elif warnings:
        status = "needs-review/tourism-scale-mismatch"
    else:
        status = "needs-review/tourism-policy-range-pass"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings) or "policy variables pass nonnegative and normalized-share checks"}


def olympic_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    coach = data.get("great_coach_model")
    recommendations = coach.get("recommendations") if isinstance(coach, dict) else None
    # Missing evidence is a warning, not a contradiction: an artifact that simply
    # omits the block is incomplete, not impossible. Only a block that exists and
    # contradicts the required structure is a hard error.
    if not isinstance(recommendations, list):
        warnings.append("great_coach_model recommendations are missing; structure cannot be checked")
    elif len(recommendations) != 3:
        errors.append(
            f"great_coach_model must provide exactly three country-sport recommendations, found {len(recommendations)}"
        )
    else:
        seen: set[tuple[str, str]] = set()
        for index, recommendation in enumerate(recommendations):
            if not isinstance(recommendation, dict):
                errors.append(f"coach recommendation {index} is not an object")
                continue
            pair = (str(recommendation.get("NOC", "")), str(recommendation.get("Sport", "")))
            if not pair[0] or not pair[1] or pair in seen:
                errors.append(f"coach recommendation {index} has an empty or duplicate country-sport pair")
            seen.add(pair)
            for key in ("benchmark_jump_score", "estimated_medal_count_gain"):
                value = _number(recommendation.get(key))
                if value is not None and value < 0.0:
                    errors.append(f"coach recommendation {index} has negative {key}")
    evaluation = data.get("model_evaluation")
    if isinstance(evaluation, dict):
        for key in ("mean_accuracy_2024", "mean_f1_2024", "mean_brier_2024"):
            value = _number(evaluation.get(key))
            if value is not None and not 0.0 <= value <= 1.0:
                errors.append(f"model evaluation {key}={value:g} is outside [0,1]")
    else:
        warnings.append("model evaluation block is missing")
    first_medal = _number(data.get("expected_first_medal_countries"))
    if first_medal is not None and first_medal < 0.0:
        errors.append("expected number of first-medal countries is negative")
    for candidate in data.get("first_medal_top_candidates", []):
        if not isinstance(candidate, dict):
            continue
        probability = _number(candidate.get("first_medal_probability"))
        if probability is not None and not 0.0 <= probability <= 1.0:
            errors.append("first-medal probability is outside [0,1]")
    for row in data.get("monte_carlo_summary_top_total", []):
        if not isinstance(row, dict):
            continue
        total = _number(row.get("expected_total"))
        gold = _number(row.get("expected_gold"))
        if total is not None and gold is not None and gold > total + 1e-6:
            errors.append("expected gold medals exceed expected total medals")
        low = _number(row.get("total_interval95_low"))
        high = _number(row.get("total_interval95_high"))
        if low is not None and high is not None and low > high + 1e-6:
            errors.append("total-medal prediction interval is reversed")
    if errors:
        status = "hard-invalid/olympic-structure"
    else:
        status = "needs-review/olympic-structure-pass"
    return {"status": status, "hard_errors": errors, "warnings": warnings, "evidence": "; ".join(errors + warnings) or "recommendation count, probability ranges, and medal interval ordering pass basic checks"}


# --- CUMCM 2024 C: crop-planting sales ceiling -------------------------------
# The 2024 C sale rule is: if a crop's seasonal output exceeds its expected sales
# d, the excess is wasted (alpha=0) or sold at 50% price (alpha=0.5). d is the
# 2023 production implied by 附件2.
#
# IMPORTANT AMBIGUITY. The two authoritative sources disagree on the scope of
# the demand cap, and it changes the achievable profit by ~1.5x:
#   * The contest statement says "某种作物每季的总产量" (the crop's seasonal TOTAL
#     output), i.e. an AGGREGATE cap. Then 7-year revenue <= sum_{(crop,season)} d*p.
#     Comparing like with like, the aggregate revenue ceiling is 36,277,448 and the
#     aggregate profit ceiling is lower.
#   * The O-award paper's eq. (19) places min(x_i*y, d) INSIDE the sum over plots i,
#     i.e. a PER-PLOT cap. Under that reading each plot may sell up to the full d,
#     so the 7-year revenue ceiling rises to 52,042,270 and the profit ceiling to
#     45,461,290 (both computed by relaxing all rotation/dispersity/bean rules, so
#     they are true upper bounds).
# Because the human Outstanding solution uses the per-plot reading, a large
# reported profit is NOT by itself evidence of an infeasible plan. So the
# aggregate-ceiling breach is recorded as a WARNING (needs-review), and only a
# value above the per-plot upper bound is treated as a hard boundary violation.
CROP_AGG_PROFIT_CEILING = 36_277_448.0
CROP_PERPLOT_REVENUE_CEILING = 52_042_270.0
CROP_PERPLOT_PROFIT_CEILING = 45_461_290.0
#: Tolerance so that a result sitting exactly on a ceiling (rounding noise) is
#: not treated as a violation.
CROP_CEILING_TOLERANCE = 0.02


def crop_planting_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    q1: dict[str, Any] = {}
    for container in (data.get("experiment_result"), data, data.get("reproduced")):
        if isinstance(container, dict) and isinstance(container.get("q1"), dict):
            q1 = container["q1"]
            break
    if not q1:
        return {
            "status": "needs-review/crop-planting-summary-missing",
            "hard_errors": [],
            "warnings": ["no q1 profit block is present; the sale-rule ceiling cannot be checked"],
            "evidence": "q1 block missing",
        }

    waste_profit = _number(q1.get("waste_profit_yuan"))
    waste_revenue = _number(q1.get("waste_revenue_yuan"))
    discount_profit = _number(q1.get("discount_profit_yuan"))

    checks = (
        ("waste_revenue_yuan", waste_revenue, CROP_PERPLOT_REVENUE_CEILING),
        ("waste_profit_yuan", waste_profit, CROP_PERPLOT_PROFIT_CEILING),
    )
    for label, value, hard_ceiling in checks:
        if value is None:
            continue
        if value > hard_ceiling * (1.0 + CROP_CEILING_TOLERANCE):
            errors.append(
                f"{label}={value:,.0f} exceeds the per-plot-capped 7-year ceiling {hard_ceiling:,.0f} yuan, "
                "so the plan is unreachable under either reading of the demand cap"
            )

    for label, value in (("waste_profit_yuan", waste_profit), ("waste_revenue_yuan", waste_revenue)):
        if value is None:
            continue
        if value > CROP_AGG_PROFIT_CEILING * (1.0 + CROP_CEILING_TOLERANCE) and not any(
            label in e for e in errors
        ):
            warnings.append(
                f"{label}={value:,.0f} exceeds the aggregate demand-cap ceiling {CROP_AGG_PROFIT_CEILING:,.0f} yuan "
                "(问题一规则: sum of expected sales x price), so it is only reachable under the O-award paper's "
                "per-plot cap (eq.19 applies min(x*y,d) per plot rather than to the crop-season total). "
                "This is an interpretation difference, not proven infeasibility."
            )

    if waste_profit is not None and discount_profit is not None and discount_profit + 1e-6 < waste_profit:
        errors.append(
            f"discount_profit_yuan={discount_profit:,.0f} is below waste_profit_yuan={waste_profit:,.0f}; "
            "the 50%-discount scenario can never earn less than the surplus-wasted scenario"
        )

    experiment = data.get("experiment_result") if isinstance(data.get("experiment_result"), dict) else {}
    q23 = experiment.get("q2_q3") if isinstance(experiment.get("q2_q3"), dict) else None
    if isinstance(q23, dict):
        rho = _number(q23.get("spearman_price_cost"))
        if rho is not None and not -1.0 <= rho <= 1.0:
            errors.append(f"spearman_price_cost={rho:g} is outside [-1,1]")

    if errors:
        status = "hard-invalid/crop-planting-boundary"
    elif warnings:
        status = "needs-review/crop-planting-demand-cap-ambiguous"
    else:
        status = "needs-review/crop-planting-summary-only"
    return {
        "status": status,
        "hard_errors": errors,
        "warnings": warnings,
        "evidence": "; ".join(errors + warnings)
        or "alpha=0 profit is within both the aggregate and per-plot demand-cap ceilings; correlation is a valid coefficient",
    }


# --------------------------------------------------------------------------- #
# Remaining task checks. Each returns {"status", "hard_errors", "warnings",
# "evidence"} and must be *programmatic*: bounds come from the stated problem
# constraints, not from a per-run human judgement. The contract is:
#   * hard_errors  -> a genuine boundary/logic contradiction (negative rate,
#                     impossible probability, union > sum, speed above the cap).
#   * warnings     -> missing evidence or a stated interpretation difference.
# The helper functions below locate the same quantity wherever a model chose to
# put it, since submitted schemas vary a lot between agents.
# --------------------------------------------------------------------------- #


def _iter_numeric(data: Any, prefix: str = "") -> list[tuple[str, float]]:
    """Flatten every finite number in ``data`` to (dotted path, value)."""
    found: list[tuple[str, float]] = []

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                child = f"{path}.{key}" if path else str(key)
                if isinstance(value, bool):
                    continue
                if isinstance(value, (int, float)):
                    found.append((child, float(value)))
                else:
                    walk(value, child)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                child = f"{path}[{index}]"
                if isinstance(value, bool):
                    continue
                if isinstance(value, (int, float)):
                    found.append((child, float(value)))
                else:
                    walk(value, child)

    walk(data, prefix)
    return found


def _dig(data: Any, path: str) -> Any:
    current = data
    for token in path.split("."):
        if isinstance(current, dict) and token in current:
            current = current[token]
        else:
            return None
    return current


def _first_number(data: Any, *paths: str) -> float | None:
    for path in paths:
        return_value = _dig(data, path)
        number = _number(return_value)
        if number is not None:
            return number
    return None


def _leaf_numbers(data: Any, leaf_pattern: str) -> list[tuple[str, float]]:
    """Numbers whose *final key* (not an ancestor) matches ``leaf_pattern``.

    Matching only the leaf avoids the classic false positive where a parent array
    is named e.g. ``..._correlations`` and a sibling field such as
    ``observations`` inside it then gets checked against the correlation range.
    """
    rx = re.compile(leaf_pattern, re.IGNORECASE)
    found: list[tuple[str, float]] = []
    for path, value in _iter_numeric(data):
        leaf = re.sub(r"\[\d+\]$", "", path.rsplit(".", 1)[-1])
        if rx.fullmatch(leaf) or rx.search(leaf):
            found.append((path, value))
    return found


def _leaf_names(data: Any, names: set[str]) -> list[tuple[str, float]]:
    """Numbers whose final key is exactly one of ``names`` (case-insensitive)."""
    wanted = {name.lower() for name in names}
    found: list[tuple[str, float]] = []
    for path, value in _iter_numeric(data):
        leaf = re.sub(r"\[\d+\]$", "", path.rsplit(".", 1)[-1]).lower()
        if leaf in wanted:
            found.append((path, value))
    return found


def _bounded_leaves(
    data: Any,
    names: set[str],
    low: float,
    high: float,
    label: str,
    errors: list[str],
) -> int:
    """Flag the exact leaf ``names`` when outside [low, high]. Returns the hit count."""
    hits = _leaf_names(data, names)
    for path, value in hits:
        if value < low - 1e-9 or value > high + 1e-9:
            errors.append(f"{label} out of range at {path}: {value:g} not in [{low:g},{high:g}]")
    return len(hits)


#: Correlation-like leaf names, matched exactly (never the arrays named *_correlations).
_CORRELATION_LEAVES = {
    "correlation", "corr", "spearman", "pearson", "spearman_r", "pearson_r",
    "spearman_corr", "pearson_corr", "spearman_coefficient", "pearson_coefficient",
    "sales_markup_corr", "actual_sales_markup_corr", "warning_correlation",
    "price_cost_corr", "yield_cost_corr", "yield_price_corr",
}
#: Classification-score leaf names, matched exactly (excludes *_n, confusion counts).
_ACCURACY_LEAVES = {
    "accuracy", "holdout_accuracy", "train_accuracy", "test_accuracy",
    "f1", "f1_score", "auc", "roc_auc", "mean_accuracy_2024", "mean_f1_2024",
    "calibrated_lightgbm_like_accuracy", "lightgbm_like_accuracy", "best_tree_holdout_accuracy",
}
#: Rate/probability leaf names that legitimately live on either the [0,1] or [0,100] scale.
_RATE_FRACTION_LEAVES = {
    "warning_rate", "final_match_warning_rate", "swing_warning_rate",
    "pod", "probability", "first_medal_probability", "coverage_rate",
}
_RATE_PERCENT_LEAVES = {
    "loss_rate_pct", "loss_rate_percent", "item_loss_rate_percent",
    "missed_area_pct", "peak_period_share_of_daily_use",
}


def multibeam_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    missed = _first_number(
        data,
        "reproduced.problem4_summary.missed_area_pct",
        "target_comparison.problem4_missed_area_pct.actual",
    )
    overlap = _first_number(
        data,
        "reproduced.problem4_summary.sa_avg_overlap_pct",
        "reproduced.problem4_summary.greedy_avg_overlap_pct",
    )
    over20 = _first_number(data, "reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles")
    length = _first_number(
        data,
        "reproduced.problem4_summary.total_length_nautical_miles",
        "target_comparison.problem4_total_length_nm.actual",
    )
    if missed is not None and not 0.0 <= missed <= 100.0:
        errors.append(f"missed_area_pct={missed:g} is outside [0,100]")
    if overlap is not None:
        if overlap < -1e-9:
            errors.append(f"average overlap percent={overlap:g} is negative")
        elif overlap > 100.0 + 1.0:
            warnings.append(
                f"average overlap percent={overlap:g} exceeds 100%, which is only reachable if line "
                "spacing is negative; check the overlap definition"
            )
    if over20 is not None and over20 < -1e-9:
        errors.append(f"overlap-over-20% length={over20:g} nm is negative")
    if length is not None and length <= 0.0:
        errors.append(f"total survey length={length:g} nm is not positive")
    if all(value is None for value in (missed, overlap, over20, length)):
        warnings.append("no problem-4 coverage summary is present; geometry cannot be replayed")
    if errors:
        status = "hard-invalid/multibeam-coverage"
    elif warnings:
        status = "needs-review/multibeam-summary-only"
    else:
        status = "range-clean/multibeam-coverage"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "missed area and overlap percentages are within [0,100] and the survey length is positive"}


def vegetable_pricing_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    _bounded_leaves(data, _RATE_FRACTION_LEAVES | {"loss_rate"}, 0.0, 1.0, "fractional loss/warning rate", errors)
    _bounded_leaves(data, _RATE_PERCENT_LEAVES, 0.0, 100.0, "percentage loss/overlap rate", errors)
    _bounded_leaves(data, _CORRELATION_LEAVES, -1.0, 1.0, "correlation coefficient", errors)
    for path, value in _leaf_names(data, {"item_count", "selected_item_count", "selected_count", "candidate_item_count", "line_count", "fringe_peak_count"}):
        if value < 0.0:
            errors.append(f"count field negative at {path}: {value:g}")
    profit = _first_number(
        data,
        "reproduced.future_week_profit_yuan",
        "target_comparison.future_week_max_profit_yuan.actual",
    )
    if profit is not None and profit < 0.0:
        warnings.append(f"reported future-week maximum profit is negative ({profit:g}); a profit-maximising plan should be positive")
    for path, value in _leaf_names(data, {"optimal_price", "price_yuan_per_jin", "price_yuan_per_kg", "sell_price"}):
        if value < 0.0:
            errors.append(f"negative price at {path}: {value:g}")
    if not errors and not warnings and not _leaf_numbers(data, "price|loss_rate|count"):
        warnings.append("no pricing, loss-rate, or item-count fields were found to check")
    if errors:
        status = "hard-invalid/vegetable-domain"
    elif warnings:
        status = "needs-review/vegetable-pricing"
    else:
        status = "range-clean/vegetable-pricing"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "loss rates, correlations, prices, and counts are within their valid domains"}


def dragon_dance_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    head = _first_number(data, "experiment_result.q5.max_head_speed_mps")
    ratio = _first_number(data, "experiment_result.q5.max_speed_ratio_when_head_1mps")
    if head is not None and head <= 0.0:
        errors.append(f"max_head_speed_mps={head:g} is not positive")
    if ratio is not None and ratio <= 0.0:
        errors.append(f"max_speed_ratio_when_head_1mps={ratio:g} is not positive")
    if head is not None and ratio is not None and head > 0.0 and ratio > 0.0:
        # The whole point of Q5: the fastest handle must not exceed the 2 m/s cap,
        # and the head speed is set to 2 / ratio, so head * ratio must equal 2.
        fastest = head * ratio
        if fastest > 2.0 + 1e-2:
            errors.append(
                f"head speed {head:g} m/s x amplification ratio {ratio:g} = {fastest:.4f} m/s exceeds the "
                "2 m/s handle-speed cap; the reported head speed is infeasible"
            )
        elif fastest < 2.0 - 5e-2:
            warnings.append(
                f"head speed x ratio = {fastest:.4f} m/s, below the 2 m/s cap; the solution does not push the "
                "limit, which is allowed but leaves margin unexplained"
            )
    if head is None or ratio is None:
        warnings.append("q5 head speed and/or amplification ratio is missing")
    if errors:
        status = "hard-invalid/dragon-kinematics"
    elif warnings:
        status = "needs-review/dragon-kinematics"
    else:
        status = "replay-feasible-under-O-geometry/dragon"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "head speed x amplification ratio equals the 2 m/s cap"}


def smoke_screen_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    durations = _leaf_numbers(data, "duration_s")
    for path, value in durations:
        if value < -1e-9:
            errors.append(f"smoke-screen duration negative at {path}: {value:g}")
    union = [value for path, value in _leaf_names(data, {"union_duration_s", "total"})]
    individual = [value for path, value in _leaf_numbers(data, "individual_duration_s")]
    # Union duration can never exceed the sum of the individual coverages.
    if individual and union:
        total = max(union)
        s = sum(individual)
        if total > s + 1e-2:
            errors.append(
                f"union cover duration {total:g}s exceeds the sum of individual coverages {s:g}s; "
                "a union cannot last longer than its parts"
            )
    _bounded_leaves(data, {"speed_mps", "speed"}, 0.0, 500.0, "drone speed", errors)
    if not durations:
        warnings.append("no smoke-screen duration fields are present")
    if errors:
        status = "hard-invalid/smoke-screen"
    elif warnings:
        status = "needs-review/smoke-screen-summary-only"
    else:
        status = "range-clean/smoke-screen-durations"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "cover durations are nonnegative and the union does not exceed the sum of its parts"}


def sic_thickness_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    for path, value in _leaf_numbers(data, "thickness_um"):
        if value <= 0.0:
            errors.append(f"epi-layer thickness must be positive at {path}: {value:g} um")
        elif value > 500.0:
            errors.append(f"epi-layer thickness implausibly large at {path}: {value:g} um")
    for path, value in _leaf_numbers(data, "angle_spread_um"):
        if value < -1e-9:
            errors.append(f"angle spread negative at {path}: {value:g}")
    two_beam = _leaf_numbers(data, "two_beam_thickness_um")
    airy = _leaf_numbers(data, "airy_thickness_um|joint_airy_corrected_thickness_um|airy_corrected_thickness_um")
    pairs = min(len(two_beam), len(airy))
    for index in range(pairs):
        tb, aa = two_beam[index][1], airy[index][1]
        if tb > 0.0 and aa > 0.0 and abs(tb - aa) / max(tb, aa) > 0.5:
            warnings.append(
                f"two-beam ({tb:g} um) and Airy ({aa:g} um) fits disagree by more than 50%; the model choice "
                "should be justified"
            )
    if not _leaf_numbers(data, "thickness_um"):
        warnings.append("no thickness fields are present")
    if errors:
        status = "hard-invalid/sic-thickness"
    elif warnings:
        status = "needs-review/sic-thickness-consistency"
    else:
        status = "range-clean/sic-thickness"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "inferred thicknesses are positive and within a plausible range"}


def wordle_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    _bounded_leaves(data, _ACCURACY_LEAVES, 0.0, 1.0, "classification score", errors)
    group = _first_number(data, "reproduced.eerie.difficulty_group", "target_comparison.eerie_group.actual")
    if group is None:
        group = _first_number(data, "reproduced.eerie_difficulty_group")
    if group is not None:
        if group < 1.0 or abs(group - round(group)) > 1e-6:
            errors.append(f"EERIE difficulty group must be a positive integer, got {group:g}")
    for path, value in _leaf_numbers(data, "eerie_distribution_sum_pct|distribution_sum_pct|sum_pct"):
        if abs(value - 100.0) > 1.0 and abs(value - 1.0) > 0.01:
            warnings.append(f"reported distribution sum at {path} is {value:g}, not 100 or 1")
    if not errors and not warnings and not _leaf_numbers(data, "accuracy|difficulty_group"):
        warnings.append("no accuracy or difficulty-group fields were found to check")
    if errors:
        status = "hard-invalid/wordle-domain"
    elif warnings:
        status = "needs-review/wordle-domain"
    else:
        status = "range-clean/wordle-domain"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "classification scores lie in [0,1] and the difficulty group is a positive integer"}


def submersible_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    # Only the canonical probability leaves are probabilities. A sibling block such
    # as ``searched_cells_uncalibrated`` reuses the same key names for cell COUNTS,
    # so anything under a *_cells_* container is skipped.
    probability_leaves = {
        "find_probability_6h", "find_probability_10h_start_1h",
        "find_probability_10h_start_3h", "find_probability_10h_start_5h",
        "find_probability_18h", "pod", "probability", "find_probability",
    }
    for path, value in _leaf_names(data, probability_leaves):
        if re.search(r"cells|count", path, re.IGNORECASE):
            continue
        if not 0.0 <= value <= 1.0:
            errors.append(f"search probability out of range at {path}: {value:g} not in [0,1]")
    for path, value in _leaf_names(data, {"multiplier"}):
        if value <= 0.0:
            errors.append(f"uncertainty multiplier must be positive at {path}: {value:g}")
    for name in ("current_multiplier", "terrain_uncertainty_multiplier"):
        value = _first_number(data, f"experiment_result.caribbean_adaptation.{name}")
        if value is not None and value < 1.0:
            warnings.append(
                f"{name}={value:g} is below 1, i.e. it reduces the uncertainty it is meant to inflate"
            )
    if not _leaf_numbers(data, "multiplier|probability|_pod"):
        warnings.append("no multiplier or probability fields were found to check")
    if errors:
        status = "hard-invalid/submersible-domain"
    elif warnings:
        status = "needs-review/submersible-domain"
    else:
        status = "range-clean/submersible-domain"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "probabilities lie in [0,1] and uncertainty multipliers are positive"}


def tennis_momentum_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    _bounded_leaves(data, _RATE_FRACTION_LEAVES, 0.0, 1.0, "warning rate", errors)
    _bounded_leaves(data, _CORRELATION_LEAVES, -1.0, 1.0, "correlation coefficient", errors)
    if not _leaf_numbers(data, "warning_rate|correlation"):
        warnings.append("no warning-rate or correlation fields were found to check")
    if errors:
        status = "hard-invalid/tennis-domain"
    elif warnings:
        status = "needs-review/tennis-domain"
    else:
        status = "range-clean/tennis-domain"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "rates lie in [0,1] and correlations in [-1,1]"}


def stair_wear_check(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    for path, value in _leaf_numbers(data, "users|passages"):
        if value < -1e-9:
            errors.append(f"user/passage count negative at {path}: {value:g}")
    peak = _first_number(data, "daily_use_pattern.peak_period_users")
    regular = _first_number(data, "daily_use_pattern.regular_hour_users_if_spread_over_10_hours")
    if peak is not None and regular is not None and peak + 1e-6 < regular:
        # Self-contradictory naming rather than a physical impossibility: the model
        # may deliberately describe a flat profile, so this only warns.
        warnings.append(
            f"peak-period users ({peak:g}) is below the 10-hour spread average ({regular:g}); the "
            "'peak' field is then not a peak, so the daily-use profile is internally inconsistent"
        )
    _bounded_leaves(data, {"peak_period_share_of_daily_use", "peak_period_share"}, 0.0, 1.0, "peak share", errors)
    depth = _leaf_numbers(data, "median_volume_loss_m3|depth_mm")
    for path, value in depth:
        if value < -1e-12:
            errors.append(f"wear depth/volume negative at {path}: {value:g}")
    if not _leaf_numbers(data, "users|peak_period_users"):
        warnings.append("no usage-frequency fields were found to check")
    if errors:
        status = "hard-invalid/stair-wear-domain"
    elif warnings:
        status = "needs-review/stair-wear-domain"
    else:
        status = "range-clean/stair-wear-domain"
    return {"status": status, "hard_errors": errors, "warnings": warnings,
            "evidence": "; ".join(errors + warnings) or "usage counts are nonnegative, the peak exceeds the spread average, and shares lie in [0,1]"}


#: Every task slug must appear here. ``scripts/test_feasibility_checks.py``
#: enforces this coverage contract so a new task cannot silently ship ungated.
CHECKS: dict[str, Any] = {
    "cumcm-2023-a-heliostat-field": heliostat_check,
    "cumcm-2023-b-multibeam-lines": multibeam_check,
    "cumcm-2023-c-vegetable-pricing": vegetable_pricing_check,
    "cumcm-2024-a-dragon-dance": dragon_dance_check,
    "cumcm-2024-b-production-decision": production_decision_check,
    "cumcm-2024-c-crop-planting": crop_planting_check,
    "cumcm-2025-a-smoke-screen": smoke_screen_check,
    "cumcm-2025-b-sic-thickness": sic_thickness_check,
    "cumcm-2025-c-nipt": nipt_check,
    "mcm-2023-a-plant-community": plant_check,
    "mcm-2023-b-maasai-mara": maasai_check,
    "mcm-2023-c-wordle": wordle_check,
    "mcm-2024-a-lamprey": lamprey_check,
    "mcm-2024-b-submersible-search": submersible_check,
    "mcm-2024-c-tennis-momentum": tennis_momentum_check,
    "mcm-2025-a-stair-wear": stair_wear_check,
    "mcm-2025-b-juneau-tourism": juneau_check,
    "mcm-2025-c-olympic-medals": olympic_check,
}


def validate_artifact(data: dict[str, Any], task_slug: str) -> dict[str, Any]:
    """Run the registered programmatic feasibility check for ``task_slug``."""
    check = CHECKS.get(task_slug)
    if check is None:
        return {
            "status": "uncovered/no-check-registered",
            "hard_errors": [],
            "warnings": [f"no feasibility check is registered for task '{task_slug}'"],
            "evidence": "task is not covered by the programmatic gate",
        }
    return check(data)


def main(argv: list[str] | None = None) -> int:
    """CLI: report gate coverage, or check one artifact against one task."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", help="path to a result JSON to check")
    parser.add_argument("--task", help="task slug to check the artifact against")
    parser.add_argument("--coverage", action="store_true", help="list registered task coverage")
    args = parser.parse_args(argv)

    if args.coverage or (args.artifact is None):
        repo_root = Path(__file__).resolve().parents[1]
        task_dirs = sorted(
            path.name for path in (repo_root / "tasks").glob("*/*") if path.is_dir()
        )
        missing = [slug for slug in task_dirs if slug not in CHECKS]
        for slug in task_dirs:
            mark = "OK " if slug in CHECKS else "MISSING"
            print(f"{mark} {slug}")
        print(f"\ncoverage: {len(task_dirs) - len(missing)}/{len(task_dirs)} tasks")
        if missing:
            print("uncovered: " + ", ".join(missing))
            return 1
        return 0

    if args.artifact:
        if not args.task:
            parser.error("--artifact requires --task")
        data = json.loads(Path(args.artifact).read_text(encoding="utf-8"))
        result = validate_artifact(data, args.task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["hard_errors"] else 0
    return 0


if __name__ == "__main__":  # pragma: no cover
    import sys

    sys.exit(main())
