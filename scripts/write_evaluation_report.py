# -*- coding: utf-8 -*-
"""Write a markdown evaluation summary for all generated TB-MathModeling tasks."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
JOBS_ROOT = REPO_ROOT / "jobs"
REPORT_PATH = REPO_ROOT / "docs" / "EVALUATION_RESULTS.md"


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


def _markdown_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        text = f"{value:.12g}"
    else:
        text = str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def _markdown_value(value: Any) -> str:
    return _markdown_cell(value) or "N/A"


def _as_float_or_none(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _job_reward(job_name: str) -> float | None:
    info = _job_info(job_name)
    reward = info.get("reward")
    return float(reward) if isinstance(reward, (int, float)) else None


def _job_info(job_name: str) -> dict[str, Any]:
    result_path = JOBS_ROOT / job_name / "result.json"
    if not result_path.exists():
        return {"job_name": job_name, "found": False}
    try:
        result = _read_json(result_path)
    except json.JSONDecodeError:
        return {"job_name": job_name, "found": True, "invalid_json": True}
    evals = result.get("stats", {}).get("evals", {})
    if not isinstance(evals, dict):
        return {"job_name": job_name, "found": True}
    info: dict[str, Any] = {"job_name": job_name, "found": True}
    for item in evals.values():
        if not isinstance(item, dict):
            continue
        info["n_trials"] = item.get("n_trials")
        info["n_errors"] = item.get("n_errors")
        exceptions = item.get("exception_stats")
        if isinstance(exceptions, dict) and exceptions:
            info["exceptions"] = ", ".join(
                f"{name}({len(ids) if isinstance(ids, list) else '?'})"
                for name, ids in sorted(exceptions.items())
            )
        metrics = item.get("metrics")
        if isinstance(metrics, list) and metrics:
            mean = metrics[0].get("mean")
            if isinstance(mean, (int, float)):
                info["reward"] = float(mean)
        break
    details = _score_details(job_name)
    if details is not None:
        info["score_details_found"] = True
        info["details_reward"] = details.get("reward")
    else:
        info["score_details_found"] = False
    return info


def _score_details(job_name: str) -> dict[str, Any] | None:
    job_dir = JOBS_ROOT / job_name
    if not job_dir.exists():
        return None
    paths = sorted(job_dir.glob("*/verifier/score_details.json"))
    if not paths:
        return None
    try:
        return _read_json(paths[0])
    except json.JSONDecodeError:
        return None


def _score_config(case: Any) -> dict[str, Any]:
    path = REPO_ROOT / "tasks" / case.contest_dir / case.slug / "tests" / "score_config.json"
    return _read_json(path)


def _status(score: dict[str, Any]) -> str:
    if score.get("scoring_version") == "tb-mathmodeling-v4-endpoint-target-minmax":
        return "v4 endpoint target-minmax"
    return "legacy fallback"


def _eval_values(details: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(details, dict):
        return {}
    raw = _as_float_or_none(details.get("raw_panel_score"))
    baseline = _as_float_or_none(details.get("baseline_panel_score"))
    selected = _as_float_or_none(details.get("reward"))
    b_eval = details.get("b_eval")
    bo_eval = details.get("bo_eval")
    b_reward = None
    bo_reward = None
    if isinstance(b_eval, dict):
        b_reward = _as_float_or_none(b_eval.get("reward"))
    if isinstance(bo_eval, dict):
        bo_reward = _as_float_or_none(bo_eval.get("reward"))
    if b_reward is None and raw is not None and baseline is not None:
        b_reward = raw - baseline
    if bo_reward is None:
        bo_reward = selected
    return {
        "selected_reward": selected,
        "eval_method": details.get("eval_method", "BO-Eval (legacy job)"),
        "b_eval_reward": b_reward,
        "bo_eval_reward": bo_reward,
    }


def _job_status(info: dict[str, Any]) -> str:
    if not info.get("found"):
        return "missing"
    if info.get("invalid_json"):
        return "invalid result.json"
    if info.get("n_errors"):
        return "error: " + str(info.get("exceptions", "unknown"))
    if info.get("score_details_found"):
        return "scored"
    return "finished without score details"


def _metric_value(metric: dict[str, Any], details: dict[str, Any], key: str) -> Any:
    if key in details:
        return details.get(key)
    if key == "actual":
        return ""
    if key == "outstanding_value":
        return metric.get("outstanding_value", metric.get("oracle_value"))
    return metric.get(key)


def _metric_b_eval_gain(metric: dict[str, Any], details: dict[str, Any]) -> Any:
    if "b_eval_signed_gain" in details:
        return details.get("b_eval_signed_gain")
    actual = _as_float_or_none(details.get("actual"))
    baseline = _as_float_or_none(_metric_value(metric, details, "baseline_value"))
    if actual is None or baseline is None:
        return ""
    direction = _metric_value(metric, details, "direction")
    if direction == "higher_is_better":
        return actual - baseline
    if direction == "lower_is_better":
        return baseline - actual
    return ""


def _metric_scored(metric: dict[str, Any], details: dict[str, Any]) -> str:
    if details.get("unscored"):
        return "no"
    weight = details.get("score_weight", metric.get("score_weight", metric.get("weight", 1.0)))
    try:
        return "yes" if float(weight) > 0.0 else "no"
    except (TypeError, ValueError):
        return "no"


def _task_metric_table(score: dict[str, Any], details: dict[str, Any] | None) -> str:
    detail_metrics = details.get("metrics", []) if isinstance(details, dict) else []
    detail_by_path = {
        str(item.get("path")): item
        for item in detail_metrics
        if isinstance(item, dict) and item.get("path") is not None
    }
    rows = [
        "| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |",
        "|---:|---|---:|---:|---|---:|---:|---:|---|---|",
    ]
    for index, metric in enumerate(score.get("metrics", []), 1):
        if not isinstance(metric, dict):
            continue
        path = str(metric.get("path", ""))
        detail = detail_by_path.get(path, {})
        direction = _metric_value(metric, detail, "direction") or "closeness_to_outstanding"
        source = metric.get("baseline_source_path", "")
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"`{_markdown_cell(path)}`",
                    _markdown_cell(_metric_value(metric, detail, "baseline_value")),
                    _markdown_cell(_metric_value(metric, detail, "outstanding_value")),
                    f"`{_markdown_cell(direction)}`",
                    _markdown_cell(_metric_value(metric, detail, "actual")),
                    _markdown_cell(detail.get("reward", "")),
                    _markdown_cell(_metric_b_eval_gain(metric, detail)),
                    _metric_scored(metric, detail),
                    _markdown_cell(source),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def main() -> None:
    builder = _load_builder()
    rows: list[str] = []
    detail_sections: list[str] = []
    endpoint_count = 0
    oracle_rewards: list[float] = []
    model_rewards: list[float] = []
    model_b_eval_rewards: list[float] = []
    model_bo_eval_rewards: list[float] = []
    for case in builder.CASES:
        score = _score_config(case)
        baseline = score.get("baseline_endpoint", {})
        if score.get("scoring_version") == "tb-mathmodeling-v4-endpoint-target-minmax":
            endpoint_count += 1
        oracle_job = f"oracle-current-{case.slug}"
        model_job = f"terminus2-deepseek-v4-flash-current-{case.slug}"
        oracle_info = _job_info(oracle_job)
        model_info = _job_info(model_job)
        oracle_reward = _job_reward(oracle_job)
        model_reward = _job_reward(model_job)
        model_details = _score_details(model_job)
        model_evals = _eval_values(model_details)
        model_b_eval_reward = model_evals.get("b_eval_reward")
        model_bo_eval_reward = model_evals.get("bo_eval_reward")
        if oracle_reward is not None:
            oracle_rewards.append(oracle_reward)
        if model_reward is not None:
            model_rewards.append(model_reward)
        if isinstance(model_b_eval_reward, (int, float)):
            model_b_eval_rewards.append(float(model_b_eval_reward))
        if isinstance(model_bo_eval_reward, (int, float)):
            model_bo_eval_rewards.append(float(model_bo_eval_reward))
        rows.append(
            "| "
            + " | ".join(
                [
                    case.contest.upper(),
                    str(case.year),
                    case.code,
                    f"`{case.slug}`",
                    _status(score),
                    score.get("default_eval_method", "B-Eval"),
                    str(score.get("metric_count")),
                    str(score.get("effective_metric_count")),
                    str(baseline.get("constant_endpoint_metric_count", "")),
                    str(baseline.get("missing_baseline_metric_count", "")),
                    f"`{baseline.get('kind')}`",
                    _markdown_cell(oracle_reward),
                    _job_status(oracle_info),
                    _markdown_cell(model_reward),
                    _markdown_cell(model_b_eval_reward),
                    _markdown_cell(model_bo_eval_reward),
                    _job_status(model_info),
                ]
            )
            + " |"
        )
        detail_sections.append(
            "\n".join(
                [
                    f"## {case.contest.upper()} {case.year} {case.code}: `{case.slug}`",
                    "",
                    f"- Scoring status: {_status(score)}",
                    f"- Default eval method: `{score.get('default_eval_method', 'B-Eval')}`",
                    f"- Metrics: {score.get('metric_count')} total, {score.get('effective_metric_count')} effective",
                    f"- Baseline endpoint: `{baseline.get('kind')}`",
                    f"- Oracle reward: {_markdown_cell(oracle_reward)} ({_job_status(oracle_info)})",
                    f"- DeepSeek/Terminus-2 job reward: {_markdown_cell(model_reward)} ({_job_status(model_info)})",
                    f"- DeepSeek/Terminus-2 B-Eval: {_markdown_value(model_b_eval_reward)}",
                    f"- DeepSeek/Terminus-2 BO-Eval: {_markdown_value(model_bo_eval_reward)}",
                    "",
                    _task_metric_table(score, model_details),
                ]
            )
        )

    oracle_mean = sum(oracle_rewards) / len(oracle_rewards) if oracle_rewards else None
    model_mean = sum(model_rewards) / len(model_rewards) if model_rewards else None
    model_b_eval_mean = sum(model_b_eval_rewards) / len(model_b_eval_rewards) if model_b_eval_rewards else None
    model_bo_eval_mean = sum(model_bo_eval_rewards) / len(model_bo_eval_rewards) if model_bo_eval_rewards else None
    content = f"""# Evaluation Results

This report is generated from local Harbor jobs and task `score_config.json` files.

- Total tasks: {len(builder.CASES)}
- Default eval method for regenerated tasks: `B-Eval`
- v4 endpoint target-minmax tasks: {endpoint_count}
- legacy fallback tasks: {len(builder.CASES) - endpoint_count}
- Oracle jobs found: {len(oracle_rewards)}
- Oracle mean reward: {_markdown_cell(oracle_mean)}
- DeepSeek/Terminus-2 jobs found: {len(model_rewards)}
- DeepSeek/Terminus-2 mean job reward: {_markdown_cell(model_mean)}
- DeepSeek/Terminus-2 mean B-Eval: {_markdown_cell(model_b_eval_mean)}
- DeepSeek/Terminus-2 mean BO-Eval: {_markdown_cell(model_bo_eval_mean)}

`B-Eval` is the default baseline-only score: `raw_panel_score - baseline_panel_score`, so negative means worse than the baseline. `BO-Eval` is the optional baseline-to-outstanding normalized score. `v4 endpoint target-minmax` means the task has real per-metric `baseline_value` and `outstanding_value` endpoints. `legacy fallback` means no semantically comparable per-metric question-result endpoint has been mapped yet, so the task still uses the older baseline-panel normalization.

| Contest | Year | Problem | Task | Scoring status | Default eval | Metrics | Effective | Exact-value | Missing baseline | Baseline kind | Oracle reward | Oracle status | DeepSeek job reward | DeepSeek B-Eval | DeepSeek BO-Eval | DeepSeek status |
|---|---:|---|---|---|---|---:|---:|---:|---:|---|---:|---|---:|---:|---:|---|
{chr(10).join(rows)}

# Per-Task Tables

{chr(10).join(detail_sections)}
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(content, encoding="utf-8")
    print(f"wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
