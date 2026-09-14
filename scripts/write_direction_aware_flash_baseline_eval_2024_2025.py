# -*- coding: utf-8 -*-
"""Recompute 2024-2025 flash-baseline evals with direction-aware metric scoring."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

from local_scoring import job_artifact_path


REPO_ROOT = Path(__file__).resolve().parents[1]
JOBS_ROOT = REPO_ROOT / "jobs"
REPORT_PATH = JOBS_ROOT / "terminus2-direction-aware-flash-baseline-bbo-2024-2025.md"
BO_DENOM_EPS = 1e-12

MODELS = {
    "flash": {
        "label": "v4 flash baseline",
        "template": "terminus2-deepseek-v4-flash-current-{slug}",
        "price_rmb_per_mtok": {"input_uncached": 2.0, "output": 4.0},
        "price_note": "DeepSeek V4-Flash peak",
    },
    "pro": {
        "label": "v4 pro",
        "template": "terminus2-deepseek-v4-pro-current-{slug}",
        "price_rmb_per_mtok": {"input_uncached": 9.0, "output": 27.0},
        "price_note": "DeepSeek V4-Pro peak",
    },
    "glm": {
        "label": "GLM-5.3",
        "template": "terminus2-glm-5.3-key2-{contest}",
        "price_rmb_per_mtok": {"input_uncached": 10.1, "output": 31.8},
        "price_note": "Zhipu GLM-5.3",
    },
    "gpt": {
        "label": "GPT-5.6 SOL high",
        "template": "terminus2-gpt-5.6-sol-high-2024-2025-{contest}-retryproxy",
        "price_rmb_per_mtok": {"input_uncached": 36.0, "output": 216.0},
        "price_note": "GPT-5.6 Sol",
    },
    "opus5": {
        "label": "Claude Opus 5",
        "template": "terminus2-claude-opus-5-2024-2025-{contest}-retryproxy",
        "price_rmb_per_mtok": {"input_uncached": 36.0, "output": 180.0},
        "price_note": "Claude Opus 5",
    },
    "kimi": {
        "label": "Kimi K3",
        "template": "terminus2-kimi-k3-2024-2025-{contest}-retryproxy",
        "price_rmb_per_mtok": {"input_uncached": 20.0, "output": 100.0},
        "price_note": "Kimi K3",
    },
    "gemini37flash": {
        "label": "Gemini 3.7 Flash high primary+retry",
        "template": "terminus2-gemini-3.7-flash-high-2024-2025-{contest}-retryproxy",
        "price_rmb_per_mtok": {"input_uncached": 5.4, "output": 27.0},
        "price_note": "Gemini 3.7 Flash discount",
        "artifact_job_overrides": {
            "cumcm-2025-a-smoke-screen": "terminus2-gemini-3.7-flash-high-2024-2025-cumcm-smoke-retry",
        },
    },
}


def _load_builder() -> Any:
    path = REPO_ROOT / "scripts" / "build_mathmodel_tasks.py"
    spec = importlib.util.spec_from_file_location("build_mathmodel_tasks", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_float(value: Any) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"expected finite number, got {value!r}")
    return number


def _try_get(data: Any, path: str) -> tuple[bool, Any]:
    cur = data
    token = ""
    i = 0
    try:
        while i < len(path):
            ch = path[i]
            if ch == ".":
                if token:
                    cur = cur[token]
                    token = ""
                i += 1
            elif ch == "[":
                if token:
                    cur = cur[token]
                    token = ""
                j = path.index("]", i)
                cur = cur[int(path[i + 1 : j])]
                i = j + 1
            else:
                token += ch
                i += 1
        if token:
            cur = cur[token]
        return True, cur
    except (KeyError, IndexError, TypeError, ValueError):
        return False, None


def _clamp01(value: float) -> float:
    return min(1.0, max(0.0, value))


def _direction(metric: dict[str, Any]) -> str:
    return str(metric.get("semantic_direction", metric.get("direction", "target_value")))


def _metric_exclusion_reason(metric: dict[str, Any], score_config: dict[str, Any]) -> str | None:
    if (
        score_config.get("oracle_source", {}).get("paper_id") == "2505964"
        and metric.get("path") == "great_coach_model.recommendations[3].estimated_medal_count_gain"
    ):
        return "excluded_prompt_asks_three_countries_not_four_recommendation_rows"
    return None


def _scale(metric: dict[str, Any]) -> float:
    oracle = _as_float(metric["oracle_value"])
    rel_scale = abs(_as_float(metric.get("rel_scale", 0.12)))
    abs_scale = abs(_as_float(metric.get("abs_scale", 1e-6)))
    baseline = metric.get("baseline_value")
    outstanding = metric.get("outstanding_value")
    if baseline is not None and outstanding is not None:
        try:
            endpoint_scale = abs(_as_float(outstanding) - _as_float(baseline))
        except (TypeError, ValueError):
            endpoint_scale = 0.0
        if endpoint_scale > 1e-12:
            return max(abs_scale, endpoint_scale, 1e-12)
    return max(abs_scale, rel_scale * max(abs(oracle), 1.0), 1e-12)


def _scale_source(metric: dict[str, Any]) -> str:
    baseline = metric.get("baseline_value")
    outstanding = metric.get("outstanding_value")
    if baseline is not None and outstanding is not None:
        try:
            if abs(_as_float(outstanding) - _as_float(baseline)) > 1e-12:
                return "endpoint_gap"
        except (TypeError, ValueError):
            pass
    return "rel_scale_times_max_abs_oracle_1"


def _over_o_score(gain: float, scale: float) -> float:
    return 1.0 + math.log1p(max(0.0, gain) / scale)


def _is_unit_interval_metric(metric: dict[str, Any]) -> bool:
    values = [metric.get("oracle_value"), metric.get("baseline_value"), metric.get("outstanding_value")]
    numeric_values: list[float] = []
    for value in values:
        if value is None:
            continue
        try:
            numeric_values.append(abs(_as_float(value)))
        except (TypeError, ValueError):
            return False
    return bool(numeric_values) and max(numeric_values) <= 1.5


def _is_percent_like_metric(metric: dict[str, Any]) -> bool:
    path = str(metric.get("path", "")).lower()
    excluded_tokens = ("multiplier", "speed_ratio", "ratio", "factor")
    if any(token in path for token in excluded_tokens):
        return False
    percent_tokens = (
        "percent",
        "percentage",
        "pct",
        "index",
        "score",
        "rate",
        "probability",
        "acceptance",
        "sustainability",
        "accuracy",
        "f1",
        "auc",
    )
    return any(token in path for token in percent_tokens)


def _scoring_actual(actual: float, metric: dict[str, Any]) -> tuple[float, str | None]:
    if _is_unit_interval_metric(metric) and _is_percent_like_metric(metric) and 10.0 < abs(actual) <= 100.0:
        return actual / 100.0, "percent_to_fraction"
    return actual, None


def _metric_validity(actual: float, metric: dict[str, Any]) -> tuple[list[str], str | None]:
    path = str(metric.get("path", "")).lower()
    oracle = _as_float(metric["oracle_value"])
    checks = ["finite_number"]

    if "correlation" in path or "spearman" in path:
        checks.append("correlation_in_minus1_to_1")
        if not -1.0 <= actual <= 1.0:
            return checks, "invalid_correlation_out_of_range"

    if path.endswith("parasite_coexistence_case.final_parasite_index"):
        checks.append("raw_population_index_scale")
        if oracle > 5.0 and 0.0 <= actual <= 1.0:
            return checks, "invalid_normalized_value_for_raw_population_index"

    if path.endswith("parasite_coexistence_case.host_fish_index"):
        checks.append("raw_population_index_scale")
        if oracle > 100.0 and 0.0 <= actual <= 10.0:
            return checks, "invalid_normalized_value_for_raw_population_index"

    bounded_unit_tokens = (
        "accuracy",
        "f1",
        "rate",
        "probability",
        "acceptance",
    )
    if any(token in path for token in bounded_unit_tokens):
        checks.append("unit_interval_quantity")
        if not 0.0 <= actual <= 1.0:
            return checks, "invalid_unit_interval_out_of_range"

    if _is_unit_interval_metric(metric) and _is_percent_like_metric(metric):
        checks.append("unit_like_percent_metric_nonnegative")
        if actual < 0.0:
            return checks, "invalid_negative_unit_like_percent_metric"

    positive_physical_tokens = (
        "speed_mps",
        "speed_ratio",
        "multiplier",
        "thickness_um",
    )
    nonnegative_quantity_tokens = (
        "duration_s",
        "visitors",
        "users",
        "count",
        "gain",
        "fee_usd",
        "revenue_usd",
    )
    if oracle > 0.0 and actual <= 0.0 and any(token in path for token in positive_physical_tokens):
        checks.append("positive_physical_quantity")
        return checks, "invalid_nonpositive_physical_quantity"
    if any(token in path for token in positive_physical_tokens):
        checks.append("positive_physical_quantity")

    if any(token in path for token in nonnegative_quantity_tokens):
        checks.append("nonnegative_quantity")
        if actual < 0.0:
            return checks, "invalid_negative_quantity"

    return checks, None


def _suspicious_metric_reason(actual: float, metric: dict[str, Any]) -> tuple[str | None, float | None]:
    path = str(metric.get("path", "")).lower()
    oracle = _as_float(metric["oracle_value"])
    if abs(oracle) <= 1e-12 or abs(actual) <= 1e-12:
        return None, None
    if any(token in path for token in ("accuracy", "f1", "rate", "probability", "acceptance")):
        return None, abs(actual / oracle)
    ratio = abs(actual / oracle)
    if "index" in path and (ratio < 0.1 or ratio > 10.0):
        return "review_index_scale_or_units", ratio
    if ratio < 0.02 or ratio > 50.0:
        return "review_extreme_actual_oracle_ratio", ratio
    return None, ratio


def _legacy_score(actual: float, metric: dict[str, Any]) -> float:
    oracle = _as_float(metric["oracle_value"])
    scale = _scale(metric)
    direction = _direction(metric)
    if direction == "higher_is_better":
        if actual >= oracle:
            return _over_o_score(actual - oracle, scale)
        shortfall = oracle - actual
        return 1.0 / (1.0 + shortfall / scale)
    if direction == "lower_is_better":
        if actual <= oracle:
            return _over_o_score(oracle - actual, scale)
        excess = actual - oracle
        return 1.0 / (1.0 + excess / scale)
    if direction == "exact_value":
        return 1.0 if actual == oracle else 0.0
    error = abs(actual - oracle)
    return 1.0 / (1.0 + error / scale)


def _endpoint_score(actual: float, metric: dict[str, Any]) -> float:
    baseline = _as_float(metric["baseline_value"])
    outstanding = _as_float(metric["outstanding_value"])
    scale = _scale(metric)
    direction = _direction(metric)
    if direction == "higher_is_better":
        denom = outstanding - baseline
        if denom <= 1e-12:
            return 0.0
        if actual >= outstanding:
            return _over_o_score(actual - outstanding, scale)
        return max(0.0, (actual - baseline) / denom)
    if direction == "lower_is_better":
        denom = baseline - outstanding
        if denom <= 1e-12:
            return 0.0
        if actual <= outstanding:
            return _over_o_score(outstanding - actual, scale)
        return max(0.0, (baseline - actual) / denom)
    if direction == "exact_value":
        return 1.0 if actual == outstanding else 0.0
    denom = abs(outstanding - baseline)
    if denom <= 1e-12:
        return 1.0 if actual == outstanding else 0.0
    return _clamp01(1.0 - abs(actual - outstanding) / denom)


def _metric_score(actual: float, metric: dict[str, Any]) -> float:
    if metric.get("normalization_mode") == "baseline_to_outstanding_target_minmax":
        return _endpoint_score(actual, metric)
    return _legacy_score(actual, metric)


def score_artifact_direction_aware(
    data: dict[str, Any],
    score_config: dict[str, Any],
) -> dict[str, Any]:
    details: list[dict[str, Any]] = []
    weighted_sum = 0.0
    weight_total = 0.0
    for metric in score_config["metrics"]:
        configured_weight = max(0.0, _as_float(metric.get("weight", 1.0)))
        weight = max(0.0, _as_float(metric.get("score_weight", configured_weight)))
        exclusion_reason = _metric_exclusion_reason(metric, score_config)
        if exclusion_reason is not None:
            weight = 0.0
        path = str(metric["path"])
        found, value = _try_get(data, path)
        item: dict[str, Any] = {
            "path": path,
            "direction": _direction(metric),
            "normalization_mode": metric.get("normalization_mode", "legacy_target_distance_to_outstanding"),
            "scale": _scale(metric),
            "scale_source": _scale_source(metric),
            "oracle_value": metric.get("oracle_value"),
            "baseline_value": metric.get("baseline_value"),
            "outstanding_value": metric.get("outstanding_value", metric.get("oracle_value")),
            "score_weight": weight,
            "found": found,
            "reward": 0.0,
        }
        if exclusion_reason is not None:
            item["excluded"] = True
            item["exclusion_reason"] = exclusion_reason
        if found:
            try:
                actual = _as_float(value)
            except (TypeError, ValueError):
                item["actual"] = value
                item["nonnumeric"] = True
            else:
                item["actual"] = actual
                actual_for_score, unit_adjustment = _scoring_actual(actual, metric)
                item["scoring_actual"] = actual_for_score
                if unit_adjustment is not None:
                    item["unit_adjustment"] = unit_adjustment
                if weight > 0.0:
                    validity_checks, invalid_reason = _metric_validity(actual_for_score, metric)
                    item["validity_checks"] = validity_checks
                    if invalid_reason is not None:
                        item["invalid"] = True
                        item["invalid_reason"] = invalid_reason
                    else:
                        suspicious_reason, actual_oracle_ratio = _suspicious_metric_reason(actual_for_score, metric)
                        if suspicious_reason is not None:
                            item["review_warning"] = suspicious_reason
                            item["actual_oracle_ratio"] = actual_oracle_ratio
                        item["reward"] = _metric_score(actual_for_score, metric)
        if weight > 0.0:
            weighted_sum += weight * float(item["reward"])
            weight_total += weight
        details.append(item)
    raw_panel_score = weighted_sum / weight_total if weight_total else 0.0
    return {
        "raw_panel_score": raw_panel_score,
        "scoreable_count": sum(
            1
            for item in details
            if float(item.get("score_weight", 0.0)) > 0.0 and item.get("found") and not item.get("nonnumeric")
        ),
        "metric_count": len(details),
        "metrics": details,
        "source": "direction_aware_rescore",
    }


def score_job_artifact_direction_aware(
    job_name: str,
    output_name: str,
    score_config: dict[str, Any],
) -> dict[str, Any] | None:
    path = job_artifact_path(JOBS_ROOT, job_name, output_name)
    if path is None:
        return None
    try:
        data = _read_json(path)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    details = score_artifact_direction_aware(data, score_config)
    details["artifact_path"] = str(path)
    return details


def _score_config(case: Any) -> dict[str, Any]:
    return _read_json(REPO_ROOT / "tasks" / case.contest_dir / case.slug / "tests" / "score_config.json")


def _expected_result(case: Any) -> dict[str, Any]:
    return _read_json(REPO_ROOT / "tasks" / case.contest_dir / case.slug / "tests" / "expected_result.json")


def _job_name(model: str, case: Any) -> str:
    return str(MODELS[model]["template"]).format(slug=case.slug, contest=case.contest)


def _job_names(model: str, case: Any) -> list[str]:
    overrides = MODELS[model].get("artifact_job_overrides", {})
    names: list[str] = []
    if isinstance(overrides, dict):
        override = overrides.get(case.slug)
        if isinstance(override, str) and override:
            # An explicit override denotes a newer/superseding retry. Prefer
            # it over the original job when both contain a scoreable artifact.
            names.append(override)
    names.append(_job_name(model, case))
    return names


def _score_model_artifact_direction_aware(
    model: str,
    case: Any,
    output_name: str,
    score_config: dict[str, Any],
) -> dict[str, Any] | None:
    for job_name in _job_names(model, case):
        details = score_job_artifact_direction_aware(job_name, output_name, score_config)
        if details is not None:
            details["job_name"] = job_name
            return details
    return None


def _raw(details: dict[str, Any] | None) -> float | None:
    if not isinstance(details, dict):
        return None
    try:
        return _as_float(details["raw_panel_score"])
    except (KeyError, TypeError, ValueError):
        return None


def _b_eval(model_raw: float | None, flash_raw: float | None) -> float | None:
    if model_raw is None or flash_raw is None:
        return None
    return model_raw - flash_raw


def _bo_eval(model_raw: float | None, flash_raw: float | None, oracle_raw: float | None) -> float | None:
    if model_raw is None or flash_raw is None or oracle_raw is None:
        return None
    denom = oracle_raw - flash_raw
    if denom <= BO_DENOM_EPS:
        return None
    return max(0.0, (model_raw - flash_raw) / denom)


def _bo_defined(record: dict[str, Any]) -> bool:
    flash_raw = record["raw"].get("flash")
    oracle_raw = record.get("oracle_raw")
    return flash_raw is not None and oracle_raw is not None and oracle_raw - flash_raw > BO_DENOM_EPS


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _cell(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        if not math.isfinite(value):
            return "N/A"
        return f"{value:.6f}"
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def _int_cell(value: int | None) -> str:
    return "N/A" if value is None else f"{value:,}"


def _money_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"¥{value:,.2f}"


def _pp_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100.0:+.2f} pp"


def _pct_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100.0:.2f}%"


def _delta_cell(new_value: float | None, old_value: float | None) -> str:
    if new_value is None or old_value is None:
        return "N/A"
    return _cell(new_value - old_value)


def _metric_delta(old_details: dict[str, Any] | None, new_details: dict[str, Any] | None) -> float | None:
    if not old_details or not new_details:
        return None
    return _raw(new_details) - _raw(old_details)


def _compare_legacy_scores(case: Any, model: str, score_config: dict[str, Any], output_name: str) -> float | None:
    from local_scoring import score_job_artifact

    for job_name in _job_names(model, case):
        details = score_job_artifact(JOBS_ROOT, job_name, output_name, score_config, "BO-Eval")
        raw = _raw(details)
        if raw is not None:
            return raw
    return None


def _model_job_names(model: str, cases: list[Any]) -> list[str]:
    seen: set[str] = set()
    names: list[str] = []
    for case in cases:
        for name in _job_names(model, case):
            if name not in seen:
                seen.add(name)
                names.append(name)
    return names


def _model_token_stats(model: str, cases: list[Any]) -> dict[str, Any]:
    stats = {
        "job_count": 0,
        "n_input_tokens": 0,
        "n_cache_tokens": 0,
        "n_output_tokens": 0,
        "billable_input_tokens": 0,
        "estimated_cost_rmb": None,
    }
    for job_name in _model_job_names(model, cases):
        path = JOBS_ROOT / job_name / "result.json"
        if not path.exists():
            continue
        try:
            data = _read_json(path)
        except json.JSONDecodeError:
            continue
        job_stats = data.get("stats")
        if not isinstance(job_stats, dict):
            continue
        input_tokens = int(job_stats.get("n_input_tokens") or 0)
        cache_tokens = int(job_stats.get("n_cache_tokens") or 0)
        output_tokens = int(job_stats.get("n_output_tokens") or 0)
        stats["job_count"] += 1
        stats["n_input_tokens"] += input_tokens
        stats["n_cache_tokens"] += cache_tokens
        stats["n_output_tokens"] += output_tokens
        stats["billable_input_tokens"] += max(0, input_tokens - cache_tokens)

    price = MODELS[model].get("price_rmb_per_mtok", {})
    if isinstance(price, dict):
        input_price = price.get("input_uncached")
        output_price = price.get("output")
        if input_price is not None and output_price is not None:
            stats["estimated_cost_rmb"] = (
                stats["billable_input_tokens"] / 1_000_000.0 * float(input_price)
                + stats["n_output_tokens"] / 1_000_000.0 * float(output_price)
            )
    return stats


def _metric_rows(score_config: dict[str, Any], details_by_model: dict[str, dict[str, Any] | None]) -> str:
    model_metric_maps: dict[str, dict[str, dict[str, Any]]] = {}
    for model, details in details_by_model.items():
        metrics = details.get("metrics", []) if details else []
        model_metric_maps[model] = {
            str(item.get("path")): item
            for item in metrics
            if isinstance(item, dict) and item.get("path") is not None
        }
    model_headers = [f"{_cell(meta['label'])} actual/score" for meta in MODELS.values()]
    rows = [
        "| " + " | ".join(["Metric", "Direction", "Mode", "Scale", *model_headers]) + " |",
        "|---|---|---|---:" + "|---:" * len(MODELS) + "|",
    ]
    for metric in score_config.get("metrics", []):
        weight = max(0.0, _as_float(metric.get("score_weight", metric.get("weight", 1.0))))
        if _metric_exclusion_reason(metric, score_config) is not None:
            continue
        if weight <= 0.0:
            continue
        path = str(metric["path"])
        cells = []
        for model in MODELS:
            item = model_metric_maps[model].get(path, {})
            actual = item.get("actual")
            scoring_actual = item.get("scoring_actual")
            score = item.get("reward")
            if item.get("unit_adjustment") and scoring_actual is not None:
                actual_cell = f"{_cell(actual)}->{_cell(scoring_actual)}"
            else:
                actual_cell = _cell(actual)
            if item.get("invalid_reason"):
                actual_cell = f"{actual_cell} ({_cell(item['invalid_reason'])})"
            cells.append(f"{actual_cell} / {_cell(score)}")
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{_cell(path)}`",
                    f"`{_cell(_direction(metric))}`",
                    f"`{_cell(metric.get('normalization_mode', 'legacy_target_distance_to_outstanding'))}`",
                    _cell(_scale(metric)),
                    *cells,
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def main() -> None:
    builder = _load_builder()
    cases = [case for case in builder.CASES if case.year in (2024, 2025)]
    records: list[dict[str, Any]] = []
    for case in cases:
        score = _score_config(case)
        oracle_details = score_artifact_direction_aware(_expected_result(case), score)
        raw_by_model: dict[str, float | None] = {}
        details_by_model: dict[str, dict[str, Any] | None] = {}
        legacy_raw_by_model: dict[str, float | None] = {}
        for model in MODELS:
            details = _score_model_artifact_direction_aware(model, case, case.output_name, score)
            details_by_model[model] = details
            raw_by_model[model] = _raw(details) if details is not None else 0.0
            legacy_raw = _compare_legacy_scores(case, model, score, case.output_name)
            legacy_raw_by_model[model] = legacy_raw if legacy_raw is not None else 0.0
        b_by_model = {
            model: _b_eval(raw_by_model[model], raw_by_model["flash"])
            for model in MODELS
            if model != "flash"
        }
        bo_by_model = {
            model: _bo_eval(raw_by_model[model], raw_by_model["flash"], _raw(oracle_details))
            for model in MODELS
            if model != "flash"
        }
        records.append(
            {
                "case": case,
                "score": score,
                "oracle_raw": _raw(oracle_details),
                "raw": raw_by_model,
                "legacy_raw": legacy_raw_by_model,
                "b": b_by_model,
                "bo": bo_by_model,
                "details": details_by_model,
            }
        )

    token_stats_by_model = {model: _model_token_stats(model, cases) for model in MODELS}
    summary_rows: list[
        tuple[str, str, int, int, float | None, float | None, float | None, float | None, dict[str, Any]]
    ] = []
    for model, meta in MODELS.items():
        artifact_count = sum(1 for r in records if r["details"].get(model) is not None)
        raw_values = [r["raw"][model] for r in records if r["raw"][model] is not None]
        legacy_values = [r["legacy_raw"][model] for r in records if r["legacy_raw"][model] is not None]
        if model == "flash":
            b_values = [0.0 for r in records if r["raw"]["flash"] is not None]
            bo_values = [0.0 for r in records if _bo_defined(r)]
        else:
            b_values = [r["b"][model] for r in records if r["b"][model] is not None]
            bo_values = [r["bo"][model] for r in records if r["bo"][model] is not None]
        summary_rows.append(
            (
                model,
                str(meta["label"]),
                artifact_count,
                len(bo_values),
                _mean(raw_values),
                _mean(b_values),
                _mean(bo_values),
                None if _mean(raw_values) is None or _mean(legacy_values) is None else _mean(raw_values) - _mean(legacy_values),
                token_stats_by_model[model],
            )
        )

    suite_rows: list[tuple[str, str, int, float | None, float | None, float | None]] = []
    for model, meta in MODELS.items():
        for suite in ("cumcm", "mcm"):
            subset = [r for r in records if r["case"].contest == suite]
            artifact_count = sum(1 for r in subset if r["details"].get(model) is not None)
            raw_values = [r["raw"][model] for r in subset if r["raw"][model] is not None]
            if model == "flash":
                b_values = [0.0 for r in subset if r["raw"]["flash"] is not None]
                bo_values = [0.0 for r in subset if _bo_defined(r)]
            else:
                b_values = [r["b"][model] for r in subset if r["b"][model] is not None]
                bo_values = [r["bo"][model] for r in subset if r["bo"][model] is not None]
            suite_rows.append(
                (str(meta["label"]), suite.upper(), artifact_count, _mean(raw_values), _mean(b_values), _mean(bo_values))
            )

    bo_defined_records = [r for r in records if _bo_defined(r)]
    saturated_records = [r for r in records if not _bo_defined(r)]
    split_rows: list[tuple[str, str, int, float | None, float | None]] = []
    split_specs = [
        ("All 12 tasks", records),
        (f"BO-defined {len(bo_defined_records)} tasks", bo_defined_records),
        (f"Flash-at/above-O {len(saturated_records)} tasks", saturated_records),
    ]
    for split_label, subset in split_specs:
        for model, meta in MODELS.items():
            artifact_count = sum(1 for r in subset if r["details"].get(model) is not None)
            raw_values = [r["raw"][model] for r in subset if r["raw"][model] is not None]
            if model == "flash":
                b_values = [0.0 for r in subset if r["raw"]["flash"] is not None]
            else:
                b_values = [
                    r["raw"][model] - r["raw"]["flash"]
                    for r in subset
                    if r["raw"][model] is not None and r["raw"]["flash"] is not None
                ]
            split_rows.append((split_label, str(meta["label"]), artifact_count, _mean(raw_values), _mean(b_values)))

    per_task_rows: list[str] = []
    for r in records:
        case = r["case"]

        def model_cell(model: str) -> str:
            if model == "flash":
                return _cell(r["raw"]["flash"])
            return f"{_cell(r['raw'][model])} / {_pp_cell(r['b'][model])} / {_pct_cell(r['bo'][model])}"

        per_task_rows.append(
            "| "
            + " | ".join(
                [
                    str(case.year),
                    case.contest.upper(),
                    case.code,
                    f"`{case.slug}`",
                    *[model_cell(model) for model in MODELS],
                    _cell(r["oracle_raw"]),
                ]
            )
            + " |"
        )

    gpt_vs_glm_rows: list[str] = []
    for r in sorted(records, key=lambda item: (item["b"]["gpt"] or 0.0) - (item["b"]["glm"] or 0.0)):
        diff_raw = _b_eval(r["raw"]["gpt"], r["raw"]["glm"])
        diff_b = None if r["b"]["gpt"] is None or r["b"]["glm"] is None else r["b"]["gpt"] - r["b"]["glm"]
        diff_bo = None if r["bo"]["gpt"] is None or r["bo"]["glm"] is None else r["bo"]["gpt"] - r["bo"]["glm"]
        gpt_vs_glm_rows.append(
            "| "
            + " | ".join(
                [
                    f"`{r['case'].slug}`",
                    _cell(diff_raw),
                    _pp_cell(diff_b),
                    _pp_cell(diff_bo),
                    _cell(r["raw"]["gpt"]),
                    _cell(r["raw"]["glm"]),
                    _pct_cell(r["bo"]["gpt"]),
                    _pct_cell(r["bo"]["glm"]),
                ]
            )
            + " |"
        )

    saturated_rows: list[str] = []
    for r in records:
        if _bo_defined(r):
            continue
        case = r["case"]
        saturated_rows.append(
            "| "
            + " | ".join(
                [
                    str(case.year),
                    case.contest.upper(),
                    case.code,
                    f"`{case.slug}`",
                    _cell(r["raw"]["flash"]),
                    _cell(r["oracle_raw"]),
                    "flash raw is at or above direction-aware O score; BO denominator is non-positive",
                ]
            )
            + " |"
        )

    invalid_metric_rows: list[str] = []
    missing_metric_rows: list[str] = []
    missing_artifact_rows: list[str] = []
    excluded_metric_rows: list[str] = []
    review_warning_rows: list[str] = []
    for r in records:
        case = r["case"]
        for model in MODELS:
            details = r["details"].get(model)
            if not details:
                missing_artifact_rows.append(
                    "| "
                    + " | ".join(
                        [
                            str(case.year),
                            case.contest.upper(),
                            case.code,
                            f"`{case.slug}`",
                            str(MODELS[model]["label"]),
                            "artifact missing or unreadable",
                        ]
                    )
                    + " |"
                )
                continue
            for item in details.get("metrics", []):
                if item.get("excluded"):
                    excluded_metric_rows.append(
                        "| "
                        + " | ".join(
                            [
                                str(case.year),
                                case.contest.upper(),
                                case.code,
                                f"`{case.slug}`",
                                str(MODELS[model]["label"]),
                                f"`{_cell(item.get('path'))}`",
                                _cell(item.get("exclusion_reason")),
                            ]
                        )
                        + " |"
                    )
                if (
                    float(item.get("score_weight", 0.0)) > 0.0
                    and (not item.get("found") or item.get("nonnumeric"))
                ):
                    missing_metric_rows.append(
                        "| "
                        + " | ".join(
                            [
                                str(case.year),
                                case.contest.upper(),
                                case.code,
                                f"`{case.slug}`",
                                str(MODELS[model]["label"]),
                                f"`{_cell(item.get('path'))}`",
                                "nonnumeric" if item.get("nonnumeric") else "missing",
                            ]
                        )
                        + " |"
                    )
                if item.get("invalid_reason"):
                    invalid_metric_rows.append(
                        "| "
                        + " | ".join(
                            [
                                str(case.year),
                                case.contest.upper(),
                                case.code,
                                f"`{case.slug}`",
                                str(MODELS[model]["label"]),
                                f"`{_cell(item.get('path'))}`",
                                _cell(item.get("actual")),
                                _cell(item.get("scoring_actual")),
                                _cell(item.get("invalid_reason")),
                            ]
                        )
                        + " |"
                    )
                if item.get("review_warning"):
                    review_warning_rows.append(
                        "| "
                        + " | ".join(
                            [
                                str(case.year),
                                case.contest.upper(),
                                case.code,
                                f"`{case.slug}`",
                                str(MODELS[model]["label"]),
                                f"`{_cell(item.get('path'))}`",
                                _cell(item.get("actual")),
                                _cell(item.get("scoring_actual")),
                                _cell(item.get("oracle_value")),
                                _cell(item.get("actual_oracle_ratio")),
                                _cell(item.get("review_warning")),
                            ]
                        )
                        + " |"
                    )

    detail_sections: list[str] = []
    focus_slugs = {
        "cumcm-2024-a-dragon-dance",
        "mcm-2024-b-submersible-search",
        "cumcm-2024-c-crop-planting",
        "cumcm-2025-a-smoke-screen",
        "cumcm-2024-b-production-decision",
        "mcm-2025-b-juneau-tourism",
    }
    for r in records:
        if r["case"].slug not in focus_slugs:
            continue
        case = r["case"]
        detail_sections.append(
            "\n".join(
                [
                    f"### {case.contest.upper()} {case.year} {case.code}: `{case.slug}`",
                    "",
                    "- Direction-aware raw: "
                    + " / ".join(f"{meta['label']}={_cell(r['raw'][model])}" for model, meta in MODELS.items()),
                    "- Legacy raw: "
                    + " / ".join(
                        f"{meta['label']}={_cell(r['legacy_raw'][model])}" for model, meta in MODELS.items()
                    ),
                    "",
                    _metric_rows(r["score"], r["details"]),
                ]
            )
        )

    lines = [
        "# Direction-Aware Flash-Baseline B/BO Evaluation: 2024-2025",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "Scope: 2024 and 2025 terminal-bench-math-modeling tasks, 12 tasks total. This report rescored the saved artifacts without modifying verifier outputs or job result files.",
        "",
        "Direction-aware metric rule:",
        "- `higher_is_better`: O-paper value scores 1.0; values above O score `1 + log1p((actual - O) / scale)`.",
        "- `lower_is_better`: O-paper value scores 1.0; values below O score `1 + log1p((O - actual) / scale)`.",
        "- `target_value`: score remains closeness to the O-paper value.",
        "- Scale uses `abs(outstanding_value - baseline_value)` when per-metric endpoints exist; otherwise it falls back to `max(abs_scale, rel_scale * max(abs(O), 1))`.",
        "- Unit guard: if a percent-like metric's configured O/baseline/outstanding values are in the unit interval but an artifact reports a value between 10 and 100, the value is treated as a percent and divided by 100 for scoring. Ratio/multiplier/factor fields are excluded from this guard.",
        "- Validity gate: every scored metric is checked before reward assignment. Current checks cover finite numeric values, positive physical quantities such as speeds/ratios/multipliers/thicknesses, nonnegative counts/time/money quantities, unit-interval rates/probabilities/accuracy/F1, correlation ranges, and manually reviewed raw-population index scale mismatches.",
        "- For below-O optimization metrics, shortfall/excess uses `1 / (1 + miss / scale)`. For endpoint min-max metrics, scores are normalized between `baseline_value` and `outstanding_value`, then continue above 1 with the same over-O log rule.",
        "",
        "Flash-baseline eval rule:",
        "- Primary eval: `B-Eval vs flash = direction_aware_raw(model) - direction_aware_raw(v4 flash)`, computed over all 12 tasks.",
        "- Supplemental eval: `BO-Eval vs flash = max(0, (direction_aware_raw(model) - direction_aware_raw(v4 flash)) / (direction_aware_raw(O) - direction_aware_raw(v4 flash)))`, computed only when `direction_aware_raw(O) > direction_aware_raw(v4 flash)`. It is not capped at 1, so above-O results remain distinguishable.",
        "- Display convention: B-Eval is shown as percentage points (`raw delta * 100 pp`); BO-Eval is shown as percent of the flash-to-O gap recovered (`ratio * 100%`).",
        "",
        "Cost rule:",
        "- Token columns are `input/cache/output` from the selected job `result.json` files. Gemini includes primary jobs plus the smoke retry job, because both consumed tokens.",
        "- Estimated cost uses the user-provided RMB prices per 1M tokens. Billable input is `max(input - cache, 0)` because only cache-miss input prices were provided; cache-hit input tokens are displayed but not charged in this estimate.",
        "- DeepSeek V4-Flash and V4-Pro rows use the provided peak prices as a conservative default.",
        "",
        "## Overall Mean",
        "",
        "| Model | Artifacts | BO-defined tasks | Mean direction-aware raw | Mean B-Eval vs flash (pp) | Mean BO-Eval vs flash on defined subset (%) | Raw delta vs legacy | Tokens input/cache/output | Billable input/output | Est. cost RMB |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for _, label, n, bo_n, raw_mean, b_mean, bo_mean, raw_delta, token_stats in summary_rows:
        tokens = (
            f"{_int_cell(token_stats['n_input_tokens'])} / "
            f"{_int_cell(token_stats['n_cache_tokens'])} / "
            f"{_int_cell(token_stats['n_output_tokens'])}"
        )
        billable_tokens = (
            f"{_int_cell(token_stats['billable_input_tokens'])} / "
            f"{_int_cell(token_stats['n_output_tokens'])}"
        )
        lines.append(
            f"| {label} | {n} | {bo_n} | {_cell(raw_mean)} | {_pp_cell(b_mean)} | {_pct_cell(bo_mean)} | "
            f"{_cell(raw_delta)} | {tokens} | {billable_tokens} | {_money_cell(token_stats['estimated_cost_rmb'])} |"
        )

    primary_ranking = sorted(
        (row for row in summary_rows if row[0] != "flash"),
        key=lambda row: row[5] if row[5] is not None else float("-inf"),
        reverse=True,
    )
    supplemental_ranking = sorted(
        (row for row in summary_rows if row[0] != "flash"),
        key=lambda row: row[6] if row[6] is not None else float("-inf"),
        reverse=True,
    )
    lines.extend(
        [
            "",
            "## Primary Readout",
            "",
            "- Primary ranking by 12-task B-Eval vs flash: "
            + " > ".join(f"{row[1]} ({_pp_cell(row[5])})" for row in primary_ranking)
            + ".",
            f"- Supplemental BO-Eval ranking on the {summary_rows[0][3]} BO-defined tasks: "
            + " > ".join(f"{row[1]} ({_pct_cell(row[6])})" for row in supplemental_ranking)
            + ".",
            "- Saturated tasks stay in raw and B-Eval. They are excluded only from BO-Eval because the baseline-to-O denominator is zero or negative.",
            f"- Split diagnostic: on the {len(bo_defined_records)} BO-defined tasks the non-baseline models beat flash on B-Eval, while the {len(saturated_records)} flash-at/above-O tasks are listed separately for denominator diagnostics.",
            "",
            "## B-Eval Split Diagnostic",
            "",
            "| Split | Model | Artifacts | Mean direction-aware raw | Mean B-Eval vs flash (pp) |",
            "|---|---|---:|---:|---:|",
            *[
                f"| {split_label} | {label} | {n} | {_cell(raw_mean)} | {_pp_cell(b_mean)} |"
                for split_label, label, n, raw_mean, b_mean in split_rows
            ],
            "",
            "## Invalid Metric Gates",
            "",
            "Invalid metric values receive reward 0 for that metric. This table is empty when no validity gate fired.",
            "",
            "| Year | Suite | Problem | Task | Model | Metric | Actual | Scoring actual | Reason |",
            "|---:|---|---|---|---|---|---:|---:|---|",
            *(invalid_metric_rows or ["| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No invalid metric values |"]),
            "",
            "## Missing Or Nonnumeric Metrics",
            "",
            "Missing or nonnumeric scored metrics receive reward 0 for that metric.",
            "",
            "### Missing Or Unreadable Artifacts",
            "",
            "| Year | Suite | Problem | Task | Model | Status |",
            "|---:|---|---|---|---|---|",
            *(
                missing_artifact_rows
                or ["| N/A | N/A | N/A | N/A | N/A | No missing or unreadable artifacts |"]
            ),
            "",
            "### Missing Or Nonnumeric Metric Values",
            "",
            "| Year | Suite | Problem | Task | Model | Metric | Status |",
            "|---:|---|---|---|---|---|---|",
            *(
                missing_metric_rows
                or ["| N/A | N/A | N/A | N/A | N/A | N/A | No missing or nonnumeric metric values |"]
            ),
            "",
            "## Excluded Score Metrics",
            "",
            "These metrics are excluded from the direction-aware rescore denominator because manual review found the score_config requirement stricter than the task prompt/schema.",
            "",
            "| Year | Suite | Problem | Task | Model | Metric | Reason |",
            "|---:|---|---|---|---|---|---|",
            *(
                excluded_metric_rows
                or ["| N/A | N/A | N/A | N/A | N/A | N/A | No excluded score metrics |"]
            ),
            "",
            "## Metric Review Warnings",
            "",
            "These values passed hard validity gates and still receive their computed reward, but their actual/O-paper ratio suggests possible unit or semantic mismatch. They should be manually reviewed before treating the leaderboard as final.",
            "",
            "| Year | Suite | Problem | Task | Model | Metric | Actual | Scoring actual | O value | Actual/O ratio | Warning |",
            "|---:|---|---|---|---|---|---:|---:|---:|---:|---|",
            *(
                review_warning_rows
                or ["| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No review warnings |"]
            ),
            "",
            "## Manual Review Resolution",
            "",
            "- `mcm-2024-a-lamprey`: the O-paper `final_parasite_index=8.562` and `host_fish_index=1080.356` are raw population-scale outputs from `final_parasite`/`final_host_fish`. Unit-scale values at these paths are not safely convertible and are treated as invalid scale mismatches.",
            "- `mcm-2024-c-tennis-momentum`: `final_match_warning_rate` values are valid probabilities in `[0,1]`; the large actual/O ratios indicate over-frequent warnings, not a unit mismatch.",
            "- `mcm-2025-a-stair-wear`: GLM user counts are nonnegative and internally consistent with its low traffic assumption; they remain valid but far from the O-paper target.",
            "- `mcm-2025-c-olympic-medals`: the official prompt asks to choose three countries. The O-paper reproduction emits four country-sport investment rows because one country has multiple sports, but all model artifacts emit three recommendation rows. The fourth row is excluded from this rescore rather than counted as missing.",
            "",
            "## Saturated Baseline Cases",
            "",
            "| Year | Suite | Problem | Task | flash raw | O raw | Treatment |",
            "|---:|---|---|---|---:|---:|---|",
            *(saturated_rows or ["| N/A | N/A | N/A | N/A | N/A | N/A | No saturated cases |"]),
        ]
    )

    lines.extend(
        [
            "",
            "## Suite Mean",
            "",
            "| Model | Suite | Artifacts | Mean direction-aware raw | Mean B-Eval vs flash (pp) | Mean BO-Eval vs flash (%) |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for label, suite, n, raw_mean, b_mean, bo_mean in suite_rows:
        lines.append(f"| {label} | {suite} | {n} | {_cell(raw_mean)} | {_pp_cell(b_mean)} | {_pct_cell(bo_mean)} |")

    lines.extend(
        [
            "",
            "## Per-Task Values",
            "",
            "Cells are `direction-aware raw / B-Eval pp vs flash / BO-Eval % vs flash` for non-baseline models. The flash column is raw only.",
            "",
            "| "
            + " | ".join(
                [
                    "Year",
                    "Suite",
                    "Problem",
                    "Task",
                    *[
                        f"{meta['label']} raw" if model == "flash" else str(meta["label"])
                        for model, meta in MODELS.items()
                    ],
                    "O raw",
                ]
            )
            + " |",
            "|---:|---|---|---" + "|---:" * len(MODELS) + "|---:|",
            *per_task_rows,
            "",
            "## GPT-5.6 SOL high vs GLM-5.3",
            "",
            "Rows are sorted by GPT-GLM B-Eval difference because B-Eval is the primary all-task metric. Negative means GLM leads on that task.",
            "",
            "| Task | GPT-GLM raw | GPT-GLM B-Eval delta (pp) | GPT-GLM BO-Eval delta (pp) | GPT raw | GLM raw | GPT BO-Eval (%) | GLM BO-Eval (%) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
            *gpt_vs_glm_rows,
            "",
            "## Focused Metric Details",
            "",
            "\n\n".join(detail_sections),
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
