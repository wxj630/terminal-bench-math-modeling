# -*- coding: utf-8 -*-
"""Compare DeepSeek v4-pro against DeepSeek v4-flash as the evaluation baseline."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

from local_scoring import job_artifact_path, score_artifact, score_job_artifact


REPO_ROOT = Path(__file__).resolve().parents[1]
JOBS_ROOT = REPO_ROOT / "jobs"
REPORT_PATH = REPO_ROOT / "docs" / "V4_PRO_FLASH_BASELINE_EVAL.md"
FLASH_JOB_TEMPLATE = "terminus2-deepseek-v4-flash-current-{slug}"
PRO_JOB_CANDIDATES = (
    "terminus2-deepseek-v4-pro-current-{slug}",
    "terminus2-deepseek-v4-pro-smoke-{slug}",
    "terminus2-deepseek-v4-pro-current-all",
    "terminus2-deepseek-v4-pro-current",
)


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


def _score_config(case: Any) -> dict[str, Any]:
    path = REPO_ROOT / "tasks" / case.contest_dir / case.slug / "tests" / "score_config.json"
    return _read_json(path)


def _expected_result(case: Any) -> dict[str, Any]:
    path = REPO_ROOT / "tasks" / case.contest_dir / case.slug / "tests" / "expected_result.json"
    return _read_json(path)


def _markdown_cell(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return "N/A"
        text = f"{value:.12g}"
    else:
        text = str(value)
    if text == "":
        return "N/A"
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def _as_float_or_none(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _job_info(job_name: str) -> dict[str, Any]:
    result_path = JOBS_ROOT / job_name / "result.json"
    if not result_path.exists():
        return {"job_name": job_name, "found": False, "status": "missing"}
    try:
        result = _read_json(result_path)
    except json.JSONDecodeError:
        return {"job_name": job_name, "found": True, "status": "invalid result.json"}
    evals = result.get("stats", {}).get("evals", {})
    info: dict[str, Any] = {"job_name": job_name, "found": True, "status": "finished"}
    if isinstance(evals, dict):
        for item in evals.values():
            if not isinstance(item, dict):
                continue
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
                    info["job_reward"] = float(mean)
            break
    if info.get("n_errors"):
        info["status"] = "error: " + str(info.get("exceptions", "unknown"))
    return info


def _existing_job_name(candidates: list[str], output_name: str) -> str | None:
    for job_name in candidates:
        job_dir = JOBS_ROOT / job_name
        if not job_dir.exists():
            continue
        if job_artifact_path(JOBS_ROOT, job_name, output_name) is not None:
            return job_name
        if (job_dir / "result.json").exists():
            return job_name
    return None


def _pro_job_name(case: Any) -> str | None:
    candidates = [template.format(slug=case.slug) for template in PRO_JOB_CANDIDATES]
    return _existing_job_name(candidates, case.output_name)


def _raw_score(details: dict[str, Any] | None) -> float | None:
    if not isinstance(details, dict):
        return None
    return _as_float_or_none(details.get("raw_panel_score"))


def _scoreable_count(details: dict[str, Any] | None) -> Any:
    if not isinstance(details, dict):
        return ""
    return details.get("scoreable_count")


def _bo_eval_against_flash(pro_raw: float | None, flash_raw: float | None, oracle_raw: float | None) -> float | None:
    if pro_raw is None or flash_raw is None or oracle_raw is None:
        return None
    denom = oracle_raw - flash_raw
    if denom <= 1e-12:
        return None
    return min(1.0, max(0.0, (pro_raw - flash_raw) / denom))


def _b_eval_against_flash(pro_raw: float | None, flash_raw: float | None) -> float | None:
    if pro_raw is None or flash_raw is None:
        return None
    return pro_raw - flash_raw


def _detail_by_path(details: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    metrics = details.get("metrics", []) if isinstance(details, dict) else []
    if not isinstance(metrics, list):
        return {}
    return {
        str(item.get("path")): item
        for item in metrics
        if isinstance(item, dict) and item.get("path") is not None
    }


def _metric_value(metric: dict[str, Any], detail: dict[str, Any], key: str) -> Any:
    if key in detail:
        return detail.get(key)
    if key == "actual":
        return ""
    if key == "outstanding_value":
        return metric.get("outstanding_value", metric.get("oracle_value"))
    return metric.get(key)


def _metric_table(score: dict[str, Any], flash_details: dict[str, Any] | None, pro_details: dict[str, Any] | None) -> str:
    flash_by_path = _detail_by_path(flash_details)
    pro_by_path = _detail_by_path(pro_details)
    rows = [
        "| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for index, metric in enumerate(score.get("metrics", []), 1):
        if not isinstance(metric, dict):
            continue
        path = str(metric.get("path", ""))
        flash_detail = flash_by_path.get(path, {})
        pro_detail = pro_by_path.get(path, {})
        flash_reward = _as_float_or_none(flash_detail.get("reward"))
        pro_reward = _as_float_or_none(pro_detail.get("reward"))
        gain = None if flash_reward is None or pro_reward is None else pro_reward - flash_reward
        direction = metric.get("semantic_direction", metric.get("direction", "target_value"))
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"`{_markdown_cell(path)}`",
                    f"`{_markdown_cell(direction)}`",
                    _markdown_cell(_metric_value(metric, pro_detail, "outstanding_value")),
                    _markdown_cell(_metric_value(metric, flash_detail, "actual")),
                    _markdown_cell(_metric_value(metric, pro_detail, "actual")),
                    _markdown_cell(flash_reward),
                    _markdown_cell(pro_reward),
                    _markdown_cell(gain),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def main() -> None:
    builder = _load_builder()
    rows: list[str] = []
    sections: list[str] = []
    b_eval_values: list[float] = []
    bo_eval_values: list[float] = []
    pro_raw_values: list[float] = []
    flash_raw_values: list[float] = []
    pro_found = 0

    for case in builder.CASES:
        score = _score_config(case)
        oracle_details = score_artifact(_expected_result(case), score, eval_method="BO-Eval")
        oracle_raw = _raw_score(oracle_details)

        flash_job = FLASH_JOB_TEMPLATE.format(slug=case.slug)
        flash_details = score_job_artifact(JOBS_ROOT, flash_job, case.output_name, score, eval_method="BO-Eval")
        flash_raw = _raw_score(flash_details)
        flash_info = _job_info(flash_job)

        pro_job = _pro_job_name(case)
        pro_details = (
            score_job_artifact(JOBS_ROOT, pro_job, case.output_name, score, eval_method="BO-Eval")
            if pro_job is not None
            else None
        )
        pro_raw = _raw_score(pro_details)
        pro_info = _job_info(pro_job) if pro_job is not None else {"status": "missing"}
        b_eval = _b_eval_against_flash(pro_raw, flash_raw)
        bo_eval = _bo_eval_against_flash(pro_raw, flash_raw, oracle_raw)

        if pro_raw is not None:
            pro_found += 1
            pro_raw_values.append(pro_raw)
        if flash_raw is not None:
            flash_raw_values.append(flash_raw)
        if b_eval is not None:
            b_eval_values.append(b_eval)
        if bo_eval is not None:
            bo_eval_values.append(bo_eval)

        rows.append(
            "| "
            + " | ".join(
                [
                    case.contest.upper(),
                    str(case.year),
                    case.code,
                    f"`{case.slug}`",
                    _markdown_cell(flash_raw),
                    _markdown_cell(pro_raw),
                    _markdown_cell(b_eval),
                    _markdown_cell(bo_eval),
                    _markdown_cell(oracle_raw),
                    _markdown_cell(_scoreable_count(flash_details)),
                    _markdown_cell(_scoreable_count(pro_details)),
                    _markdown_cell(flash_info.get("status")),
                    _markdown_cell(pro_info.get("status")),
                    f"`{_markdown_cell(pro_job)}`" if pro_job else "N/A",
                ]
            )
            + " |"
        )

        sections.append(
            "\n".join(
                [
                    f"## {case.contest.upper()} {case.year} {case.code}: `{case.slug}`",
                    "",
                    f"- Final question: {_markdown_cell(score.get('final_question', {}).get('plain_question'))}",
                    f"- v4-flash baseline job: `{flash_job}`; status: {_markdown_cell(flash_info.get('status'))}; raw: {_markdown_cell(flash_raw)}",
                    f"- v4-pro job: `{_markdown_cell(pro_job)}`; status: {_markdown_cell(pro_info.get('status'))}; raw: {_markdown_cell(pro_raw)}",
                    f"- v4-pro B-Eval vs v4-flash: {_markdown_cell(b_eval)}",
                    f"- v4-pro BO-Eval vs v4-flash-to-O: {_markdown_cell(bo_eval)}",
                    "",
                    _metric_table(score, flash_details, pro_details),
                ]
            )
        )

    mean = lambda values: sum(values) / len(values) if values else None
    content = "\n".join(
        [
            "# DeepSeek v4-pro vs v4-flash Baseline Evaluation",
            "",
            "This report treats the saved `terminus2-deepseek-v4-flash-current-*` jobs as the model baseline. "
            "Both models are rescored with the current final-question `score_config.json` panels.",
            "",
            "Definitions:",
            "- `raw_panel_score(model)` is the verifier's current final-question raw panel score for that model artifact.",
            "- `B-Eval vs flash = raw_panel_score(v4-pro) - raw_panel_score(v4-flash)`. Negative means v4-pro is worse than v4-flash on that task.",
            "- `BO-Eval vs flash = clamp((raw_panel_score(v4-pro) - raw_panel_score(v4-flash)) / (raw_panel_score(O) - raw_panel_score(v4-flash)), 0, 1)`. It is `N/A` when the flash baseline is already at or above the O reference on the raw panel.",
            "",
            f"- Total tasks: {len(builder.CASES)}",
            f"- v4-pro tasks with scoreable artifacts: {pro_found}",
            f"- Mean v4-flash raw panel score: {_markdown_cell(mean(flash_raw_values))}",
            f"- Mean v4-pro raw panel score: {_markdown_cell(mean(pro_raw_values))}",
            f"- Mean v4-pro B-Eval vs flash: {_markdown_cell(mean(b_eval_values))}",
            f"- Mean v4-pro BO-Eval vs flash: {_markdown_cell(mean(bo_eval_values))}",
            "",
            "## Summary",
            "",
            "| Contest | Year | Problem | Task | flash raw | pro raw | pro B-Eval vs flash | pro BO-Eval vs flash | O raw | flash covered | pro covered | flash status | pro status | pro job |",
            "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
            "\n".join(rows),
            "",
            "# Per-Task Details",
            "",
            "\n\n".join(sections),
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(content, encoding="utf-8")
    print(f"wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
