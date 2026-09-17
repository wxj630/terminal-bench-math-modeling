#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 2023-2025 all-model BO-Eval report and AA-style figures."""

from __future__ import annotations

import importlib.util
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from feasibility_checks import validate_artifact


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
JOBS = ROOT / "jobs"
FIGURES = JOBS / "figures"
REPORT_PATH = JOBS / "terminus2-direction-aware-flash-baseline-bbo-2023-2025.md"

# Figure naming/selection. The text-only board keeps the historical prefix; the
# multimodal board re-runs the same renderers with its own prefix and a narrowed
# model set, so both boards are guaranteed to share one drawing implementation.
FIGURE_PREFIX = "aa-style-2023-2025"
#: When non-empty, only these summary labels are drawn (charts only; the report,
#: token audit and feasibility audit still cover every registered model).
SUMMARY_FILTER: set[str] = set()
PRICE_SNAPSHOT_PATH = JOBS / "openrouter-pricing-used-2023-2025.json"
TOKEN_AUDIT_PATH = JOBS / "model-token-audit-2023-2025.json"
FEASIBILITY_AUDIT_PATH = JOBS / "terminus2-all-model-feasibility-audit-2023-2025.md"

BO_DENOM_EPS = 1e-12
ROBUST_GAP_FLOOR = 0.10
ROBUST_SATURATED_GAIN_CLIP = 0.10
ROBUST_RATIO_CLIP = 1.0
ROBUST_FAILURE_SCORE = -1.0
OPENROUTER_MODELS_API = "https://openrouter.ai/api/v1/models"
OPENROUTER_USD_TO_RMB = 6.737012
HARD_GATE_O_RAW = 0.0
MANUAL_HARD_GATES = {
    (
        "glm",
        "cumcm-2023-a-heliostat-field",
    ): "explicit Q3 design note violates heliostat installation-height bound: one tail mirror uses z=1.9024 m, below the required 2 m minimum",
    (
        "oxalpha",
        "cumcm-2025-a-smoke-screen",
    ): "independent smoke-screen replay gives 0.00s coverage under O-reference line-of-sight geometry",
    (
        "kimi",
        "mcm-2025-b-juneau-tourism",
    ): "unit/scale invalid: resident_acceptance_index=1.5 and sustainability_score=232.2 on a unit-scale score",
    (
        "kimi",
        "mcm-2025-c-olympic-medals",
    ): "invalid high coach-effect result: only three scored recommendations and endpoint verifier reward is negative/BO 0",
}


def openrouter_rmb_per_mtok(usd_per_token: str | float) -> float:
    return float(usd_per_token) * 1_000_000.0 * OPENROUTER_USD_TO_RMB


def openrouter_price_map(pricing: dict[str, Any]) -> dict[str, float | None]:
    def convert(key: str) -> float | None:
        value = pricing.get(key)
        if value is None:
            return None
        try:
            return openrouter_rmb_per_mtok(value)
        except (TypeError, ValueError):
            return None

    return {
        "input_uncached": convert("prompt"),
        "input_cached": convert("input_cache_read"),
        "explicit_cache_create": convert("input_cache_write"),
        "output": convert("completion"),
    }


def apply_openrouter_catalog_prices(models: dict[str, dict[str, Any]]) -> None:
    """Refresh prices from OpenRouter's public model catalog; keep local fallback on failure."""
    for meta in models.values():
        if meta.get("omit_cost"):
            meta["price_source"] = "cost omitted"
            continue
        meta["price_source"] = "user-supplied fixed snapshot" if meta.get("fixed_price") else "local fallback"
    try:
        request = Request(OPENROUTER_MODELS_API, headers={"User-Agent": "terminal-bench-math-modeling-price-refresh/1.0"})
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, HTTPError, URLError, json.JSONDecodeError):
        return

    catalog = {item.get("id"): item for item in payload.get("data", []) if isinstance(item, dict)}
    snapshot: dict[str, Any] = {"source": OPENROUTER_MODELS_API, "usd_to_rmb": OPENROUTER_USD_TO_RMB, "models": {}}
    for key, meta in models.items():
        if meta.get("omit_cost"):
            snapshot["models"][key] = {
                "model_id": meta.get("openrouter_model"),
                "name": meta.get("label"),
                "raw_pricing_usd_per_token": None,
                "price_rmb_per_mtok": {},
                "note": meta.get("price_note", "cost omitted"),
            }
            continue
        if meta.get("fixed_price"):
            snapshot["models"][key] = {
                "model_id": meta.get("openrouter_model"),
                "name": meta.get("label"),
                "raw_pricing_usd_per_token": None,
                "price_rmb_per_mtok": meta.get("price_rmb_per_mtok", {}),
                "note": meta.get("price_note", "user-supplied fixed price"),
            }
            continue
        model_id = meta.get("openrouter_model")
        item = catalog.get(model_id)
        if not item:
            continue
        pricing = item.get("pricing")
        if not isinstance(pricing, dict):
            continue
        refreshed = openrouter_price_map(pricing)
        price = dict(meta.get("price_rmb_per_mtok", {}))
        for field, value in refreshed.items():
            if value is not None:
                price[field] = value
        meta["price_rmb_per_mtok"] = price
        meta["price_source"] = "OpenRouter live"
        meta["openrouter_name"] = item.get("name") or model_id
        snapshot["models"][key] = {
            "model_id": model_id,
            "name": meta["openrouter_name"],
            "raw_pricing_usd_per_token": pricing,
            "price_rmb_per_mtok": price,
        }
    try:
        PRICE_SNAPSHOT_PATH.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    except OSError:
        pass


def load_base() -> Any:
    sys.path.insert(0, str(SCRIPTS))
    path = SCRIPTS / "write_direction_aware_flash_baseline_eval_2024_2025.py"
    spec = importlib.util.spec_from_file_location("direction_eval_2024_2025", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def model_config(builder: Any) -> dict[str, dict[str, Any]]:
    models: dict[str, dict[str, Any]] = {
        "flash": {
            "label": "v4 flash baseline",
            "short": "DeepSeek V4 Flash",
            "template": "terminus2-deepseek-v4-flash-0731-rerun-2023-2025-{contest}",
            "color": "#2f80ed",
            "openrouter_model": "deepseek/deepseek-v4-flash-0731",
            "provenance": "4-hour rerun jobs: terminus2-deepseek-v4-flash-0731-rerun-2023-2025-cumcm and terminus2-deepseek-v4-flash-0731-rerun-2023-2025-mcm",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.00000006"),
                "input_cached": openrouter_rmb_per_mtok("0.000000012"),
                "output": openrouter_rmb_per_mtok("0.00000012"),
            },
        },
        "flash_opencode": {
            "label": "opencode + deepseek-flash",
            "short": "DeepSeek Flash (opencode)",
            "template": "opencode-deepseek-flash-2023-2025-{contest}",
            # Tasks whose only scoreable artifact came from a later recovery job
            # (environment failures: install timeout / apt flake / stream hang / reboot).
            "artifact_job_overrides": {
                "cumcm-2023-a-heliostat-field": "opencode-deepseek-flash-helio-retry3",
                "cumcm-2023-c-vegetable-pricing": "opencode-deepseek-flash-cumcm-retry",
                "cumcm-2024-a-dragon-dance": "opencode-deepseek-flash-cumcm-retry",
                "cumcm-2025-a-smoke-screen": "opencode-deepseek-flash-cumcm-retry",
                "mcm-2025-b-juneau-tourism": "opencode-deepseek-flash-mcm-retry",
                # Artifact recovered after a filename typo (hyphen vs the required
                # underscore); the latest attempt's scripts were replayed to
                # reproduce it and rescored with the task verifier.
                "mcm-2024-a-lamprey": "opencode-deepseek-flash-mcm-retry",
            },
            "color": "#00897b",
            "openrouter_model": "deepseek/deepseek-v4.1-flash",
            "price_rmb_per_mtok": {
                # DeepSeek V4.1 Flash is priced at 2x during weekday UTC windows
                # 100-400 and 600-1000. OpenRouter's catalog exposes the PEAK rate
                # as the base `prompt`/`completion` price and the off-peak rate as
                # an override, so the quoted base is already the peak: no extra
                # multiplier is applied here (doing so double-counts the peak).
                # Its reasoning counter is additive
                # (total == input + output + reasoning + cache_read, verified per
                # step across every trial), so reasoning is billed on top.
                "billing": {"peak_multiplier": 1.0, "reasoning_is_additive": True},
            },
            "provenance": "opencode CLI agent jobs run 2026-09-11: opencode-deepseek-flash-2023-2025-cumcm and opencode-deepseek-flash-2023-2025-mcm (model openai/deepseek-flash via api.deepseek.com)",
        },
        "flash_opencode_max": {
            "label": "opencode + deepseek-flash (max)",
            "short": "DeepSeek Flash max (opencode)",
            "template": "opencode-deepseek-flash-max-{contest}",
            # Same agent/model as flash_opencode, but run with
            # `--agent-kwarg variant=max` (DeepSeek thinking effort = max, one notch
            # above the default `high`). Kept as a separate entry so the two tiers
            # can be compared directly.
            "artifact_job_overrides": {},
            "color": "#00695c",
            "openrouter_model": "deepseek/deepseek-v4.1-flash",
            "price_rmb_per_mtok": {
                "billing": {"peak_multiplier": 1.0, "reasoning_is_additive": True},
            },
            "provenance": "opencode CLI agent jobs run 2026-09-15: opencode-deepseek-flash-max-cumcm and opencode-deepseek-flash-max-mcm (model openai/deepseek-flash via api.deepseek.com, --variant max)",
        },
        "codex_gpt55_xhigh": {
            "label": "codex + gpt-5.5 xhigh",
            "short": "GPT-5.5 xhigh (codex)",
            "template": "codex-gpt55-xhigh-2023-2025-{contest}",
            "artifact_job_overrides": {},
            "color": "#000000",
            "openrouter_model": "openai/gpt-5.5",
            "price_rmb_per_mtok": {
                # OpenAI reports output_tokens already including reasoning, and
                # its >272k-token long-context tier was never reached (max single
                # request observed 219,735), so the base rate applies.
                "billing": {"peak_multiplier": 1.0, "reasoning_is_additive": False},
            },
            "provenance": "codex CLI agent jobs run 2026-09-12: codex-gpt55-xhigh-2023-2025-cumcm and codex-gpt55-xhigh-2023-2025-mcm (model gpt-5.5, reasoning_effort=xhigh, via CLIPROXY)",
        },
        "pro": {
            "label": "v4 pro",
            "short": "DeepSeek V4 Pro",
            "template": "terminus2-deepseek-v4-pro-current-{slug}",
            "color": "#2945d9",
            "openrouter_model": "deepseek/deepseek-v4-pro",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.00000087"),
                "input_cached": openrouter_rmb_per_mtok("0.0000000725"),
                "output": openrouter_rmb_per_mtok("0.00000174"),
            },
        },
        "glm": {
            "label": "GLM-5.3",
            "short": "GLM-5.3",
            "template": "terminus2-glm-5.3-key2-{contest}",
            "color": "#6f6f6f",
            "openrouter_model": "z-ai/glm-5.3",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.0000014"),
                "input_cached": openrouter_rmb_per_mtok("0.00000026"),
                "output": openrouter_rmb_per_mtok("0.0000044"),
            },
        },
        "gpt": {
            "label": "GPT-5.6 SOL high",
            "short": "GPT-5.6 Sol",
            "template": "terminus2-gpt-5.6-sol-high-2024-2025-{contest}-retryproxy",
            "artifact_job_overrides": {},
            "color": "#202020",
            "openrouter_model": "openai/gpt-5.6-sol",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.000002"),
                "input_cached": openrouter_rmb_per_mtok("0.0000002"),
                "output": openrouter_rmb_per_mtok("0.00001"),
            },
        },
        "gptx": {
            "label": "GPT-5.6 SOL xhigh",
            "short": "GPT-5.6 Sol XH",
            "template": "terminus2-gpt-5.6-sol-xhigh-2023-2025-{contest}-retryproxy",
            # The monitored single-task retries supersede the original xhigh
            # trials for these two cells: crop planting produced a scoreable
            # artifact, while heliostat field ended in the final 2h timeout.
            "artifact_job_overrides": {
                "cumcm-2024-c-crop-planting": "terminus2-gpt-5.6-sol-xhigh-1h-retry3-crop-20260908",
                "cumcm-2023-a-heliostat-field": "terminus2-gpt-5.6-sol-xhigh-2h-resume-helio-20260909",
                "mcm-2023-b-maasai-mara": "terminus2-gpt-5.6-sol-xhigh-1h-retry2-maasai-20260908",
            },
            "color": "#0f766e",
            "openrouter_model": "openai/gpt-5.6-sol",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.000002"),
                "input_cached": openrouter_rmb_per_mtok("0.0000002"),
                "output": openrouter_rmb_per_mtok("0.00001"),
            },
        },
        "kimi": {
            "label": "Kimi K3",
            "short": "Kimi K3",
            "template": "terminus2-kimi-k3-2024-2025-{contest}-retryproxy",
            "artifact_job_overrides": {},
            "color": "#1f83ff",
            "openrouter_model": "moonshotai/kimi-k3",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.000003"),
                "input_cached": openrouter_rmb_per_mtok("0.0000003"),
                "output": openrouter_rmb_per_mtok("0.000015"),
            },
        },
        "gemini37flash": {
            "label": "Gemini 3.7 Flash high primary+retry",
            "short": "Gemini 3.7 Flash",
            "template": "terminus2-gemini-3.7-flash-high-2024-2025-{contest}-retryproxy",
            "artifact_job_overrides": {
                "cumcm-2025-a-smoke-screen": "terminus2-gemini-3.7-flash-high-2024-2025-cumcm-smoke-retry",
            },
            "color": "#34a853",
            "openrouter_model": "google/gemini-3.7-flash",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.000000375"),
                "input_cached": openrouter_rmb_per_mtok("0.0000000375"),
                "output": openrouter_rmb_per_mtok("0.000001875"),
            },
        },
        "qwen": {
            "label": "Qwen3.8-27B-FP8 thinking",
            "short": "Qwen3.8 27B",
            "template": "terminus2-qwen3-8-27b-fp8-h800-thinking-2024-2025-{contest}-retryproxy",
            "artifact_job_overrides": {},
            "color": "#7c3aed",
            "openrouter_model": "qwen/qwen3.8-27b",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.000000425"),
                "input_cached": openrouter_rmb_per_mtok("0.000000085"),
                "explicit_cache_create": openrouter_rmb_per_mtok("0.00000053125"),
                "output": openrouter_rmb_per_mtok("0.00000255"),
            },
        },
        "oxalpha": {
            "label": "GLM-5.3-Flash (ox-alpha)",
            "short": "GLM-5.3-Flash",
            "template": "terminus2-openrouter-ox-alpha-2023-2025-{contest}-retryproxy",
            "artifact_job_overrides": {},
            "color": "#f59e0b",
            "openrouter_model": "z-ai/glm-5.3-flash",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.000000075"),
                "input_cached": openrouter_rmb_per_mtok("0.000000015"),
                "output": openrouter_rmb_per_mtok("0.00000025"),
            },
            "price_note": "User-supplied fixed snapshot",
            "fixed_price": True,
        },
        "qwenflash": {
            "label": "Qwen3.8 Flash (Bailian)",
            "short": "Qwen3.8 Flash",
            "template": "terminus2-openrouter-bailian-qwen3.8-flash-2023-2025-{contest}",
            "artifact_job_overrides": {},
            "color": "#0f766e",
            "openrouter_model": "qwen/qwen3.8-flash",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.00000015"),
                "input_cached": openrouter_rmb_per_mtok("0.000000016"),
                "explicit_cache_create": openrouter_rmb_per_mtok("0.00000020"),
                "output": openrouter_rmb_per_mtok("0.00000047"),
            },
            "price_note": "User-supplied fixed snapshot",
            "fixed_price": True,
        },
        "hy4": {
            "label": "Tencent Hy4 Preview",
            "short": "Hy4 Preview",
            "template": "terminus2-tencent-hy4-preview-2023-2025-{contest}",
            "artifact_job_overrides": {},
            "color": "#dc2626",
            "openrouter_model": "tencent/hy4-preview",
            "price_rmb_per_mtok": {
                "input_uncached": openrouter_rmb_per_mtok("0.000000834"),
                "input_cached": openrouter_rmb_per_mtok("0.000000042"),
                "output": openrouter_rmb_per_mtok("0.000002501"),
            },
        },
    }
    for case in builder.CASES:
        if case.year != 2023:
            continue
        for model in ("gpt", "kimi", "gemini37flash", "qwen"):
            template = str(models[model]["template"]).replace("2024-2025", "2023")
            models[model]["artifact_job_overrides"][case.slug] = template.format(
                contest=case.contest,
                slug=case.slug,
            )
    apply_openrouter_catalog_prices(models)
    return models


@dataclass
class Summary:
    model: str
    label: str
    short: str
    artifacts: int
    bo_defined_tasks: int
    raw_mean: float | None
    o_mean: float | None
    b_mean: float | None
    effect_mean: float | None
    bo_mean: float | None
    input_tokens: int
    cache_tokens: int
    raw_cache_tokens: int
    output_tokens: int
    #: Reasoning tokens the provider reports outside ``output_tokens`` (0 when the
    #: provider already folds reasoning into its completion counter).
    reasoning_tokens: int
    billable_input_tokens: int
    cost_rmb: float | None
    cost_usd: float | None
    cache_hit_rate: float | None
    cache_imputed_from_peer_avg: bool
    hard_gate_count: int
    hard_gated_raw_mean: float | None
    hard_gated_o_mean: float | None
    hard_gated_effect_mean: float | None
    canonical_tasks: int
    valid_tasks: int
    running_tasks: int
    error_tasks: int
    pending_tasks: int
    excluded_retry_trials: int

    @property
    def color(self) -> str:
        return MODELS[self.model]["color"]

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


MODELS: dict[str, dict[str, Any]] = {}


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def cell(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        if not math.isfinite(value):
            return "N/A"
        return f"{value:.6f}"
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def int_cell(value: int | None) -> str:
    return "N/A" if value is None else f"{value:,}"


def pp_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100.0:+.2f} pp"


def pct_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100.0:.2f}%"


def money_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"¥{value:,.2f}"


def usd_money_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"${value:,.6f}"


def price_cell(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"¥{value:.4f}/M"


def bo_defined(record: dict[str, Any]) -> bool:
    flash_raw = record["raw"].get("flash")
    oracle_raw = record.get("oracle_raw")
    return flash_raw is not None and oracle_raw is not None and oracle_raw - flash_raw > BO_DENOM_EPS


def bo_eval(model_raw: float | None, flash_raw: float | None, oracle_raw: float | None) -> float | None:
    if model_raw is None or flash_raw is None or oracle_raw is None:
        return None
    denom = oracle_raw - flash_raw
    if denom <= BO_DENOM_EPS:
        return None
    return max(0.0, (model_raw - flash_raw) / denom)


def o_eval(model_raw: float | None, oracle_raw: float | None) -> float | None:
    if model_raw is None or oracle_raw is None or abs(oracle_raw) <= BO_DENOM_EPS:
        return None
    return min(1.0, max(0.0, model_raw / oracle_raw))


def clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def robust_effect(
    model_raw: float | None,
    flash_raw: float | None,
    oracle_raw: float | None,
    *,
    failure: bool = False,
) -> float | None:
    """Main Robust BO-Eval metric with small-denominator and outlier clipping."""
    if failure:
        return ROBUST_FAILURE_SCORE
    if model_raw is None or flash_raw is None:
        return None
    gain = model_raw - flash_raw
    if oracle_raw is None:
        return clamp(gain, -ROBUST_SATURATED_GAIN_CLIP, ROBUST_SATURATED_GAIN_CLIP)
    gap = oracle_raw - flash_raw
    if gap <= BO_DENOM_EPS or gap < ROBUST_GAP_FLOOR:
        return clamp(gain, -ROBUST_SATURATED_GAIN_CLIP, ROBUST_SATURATED_GAIN_CLIP)
    return clamp(gain / gap, -ROBUST_RATIO_CLIP, ROBUST_RATIO_CLIP)


def hard_gate_reason(model: str, task_slug: str, details: dict[str, Any] | None) -> str | None:
    """Return a whole-task hard-gate reason for clearly non-feasible cells only."""
    manual_reason = MANUAL_HARD_GATES.get((model, task_slug))
    if manual_reason is not None:
        return manual_reason
    if details is None:
        return None
    artifact_path = details.get("artifact_path")
    try:
        data = json.loads(Path(artifact_path).read_text(encoding="utf-8"))
    except (TypeError, OSError, json.JSONDecodeError):
        data = None
    if isinstance(data, dict):
        validation = validate_artifact(data, task_slug)
        if validation.get("hard_errors"):
            return (
                f"{validation.get('status', 'hard-invalid')}: "
                f"{validation.get('evidence', 'shared feasibility check found a hard constraint violation')}"
            )
    invalid_metrics = [
        str(item.get("path", "unknown"))
        for item in details.get("metrics", [])
        if not item.get("excluded") and item.get("invalid_reason")
    ]
    if not invalid_metrics:
        return None
    # The lamprey score config compares raw population-scale O-paper fields
    # with model-specific normalized indices. This shared metric-contract
    # mismatch is not evidence that every ecosystem model violates a
    # biological boundary. Keep the metric warning in the audit, but do not
    # turn it into a whole-task feasibility penalty.
    if task_slug == "mcm-2024-a-lamprey":
        return None
    sample = ", ".join(invalid_metrics[:2])
    if len(invalid_metrics) > 2:
        sample += f", +{len(invalid_metrics) - 2} more"
    return f"score-config hard-invalid metric(s): {sample}"


def fallback_effect(model_raw: float | None, flash_raw: float | None, oracle_raw: float | None) -> float | None:
    """Legacy main effect metric kept for comparison/debugging."""
    if model_raw is None or flash_raw is None:
        return None
    b_eval = model_raw - flash_raw
    if oracle_raw is not None and oracle_raw - flash_raw > BO_DENOM_EPS and b_eval >= 0.0:
        return b_eval / (oracle_raw - flash_raw)
    return b_eval


def model_job_names(base: Any, model: str, cases: list[Any]) -> list[str]:
    seen: set[str] = set()
    names: list[str] = []
    for case in cases:
        for name in base._job_names(model, case):
            if name not in seen:
                seen.add(name)
                names.append(name)
    return names


def _billing_rate(price: dict[str, Any], metal: str) -> float | None:
    """Return the rate for ``metal`` (input_uncached/input_cached/output).

    ``billing.peak_multiplier`` exists because some providers (DeepSeek V4.1
    Flash) charge a higher rate during set UTC windows; the board quotes the
    peak rate so a run is never under-costed.
    """
    rate = price.get(metal)
    if rate is None:
        return None
    billing = price.get("billing")
    if isinstance(billing, dict):
        multiplier = billing.get("peak_multiplier")
        if multiplier:
            rate = float(rate) * float(multiplier)
    return float(rate)


def estimate_model_cost(
    model: str,
    input_tokens: int,
    cache_tokens: int,
    output_tokens: int,
    reasoning_tokens: int = 0,
) -> float | None:
    price = MODELS[model].get("price_rmb_per_mtok", {})
    if not isinstance(price, dict):
        return None
    input_price = _billing_rate(price, "input_uncached")
    cached_price = _billing_rate(price, "input_cached")
    output_price = _billing_rate(price, "output")
    if input_price is None or output_price is None:
        return None
    billing = price.get("billing") if isinstance(price.get("billing"), dict) else {}
    billable_output = output_tokens
    if billing.get("reasoning_is_additive"):
        # The provider reports reasoning outside its completion counter, so it is
        # billed on top of the answer tokens rather than being a breakdown of them.
        billable_output += reasoning_tokens
    billable_input_tokens = max(0, input_tokens - cache_tokens)
    cost = billable_input_tokens / 1_000_000.0 * input_price
    if cached_price is not None:
        cost += cache_tokens / 1_000_000.0 * cached_price
    cost += billable_output / 1_000_000.0 * output_price
    return cost


def estimate_model_cost_usd(
    model: str,
    input_tokens: int,
    cache_tokens: int,
    output_tokens: int,
    reasoning_tokens: int = 0,
) -> float | None:
    cost_rmb = estimate_model_cost(model, input_tokens, cache_tokens, output_tokens, reasoning_tokens)
    return None if cost_rmb is None else cost_rmb / OPENROUTER_USD_TO_RMB


def _reasoning_tokens_from_stream(trial_dir: Path) -> int:
    """Sum reasoning tokens the agent billed outside its completion counter.

    Provider accounting differs and this matters for cost:

    * OpenAI Responses (codex/gpt-5.5) reports ``output_tokens`` that already
      *include* reasoning, so nothing is added here.
    * OpenCode + OpenRouter (deepseek) reports reasoning as its own counter:
      ``total == input + output + reasoning + cache_read`` (verified on every
      step of every trial), so reasoning is additive and must be billed.

    Only ``agent/opencode.txt`` carries the separate counter, so reading it is
    enough to recover the additive amount; the billing rule itself lives in the
    per-model ``billing`` config.
    """
    stream = trial_dir / "agent" / "opencode.txt"
    if not stream.exists():
        return 0
    total = 0
    try:
        handle = stream.open(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    with handle:
        for line in handle:
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "step_finish":
                continue
            tokens = (event.get("part") or {}).get("tokens") or {}
            total += int(tokens.get("reasoning") or 0)
    return total


def _trial_tokens(trial_dir: Path, data: dict[str, Any] | None) -> tuple[int, int, int, int]:
    """Read final trial counters plus additive reasoning tokens.

    Returns ``(input, cache, output, reasoning_extra)`` where ``reasoning_extra``
    is the amount that must be billed on top of ``output`` (0 when the provider
    already folds it into ``output``).
    """
    agent_result = data.get("agent_result") if isinstance(data, dict) else None
    if isinstance(agent_result, dict):
        values = (
            int(agent_result.get("n_input_tokens") or 0),
            int(agent_result.get("n_cache_tokens") or 0),
            int(agent_result.get("n_output_tokens") or 0),
        )
        if any(values):
            return (*values, _reasoning_tokens_from_stream(trial_dir))
    trajectory = trial_dir / "agent" / "trajectory.json"
    try:
        payload = json.loads(trajectory.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0, 0, 0, 0
    metrics = payload.get("final_metrics") if isinstance(payload, dict) else None
    if not isinstance(metrics, dict):
        return 0, 0, 0, 0
    return (
        int(metrics.get("total_prompt_tokens") or 0),
        int(metrics.get("total_cached_tokens") or 0),
        int(metrics.get("total_completion_tokens") or 0),
        _reasoning_tokens_from_stream(trial_dir),
    )


def _trial_candidate(base: Any, model: str, case: Any, result_path: Path, source: str) -> dict[str, Any]:
    try:
        data = base._read_json(result_path)
    except Exception:
        data = None
    if not isinstance(data, dict):
        data = {}
    trial_dir = result_path.parent
    exception = data.get("exception_info")
    verifier = data.get("verifier_result")
    rewards = verifier.get("rewards") if isinstance(verifier, dict) else None
    reward = rewards.get("reward") if isinstance(rewards, dict) else None
    artifact_dir = trial_dir / "artifacts"
    artifact_path = artifact_dir / "root" / "results" / case.output_name
    artifact = artifact_dir.is_dir() and any(path.is_file() for path in artifact_dir.rglob("*"))
    input_tokens, cache_tokens, output_tokens, reasoning_tokens = _trial_tokens(trial_dir, data)
    finished = bool(data.get("finished_at"))
    valid = artifact and exception is None and reward is not None
    running = not valid and exception is None and not finished and any((input_tokens, cache_tokens, output_tokens))
    return {
        "trial_id": trial_dir.name,
        "path": str(trial_dir),
        "source": source,
        "valid": valid,
        "running": running,
        "finished": finished,
        "artifact": artifact,
        "reward": reward,
        "exception_type": exception.get("exception_type") if isinstance(exception, dict) else None,
        "input_tokens": input_tokens,
        "cache_tokens": cache_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
    }


def _candidate_trials(base: Any, model: str, case: Any) -> list[dict[str, Any]]:
    """Collect only this model and this task; archives are included for retry auditability."""
    expected_jobs = model_job_names(base, model, [case])
    roots: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for job_name in expected_jobs:
        for root in [JOBS / job_name, *JOBS.joinpath(".failed-archives").glob(f"**/{job_name}")]:
            if not root.is_dir() or root in seen:
                continue
            seen.add(root)
            roots.append((root, "archive-job" if ".failed-archives" in root.parts else "job"))
    candidates: list[dict[str, Any]] = []
    for root, source in roots:
        for trial_dir in sorted(root.iterdir()):
            if not trial_dir.is_dir() or not trial_dir.name.startswith(case.slug + "__"):
                continue
            result_path = trial_dir / "result.json"
            trajectory_path = trial_dir / "agent" / "trajectory.json"
            if not result_path.exists() and not trajectory_path.exists():
                continue
            candidates.append(_trial_candidate(base, model, case, result_path, source))

    # Manually preserved failed/resumed trials may be direct archive children rather than a job directory.
    target_model = "openai/" + str(MODELS[model].get("openrouter_model", ""))
    for trial_dir in JOBS.joinpath(".failed-archives").glob(f"**/{case.slug}__*"):
        config_path = trial_dir / "config.json"
        result_path = trial_dir / "result.json"
        trajectory_path = trial_dir / "agent" / "trajectory.json"
        if not (result_path.exists() or trajectory_path.exists()) or not config_path.exists():
            continue
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        model_name = (config.get("agent") or {}).get("model_name")
        if model_name != target_model or trial_dir in {Path(item["path"]) for item in candidates}:
            continue
        candidates.append(_trial_candidate(base, model, case, result_path, "archive-trial"))
    return candidates


def _select_canonical(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not candidates:
        return None
    # Valid results win. Once a task has a finished exception record, it is final;
    # archived unfinished trajectories must not resurrect it as running.
    def rank(item: dict[str, Any]) -> tuple[int, int, int, int, int, str]:
        return (
            4 if item["valid"] else 0,
            3 if item["finished"] and item["exception_type"] else 0,
            2 if item["running"] else 0,
            1 if item["finished"] else 0,
            1 if item["source"] == "job" else 0,
            int(item["input_tokens"] > 0),
            item["path"],
        )
    return max(candidates, key=rank)


def write_token_audit(token_stats: dict[str, dict[str, Any]], cases: list[Any]) -> None:
    payload = {
        "scope": "2023-2025, 18 tasks",
        "generated": date.today().isoformat(),
        "policy": {
            "unit": "one canonical trial per model x task",
            "priority": "valid artifact > live trajectory > one finished/error record",
            "excluded_retries_are_not_summed": True,
            "actual_openrouter_activity_spend_is_not_reconstructed_here": True,
        },
        "models": {
            model: {
                key: value
                for key, value in stats.items()
                if key not in {"task_records"}
            }
            | {"tasks": stats.get("task_records", [])}
            for model, stats in token_stats.items()
        },
    }
    TOKEN_AUDIT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def model_token_stats(base: Any, model: str, cases: list[Any]) -> dict[str, Any]:
    stats = {
        "job_count": 0,
        "n_input_tokens": 0,
        "n_cache_tokens": 0,
        "raw_n_cache_tokens": 0,
        "n_output_tokens": 0,
        "n_reasoning_tokens": 0,
        "billable_input_tokens": 0,
        "estimated_cost_rmb": None,
        "cache_hit_rate": None,
        "cache_imputed_from_peer_avg": False,
        "canonical_tasks": len(cases),
        "valid_tasks": 0,
        "running_tasks": 0,
        "error_tasks": 0,
        "pending_tasks": 0,
        "excluded_retry_trials": 0,
        "task_records": [],
    }
    for case in cases:
        candidates = _candidate_trials(base, model, case)
        selected = _select_canonical(candidates)
        if selected is None:
            stats["pending_tasks"] += 1
            status = "pending"
            selected_payload = None
        else:
            stats["n_input_tokens"] += selected["input_tokens"]
            stats["n_cache_tokens"] += selected["cache_tokens"]
            stats["raw_n_cache_tokens"] += selected["cache_tokens"]
            stats["n_output_tokens"] += selected["output_tokens"]
            stats["n_reasoning_tokens"] += selected.get("reasoning_tokens", 0)
            if selected["valid"]:
                stats["valid_tasks"] += 1
                status = "valid"
            elif selected["running"]:
                stats["running_tasks"] += 1
                status = "running"
            elif selected["finished"] or selected["exception_type"]:
                stats["error_tasks"] += 1
                status = "error"
            else:
                stats["pending_tasks"] += 1
                status = "pending"
            selected_payload = selected
        stats["excluded_retry_trials"] += max(0, len(candidates) - (1 if selected else 0))
        stats["task_records"].append(
            {
                "task": case.slug,
                "status": status,
                "selected": selected_payload,
                "excluded": [item for item in candidates if not selected or item["path"] != selected["path"]],
            }
        )
    if stats["n_input_tokens"] > 0:
        stats["cache_hit_rate"] = stats["n_cache_tokens"] / stats["n_input_tokens"]
    stats["billable_input_tokens"] = max(0, stats["n_input_tokens"] - stats["n_cache_tokens"])
    stats["job_count"] = len(model_job_names(base, model, cases))
    stats["estimated_cost_rmb"] = estimate_model_cost(
        model,
        int(stats["n_input_tokens"]),
        int(stats["n_cache_tokens"]),
        int(stats["n_output_tokens"]),
        int(stats["n_reasoning_tokens"]),
    )
    return stats


def compute() -> tuple[Any, list[Any], list[dict[str, Any]], list[Summary]]:
    base = load_base()
    builder = base._load_builder()
    global MODELS
    MODELS = model_config(builder)
    base.MODELS = MODELS
    cases = [case for case in builder.CASES if case.year in (2023, 2024, 2025)]
    canonical: dict[tuple[str, str], dict[str, Any] | None] = {
        (model, case.slug): _select_canonical(_candidate_trials(base, model, case))
        for model in MODELS
        for case in cases
    }
    records: list[dict[str, Any]] = []
    for case in cases:
        score_config = base._score_config(case)
        oracle_details = base.score_artifact_direction_aware(base._expected_result(case), score_config)
        oracle_raw = base._raw(oracle_details)
        raw_by_model: dict[str, float | None] = {}
        details_by_model: dict[str, dict[str, Any] | None] = {"oracle": oracle_details}
        for model in MODELS:
            selected = canonical[(model, case.slug)]
            # Completion status is authoritative for the two monitored models:
            # an artifact attached to a final error is audit evidence, not a
            # completed model answer. Scoreable artifacts remain independent.
            if model in {"oxalpha", "qwenflash"} and (selected is None or not selected["valid"]):
                details = None
            else:
                details = base._score_model_artifact_direction_aware(model, case, case.output_name, score_config)
            details_by_model[model] = details
            raw_by_model[model] = base._raw(details) if details is not None else 0.0
        b_by_model = {
            model: raw_by_model[model] - raw_by_model["flash"]
            for model in MODELS
            if model != "flash" and raw_by_model[model] is not None and raw_by_model["flash"] is not None
        }
        bo_by_model = {
            model: bo_eval(raw_by_model[model], raw_by_model["flash"], oracle_raw)
            for model in MODELS
            if model != "flash"
        }
        o_by_model = {
            model: o_eval(raw_by_model[model], oracle_raw)
            for model in MODELS
        }
        effect_by_model = {
            model: 0.0
            if model == "flash"
            else robust_effect(
                raw_by_model[model],
                raw_by_model["flash"],
                oracle_raw,
                failure=details_by_model[model] is None,
            )
            for model in MODELS
        }
        hard_gate_by_model = {
            model: hard_gate_reason(model, case.slug, details_by_model.get(model))
            for model in MODELS
        }
        gated_raw_by_model = {
            model: HARD_GATE_O_RAW if hard_gate_by_model.get(model) else raw_by_model[model]
            for model in MODELS
        }
        gated_o_by_model = {
            model: o_eval(gated_raw_by_model[model], oracle_raw)
            for model in MODELS
        }
        gated_effect_by_model = {
            model: 0.0
            if model == "flash"
            else robust_effect(
                gated_raw_by_model[model],
                gated_raw_by_model["flash"],
                oracle_raw,
                failure=bool(hard_gate_by_model.get(model)) or details_by_model[model] is None,
            )
            for model in MODELS
        }
        records.append(
            {
                "case": case,
                "score": score_config,
                "oracle_raw": oracle_raw,
                "raw": raw_by_model,
                "o": o_by_model,
                "b": b_by_model,
                "bo": bo_by_model,
                "effect": effect_by_model,
                "hard_gate": hard_gate_by_model,
                "gated_raw": gated_raw_by_model,
                "gated_o": gated_o_by_model,
                "gated_effect": gated_effect_by_model,
                "details": details_by_model,
            }
        )

    token_stats = {model: model_token_stats(base, model, cases) for model in MODELS}
    write_token_audit(token_stats, cases)
    summaries: list[Summary] = []
    for model, meta in MODELS.items():
        if model in {"oxalpha", "qwenflash"}:
            artifact_count = sum(
                1
                for case in cases
                if canonical[(model, case.slug)] is not None
                and canonical[(model, case.slug)]["artifact"]
            )
        else:
            artifact_count = sum(1 for record in records if record["details"].get(model) is not None)
        raw_values = [record["raw"][model] for record in records if record["raw"][model] is not None]
        if model == "flash":
            b_values = [0.0 for _ in records]
            bo_values = [0.0 for record in records if bo_defined(record)]
            effect_values = [0.0 for _ in records]
        else:
            b_values = [record["b"][model] for record in records if record["b"].get(model) is not None]
            bo_values = [record["bo"][model] for record in records if record["bo"].get(model) is not None]
            effect_values = [record["effect"][model] for record in records if record["effect"].get(model) is not None]
        o_values = [record["o"][model] for record in records if record["o"].get(model) is not None]
        gated_raw_values = [record["gated_raw"][model] for record in records if record["gated_raw"].get(model) is not None]
        gated_o_values = [record["gated_o"][model] for record in records if record["gated_o"].get(model) is not None]
        if model == "flash":
            gated_effect_values = [0.0 for _ in records]
        else:
            gated_effect_values = [
                record["gated_effect"][model]
                for record in records
                if record["gated_effect"].get(model) is not None
            ]
        hard_gate_count = sum(1 for record in records if record["hard_gate"].get(model))
        ts = token_stats[model]
        summaries.append(
            Summary(
                model=model,
                label=str(meta["label"]),
                short=str(meta["short"]),
                artifacts=artifact_count,
                bo_defined_tasks=len(bo_values),
                raw_mean=mean(raw_values),
                o_mean=mean(o_values),
                b_mean=mean(b_values),
                effect_mean=mean(effect_values),
                bo_mean=mean(bo_values),
                input_tokens=int(ts["n_input_tokens"]),
                cache_tokens=int(ts["n_cache_tokens"]),
                raw_cache_tokens=int(ts["raw_n_cache_tokens"]),
                output_tokens=int(ts["n_output_tokens"]),
                reasoning_tokens=int(ts.get("n_reasoning_tokens") or 0),
                billable_input_tokens=int(ts["billable_input_tokens"]),
                cost_rmb=ts["estimated_cost_rmb"],
                cost_usd=estimate_model_cost_usd(
                    model,
                    int(ts["n_input_tokens"]),
                    int(ts["n_cache_tokens"]),
                    int(ts["n_output_tokens"]),
                    int(ts.get("n_reasoning_tokens") or 0),
                ),
                cache_hit_rate=ts["cache_hit_rate"],
                cache_imputed_from_peer_avg=bool(ts["cache_imputed_from_peer_avg"]),
                hard_gate_count=hard_gate_count,
                hard_gated_raw_mean=mean(gated_raw_values),
                hard_gated_o_mean=mean(gated_o_values),
                hard_gated_effect_mean=mean(gated_effect_values),
                canonical_tasks=int(ts["canonical_tasks"]),
                valid_tasks=int(ts["valid_tasks"]),
                running_tasks=int(ts["running_tasks"]),
                error_tasks=int(ts["error_tasks"]),
                pending_tasks=int(ts["pending_tasks"]),
                excluded_retry_trials=int(ts["excluded_retry_trials"]),
            )
        )
    return base, cases, records, summaries


def split_mean(records: list[dict[str, Any]], model: str, *, year: int | None = None, suite: str | None = None) -> float | None:
    subset = records
    if year is not None:
        subset = [record for record in subset if record["case"].year == year]
    if suite is not None:
        subset = [record for record in subset if record["case"].contest == suite]
    if model == "flash":
        return 0.0 if subset else None
    values = [record["effect"][model] for record in subset if record["effect"].get(model) is not None]
    return mean(values)


def split_o_mean(records: list[dict[str, Any]], model: str, *, year: int | None = None, suite: str | None = None) -> float | None:
    subset = records
    if year is not None:
        subset = [record for record in subset if record["case"].year == year]
    if suite is not None:
        subset = [record for record in subset if record["case"].contest == suite]
    values = [record["o"][model] for record in subset if record["o"].get(model) is not None]
    return mean(values)


def split_hard_gated_o_mean(records: list[dict[str, Any]], model: str, *, year: int | None = None, suite: str | None = None) -> float | None:
    subset = records
    if year is not None:
        subset = [record for record in subset if record["case"].year == year]
    if suite is not None:
        subset = [record for record in subset if record["case"].contest == suite]
    values = [record["gated_o"][model] for record in subset if record["gated_o"].get(model) is not None]
    return mean(values)


def split_hard_gated_effect_mean(records: list[dict[str, Any]], model: str, *, year: int | None = None, suite: str | None = None) -> float | None:
    subset = records
    if year is not None:
        subset = [record for record in subset if record["case"].year == year]
    if suite is not None:
        subset = [record for record in subset if record["case"].contest == suite]
    if model == "flash":
        return 0.0 if subset else None
    values = [record["gated_effect"][model] for record in subset if record["gated_effect"].get(model) is not None]
    return mean(values)


def artifact_count(records: list[dict[str, Any]], model: str, *, year: int | None = None, suite: str | None = None) -> int:
    subset = records
    if year is not None:
        subset = [record for record in subset if record["case"].year == year]
    if suite is not None:
        subset = [record for record in subset if record["case"].contest == suite]
    return sum(1 for record in subset if record["details"].get(model) is not None)


def gate_task_list(records: list[dict[str, Any]], model: str) -> list[str]:
    return [record["case"].slug for record in records if record["hard_gate"].get(model)]


def gate_task_cell(records: list[dict[str, Any]], model: str) -> str:
    tasks = gate_task_list(records, model)
    if not tasks:
        return "0"
    return f"{len(tasks)}: " + ", ".join(f"`{task}`" for task in tasks)


def write_report(cases: list[Any], records: list[dict[str, Any]], summaries: list[Summary]) -> Path:
    robust_ratio_records = [
        record
        for record in records
        if record["raw"].get("flash") is not None
        and record.get("oracle_raw") is not None
        and record["oracle_raw"] - record["raw"]["flash"] >= ROBUST_GAP_FLOOR
    ]
    saturated_records = [record for record in records if record not in robust_ratio_records]
    qwen_summary = next((summary for summary in summaries if summary.model == "qwen"), None)
    qwen_cache_note = (
        "- No peer-average cache imputation is used. Cache tokens in this report are the raw per-trial counters; "
        "Qwen3.8 Flash uses the supplied OpenRouter cached-read price."
    )
    price_lines = [
        "| Model | OpenRouter model | Price source | Input | Cached read | Cache write/create | Output |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for model, meta in MODELS.items():
        price = meta.get("price_rmb_per_mtok", {})
        price_lines.append(
            "| "
            + " | ".join(
                [
                    str(meta["label"]),
                    f"`{meta.get('openrouter_model', 'N/A')}`",
                    str(meta.get("price_source", "local fallback")),
                    price_cell(price.get("input_uncached") if isinstance(price, dict) else None),
                    price_cell(price.get("input_cached") if isinstance(price, dict) else None),
                    price_cell(price.get("explicit_cache_create") if isinstance(price, dict) else None),
                    price_cell(price.get("output") if isinstance(price, dict) else None),
                ]
            )
            + " |"
        )
    o_ranking = sorted(
        [summary for summary in summaries if summary.model != "flash"],
        key=lambda item: item.o_mean if item.o_mean is not None else float("-inf"),
        reverse=True,
    )
    robust_ranking = sorted(
        [summary for summary in summaries if summary.model != "flash"],
        key=lambda item: item.effect_mean if item.effect_mean is not None else float("-inf"),
        reverse=True,
    )
    hard_gated_ranking = sorted(
        summaries,
        key=lambda item: item.hard_gated_o_mean if item.hard_gated_o_mean is not None else float("-inf"),
        reverse=True,
    )
    hard_gated_non_baseline = [summary for summary in hard_gated_ranking if summary.model != "flash"]
    hard_gated_robust_ranking = sorted(
        [summary for summary in summaries if summary.model != "flash"],
        key=lambda item: item.hard_gated_effect_mean if item.hard_gated_effect_mean is not None else float("-inf"),
        reverse=True,
    )
    gate_rows: list[str] = []
    for record in records:
        case = record["case"]
        for model in MODELS:
            reason = record["hard_gate"].get(model)
            if not reason:
                continue
            gate_rows.append(
                "| "
                + " | ".join(
                    [
                        str(MODELS[model]["label"]),
                        f"`{case.slug}`",
                        cell(record["raw"].get(model)),
                        cell(record["gated_raw"].get(model)),
                        pct_cell(record["o"].get(model)),
                        pct_cell(record["gated_o"].get(model)),
                        pct_cell(record["effect"].get(model)),
                        pct_cell(record["gated_effect"].get(model)),
                        reason,
                    ]
                )
                + " |"
            )

    lines = [
        "# O-Eval and Robust BO-Eval: 2023-2025",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "Scope: 2023, 2024, and 2025 terminal-bench-math-modeling tasks, 18 tasks total. This report rescored saved artifacts only; it does not rerun models or modify job result files.",
        "",
        "Primary O-Eval rule: `clamp(model direction-aware raw / O raw, 0, 1)`, averaged over all 18 tasks. Since the O-award reproduction is normalized near raw=1 on these tasks, O-Eval is the easiest-to-read absolute oracle-normalized score, and overshoots are capped at 100%.",
        "",
        f"Secondary Robust BO-Eval rule: let `gain = model raw - flash raw` and `gap = O raw - flash raw`. If `gap >= {ROBUST_GAP_FLOOR:.2f}`, score `clip(gain / gap, -100%, +100%)`; otherwise score `clip(gain, -{ROBUST_SATURATED_GAIN_CLIP * 100:.0f}pp, +{ROBUST_SATURATED_GAIN_CLIP * 100:.0f}pp)`. Normal completed tasks still use the clipped fallback on tiny-gap cases, but any missing or non-scoreable artifact is assigned `-100%` so a completely unfinished task gets the worst possible score.",
        "",
        "Tempered hard-gated rule: only clearly non-feasible cells are whole-task penalized. Automatic scorer hard-invalid metrics and manually replay-proven invalid high-score cells receive gated raw `0` for O-Eval and `-100%` for Robust BO-Eval. Needs-review/proxy cells remain scored but are not used as stronger-than-O claims without a better replay verifier.",
        "",
        f"Robust ratio tasks with gap >= {ROBUST_GAP_FLOOR:.2f}: {len(robust_ratio_records)}. Saturated or near-zero-gap tasks using clipped B-Eval: {len(saturated_records)}.",
        "",
        "## Overall Mean",
        "",
        "| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB | Canonical valid/running/error/pending | Excluded retries |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|",
    ]
    for summary in summaries:
        lines.append(
            f"| {summary.label} | {summary.artifacts} | {cell(summary.raw_mean)} | "
            f"{pct_cell(summary.o_mean)} | {pp_cell(summary.b_mean)} | {pct_cell(summary.effect_mean)} | "
            f"{int_cell(summary.input_tokens)} / {int_cell(summary.cache_tokens)} / {int_cell(summary.output_tokens)} | "
            f"{int_cell(summary.billable_input_tokens)} / {int_cell(summary.output_tokens)} | {usd_money_cell(summary.cost_usd)}"
        )
        lines[-1] += (
            f" | {money_cell(summary.cost_rmb)} | {summary.valid_tasks}/{summary.running_tasks}/{summary.error_tasks}/{summary.pending_tasks} | "
            f"{summary.excluded_retry_trials} |"
        )

    lines.extend(
        [
            "",
            "## Tempered Hard-Gated Leaderboard",
            "",
            "| Rank | Model | Hard-gated O-Eval | Hard-gated Robust BO-Eval | Original O-Eval | Original Robust BO-Eval | Hard-gated raw mean | Hard gates | Est. cost RMB |",
            "|---:|---|---:|---:|---:|---:|---:|---|---:|",
        ]
    )
    for rank, summary in enumerate(hard_gated_ranking, start=1):
        lines.append(
            f"| {rank} | {summary.label} | {pct_cell(summary.hard_gated_o_mean)} | "
            f"{pct_cell(summary.hard_gated_effect_mean)} | {pct_cell(summary.o_mean)} | "
            f"{pct_cell(summary.effect_mean)} | {cell(summary.hard_gated_raw_mean)} | "
            f"{gate_task_cell(records, summary.model)} | {money_cell(summary.cost_rmb)} |"
        )

    lines.extend(
        [
            "",
            "## Hard Gate Decisions",
            "",
            "| Model | Task | Raw before gate | Gated raw | O-Eval before | Hard-gated O-Eval | Robust before | Hard-gated Robust | Reason |",
            "|---|---|---:|---:|---:|---:|---:|---:|---|",
            *(gate_rows if gate_rows else ["| none | none | N/A | N/A | N/A | N/A | N/A | N/A | no hard-gated cells |"]),
            "",
            "## Primary Readout",
            "",
            "- 18-task primary O-Eval ranking: " + " > ".join(f"{item.label} ({pct_cell(item.o_mean)})" for item in o_ranking) + ".",
            "- Tempered hard-gated O-Eval ranking: " + " > ".join(f"{item.label} ({pct_cell(item.hard_gated_o_mean)})" for item in hard_gated_non_baseline) + ".",
            "- Secondary Robust BO-Eval ranking: " + " > ".join(f"{item.label} ({pct_cell(item.effect_mean)})" for item in robust_ranking) + ".",
            "- Tempered hard-gated Robust BO-Eval ranking: " + " > ".join(f"{item.label} ({pct_cell(item.hard_gated_effect_mean)})" for item in hard_gated_robust_ranking) + ".",
            "- These two metrics are complementary, not competing: O-Eval is the absolute oracle-normalized score for the headline leaderboard, while Robust BO-Eval is the baseline-relative gain view. If the rankings disagree, it usually means a model is closer to O in absolute terms but does not pull as far ahead of flash, or it gains a lot on a few weak-baseline tasks without being closest overall. This report therefore uses O-Eval as the final ranking and Robust BO-Eval as a diagnostic view.",
            "- The hard-gated tables are the cautious public-facing view: they keep the normal O-Eval leaderboard visible, but remove credit from cells that are clearly not feasible solutions.",
            "- The GLM-5.3-Flash vs DeepSeek flash difference is a good example: Robust can favor the model that moves farther above flash, while O-Eval still favors the model that lands closer to the oracle anchor.",
            "- v4 flash baseline now uses the 4-hour rerun jobs: `terminus2-deepseek-v4-flash-0731-rerun-2023-2025-cumcm` and `terminus2-deepseek-v4-flash-0731-rerun-2023-2025-mcm`.",
            f"- Cost is estimated from OpenRouter model catalog prices (`prompt`, `input_cache_read`, `input_cache_write`, `completion`) converted from USD/token to RMB/M tokens at USD/CNY={OPENROUTER_USD_TO_RMB}.",
            "- Token/cost totals use exactly one canonical trial per model x task. A valid artifact outranks a live trajectory; retries are retained in the audit but excluded from these totals.",
            "- Cost is an evaluation-normalized estimate, not the actual OpenRouter Activity/Usage bill. Activity/Usage includes every request from retries and is the authority for actual spend.",
            "- Cache-hit input is charged using `input_cache_read`; explicit cache write/create is not added because trial result files expose no cache-write token counter.",
            qwen_cache_note,
            "- Fixed monitored prices: GLM-5.3-Flash (ox-alpha) input $0.075/M, cached read $0.015/M, output $0.25/M; Qwen3.8 Flash (Bailian) input $0.15/M, cached read $0.016/M, cached write $0.20/M, output $0.47/M. The requested estimate uses input, cached-read, and output counters; no cache-write token counter is available.",
            "- GLM-5.3-Flash (ox-alpha) has 17 valid completed tasks and one final model-timeout failure on `cumcm-2023-a-heliostat-field`; that task is excluded from valid results and will not be retried.",
            f"- Per-task selection audit: `{TOKEN_AUDIT_PATH.name}`.",
            f"- Price snapshot used by this run: `{PRICE_SNAPSHOT_PATH.name}`.",
            "- Claude Opus 5 is not listed because no completed artifacts were present in the workspace for the 18-task scope.",
            "",
            "## Price Table",
            "",
            *price_lines,
            "",
            "## Figures",
            "",
            "- Clickable dashboard: `terminus2-bo-eval-aa-dashboard-2023-2025.html`",
            f"- All-model feasibility audit: `{FEASIBILITY_AUDIT_PATH.name}`",
            "- Hard-gated O-Eval effect: `figures/aa-style-2023-2025-hard-gated-o-eval-bar.png`",
            "- Hard-gated O-Eval score-cost: `figures/aa-style-2023-2025-hard-gated-o-eval-cost-scatter.png`",
            "- O-Eval effect: `figures/aa-style-2023-2025-o-eval-bar.png`",
            "- O-Eval score-cost: `figures/aa-style-2023-2025-o-eval-cost-scatter.png`",
            "- Robust BO-Eval effect: `figures/aa-style-2023-2025-boeval-effect-bar.png`",
            "- Robust BO-Eval score-cost: `figures/aa-style-2023-2025-boeval-score-cost.png`",
            "- Token usage: `figures/aa-style-2023-2025-token-usage.png`",
            "- Cost: `figures/aa-style-2023-2025-cost.png`",
            "- O-Eval year split: `figures/aa-style-2023-2025-o-eval-year-split.png`",
            "- O-Eval suite split: `figures/aa-style-2023-2025-o-eval-suite-split.png`",
            "- Diagnostic Robust BO-Eval year split: `figures/aa-style-2023-2025-boeval-year-split.png`",
            "- Diagnostic Robust BO-Eval suite split: `figures/aa-style-2023-2025-boeval-suite-split.png`",
            "",
            "## Year Mean O-Eval",
            "",
            "| Model | 2023 | 2024 | 2025 |",
            "|---|---:|---:|---:|",
        ]
    )
    for summary in summaries:
        lines.append(
            f"| {summary.label} | "
            f"{pct_cell(split_o_mean(records, summary.model, year=2023))} | "
            f"{pct_cell(split_o_mean(records, summary.model, year=2024))} | "
            f"{pct_cell(split_o_mean(records, summary.model, year=2025))} |"
        )

    lines.extend(
        [
            "",
            "## Suite Mean O-Eval",
            "",
            "| Model | CUMCM | MCM |",
            "|---|---:|---:|",
        ]
    )
    for summary in summaries:
        lines.append(
            f"| {summary.label} | {pct_cell(split_o_mean(records, summary.model, suite='cumcm'))} | "
            f"{pct_cell(split_o_mean(records, summary.model, suite='mcm'))} |"
        )

    lines.extend(
        [
            "",
            "## Year Mean Robust BO-Eval",
            "",
            "| Model | 2023 | 2024 | 2025 |",
            "|---|---:|---:|---:|",
        ]
    )
    for summary in summaries:
        lines.append(
            f"| {summary.label} | "
            f"{pct_cell(split_mean(records, summary.model, year=2023))} | "
            f"{pct_cell(split_mean(records, summary.model, year=2024))} | "
            f"{pct_cell(split_mean(records, summary.model, year=2025))} |"
        )

    lines.extend(
        [
            "",
            "## Suite Mean Robust BO-Eval",
            "",
            "| Model | CUMCM | MCM | CUMCM artifacts | MCM artifacts |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for summary in summaries:
        lines.append(
            f"| {summary.label} | {pct_cell(split_mean(records, summary.model, suite='cumcm'))} | "
            f"{pct_cell(split_mean(records, summary.model, suite='mcm'))} | "
            f"{artifact_count(records, summary.model, suite='cumcm')} | "
            f"{artifact_count(records, summary.model, suite='mcm')} |"
        )

    lines.extend(
        [
            "",
            "## Saturated Or Near-Zero Gap Cases",
            "",
            "| Year | Suite | Problem | Task | flash raw | O raw |",
            "|---:|---|---|---|---:|---:|",
        ]
    )
    for record in saturated_records:
        case = record["case"]
        lines.append(
            f"| {case.year} | {case.contest.upper()} | {case.code} | `{case.slug}` | "
            f"{cell(record['raw']['flash'])} | {cell(record['oracle_raw'])} |"
        )

    lines.extend(
        [
            "",
            "## Per-Task Values",
            "",
            "Cells are `direction-aware raw / O-Eval % / B-Eval vs flash / Robust BO-Eval %`.",
            "",
            "| Year | Suite | Problem | Task | " + " | ".join(str(meta["label"]) for meta in MODELS.values()) + " | O raw |",
            "|---:|---|---|---" + "|---:" * len(MODELS) + "|---:|",
        ]
    )
    for record in records:
        case = record["case"]
        cells = []
        for model in MODELS:
            if model == "flash":
                cells.append(f"{cell(record['raw'][model])} / {pct_cell(record['o'][model])} / 0.00% / 0.00%")
            else:
                cells.append(
                    f"{cell(record['raw'][model])} / {pct_cell(record['o'][model])} / "
                    f"{pct_cell(record['bo'][model])} / {pct_cell(record['effect'][model])}"
                )
        lines.append(
            "| "
            + " | ".join([str(case.year), case.contest.upper(), case.code, f"`{case.slug}`", *cells, cell(record["oracle_raw"])])
            + " |"
        )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return REPORT_PATH


def svg_text(
    x: float,
    y: float,
    text: str,
    *,
    size: int = 20,
    weight: int = 600,
    fill: str = "#151515",
    anchor: str = "start",
    cls: str = "",
    transform: str = "",
) -> str:
    cls_attr = f' class="{cls}"' if cls else ""
    transform_attr = f' transform="{transform}"' if transform else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}"{cls_attr}{transform_attr}>{escape(text)}</text>'
    )


def svg_rect(x: float, y: float, w: float, h: float, fill: str, *, rx: float = 0, stroke: str | None = None, opacity: float | None = None) -> str:
    attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'width="{w:.1f}"', f'height="{h:.1f}"', f'fill="{fill}"']
    if rx:
        attrs.append(f'rx="{rx:.1f}"')
    if stroke:
        attrs.append(f'stroke="{stroke}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:.3f}"')
    return f"<rect {' '.join(attrs)} />"


def svg_line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#d7d7d7", width: float = 1.0, dash: str | None = None) -> str:
    attrs = [f'x1="{x1:.1f}"', f'y1="{y1:.1f}"', f'x2="{x2:.1f}"', f'y2="{y2:.1f}"', f'stroke="{stroke}"', f'stroke-width="{width:.1f}"']
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    return f"<line {' '.join(attrs)} />"


def shell(width: int, height: int, body: list[str]) -> str:
    style = """
    <style>
      .title { font-family: Georgia, Times, serif; font-size: 42px; font-weight: 500; fill: #050505; }
      .subtitle { font-family: Arial, Helvetica, sans-serif; font-size: 22px; fill: #777777; font-weight: 650; }
      .axis { font-family: Arial, Helvetica, sans-serif; font-size: 18px; fill: #777777; font-weight: 650; }
      .axis-title { font-family: Arial, Helvetica, sans-serif; font-size: 22px; fill: #111111; font-weight: 720; }
      .label { font-family: Arial, Helvetica, sans-serif; font-size: 19px; fill: #151515; font-weight: 700; }
      .small { font-family: Arial, Helvetica, sans-serif; font-size: 18px; fill: #777777; font-weight: 650; }
    </style>
    """
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">{style}<rect width="{width}" height="{height}" fill="#ffffff"/>' + "\n".join(body) + "</svg>\n"


def convert_svg(svg_path: Path) -> Path:
    png_path = svg_path.with_suffix(".png")
    commands = [
        ["magick", str(svg_path), str(png_path)],
        ["convert", str(svg_path), str(png_path)],
        ["sips", "-s", "format", "png", str(svg_path), "--out", str(png_path)],
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
    raise RuntimeError(f"could not convert {svg_path}: {'; '.join(errors)}")


def write_svg(path: Path, width: int, height: int, body: list[str]) -> Path:
    path.write_text(shell(width, height, body), encoding="utf-8")
    convert_svg(path)
    return path


def y_scale(value: float, y: float, h: float, domain_max: float) -> float:
    return y + h - value / domain_max * h


def y_scale_range(value: float, y: float, h: float, domain_min: float, domain_max: float) -> float:
    return y + h - (value - domain_min) / (domain_max - domain_min) * h


def nice_domain(values: list[float], step: float = 50.0) -> float:
    max_value = max(values) if values else step
    return max(step, math.ceil(max_value * 1.12 / step) * step)


def effect_axis_step(values: list[float]) -> float:
    max_abs = max((abs(value) for value in values), default=0.0)
    if max_abs <= 20:
        return 5.0
    if max_abs <= 50:
        return 10.0
    return 20.0


def effect_axis_domain(values: list[float], *, min_span: float = 20.0) -> tuple[float, float, float]:
    """Use a tight robust-score axis so small but meaningful gaps stay visible."""
    values = values or [0.0]
    step = effect_axis_step(values)
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
    # SVG text has no layout pass here; this is enough for short model labels.
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
    sizes = [19, 17]
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


def ticks(domain_max: float, step: float) -> list[float]:
    values: list[float] = []
    current = 0.0
    while current <= domain_max + 1e-9:
        values.append(current)
        current += step
    if values[-1] < domain_max - 1e-9:
        values.append(domain_max)
    return values


def range_ticks(domain_min: float, domain_max: float, step: float) -> list[float]:
    values: list[float] = []
    current = math.floor(domain_min / step) * step
    while current <= domain_max + 1e-9:
        values.append(current)
        current += step
    return values


def write_effect_bar(summaries: list[Summary]) -> Path:
    width, height = 1800, 1040
    chart_x, chart_y, chart_w, chart_h = 132, 300, 1540, 455
    rows = sorted(summaries, key=lambda item: item.effect_mean or 0.0, reverse=True)
    values = [(row.effect_mean or 0.0) * 100.0 for row in rows]
    domain_min, domain_max, tick_step = effect_axis_domain(values)
    body = [
        svg_rect(24, 24, width - 48, height - 48, "#ffffff", rx=16, stroke="#dedede"),
        svg_text(72, 126, "18-Task Robust BO-Eval", size=42, weight=500),
        svg_text(72, 168, "Wins and losses are clipped symmetrically to +/-100%; saturated or tiny-gap completed tasks use clipped B-Eval, while missing/non-scoreable artifacts are assigned -100%.", size=22, weight=650, fill="#777777"),
    ]
    for tick in range_ticks(domain_min, domain_max, tick_step):
        yy = y_scale_range(tick, chart_y, chart_h, domain_min, domain_max)
        body.append(svg_line(chart_x, yy, chart_x + chart_w, yy, dash=None if abs(tick) < 1e-9 else "4 8", stroke="#aaaaaa" if abs(tick) < 1e-9 else "#d7d7d7", width=1.4 if abs(tick) < 1e-9 else 1.0))
        body.append(svg_text(chart_x - 18, yy + 6, f"{tick:.0f}%", size=18, fill="#777777", anchor="end"))
    gap = 30
    bar_w = (chart_w - gap * (len(rows) - 1)) / len(rows)
    y_zero = y_scale_range(0.0, chart_y, chart_h, domain_min, domain_max)
    for idx, row in enumerate(rows):
        value = (row.effect_mean or 0.0) * 100.0
        x = chart_x + idx * (bar_w + gap)
        y_value = y_scale_range(value, chart_y, chart_h, domain_min, domain_max)
        y = min(y_value, y_zero)
        h = abs(y_zero - y_value)
        body.append(svg_rect(x, y, bar_w, h, row.color, rx=8))
        label_fill = "#ffffff" if value >= 0 else row.color
        label_y = y + max(30, h * 0.5) if value >= 0 else y + h + 28
        body.append(svg_text(x + bar_w / 2, label_y, f"{value:.1f}%", size=22, weight=800, fill=label_fill, anchor="middle"))
        body.append(svg_text(x + bar_w / 2, y - 12, f"{row.artifacts}/18", size=18, fill="#8a8a8a", anchor="middle"))
        label_lines = row.short.split(" ")
        if len(label_lines) > 2:
            label_lines = [" ".join(label_lines[:2]), " ".join(label_lines[2:])]
        for j, part in enumerate(label_lines):
            body.append(svg_text(x + bar_w / 2, chart_y + chart_h + 42 + j * 22, part, size=18, weight=700, anchor="middle"))
    body.append(svg_text(chart_x + chart_w / 2, height - 70, "Robust BO-Eval is averaged over all 18 tasks; tiny-gap completed tasks fall back to clipped B-Eval, and missing/non-scoreable artifacts are pinned to -100%.", size=18, fill="#777777", anchor="middle"))
    return write_svg(FIGURES / "aa-style-2023-2025-boeval-effect-bar.svg", width, height, body)


def write_split_bars(records: list[dict[str, Any]], summaries: list[Summary], *, split: str, metric: str) -> Path:
    width, height = 1800, 1120
    chart_x, chart_y, chart_w, chart_h = 132, 300, 1540, 500
    if split == "year":
        groups = [("2023", {"year": 2023}), ("2024", {"year": 2024}), ("2025", {"year": 2025})]
        if metric == "o":
            title = "O-Eval by Year"
            subtitle = "Primary O-normalized score split by contest year; missing or non-scoreable artifacts enter the mean as raw 0."
            filename = f"{FIGURE_PREFIX}-o-eval-year-split.svg"
        else:
            title = "Robust BO-Eval by Year"
            subtitle = "Diagnostic baseline-relative split with symmetric clipping; missing/non-scoreable artifacts are assigned -100%."
            filename = f"{FIGURE_PREFIX}-boeval-year-split.svg"
    else:
        groups = [("CUMCM", {"suite": "cumcm"}), ("MCM", {"suite": "mcm"})]
        if metric == "o":
            title = "O-Eval by Suite"
            subtitle = "Primary O-normalized score split by CUMCM and MCM, showing where each model's absolute performance comes from."
            filename = f"{FIGURE_PREFIX}-o-eval-suite-split.svg"
        else:
            title = "Robust BO-Eval by Suite"
            subtitle = "Diagnostic CUMCM/MCM split for baseline-relative gains; missing/non-scoreable artifacts are assigned -100%."
            filename = f"{FIGURE_PREFIX}-boeval-suite-split.svg"
    selected = [s for s in summaries if not SUMMARY_FILTER or s.label in SUMMARY_FILTER]
    models = selected if metric == "o" else [summary for summary in selected if summary.model != "flash"]
    all_values = []
    for _, filters in groups:
        for row in models:
            if metric == "o":
                value = split_o_mean(records, row.model, year=filters.get("year"), suite=filters.get("suite"))
            else:
                value = split_mean(records, row.model, year=filters.get("year"), suite=filters.get("suite"))
            all_values.append(0.0 if value is None else value * 100.0)
    if metric == "o":
        domain_min = 0.0
        domain_max = max(100.0, math.ceil(max(all_values or [0.0]) * 1.12 / 20.0) * 20.0)
        tick_step = 20.0
    else:
        domain_min, domain_max, tick_step = effect_axis_domain(all_values, min_span=40.0)
    body = [
        svg_rect(24, 24, width - 48, height - 48, "#ffffff", rx=16, stroke="#dedede"),
        svg_text(72, 126, title, size=42, weight=500),
        svg_text(72, 168, subtitle, size=22, weight=650, fill="#777777"),
    ]
    for tick in range_ticks(domain_min, domain_max, step=tick_step):
        yy = y_scale_range(tick, chart_y, chart_h, domain_min, domain_max)
        body.append(svg_line(chart_x, yy, chart_x + chart_w, yy, dash=None if abs(tick) < 1e-9 else "4 8", stroke="#aaaaaa" if abs(tick) < 1e-9 else "#d7d7d7", width=1.4 if abs(tick) < 1e-9 else 1.0))
        body.append(svg_text(chart_x - 18, yy + 6, f"{tick:.0f}%", size=18, fill="#777777", anchor="end"))
    group_gap = 96
    group_w = (chart_w - group_gap * (len(groups) - 1)) / len(groups)
    bar_gap = 12
    bar_w = (group_w - bar_gap * (len(models) - 1)) / len(models)
    for gidx, (group_label, filters) in enumerate(groups):
        gx = chart_x + gidx * (group_w + group_gap)
        body.append(svg_text(gx + group_w / 2, chart_y + chart_h + 50, group_label, size=24, weight=800, anchor="middle"))
        for midx, row in enumerate(models):
            if metric == "o":
                value = split_o_mean(records, row.model, year=filters.get("year"), suite=filters.get("suite"))
            else:
                value = split_mean(records, row.model, year=filters.get("year"), suite=filters.get("suite"))
            pct = 0.0 if value is None else value * 100.0
            x = gx + midx * (bar_w + bar_gap)
            y_zero = y_scale_range(0.0, chart_y, chart_h, domain_min, domain_max)
            y_value = y_scale_range(pct, chart_y, chart_h, domain_min, domain_max)
            y = min(y_zero, y_value)
            h = abs(y_zero - y_value)
            body.append(svg_rect(x, y, bar_w, h, row.color, rx=5))
            if h > 34:
                body.append(svg_text(x + bar_w / 2, y + h / 2 + 7, f"{pct:.0f}", size=15, weight=800, fill="#ffffff", anchor="middle"))
    legend_x, legend_y = chart_x, height - 180
    for idx, row in enumerate(models):
        x = legend_x + (idx % 4) * 360
        y = legend_y + (idx // 4) * 42
        body.append(svg_rect(x, y, 22, 16, row.color, rx=3))
        body.append(svg_text(x + 32, y + 16, row.short, size=18, fill="#555555"))
    return write_svg(FIGURES / filename, width, height, body)


def log_x(value: float, domain_min: float, domain_max: float, range_min: float, range_max: float) -> float:
    return range_min + (math.log(value) - math.log(domain_min)) / (math.log(domain_max) - math.log(domain_min)) * (range_max - range_min)


def write_score_cost_scatter(summaries: list[Summary]) -> Path:
    width, height = 1800, 1100
    chart_x, chart_y, chart_w, chart_h = 154, 320, 1450, 560
    priced = [row for row in summaries if row.cost_rmb is not None and row.cost_rmb > 0]
    x_min = max(1.0, min(row.cost_rmb for row in priced) * 0.72)
    x_max = max(row.cost_rmb for row in priced) * 1.28
    effect_values = [(row.effect_mean or 0.0) * 100.0 for row in summaries]
    score_threshold = max(5.0, min(10.0, max(effect_values) * 0.75))
    y_min, y_max, y_step = effect_axis_domain(effect_values)
    if y_max <= score_threshold:
        y_max = math.ceil((score_threshold + y_step) / y_step) * y_step

    def sx(value: float) -> float:
        return log_x(value, x_min, x_max, chart_x, chart_x + chart_w)

    def sy(value: float) -> float:
        return y_scale_range(value, chart_y, chart_h, y_min, y_max)

    body = [
        svg_rect(24, 24, width - 48, height - 48, "#ffffff", rx=16, stroke="#dedede"),
        svg_text(72, 126, "Robust BO-Eval vs Cost", size=42, weight=500),
        svg_text(72, 168, "18-task robust main metric against estimated RMB cost. X axis is log-scaled; wins and losses are clipped symmetrically before averaging.", size=22, weight=650, fill="#777777"),
    ]
    cost_ticks = [10, 20, 50, 100, 150, 200, 500, 800]
    for tick in cost_ticks:
        if tick < x_min or tick > x_max:
            continue
        x = sx(tick)
        body.append(svg_line(x, chart_y, x, chart_y + chart_h, stroke="#eeeeee", dash="4 8"))
        body.append(svg_text(x, chart_y + chart_h + 38, f"¥{tick}", size=18, fill="#777777", anchor="middle"))
    for tick in range_ticks(y_min, y_max, step=y_step):
        y = sy(tick)
        body.append(svg_line(chart_x, y, chart_x + chart_w, y, dash=None if abs(tick) < 1e-9 else "4 8", stroke="#aaaaaa" if abs(tick) < 1e-9 else "#d7d7d7", width=1.4 if abs(tick) < 1e-9 else 1.0))
        body.append(svg_text(chart_x - 18, y + 6, f"{tick:.0f}%", size=18, fill="#777777", anchor="end"))
    body.append(svg_line(chart_x, chart_y + chart_h, chart_x + chart_w, chart_y + chart_h, stroke="#aaaaaa", width=1.3))
    body.append(svg_line(chart_x, chart_y, chart_x, chart_y + chart_h, stroke="#aaaaaa", width=1.3))
    body.append(svg_text(chart_x + chart_w / 2, chart_y + chart_h + 82, "Estimated cost (RMB, log scale)", size=22, weight=720, anchor="middle"))
    body.append(
        svg_text(
            chart_x - 100,
            chart_y + chart_h / 2,
            "Robust BO-Eval (%)",
            size=22,
            weight=720,
            anchor="middle",
            transform=f"rotate(-90 {chart_x - 100:.1f} {chart_y + chart_h / 2:.1f})",
        )
    )

    cost_threshold = 80.0
    if x_min < cost_threshold < x_max:
        body.append(svg_rect(chart_x, chart_y, sx(cost_threshold) - chart_x, sy(score_threshold) - chart_y, "#e8f7eb", opacity=0.75))
        body.append(svg_text(chart_x + 20, chart_y + 34, f"value zone: <=¥{cost_threshold:.0f}, >={score_threshold:.1f}% robust", size=18, fill="#3f7f4a"))
        body.append(svg_line(sx(cost_threshold), chart_y, sx(cost_threshold), chart_y + chart_h, stroke="#9ca3af", dash="6 7"))
    body.append(svg_line(chart_x, sy(score_threshold), chart_x + chart_w, sy(score_threshold), stroke="#9ca3af", dash="6 7"))

    point_specs: list[tuple[str, float, float, list[str]]] = []
    for row in priced:
        x = sx(float(row.cost_rmb))
        y = sy((row.effect_mean or 0.0) * 100.0)
        label = row.short if row.artifacts >= 18 else f"{row.short} ({row.artifacts}/18)"
        point_specs.append((row.model, x, y, [label, f"{(row.effect_mean or 0.0) * 100:.1f}% / ¥{row.cost_rmb:.1f}"]))
    placements = place_point_labels(point_specs, (chart_x + 8, chart_y + 8, chart_x + chart_w - 8, chart_y + chart_h - 8))
    for row in priced:
        x = sx(float(row.cost_rmb))
        y = sy((row.effect_mean or 0.0) * 100.0)
        radius = 9 + min(8, row.artifacts / 18 * 8)
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{row.color}" stroke="#ffffff" stroke-width="3"/>')
        label_x, label_y, anchor = placements[row.model]
        label = row.short if row.artifacts >= 18 else f"{row.short} ({row.artifacts}/18)"
        body.append(svg_text(label_x, label_y, label, size=19, weight=700, fill="#333333", anchor=anchor))
        body.append(svg_text(label_x, label_y + 24, f"{(row.effect_mean or 0.0) * 100:.1f}% / ¥{row.cost_rmb:.1f}", size=17, weight=650, fill="#777777", anchor=anchor))

    no_cost_rows = [row for row in summaries if row.cost_rmb is None and row.model != "flash"]
    if no_cost_rows:
        note = "; ".join(f"{row.short}: {(row.effect_mean or 0.0) * 100:.1f}% robust, cost N/A" for row in no_cost_rows)
        body.append(svg_rect(760, 218, 900, 48, "#f3e8ff", rx=8))
        body.append(svg_text(780, 250, note, size=18, weight=700, fill="#6d28d9"))

    body.append(svg_text(chart_x + chart_w / 2, height - 72, "Cost uses the same report estimate. Cache-hit input is not charged except where a model price table explicitly provides it.", size=18, fill="#777777", anchor="middle"))
    return write_svg(FIGURES / "aa-style-2023-2025-boeval-score-cost.svg", width, height, body)


def write_hard_gated_o_bar(summaries: list[Summary]) -> Path:
    width, height = 1800, 1040
    chart_x, chart_y, chart_w, chart_h = 132, 300, 1540, 455
    rows = sorted(summaries, key=lambda item: item.hard_gated_o_mean or 0.0, reverse=True)
    values = [(row.hard_gated_o_mean or 0.0) * 100.0 for row in rows]
    domain_max = max(100.0, math.ceil(max(values or [0.0]) * 1.12 / 20.0) * 20.0)
    body = [
        svg_rect(24, 24, width - 48, height - 48, "#ffffff", rx=16, stroke="#dedede"),
        svg_text(72, 126, "18-Task Hard-Gated O-Eval", size=42, weight=500),
        svg_text(72, 168, "Tempered gate: only clearly non-feasible cells are zeroed; needs-review/proxy cells stay scored with caveats.", size=22, weight=650, fill="#777777"),
    ]
    for tick in ticks(domain_max, 20.0):
        yy = y_scale(tick, chart_y, chart_h, domain_max)
        body.append(svg_line(chart_x, yy, chart_x + chart_w, yy, dash="4 8" if tick else None, stroke="#d7d7d7"))
        body.append(svg_text(chart_x - 18, yy + 6, f"{tick:.0f}%", size=18, fill="#777777", anchor="end"))
    gap = 30
    bar_w = (chart_w - gap * (len(rows) - 1)) / len(rows)
    for idx, row in enumerate(rows):
        value = (row.hard_gated_o_mean or 0.0) * 100.0
        x = chart_x + idx * (bar_w + gap)
        y = y_scale(value, chart_y, chart_h, domain_max)
        h = chart_y + chart_h - y
        body.append(svg_rect(x, y, bar_w, h, row.color, rx=8))
        body.append(svg_text(x + bar_w / 2, y + max(32, h * 0.5), f"{value:.1f}%", size=22, weight=800, fill="#ffffff", anchor="middle"))
        gate_text = f"{row.hard_gate_count} gate" if row.hard_gate_count == 1 else f"{row.hard_gate_count} gates"
        body.append(svg_text(x + bar_w / 2, y - 12, gate_text, size=18, fill="#8a8a8a", anchor="middle"))
        label_lines = row.short.split(" ")
        if len(label_lines) > 2:
            label_lines = [" ".join(label_lines[:2]), " ".join(label_lines[2:])]
        for j, part in enumerate(label_lines):
            body.append(svg_text(x + bar_w / 2, chart_y + chart_h + 42 + j * 22, part, size=18, weight=700, anchor="middle"))
    body.append(svg_text(chart_x + chart_w / 2, height - 70, "Hard-gated O-Eval is the cautious public-facing score: clear non-feasible cells count as raw 0 before the 18-task mean.", size=18, fill="#777777", anchor="middle"))
    return write_svg(FIGURES / "aa-style-2023-2025-hard-gated-o-eval-bar.svg", width, height, body)


def write_hard_gated_o_score_cost_scatter(summaries: list[Summary]) -> Path:
    width, height = 1800, 1100
    chart_x, chart_y, chart_w, chart_h = 154, 320, 1450, 560
    priced = [row for row in summaries if row.cost_rmb is not None and row.cost_rmb > 0]
    x_min = max(1.0, min(row.cost_rmb for row in priced) * 0.72)
    x_max = max(row.cost_rmb for row in priced) * 1.28
    values = [(row.hard_gated_o_mean or 0.0) * 100.0 for row in priced]
    y_min = 0.0
    y_max = max(100.0, math.ceil(max(values or [0.0]) * 1.12 / 20.0) * 20.0)

    def sx(value: float) -> float:
        return log_x(value, x_min, x_max, chart_x, chart_x + chart_w)

    def sy(value: float) -> float:
        return y_scale_range(value, chart_y, chart_h, y_min, y_max)

    body = [
        svg_rect(24, 24, width - 48, height - 48, "#ffffff", rx=16, stroke="#dedede"),
        svg_text(72, 126, "Hard-Gated O-Eval vs Cost", size=42, weight=500),
        svg_text(72, 168, "Cautious O-normalized score against estimated RMB cost. X axis is log-scaled.", size=22, weight=650, fill="#777777"),
    ]
    cost_ticks = [10, 20, 50, 100, 150, 200, 500, 800]
    for tick in cost_ticks:
        if tick < x_min or tick > x_max:
            continue
        x = sx(tick)
        body.append(svg_line(x, chart_y, x, chart_y + chart_h, stroke="#eeeeee", dash="4 8"))
        body.append(svg_text(x, chart_y + chart_h + 38, f"¥{tick}", size=18, fill="#777777", anchor="middle"))
    for tick in ticks(y_max, 20.0):
        y = sy(tick)
        body.append(svg_line(chart_x, y, chart_x + chart_w, y, dash="4 8" if tick else None, stroke="#d7d7d7"))
        body.append(svg_text(chart_x - 18, y + 6, f"{tick:.0f}%", size=18, fill="#777777", anchor="end"))
    body.append(svg_line(chart_x, chart_y + chart_h, chart_x + chart_w, chart_y + chart_h, stroke="#aaaaaa", width=1.3))
    body.append(svg_line(chart_x, chart_y, chart_x, chart_y + chart_h, stroke="#aaaaaa", width=1.3))
    body.append(svg_text(chart_x + chart_w / 2, chart_y + chart_h + 82, "Estimated cost (RMB, log scale)", size=22, weight=720, anchor="middle"))
    body.append(
        svg_text(
            chart_x - 100,
            chart_y + chart_h / 2,
            "Hard-gated O-Eval (%)",
            size=22,
            weight=720,
            anchor="middle",
            transform=f"rotate(-90 {chart_x - 100:.1f} {chart_y + chart_h / 2:.1f})",
        )
    )
    cost_threshold = 80.0
    score_threshold = 75.0
    if x_min < cost_threshold < x_max:
        body.append(svg_rect(chart_x, chart_y, sx(cost_threshold) - chart_x, sy(score_threshold) - chart_y, "#e8f7eb", opacity=0.75))
        body.append(svg_text(chart_x + 20, chart_y + 34, f"value zone: <=¥{cost_threshold:.0f}, >={score_threshold:.0f}% gated O", size=18, fill="#3f7f4a"))
        body.append(svg_line(sx(cost_threshold), chart_y, sx(cost_threshold), chart_y + chart_h, stroke="#9ca3af", dash="6 7"))
    body.append(svg_line(chart_x, sy(score_threshold), chart_x + chart_w, sy(score_threshold), stroke="#9ca3af", dash="6 7"))

    point_specs: list[tuple[str, float, float, list[str]]] = []
    for row in priced:
        x = sx(float(row.cost_rmb))
        y = sy((row.hard_gated_o_mean or 0.0) * 100.0)
        gate_suffix = "" if row.hard_gate_count == 0 else f", {row.hard_gate_count} gate"
        label = row.short if row.artifacts >= 18 else f"{row.short} ({row.artifacts}/18)"
        point_specs.append((row.model, x, y, [label, f"{(row.hard_gated_o_mean or 0.0) * 100:.1f}% / ¥{row.cost_rmb:.1f}{gate_suffix}"]))
    placements = place_point_labels(point_specs, (chart_x + 8, chart_y + 8, chart_x + chart_w - 8, chart_y + chart_h - 8))
    for row in priced:
        x = sx(float(row.cost_rmb))
        y = sy((row.hard_gated_o_mean or 0.0) * 100.0)
        radius = 9 + min(8, row.artifacts / 18 * 8)
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{row.color}" stroke="#ffffff" stroke-width="3"/>')
        label_x, label_y, anchor = placements[row.model]
        gate_suffix = "" if row.hard_gate_count == 0 else f", {row.hard_gate_count} gate"
        label = row.short if row.artifacts >= 18 else f"{row.short} ({row.artifacts}/18)"
        body.append(svg_text(label_x, label_y, label, size=19, weight=700, fill="#333333", anchor=anchor))
        body.append(svg_text(label_x, label_y + 24, f"{(row.hard_gated_o_mean or 0.0) * 100:.1f}% / ¥{row.cost_rmb:.1f}{gate_suffix}", size=17, weight=650, fill="#777777", anchor=anchor))

    body.append(svg_text(chart_x + chart_w / 2, height - 72, "The hard gate changes scores only where the artifact is clearly not a feasible solution; cost estimates are unchanged.", size=18, fill="#777777", anchor="middle"))
    return write_svg(FIGURES / "aa-style-2023-2025-hard-gated-o-eval-cost-scatter.svg", width, height, body)


def write_token_usage(summaries: list[Summary]) -> Path:
    width, height = 1800, 1060
    chart_x, chart_y, chart_w, chart_h = 132, 320, 1540, 430
    rows = sorted(summaries, key=lambda item: item.total_tokens)
    max_tokens = max(row.total_tokens for row in rows) / 1_000_000
    domain_max = math.ceil(max_tokens / 20.0) * 20.0
    body = [
        svg_rect(24, 24, width - 48, height - 48, "#ffffff", rx=16, stroke="#dedede"),
        svg_text(72, 126, "Token Usage", size=42, weight=500),
        svg_text(72, 168, "Input/cache/output usage in million tokens. Monitored Qwen cache counters use the supplied cached-read price.", size=22, weight=650, fill="#777777"),
    ]
    for tick in range(0, int(domain_max) + 1, 20):
        yy = y_scale(tick, chart_y, chart_h, domain_max)
        body.append(svg_line(chart_x, yy, chart_x + chart_w, yy, dash="4 8"))
        body.append(svg_text(chart_x - 18, yy + 6, f"{tick}M", size=18, fill="#777777", anchor="end"))
    gap = 30
    bar_w = (chart_w - gap * (len(rows) - 1)) / len(rows)
    for idx, row in enumerate(rows):
        x = chart_x + idx * (bar_w + gap)
        segments = [
            (row.billable_input_tokens, "#4c4c4c", "input"),
            (row.cache_tokens, "#cfcfcf", "cache"),
            (row.output_tokens, row.color, "output"),
        ]
        cursor = chart_y + chart_h
        for value, color, label in segments:
            if value <= 0:
                continue
            h = value / 1_000_000 / domain_max * chart_h
            cursor -= h
            body.append(svg_rect(x, cursor, bar_w, h, color, rx=5 if cursor <= chart_y + 5 else 0))
            if h > 42:
                body.append(svg_text(x + bar_w / 2, cursor + h / 2 + 6, f"{value / 1_000_000:.1f}", size=16, weight=800, fill="#ffffff", anchor="middle"))
        body.append(svg_text(x + bar_w / 2, cursor - 12, f"{row.total_tokens / 1_000_000:.1f}M", size=17, fill="#888888", anchor="middle"))
        label_lines = row.short.split(" ")
        if len(label_lines) > 2:
            label_lines = [" ".join(label_lines[:2]), " ".join(label_lines[2:])]
        for j, part in enumerate(label_lines):
            body.append(svg_text(x + bar_w / 2, chart_y + chart_h + 42 + j * 22, part, size=18, weight=700, anchor="middle"))
    body.append(svg_text(chart_x + chart_w / 2, height - 70, f"Cache-hit input is shown for capacity analysis; OpenRouter prices converted at USD/CNY {OPENROUTER_USD_TO_RMB}.", size=18, fill="#777777", anchor="middle"))
    return write_svg(FIGURES / "aa-style-2023-2025-token-usage.svg", width, height, body)


def write_figures(records: list[dict[str, Any]], summaries: list[Summary]) -> list[Path]:
    FIGURES.mkdir(parents=True, exist_ok=True)
    return [
        write_hard_gated_o_bar(summaries),
        write_hard_gated_o_score_cost_scatter(summaries),
        write_effect_bar(summaries),
        write_score_cost_scatter(summaries),
        write_split_bars(records, summaries, split="year", metric="o"),
        write_split_bars(records, summaries, split="suite", metric="o"),
        write_split_bars(records, summaries, split="year", metric="robust"),
        write_split_bars(records, summaries, split="suite", metric="robust"),
        write_token_usage(summaries),
    ]


def write_primary_aa_style_figures(report: Path) -> list[Path]:
    script = SCRIPTS / "write_aa_style_eval_figures.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--report-path",
            str(report),
            "--output-prefix",
            "aa-style-2023-2025",
        ],
        check=True,
    )
    names = [
        "aa-style-2023-2025-effect-bar.svg",
        "aa-style-2023-2025-effect-cost-scatter.svg",
        "aa-style-2023-2025-o-eval-bar.svg",
        "aa-style-2023-2025-o-eval-cost-scatter.svg",
        "aa-style-2023-2025-token-usage.svg",
        "aa-style-2023-2025-cost.svg",
    ]
    return [FIGURES / name for name in names]


def main() -> None:
    _, cases, records, summaries = compute()
    report = write_report(cases, records, summaries)
    paths = write_figures(records, summaries)
    paths.extend(write_primary_aa_style_figures(report))
    print(report)
    for path in paths:
        print(path)
        print(path.with_suffix(".png"))


if __name__ == "__main__":
    main()
