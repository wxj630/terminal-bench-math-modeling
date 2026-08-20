# -*- coding: utf-8 -*-
"""Write a compact task/answer summary for the current TB-MathModeling set."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

from local_scoring import score_job_artifact


REPO_ROOT = Path(__file__).resolve().parents[1]
JOBS_ROOT = REPO_ROOT / "jobs"
REPORT_PATH = REPO_ROOT / "docs" / "TASK_ANSWER_SUMMARY.md"


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


def _markdown(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        text = str(value).lower()
    elif isinstance(value, float):
        text = f"{value:.12g}"
    else:
        text = str(value)
    if text == "":
        return "N/A"
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def _shorten(text: str, limit: int = 120) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _as_float_or_none(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _get(data: Any, path: str) -> Any:
    cur = data
    token = ""
    i = 0
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
            cur = cur[int(path[i + 1:j])]
            i = j + 1
        else:
            token += ch
            i += 1
    if token:
        cur = cur[token]
    return cur


def _try_get(data: Any, path: str) -> tuple[bool, Any]:
    try:
        return True, _get(data, path)
    except (KeyError, IndexError, TypeError, ValueError):
        return False, None


def _score_config(case: Any) -> dict[str, Any]:
    return _read_json(REPO_ROOT / "tasks" / case.contest_dir / case.slug / "tests" / "score_config.json")


def _instruction_path(case: Any) -> Path:
    return REPO_ROOT / "tasks" / case.contest_dir / case.slug / "instruction.md"


def _subquestions(case: Any) -> list[tuple[str, str]]:
    text = _instruction_path(case).read_text(encoding="utf-8")
    rows: list[tuple[str, str]] = []
    seen: set[str] = set()
    for match in re.finditer(r"^\|\s*(Q\d+)\s*\|\s*([^|]+?)\s*\|", text, flags=re.MULTILINE):
        label = match.group(1)
        if label in seen:
            continue
        seen.add(label)
        rows.append((label, _shorten(match.group(2), 100)))
    if rows:
        return rows
    for match in re.finditer(r"^问题\s*([0-9一二三四五六七八九十]+)\s*(.+)$", text, flags=re.MULTILINE):
        label = f"问题{match.group(1)}"
        if label in seen:
            continue
        seen.add(label)
        rows.append((label, _shorten(match.group(2), 100)))
    return rows


def _job_name(case: Any) -> str:
    return f"terminus2-deepseek-v4-flash-current-{case.slug}"


def _job_info(
    job_name: str,
    score_config: dict[str, Any] | None = None,
    output_name: str | None = None,
) -> dict[str, Any]:
    result_path = JOBS_ROOT / job_name / "result.json"
    if not result_path.exists():
        return {"found": False, "status": "missing"}
    try:
        result = _read_json(result_path)
    except json.JSONDecodeError:
        return {"found": True, "status": "invalid result.json"}
    evals = result.get("stats", {}).get("evals", {})
    info: dict[str, Any] = {"found": True, "status": "finished"}
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
    details = _score_details(job_name, score_config, output_name)
    if details is not None:
        info["job_reward"] = details.get("reward")
    if info.get("n_errors"):
        info["status"] = "error: " + str(info.get("exceptions", "unknown"))
    elif details is not None:
        info["status"] = "scored"
    return info


def _score_details(
    job_name: str,
    score_config: dict[str, Any] | None = None,
    output_name: str | None = None,
) -> dict[str, Any] | None:
    if score_config is not None and output_name is not None:
        rescored = score_job_artifact(JOBS_ROOT, job_name, output_name, score_config)
        if rescored is not None:
            return rescored
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


def _job_artifact(case: Any) -> dict[str, Any] | None:
    job_dir = JOBS_ROOT / _job_name(case)
    if not job_dir.exists():
        return None
    paths = sorted(job_dir.glob(f"*/artifacts/root/results/{case.output_name}"))
    if not paths:
        return None
    try:
        return _read_json(paths[0])
    except json.JSONDecodeError:
        return None


def _eval_values(details: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(details, dict):
        return {}
    raw = _as_float_or_none(details.get("raw_panel_score"))
    baseline = _as_float_or_none(details.get("baseline_panel_score"))
    selected = _as_float_or_none(details.get("reward"))
    b_eval = details.get("b_eval")
    bo_eval = details.get("bo_eval")
    b_reward = _as_float_or_none(b_eval.get("reward")) if isinstance(b_eval, dict) else None
    bo_reward = _as_float_or_none(bo_eval.get("reward")) if isinstance(bo_eval, dict) else None
    if b_reward is None and raw is not None and baseline is not None:
        b_reward = raw - baseline
    if bo_reward is None:
        bo_reward = selected
    return {
        "selected_reward": selected,
        "b_eval_reward": b_reward,
        "bo_eval_reward": bo_reward,
        "raw_panel_score": raw,
        "baseline_panel_score": baseline,
        "scoreable_count": details.get("scoreable_count"),
    }


def _direction_label(direction: Any, scored: bool) -> str:
    mapping = {
        "higher_is_better": "越高越好",
        "lower_is_better": "越低越好",
        "closeness_to_outstanding": "越接近 verifier/O奖值越好",
        "exact_value": "精确值；不计分",
        "unscored_missing_baseline": "缺 baseline；不计分",
        "missing_baseline": "缺 baseline；不计分",
    }
    text = str(direction or "closeness_to_outstanding")
    label = mapping.get(text, text)
    if not scored and "不计分" not in label:
        label += "；不计分"
    return label


def _metric_detail_map(details: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(details, dict):
        return {}
    metrics = details.get("metrics", [])
    if not isinstance(metrics, list):
        return {}
    return {
        str(item.get("path")): item
        for item in metrics
        if isinstance(item, dict) and item.get("path") is not None
    }


def _actual_value(case: Any, path: str, detail: dict[str, Any], artifact: dict[str, Any] | None) -> Any:
    if detail.get("found") and "actual" in detail:
        return detail.get("actual")
    if isinstance(artifact, dict):
        found, value = _try_get(artifact, path)
        if found:
            return value
    return None


def _scored(metric: dict[str, Any], detail: dict[str, Any]) -> bool:
    if detail.get("unscored"):
        return False
    weight = detail.get("score_weight", metric.get("score_weight", metric.get("weight", 1.0)))
    try:
        return float(weight) > 0.0
    except (TypeError, ValueError):
        return False


def _task_anchor(case: Any) -> str:
    return f"{case.contest}-{case.year}-{case.code.lower()}"


def _write_task_section(case: Any, score: dict[str, Any]) -> str:
    subqs = _subquestions(case)
    job_name = _job_name(case)
    job_info = _job_info(job_name, score, case.output_name)
    details = _score_details(job_name, score, case.output_name)
    detail_by_path = _metric_detail_map(details)
    artifact = _job_artifact(case)
    evals = _eval_values(details)
    final_question = score.get("final_question", {})
    metric_items = [item for item in score.get("metrics", []) if isinstance(item, dict)]
    aligned_actual_count = 0
    for metric in metric_items:
        path = str(metric.get("path", ""))
        actual = _actual_value(case, path, detail_by_path.get(path, {}), artifact)
        if actual is not None:
            aligned_actual_count += 1
    q_lines = [f"- {label}: {text}" for label, text in subqs]
    if not q_lines:
        q_lines = ["- N/A: 当前 instruction 未抽取出显式子问题。"]
    rows = [
        "| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |",
        "|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for index, metric in enumerate(metric_items, 1):
        path = str(metric.get("path", ""))
        detail = detail_by_path.get(path, {})
        scored = _scored(metric, detail)
        direction = detail.get("direction", metric.get("direction", "closeness_to_outstanding"))
        rows.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"`{_markdown(path)}`",
                    _direction_label(direction, scored),
                    _markdown(metric.get("outstanding_value", metric.get("oracle_value"))),
                    _markdown(metric.get("baseline_value")),
                    _markdown(_actual_value(case, path, detail, artifact)),
                    _markdown(detail.get("reward")),
                    "是" if scored else "否",
                ]
            )
            + " |"
        )
    return "\n".join(
        [
            f"## {case.title}",
            "",
            f"- Task slug: `{case.slug}`",
            f"- 简洁任务描述: {case.title}",
            f"- 最后评测问题: {_markdown(final_question.get('plain_question'))}",
            f"- final answer: {_markdown(final_question.get('final_answer_summary'))}",
            f"- baseline模型: {_markdown(final_question.get('baseline_model_summary'))}",
            *([f"- 备注: {_markdown(final_question.get('note'))}"] if final_question.get("note") else []),
            f"- 当前 instruction 子问题数: {len(subqs)}",
            f"- 最后答案数值项: {score.get('scored_final_answer_numeric_field_count', score.get('effective_metric_count'))} 个计分 / {score.get('final_answer_numeric_field_count', score.get('metric_count'))} 个总项",
            f"- 评分版本: `{score.get('scoring_version')}`",
            f"- v4-flash job: `{job_name}`; 状态: {_markdown(job_info.get('status'))}; 当前口径 reward: {_markdown(evals.get('selected_reward'))}",
            f"- v4-flash B-Eval: {_markdown(evals.get('b_eval_reward'))}; BO-Eval: {_markdown(evals.get('bo_eval_reward'))}; raw panel score: {_markdown(evals.get('raw_panel_score'))}",
            f"- v4-flash 对齐 verifier metric path 的答案覆盖: {aligned_actual_count}/{len(metric_items)}",
            "",
            "子问题:",
            *q_lines,
            "",
            "Verifier/O 答案与 v4-flash 答案:",
            "",
            "\n".join(rows),
        ]
    )


def main() -> None:
    builder = _load_builder()
    summary_rows: list[str] = []
    sections: list[str] = []
    for case in builder.CASES:
        score = _score_config(case)
        subqs = _subquestions(case)
        details = _score_details(_job_name(case), score, case.output_name)
        evals = _eval_values(details)
        job_info = _job_info(_job_name(case), score, case.output_name)
        final_question = score.get("final_question", {})
        summary_rows.append(
            "| "
            + " | ".join(
                [
                    case.contest.upper(),
                    str(case.year),
                    case.code,
                    f"[`{case.slug}`](#{_task_anchor(case)})",
                    _markdown(case.title),
                    _markdown(_shorten(str(final_question.get("plain_question", "")), 70)),
                    str(len(subqs)),
                    str(score.get("scored_final_answer_numeric_field_count", score.get("effective_metric_count"))),
                    _markdown(job_info.get("status")),
                    _markdown(evals.get("b_eval_reward")),
                    _markdown(evals.get("bo_eval_reward")),
                ]
            )
            + " |"
        )
        sections.append(f'<a id="{_task_anchor(case)}"></a>\n\n' + _write_task_section(case, score))
    content = "\n".join(
        [
            "# TB-MathModeling 任务与答案汇总",
            "",
            "本文档汇总当前 18 道题：3 年 x 2 个竞赛 x A/B/C 三题。",
            "",
            "口径说明:",
            "- 当前 verifier 只看最后一问的数值核心；如果最后一问本身是备忘录或文字建议，就使用支撑该建议的最后可量化答案。",
            "- `最后答案数值项` 不是全题所有数字，而是表达 final answer 所需的少量核心数字；有些最终答案天然是一个向量或几种情景结果，所以会有 2-6 个数值项。",
            "- `Verifier/O answer` 是 verifier 使用的数值答案，来自 O 奖论文复现结果；它不是数学建模问题唯一可能的正确答案。",
            "- `Baseline answer = N/A` 不表示没有 baseline；它表示当前 baseline 结果没有和该 final answer 同语义的逐项字段，评分仍会用该题的 baseline panel score，不强行把无关数字凑成端点。",
            "- 方向标签来自 `score_config.json`：有真实 baseline-to-outstanding 端点时标为 `越高越好` / `越低越好`；legacy fallback 指标没有逐指标 baseline 方向，因此标为 `越接近 verifier/O奖值越好`。",
            "- `v4-flash answer` 来自当前 `terminus2-deepseek-v4-flash-current-*` jobs，并用当前 `score_config.json` 对保存下来的 artifact 重新计分；`N/A` 表示没有找到该路径下的答案。",
            "- 当前默认 benchmark reward 是 `B-Eval`；本文档会用当前 `score_config.json` 对已有 artifact 重新计分，并同时列出 `BO-Eval`。",
            "",
            "## 总览",
            "",
            "| 竞赛 | 年份 | 题号 | Task | 简洁描述 | 最后评测问题 | 子问题数 | 最后答案数值项 | v4-flash 状态 | v4 B-Eval | v4 BO-Eval |",
            "|---|---:|---|---|---|---|---:|---:|---|---:|---:|",
            "\n".join(summary_rows),
            "",
            "# 分题表格",
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
