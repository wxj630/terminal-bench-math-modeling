# O-Eval and Robust BO-Eval: 2023-2025

Generated: 2026-09-14

Scope: 2023, 2024, and 2025 terminal-bench-math-modeling tasks, 18 tasks total. This report rescored saved artifacts only; it does not rerun models or modify job result files.

Primary O-Eval rule: `clamp(model direction-aware raw / O raw, 0, 1)`, averaged over all 18 tasks. Since the O-award reproduction is normalized near raw=1 on these tasks, O-Eval is the easiest-to-read absolute oracle-normalized score, and overshoots are capped at 100%.

Secondary Robust BO-Eval rule: let `gain = model raw - flash raw` and `gap = O raw - flash raw`. If `gap >= 0.10`, score `clip(gain / gap, -100%, +100%)`; otherwise score `clip(gain, -10pp, +10pp)`. Normal completed tasks still use the clipped fallback on tiny-gap cases, but any missing or non-scoreable artifact is assigned `-100%` so a completely unfinished task gets the worst possible score.

Tempered hard-gated rule: only clearly non-feasible cells are whole-task penalized. Automatic scorer hard-invalid metrics and manually replay-proven invalid high-score cells receive gated raw `0` for O-Eval and `-100%` for Robust BO-Eval. Needs-review/proxy cells remain scored but are not used as stronger-than-O claims without a better replay verifier.

Robust ratio tasks with gap >= 0.10: 11. Saturated or near-zero-gap tasks using clipped B-Eval: 7.

## Overall Mean

| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB | Canonical valid/running/error/pending | Excluded retries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| v4 flash baseline | 17 | 0.838752 | 58.14% | +0.00 pp | 0.00% | 33,032,997 / 31,802,112 / 1,896,174 | 1,230,885 / 1,896,174 | $0.683019 | ¥4.60 | 18/0/0/0 | 0 |
| opencode + deepseek-flash | 18 | 0.907032 | 62.19% | +6.83 pp | 12.24% | 89,376,395 / 88,668,288 / 569,862 | 708,107 / 569,862 | $2.536206 | ¥17.09 | 18/0/0/0 | 6 |
| codex + gpt-5.5 xhigh | 18 | 0.854280 | 64.29% | +1.55 pp | 17.03% | 108,584,170 / 105,199,744 / 994,910 | 3,384,426 / 994,910 | $99.369302 | ¥669.45 | 18/0/0/0 | 0 |
| v4 pro | 18 | 0.713865 | 58.44% | -12.49 pp | 6.91% | 21,309,105 / 20,096,768 / 1,748,356 | 1,212,337 / 1,748,356 | $10.247542 | ¥69.04 | 18/0/0/0 | 0 |
| GLM-5.3 | 18 | 0.646092 | 56.25% | -19.27 pp | 6.03% | 92,056,972 / 89,637,696 / 2,638,779 | 2,419,276 / 2,638,779 | $38.303415 | ¥258.05 | 18/0/0/0 | 0 |
| GPT-5.6 SOL high | 18 | 0.892644 | 60.10% | +5.39 pp | 10.01% | 8,774,606 / 7,566,848 / 497,473 | 1,207,758 / 497,473 | $8.903616 | ¥59.98 | 18/0/0/0 | 0 |
| GPT-5.6 SOL xhigh | 17 | 0.700131 | 56.84% | -13.86 pp | 3.68% | 16,596,399 / 14,928,768 / 841,198 | 1,667,631 / 841,198 | $14.732996 | ¥99.26 | 17/0/1/0 | 3 |
| Kimi K3 | 18 | 0.934701 | 64.24% | +9.59 pp | 21.27% | 30,146,116 / 28,928,953 / 956,805 | 1,217,163 / 956,805 | $24.687377 | ¥166.32 | 17/0/1/0 | 0 |
| Gemini 3.7 Flash high primary+retry | 15 | 0.674352 | 53.58% | -16.44 pp | -8.14% | 69,131,259 / 62,497,004 / 705,776 | 6,634,255 / 705,776 | $12.309627 | ¥82.93 | 18/0/0/0 | 1 |
| Qwen3.8-27B-FP8 thinking | 18 | 0.830722 | 62.24% | -0.80 pp | 16.30% | 47,245,909 / 0 / 3,178,409 | 47,245,909 / 3,178,409 | $18.215567 | ¥122.72 | 17/0/1/0 | 0 |
| GLM-5.3-Flash (ox-alpha) | 18 | 0.724187 | 55.09% | -11.46 pp | 4.93% | 107,726,029 / 101,466,688 / 3,683,366 | 6,259,341 / 3,683,366 | $2.912292 | ¥19.62 | 17/0/1/0 | 20 |
| Qwen3.8 Flash (Bailian) | 18 | 0.626646 | 51.32% | -21.21 pp | -1.82% | 299,616,972 / 293,563,264 / 6,814,374 | 6,053,708 / 6,814,374 | $8.807824 | ¥59.34 | 16/0/2/0 | 0 |
| Tencent Hy4 Preview | 18 | 0.912611 | 61.82% | +7.39 pp | 11.21% | 133,731,323 / 128,999,040 / 2,068,825 | 4,732,283 / 2,068,825 | $14.538815 | ¥97.95 | 18/0/0/0 | 0 |

## Tempered Hard-Gated Leaderboard

| Rank | Model | Hard-gated O-Eval | Hard-gated Robust BO-Eval | Original O-Eval | Original Robust BO-Eval | Hard-gated raw mean | Hard gates | Est. cost RMB |
|---:|---|---:|---:|---:|---:|---:|---|---:|
| 1 | codex + gpt-5.5 xhigh | 64.29% | 17.03% | 64.29% | 17.03% | 0.854280 | 0 | ¥669.45 |
| 2 | Qwen3.8-27B-FP8 thinking | 62.24% | 16.30% | 62.24% | 16.30% | 0.830722 | 0 | ¥122.72 |
| 3 | opencode + deepseek-flash | 62.19% | 12.24% | 62.19% | 12.24% | 0.907032 | 0 | ¥17.09 |
| 4 | Tencent Hy4 Preview | 61.82% | 11.21% | 61.82% | 11.21% | 0.912611 | 0 | ¥97.95 |
| 5 | GPT-5.6 SOL high | 60.10% | 10.45% | 60.10% | 10.01% | 0.892644 | 0 | ¥59.98 |
| 6 | v4 pro | 58.44% | 6.91% | 58.44% | 6.91% | 0.713865 | 0 | ¥69.04 |
| 7 | GPT-5.6 SOL xhigh | 56.84% | 3.68% | 56.84% | 3.68% | 0.700131 | 0 | ¥99.26 |
| 8 | v4 flash baseline | 54.04% | 0.00% | 58.14% | 0.00% | 0.797740 | 1: `cumcm-2023-a-heliostat-field` | ¥4.60 |
| 9 | Kimi K3 | 53.13% | 4.43% | 64.24% | 21.27% | 0.687166 | 2: `mcm-2025-b-juneau-tourism`, `mcm-2025-c-olympic-medals` | ¥166.32 |
| 10 | Qwen3.8 Flash (Bailian) | 51.32% | -1.82% | 51.32% | -1.82% | 0.626646 | 0 | ¥59.34 |
| 11 | GLM-5.3 | 50.70% | -5.09% | 56.25% | 6.03% | 0.568674 | 1: `cumcm-2023-a-heliostat-field` | ¥258.05 |
| 12 | GLM-5.3-Flash (ox-alpha) | 49.53% | -1.18% | 55.09% | 4.93% | 0.582372 | 1: `cumcm-2025-a-smoke-screen` | ¥19.62 |
| 13 | Gemini 3.7 Flash high primary+retry | 48.20% | -18.60% | 53.58% | -8.14% | 0.620518 | 1: `cumcm-2023-a-heliostat-field` | ¥82.93 |

## Hard Gate Decisions

| Model | Task | Raw before gate | Gated raw | O-Eval before | Hard-gated O-Eval | Robust before | Hard-gated Robust | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|
| v4 flash baseline | `cumcm-2023-a-heliostat-field` | 0.738213 | 0.000000 | 73.82% | 0.00% | 0.00% | 0.00% | hard-invalid/heliostat-constraint: Q2 rated-power constraint violation: 53.795541 MW is below the required approximately 60 MW; Q3 rated-power constraint violation: 53.795541 MW is below the required approximately 60 MW; Q3 does not expose numeric mirror dimensions |
| GLM-5.3 | `cumcm-2023-a-heliostat-field` | 1.393536 | 0.000000 | 100.00% | 0.00% | 100.00% | -100.00% | explicit Q3 design note violates heliostat installation-height bound: one tail mirror uses z=1.9024 m, below the required 2 m minimum |
| Gemini 3.7 Flash high primary+retry | `cumcm-2023-a-heliostat-field` | 0.969010 | 0.000000 | 96.90% | 0.00% | 88.16% | -100.00% | hard-invalid/heliostat-constraint: Question 2 rated-power constraint violation: 55.460000 MW is below the required approximately 60 MW; Question 3 rated-power constraint violation: 54.966000 MW is below the required approximately 60 MW |
| GLM-5.3-Flash (ox-alpha) | `cumcm-2025-a-smoke-screen` | 2.552664 | 0.000000 | 100.00% | 0.00% | 10.00% | -100.00% | independent smoke-screen replay gives 0.00s coverage under O-reference line-of-sight geometry |
| Kimi K3 | `mcm-2025-b-juneau-tourism` | 1.460140 | 0.000000 | 100.00% | 0.00% | 100.00% | -100.00% | unit/scale invalid: resident_acceptance_index=1.5 and sustainability_score=232.2 on a unit-scale score |
| Kimi K3 | `mcm-2025-c-olympic-medals` | 2.995504 | 0.000000 | 100.00% | 0.00% | 10.00% | -100.00% | invalid high coach-effect result: only three scored recommendations and endpoint verifier reward is negative/BO 0 |

## Primary Readout

- 18-task primary O-Eval ranking: codex + gpt-5.5 xhigh (64.29%) > Kimi K3 (64.24%) > Qwen3.8-27B-FP8 thinking (62.24%) > opencode + deepseek-flash (62.19%) > Tencent Hy4 Preview (61.82%) > GPT-5.6 SOL high (60.10%) > v4 pro (58.44%) > GPT-5.6 SOL xhigh (56.84%) > GLM-5.3 (56.25%) > GLM-5.3-Flash (ox-alpha) (55.09%) > Gemini 3.7 Flash high primary+retry (53.58%) > Qwen3.8 Flash (Bailian) (51.32%).
- Tempered hard-gated O-Eval ranking: codex + gpt-5.5 xhigh (64.29%) > Qwen3.8-27B-FP8 thinking (62.24%) > opencode + deepseek-flash (62.19%) > Tencent Hy4 Preview (61.82%) > GPT-5.6 SOL high (60.10%) > v4 pro (58.44%) > GPT-5.6 SOL xhigh (56.84%) > Kimi K3 (53.13%) > Qwen3.8 Flash (Bailian) (51.32%) > GLM-5.3 (50.70%) > GLM-5.3-Flash (ox-alpha) (49.53%) > Gemini 3.7 Flash high primary+retry (48.20%).
- Secondary Robust BO-Eval ranking: Kimi K3 (21.27%) > codex + gpt-5.5 xhigh (17.03%) > Qwen3.8-27B-FP8 thinking (16.30%) > opencode + deepseek-flash (12.24%) > Tencent Hy4 Preview (11.21%) > GPT-5.6 SOL high (10.01%) > v4 pro (6.91%) > GLM-5.3 (6.03%) > GLM-5.3-Flash (ox-alpha) (4.93%) > GPT-5.6 SOL xhigh (3.68%) > Qwen3.8 Flash (Bailian) (-1.82%) > Gemini 3.7 Flash high primary+retry (-8.14%).
- Tempered hard-gated Robust BO-Eval ranking: codex + gpt-5.5 xhigh (17.03%) > Qwen3.8-27B-FP8 thinking (16.30%) > opencode + deepseek-flash (12.24%) > Tencent Hy4 Preview (11.21%) > GPT-5.6 SOL high (10.45%) > v4 pro (6.91%) > Kimi K3 (4.43%) > GPT-5.6 SOL xhigh (3.68%) > GLM-5.3-Flash (ox-alpha) (-1.18%) > Qwen3.8 Flash (Bailian) (-1.82%) > GLM-5.3 (-5.09%) > Gemini 3.7 Flash high primary+retry (-18.60%).
- These two metrics are complementary, not competing: O-Eval is the absolute oracle-normalized score for the headline leaderboard, while Robust BO-Eval is the baseline-relative gain view. If the rankings disagree, it usually means a model is closer to O in absolute terms but does not pull as far ahead of flash, or it gains a lot on a few weak-baseline tasks without being closest overall. This report therefore uses O-Eval as the final ranking and Robust BO-Eval as a diagnostic view.
- The hard-gated tables are the cautious public-facing view: they keep the normal O-Eval leaderboard visible, but remove credit from cells that are clearly not feasible solutions.
- The GLM-5.3-Flash vs DeepSeek flash difference is a good example: Robust can favor the model that moves farther above flash, while O-Eval still favors the model that lands closer to the oracle anchor.
- v4 flash baseline now uses the 4-hour rerun jobs: `terminus2-deepseek-v4-flash-0731-rerun-2023-2025-cumcm` and `terminus2-deepseek-v4-flash-0731-rerun-2023-2025-mcm`.
- Cost is estimated from OpenRouter model catalog prices (`prompt`, `input_cache_read`, `input_cache_write`, `completion`) converted from USD/token to RMB/M tokens at USD/CNY=6.737012.
- Token/cost totals use exactly one canonical trial per model x task. A valid artifact outranks a live trajectory; retries are retained in the audit but excluded from these totals.
- Cost is an evaluation-normalized estimate, not the actual OpenRouter Activity/Usage bill. Activity/Usage includes every request from retries and is the authority for actual spend.
- Cache-hit input is charged using `input_cache_read`; explicit cache write/create is not added because trial result files expose no cache-write token counter.
- No peer-average cache imputation is used. Cache tokens in this report are the raw per-trial counters; Qwen3.8 Flash uses the supplied OpenRouter cached-read price.
- Fixed monitored prices: GLM-5.3-Flash (ox-alpha) input $0.075/M, cached read $0.015/M, output $0.25/M; Qwen3.8 Flash (Bailian) input $0.15/M, cached read $0.016/M, cached write $0.20/M, output $0.47/M. The requested estimate uses input, cached-read, and output counters; no cache-write token counter is available.
- GLM-5.3-Flash (ox-alpha) has 17 valid completed tasks and one final model-timeout failure on `cumcm-2023-a-heliostat-field`; that task is excluded from valid results and will not be retried.
- Per-task selection audit: `model-token-audit-2023-2025.json`.
- Price snapshot used by this run: `openrouter-pricing-used-2023-2025.json`.
- Claude Opus 5 is not listed because no completed artifacts were present in the workspace for the 18-task scope.

## Price Table

| Model | OpenRouter model | Price source | Input | Cached read | Cache write/create | Output |
|---|---|---|---:|---:|---:|---:|
| v4 flash baseline | `deepseek/deepseek-v4-flash-0731` | OpenRouter live | ¥0.4042/M | ¥0.0808/M | N/A | ¥0.8084/M |
| opencode + deepseek-flash | `deepseek/deepseek-v4.1-flash` | OpenRouter live | ¥2.0211/M | ¥0.0404/M | N/A | ¥8.0844/M |
| codex + gpt-5.5 xhigh | `openai/gpt-5.5` | OpenRouter live | ¥33.6851/M | ¥3.3685/M | N/A | ¥202.1104/M |
| v4 pro | `deepseek/deepseek-v4-pro` | OpenRouter live | ¥10.7792/M | ¥0.9095/M | N/A | ¥21.5584/M |
| GLM-5.3 | `z-ai/glm-5.3` | OpenRouter live | ¥9.4318/M | ¥1.7516/M | N/A | ¥29.6429/M |
| GPT-5.6 SOL high | `openai/gpt-5.6-sol` | OpenRouter live | ¥13.4740/M | ¥1.3474/M | ¥16.8425/M | ¥67.3701/M |
| GPT-5.6 SOL xhigh | `openai/gpt-5.6-sol` | OpenRouter live | ¥13.4740/M | ¥1.3474/M | ¥16.8425/M | ¥67.3701/M |
| Kimi K3 | `moonshotai/kimi-k3` | OpenRouter live | ¥17.8405/M | ¥2.0389/M | N/A | ¥89.4859/M |
| Gemini 3.7 Flash high primary+retry | `google/gemini-3.7-flash` | OpenRouter live | ¥5.0528/M | ¥0.5053/M | ¥0.2807/M | ¥25.2638/M |
| Qwen3.8-27B-FP8 thinking | `qwen/qwen3.8-27b` | OpenRouter live | ¥1.4417/M | ¥1.0106/M | ¥3.5790/M | ¥17.1794/M |
| GLM-5.3-Flash (ox-alpha) | `z-ai/glm-5.3-flash` | user-supplied fixed snapshot | ¥0.5053/M | ¥0.1011/M | N/A | ¥1.6843/M |
| Qwen3.8 Flash (Bailian) | `qwen/qwen3.8-flash` | user-supplied fixed snapshot | ¥1.0106/M | ¥0.1078/M | ¥1.3474/M | ¥3.1664/M |
| Tencent Hy4 Preview | `tencent/hy4-preview` | OpenRouter live | ¥5.6187/M | ¥0.2830/M | N/A | ¥16.8493/M |

## Figures

- Clickable dashboard: `terminus2-bo-eval-aa-dashboard-2023-2025.html`
- All-model feasibility audit: `terminus2-all-model-feasibility-audit-2023-2025.md`
- Hard-gated O-Eval effect: `figures/aa-style-2023-2025-hard-gated-o-eval-bar.png`
- Hard-gated O-Eval score-cost: `figures/aa-style-2023-2025-hard-gated-o-eval-cost-scatter.png`
- O-Eval effect: `figures/aa-style-2023-2025-o-eval-bar.png`
- O-Eval score-cost: `figures/aa-style-2023-2025-o-eval-cost-scatter.png`
- Robust BO-Eval effect: `figures/aa-style-2023-2025-boeval-effect-bar.png`
- Robust BO-Eval score-cost: `figures/aa-style-2023-2025-boeval-score-cost.png`
- Token usage: `figures/aa-style-2023-2025-token-usage.png`
- Cost: `figures/aa-style-2023-2025-cost.png`
- O-Eval year split: `figures/aa-style-2023-2025-o-eval-year-split.png`
- O-Eval suite split: `figures/aa-style-2023-2025-o-eval-suite-split.png`
- Diagnostic Robust BO-Eval year split: `figures/aa-style-2023-2025-boeval-year-split.png`
- Diagnostic Robust BO-Eval suite split: `figures/aa-style-2023-2025-boeval-suite-split.png`

## Year Mean O-Eval

| Model | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| v4 flash baseline | 67.74% | 39.66% | 67.03% |
| opencode + deepseek-flash | 77.94% | 48.40% | 60.23% |
| codex + gpt-5.5 xhigh | 66.93% | 63.53% | 62.39% |
| v4 pro | 62.17% | 56.92% | 56.23% |
| GLM-5.3 | 65.89% | 40.12% | 62.76% |
| GPT-5.6 SOL high | 78.80% | 45.39% | 56.12% |
| GPT-5.6 SOL xhigh | 55.56% | 57.06% | 57.90% |
| Kimi K3 | 62.00% | 51.89% | 78.83% |
| Gemini 3.7 Flash high primary+retry | 59.63% | 44.05% | 57.08% |
| Qwen3.8-27B-FP8 thinking | 76.73% | 64.08% | 45.90% |
| GLM-5.3-Flash (ox-alpha) | 60.91% | 56.39% | 47.97% |
| Qwen3.8 Flash (Bailian) | 57.70% | 38.06% | 58.22% |
| Tencent Hy4 Preview | 82.82% | 43.08% | 59.57% |

## Suite Mean O-Eval

| Model | CUMCM | MCM |
|---|---:|---:|
| v4 flash baseline | 79.24% | 37.04% |
| opencode + deepseek-flash | 87.82% | 36.55% |
| codex + gpt-5.5 xhigh | 88.23% | 40.34% |
| v4 pro | 78.07% | 38.81% |
| GLM-5.3 | 68.05% | 44.46% |
| GPT-5.6 SOL high | 81.89% | 38.31% |
| GPT-5.6 SOL xhigh | 68.89% | 44.79% |
| Kimi K3 | 85.82% | 42.67% |
| Gemini 3.7 Flash high primary+retry | 87.97% | 19.20% |
| Qwen3.8-27B-FP8 thinking | 87.28% | 37.20% |
| GLM-5.3-Flash (ox-alpha) | 73.12% | 37.06% |
| Qwen3.8 Flash (Bailian) | 67.81% | 34.84% |
| Tencent Hy4 Preview | 77.94% | 45.70% |

## Year Mean Robust BO-Eval

| Model | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 0.00% |
| opencode + deepseek-flash | 22.00% | 24.98% | -10.25% |
| codex + gpt-5.5 xhigh | 14.93% | 45.70% | -9.55% |
| v4 pro | 9.43% | 27.49% | -16.18% |
| GLM-5.3 | 19.52% | 5.94% | -7.38% |
| GPT-5.6 SOL high | 22.65% | 21.52% | -14.13% |
| GPT-5.6 SOL xhigh | -20.25% | 40.49% | -9.21% |
| Kimi K3 | 9.51% | 38.23% | 16.06% |
| Gemini 3.7 Flash high primary+retry | -4.74% | -6.87% | -12.83% |
| Qwen3.8-27B-FP8 thinking | 19.69% | 47.01% | -17.79% |
| GLM-5.3-Flash (ox-alpha) | -12.77% | 39.99% | -12.44% |
| Qwen3.8 Flash (Bailian) | 9.30% | -2.52% | -12.25% |
| Tencent Hy4 Preview | 29.83% | 12.65% | -8.84% |

## Suite Mean Robust BO-Eval

| Model | CUMCM | MCM | CUMCM artifacts | MCM artifacts |
|---|---:|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 8 | 9 |
| opencode + deepseek-flash | 24.62% | -0.13% | 9 | 9 |
| codex + gpt-5.5 xhigh | 27.16% | 6.89% | 9 | 9 |
| v4 pro | 11.41% | 2.42% | 9 | 9 |
| GLM-5.3 | 1.56% | 10.49% | 9 | 9 |
| GPT-5.6 SOL high | 12.39% | 7.63% | 9 | 9 |
| GPT-5.6 SOL xhigh | -4.35% | 11.70% | 8 | 9 |
| Kimi K3 | 27.00% | 15.53% | 9 | 9 |
| Gemini 3.7 Flash high primary+retry | 13.34% | -29.63% | 9 | 6 |
| Qwen3.8-27B-FP8 thinking | 21.38% | 11.21% | 9 | 9 |
| GLM-5.3-Flash (ox-alpha) | -1.08% | 10.94% | 8 | 9 |
| Qwen3.8 Flash (Bailian) | -9.14% | 5.49% | 7 | 9 |
| Tencent Hy4 Preview | 4.48% | 17.94% | 9 | 9 |

## Saturated Or Near-Zero Gap Cases

| Year | Suite | Problem | Task | flash raw | O raw |
|---:|---|---|---|---:|---:|
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.492402 | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.550299 | 1.000000 |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 1.347590 | 1.000000 |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 1.527989 | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.506359 | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.632029 | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.575307 | 1.000000 |

## Per-Task Values

Cells are `direction-aware raw / O-Eval % / B-Eval vs flash / Robust BO-Eval %`.

| Year | Suite | Problem | Task | v4 flash baseline | opencode + deepseek-flash | codex + gpt-5.5 xhigh | v4 pro | GLM-5.3 | GPT-5.6 SOL high | GPT-5.6 SOL xhigh | Kimi K3 | Gemini 3.7 Flash high primary+retry | Qwen3.8-27B-FP8 thinking | GLM-5.3-Flash (ox-alpha) | Qwen3.8 Flash (Bailian) | Tencent Hy4 Preview | O raw |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 0.738213 / 73.82% / 0.00% / 0.00% | 1.103930 / 100.00% / 139.70% / 100.00% | 1.097346 / 100.00% / 137.19% / 100.00% | 1.312936 / 100.00% / 219.54% / 100.00% | 1.393536 / 100.00% / 250.33% / 100.00% | 0.971969 / 97.20% / 89.29% / 89.29% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.975341 / 97.53% / 90.58% / 90.58% | 0.969010 / 96.90% / 88.16% / 88.16% | 1.244533 / 100.00% / 193.41% / 100.00% | 0.000000 / 0.00% / 0.00% / -100.00% | 1.455864 / 100.00% / 274.14% / 100.00% | 1.464003 / 100.00% / 277.24% / 100.00% | 1.000000 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.492402 / 100.00% / 0.00% / 0.00% | 1.566098 / 100.00% / N/A / 7.37% | 2.542996 / 100.00% / N/A / 10.00% | 1.496072 / 100.00% / N/A / 0.37% | 1.500666 / 100.00% / N/A / 0.83% | 2.425664 / 100.00% / N/A / 10.00% | 1.463138 / 100.00% / N/A / -2.93% | 1.410390 / 100.00% / N/A / -8.20% | 1.496423 / 100.00% / N/A / 0.40% | 1.501820 / 100.00% / N/A / 0.94% | 1.500621 / 100.00% / N/A / 0.82% | 1.542730 / 100.00% / N/A / 5.03% | 2.349865 / 100.00% / N/A / 10.00% | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.550299 / 100.00% / 0.00% / 0.00% | 1.714187 / 100.00% / N/A / -10.00% | 1.635081 / 100.00% / N/A / -10.00% | 0.597918 / 59.79% / N/A / -10.00% | 0.355098 / 35.51% / N/A / -10.00% | 1.589944 / 100.00% / N/A / -10.00% | 1.427361 / 100.00% / N/A / -10.00% | 1.134708 / 100.00% / N/A / -10.00% | 2.523435 / 100.00% / N/A / -2.69% | 1.292870 / 100.00% / N/A / -10.00% | 1.707570 / 100.00% / N/A / -10.00% | 1.755009 / 100.00% / N/A / -10.00% | 0.963631 / 96.36% / N/A / -10.00% | 1.000000 |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 1.347590 / 100.00% / 0.00% / 0.00% | 0.498202 / 49.82% / N/A / -10.00% | 0.498202 / 49.82% / N/A / -10.00% | 0.999998 / 100.00% / N/A / -10.00% | 0.498202 / 49.82% / N/A / -10.00% | 0.498202 / 49.82% / N/A / -10.00% | 0.498202 / 49.82% / N/A / -10.00% | 0.075390 / 7.54% / N/A / -10.00% | 1.000000 / 100.00% / N/A / -10.00% | 0.498231 / 49.82% / N/A / -10.00% | 0.498202 / 49.82% / N/A / -10.00% | 0.498202 / 49.82% / N/A / -10.00% | 0.498202 / 49.82% / N/A / -10.00% | 1.000000 |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.737706 / 73.77% / 73.77% / 73.77% | 0.788883 / 78.89% / 78.89% / 78.89% | 0.318573 / 31.86% / 31.86% / 31.86% | 0.257329 / 25.73% / 25.73% / 25.73% | 0.444542 / 44.45% / 44.45% / 44.45% | 0.479172 / 47.92% / 47.92% / 47.92% | 0.943081 / 94.31% / 94.31% / 94.31% | 0.469069 / 46.91% / 46.91% / 46.91% | 1.445692 / 100.00% / 144.57% / 100.00% | 0.390214 / 39.02% / 39.02% / 39.02% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.366504 / 36.65% / 36.65% / 36.65% | 1.000000 |
| 2024 | CUMCM | C | `cumcm-2024-c-crop-planting` | 0.631481 / 63.15% / 0.00% / 0.00% | 1.593766 / 100.00% / 261.12% / 100.00% | 1.361571 / 100.00% / 198.11% / 100.00% | 1.448533 / 100.00% / 221.71% / 100.00% | 0.455660 / 45.57% / 0.00% / -47.71% | 0.918474 / 91.85% / 77.88% / 77.88% | 1.015015 / 100.00% / 104.07% / 100.00% | 1.076446 / 100.00% / 120.74% / 100.00% | 0.756826 / 75.68% / 34.01% / 34.01% | 1.081087 / 100.00% / 122.00% / 100.00% | 1.121885 / 100.00% / 133.07% / 100.00% | 0.939687 / 93.97% / 83.63% / 83.63% | 0.625186 / 62.52% / 0.00% / -1.71% | 1.000000 |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 1.527989 / 100.00% / 0.00% / 0.00% | 3.578239 / 100.00% / N/A / 10.00% | 1.829285 / 100.00% / N/A / 10.00% | 1.532372 / 100.00% / N/A / 0.44% | 0.854445 / 85.44% / N/A / -10.00% | 3.416382 / 100.00% / N/A / 10.00% | 0.939201 / 93.92% / N/A / -10.00% | 2.894037 / 100.00% / N/A / 10.00% | 1.239279 / 100.00% / N/A / -10.00% | 2.591825 / 100.00% / N/A / 10.00% | 2.552664 / 100.00% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 4.004026 / 100.00% / N/A / 10.00% | 1.000000 |
| 2025 | CUMCM | B | `cumcm-2025-b-sic-thickness` | 0.762319 / 76.23% / 0.00% / 0.00% | 0.668246 / 66.82% / 0.00% / -39.58% | 0.704257 / 70.43% / 0.00% / -24.43% | 0.109821 / 10.98% / 0.00% / -100.00% | 0.703334 / 70.33% / 0.00% / -24.82% | 0.537264 / 53.73% / 0.00% / -94.69% | 0.657456 / 65.75% / 0.00% / -44.12% | 0.729831 / 72.98% / 0.00% / -13.67% | 0.722558 / 72.26% / 0.00% / -16.73% | 0.357013 / 35.70% / 0.00% / -100.00% | 0.691962 / 69.20% / 0.00% / -29.60% | 0.664995 / 66.50% / 0.00% / -40.95% | 0.561223 / 56.12% / 0.00% / -84.61% | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.506359 / 100.00% / 0.00% / 0.00% | 1.235518 / 100.00% / N/A / -10.00% | 0.949136 / 94.91% / N/A / -10.00% | 1.360909 / 100.00% / N/A / -10.00% | 1.071182 / 100.00% / N/A / -10.00% | 1.452420 / 100.00% / N/A / -5.39% | 0.626050 / 62.60% / N/A / -10.00% | 1.289804 / 100.00% / N/A / -10.00% | 1.234068 / 100.00% / N/A / -10.00% | 1.521520 / 100.00% / N/A / 1.52% | 1.073057 / 100.00% / N/A / -10.00% | 1.287680 / 100.00% / N/A / -10.00% | 1.184644 / 100.00% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.632029 / 100.00% / 0.00% / 0.00% | 1.340862 / 100.00% / N/A / -10.00% | 0.702577 / 70.26% / N/A / -10.00% | 1.179422 / 100.00% / N/A / -10.00% | 1.538784 / 100.00% / N/A / -9.32% | 1.364424 / 100.00% / N/A / -10.00% | 1.364410 / 100.00% / N/A / -10.00% | 0.469546 / 46.95% / N/A / -10.00% | 0.545375 / 54.54% / N/A / -10.00% | 1.070439 / 100.00% / N/A / -10.00% | 1.163407 / 100.00% / N/A / -10.00% | 0.373162 / 37.32% / N/A / -10.00% | 1.296434 / 100.00% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | 0.102093 / 10.21% / 0.00% / 0.00% | 0.130340 / 13.03% / 3.15% / 3.15% | 0.033496 / 3.35% / 0.00% / -7.64% | 0.034371 / 3.44% / 0.00% / -7.54% | 0.068142 / 6.81% / 0.00% / -3.78% | 0.032355 / 3.24% / 0.00% / -7.77% | 0.073712 / 7.37% / 0.00% / -3.16% | 0.028745 / 2.87% / 0.00% / -8.17% | 0.063352 / 6.34% / 0.00% / -4.31% | 0.024041 / 2.40% / 0.00% / -8.69% | 0.088569 / 8.86% / 0.00% / -1.51% | 0.023241 / 2.32% / 0.00% / -8.78% | 0.022503 / 2.25% / 0.00% / -8.86% | 1.000000 |
| 2023 | MCM | C | `mcm-2023-c-wordle` | 0.224201 / 22.42% / 0.00% / 0.00% | 0.546040 / 54.60% / 41.48% / 41.48% | 0.280001 / 28.00% / 7.19% / 7.19% | 0.097978 / 9.80% / 0.00% / -16.27% | 0.529999 / 53.00% / 39.42% / 39.42% | 0.723478 / 72.35% / 64.36% / 64.36% | 0.259776 / 25.98% / 4.59% / 4.59% | 0.246521 / 24.65% / 2.88% / 2.88% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.580000 / 58.00% / 45.86% / 45.86% | 0.565840 / 56.58% / 44.04% / 44.04% | 0.065441 / 6.54% / 0.00% / -20.46% | 0.983080 / 98.31% / 97.82% / 97.82% | 1.000000 |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | 0.070175 / 7.02% / 0.00% / 0.00% | 0.070175 / 7.02% / 0.00% / 0.00% | 0.265383 / 26.54% / 20.99% / 20.99% | 0.235294 / 23.53% / 17.76% / 17.76% | 0.125000 / 12.50% / 5.90% / 5.90% | 0.070175 / 7.02% / 0.00% / 0.00% | 0.070175 / 7.02% / 0.00% / 0.00% | 0.246711 / 24.67% / 18.99% / 18.99% | 0.228957 / 22.90% / 17.08% / 17.08% | 0.070175 / 7.02% / 0.00% / 0.00% | 0.089589 / 8.96% / 2.09% / 2.09% | 0.108108 / 10.81% / 4.08% / 4.08% | 0.015564 / 1.56% / 0.00% / -5.87% | 1.000000 |
| 2024 | MCM | B | `mcm-2024-b-submersible-search` | 0.371417 / 37.14% / 0.00% / 0.00% | 0.212392 / 21.24% / 0.00% / -25.30% | 0.403101 / 40.31% / 5.04% / 5.04% | 0.296505 / 29.65% / 0.00% / -11.92% | 0.709302 / 70.93% / 53.75% / 53.75% | 0.389026 / 38.90% / 2.80% / 2.80% | 0.662162 / 66.22% / 46.25% / 46.25% | 0.470888 / 47.09% / 15.82% / 15.82% | 0.187946 / 18.79% / 0.00% / -29.19% | 0.753209 / 75.32% / 60.74% / 60.74% | 0.632353 / 63.24% / 41.51% / 41.51% | 0.272873 / 27.29% / 0.00% / -15.68% | 0.300348 / 30.03% / 0.00% / -11.31% | 1.000000 |
| 2024 | MCM | C | `mcm-2024-c-tennis-momentum` | 0.306291 / 30.63% / 0.00% / 0.00% | 0.385581 / 38.56% / 11.43% / 11.43% | 0.856263 / 85.63% / 79.28% / 79.28% | 0.564619 / 56.46% / 37.24% / 37.24% | 0.361433 / 36.14% / 7.95% / 7.95% | 0.403266 / 40.33% / 13.98% / 13.98% | 0.713777 / 71.38% / 58.74% / 58.74% | 0.377542 / 37.75% / 10.27% / 10.27% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.523386 / 52.34% / 31.29% / 31.29% | 0.773319 / 77.33% / 67.32% / 67.32% | 0.464638 / 46.46% / 22.83% / 22.83% | 0.778964 / 77.90% / 68.14% / 68.14% | 1.000000 |
| 2025 | MCM | A | `mcm-2025-a-stair-wear` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.233333 / 23.33% / 23.33% / 23.33% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2025 | MCM | B | `mcm-2025-b-juneau-tourism` | 0.259364 / 25.94% / 0.00% / 0.00% | 0.171015 / 17.10% / 0.00% / -11.93% | 0.090096 / 9.01% / 0.00% / -22.85% | 0.426076 / 42.61% / 22.51% / 22.51% | 0.337214 / 33.72% / 10.51% / 10.51% | 0.372904 / 37.29% / 15.33% / 15.33% | 0.251056 / 25.11% / 0.00% / -1.12% | 1.460140 / 100.00% / 162.13% / 100.00% | 0.702044 / 70.20% / 59.77% / 59.77% | 0.025227 / 2.52% / 0.00% / -31.61% | 0.000000 / 0.00% / 0.00% / -35.02% | 0.907133 / 90.71% / 87.46% / 87.46% | 0.567213 / 56.72% / 41.57% / 41.57% | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.575307 / 100.00% / 0.00% / 0.00% | 0.774277 / 77.43% / N/A / -10.00% | 1.339365 / 100.00% / N/A / -10.00% | 0.838169 / 83.82% / N/A / -10.00% | 0.870336 / 87.03% / N/A / -10.00% | 0.457106 / 45.71% / N/A / -10.00% | 2.101688 / 100.00% / N/A / 10.00% | 2.995504 / 100.00% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 0.138589 / 13.86% / N/A / -10.00% | 0.186115 / 18.61% / N/A / -10.00% | 0.920868 / 92.09% / N/A / -10.00% | 0.445610 / 44.56% / N/A / -10.00% | 1.000000 |