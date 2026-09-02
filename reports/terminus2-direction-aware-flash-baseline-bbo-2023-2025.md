# O-Eval and Robust BO-Eval: 2023-2025

Generated: 2026-09-02

Scope: 2023, 2024, and 2025 terminal-bench-math-modeling tasks, 18 tasks total. This report rescored saved artifacts only; it does not rerun models or modify job result files.

Primary O-Eval rule: `model direction-aware raw / O raw`, averaged over all 18 tasks. Since the O-award reproduction is normalized near raw=1 on these tasks, O-Eval is the easiest-to-read absolute oracle-normalized score.

Secondary Robust BO-Eval rule: let `gain = model raw - flash raw` and `gap = O raw - flash raw`. If `gap >= 0.10`, score `clip(gain / gap, -100%, +100%)`; otherwise score `clip(gain, -10pp, +10pp)`. Normal completed tasks still use the clipped fallback on tiny-gap cases, but any missing or non-scoreable artifact is assigned `-100%` so a completely unfinished task gets the worst possible score.

Tempered hard-gated rule: only clearly non-feasible cells are whole-task penalized. Automatic scorer hard-invalid metrics and manually replay-proven invalid high-score cells receive gated raw `0` for O-Eval and `-100%` for Robust BO-Eval. Needs-review/proxy cells remain scored but are not used as stronger-than-O claims without a better replay verifier.

Robust ratio tasks with gap >= 0.10: 12. Saturated or near-zero-gap tasks using clipped B-Eval: 6.

## Overall Mean

| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB | Canonical valid/running/error/pending | Excluded retries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| v4 flash baseline | 17 | 0.756518 | 75.65% | +0.00 pp | 0.00% | 33,032,997 / 31,802,112 / 1,896,174 | 1,230,885 / 1,896,174 | $0.930153 | ¥6.27 | 18/0/0/0 | 0 |
| v4 pro | 18 | 0.618719 | 61.87% | -13.78 pp | 2.28% | 21,309,105 / 20,096,768 / 1,748,356 | 1,212,337 / 1,748,356 | $6.653558 | ¥44.83 | 18/0/0/0 | 0 |
| GLM-5.3 | 18 | 0.598189 | 59.82% | -15.83 pp | 5.45% | 92,056,972 / 89,637,696 / 2,638,779 | 2,419,276 / 2,638,779 | $38.303415 | ¥258.05 | 18/0/0/0 | 0 |
| GPT-5.6 SOL high | 18 | 0.841554 | 84.16% | +8.50 pp | 8.08% | 8,774,606 / 7,566,848 / 497,473 | 1,207,758 / 497,473 | $8.903616 | ¥59.98 | 18/0/0/0 | 0 |
| Kimi K3 | 18 | 0.868798 | 86.88% | +11.23 pp | 12.19% | 30,146,116 / 28,928,953 / 956,805 | 1,217,163 / 956,805 | $26.682250 | ¥179.76 | 17/0/1/0 | 0 |
| Gemini 3.7 Flash high primary+retry | 15 | 0.578610 | 57.86% | -17.79 pp | -14.37% | 69,131,259 / 62,497,004 / 705,776 | 6,634,255 / 705,776 | $12.309627 | ¥82.93 | 18/0/0/0 | 1 |
| Qwen3.8-27B-FP8 thinking | 18 | 0.754457 | 75.45% | -0.21 pp | 9.94% | 47,245,909 / 0 / 3,178,409 | 47,245,909 / 3,178,409 | $28.184454 | ¥189.88 | 17/0/1/0 | 0 |
| GLM-5.3-Flash (ox-alpha) | 18 | 0.655886 | 65.59% | -10.06 pp | -1.46% | 107,726,029 / 101,466,688 / 3,683,366 | 6,259,341 / 3,683,366 | $2.912292 | ¥19.62 | 17/0/1/0 | 20 |
| Qwen3.8 Flash (Bailian) | 18 | 0.564887 | 56.49% | -19.16 pp | -7.33% | 299,616,972 / 293,563,264 / 6,814,374 | 6,053,708 / 6,814,374 | $8.807824 | ¥59.34 | 16/0/2/0 | 0 |
| Tencent Hy4 Preview | 18 | 0.865183 | 86.52% | +10.87 pp | 11.70% | 133,731,323 / 128,999,040 / 2,068,825 | 4,732,283 / 2,068,825 | $14.538815 | ¥97.95 | 18/0/0/0 | 0 |

## Tempered Hard-Gated Leaderboard

| Rank | Model | Hard-gated O-Eval | Hard-gated Robust BO-Eval | Original O-Eval | Original Robust BO-Eval | Hard-gated raw mean | Hard gates | Est. cost RMB |
|---:|---|---:|---:|---:|---:|---:|---|---:|
| 1 | Tencent Hy4 Preview | 86.43% | 6.47% | 86.52% | 11.70% | 0.864318 | 1: `mcm-2024-a-lamprey` | ¥97.95 |
| 2 | GPT-5.6 SOL high | 83.77% | 2.53% | 84.16% | 8.08% | 0.837656 | 1: `mcm-2024-a-lamprey` | ¥59.98 |
| 3 | v4 flash baseline | 75.26% | 0.00% | 75.65% | 0.00% | 0.752619 | 1: `mcm-2024-a-lamprey` | ¥6.27 |
| 4 | Qwen3.8-27B-FP8 thinking | 75.06% | 4.38% | 75.45% | 9.94% | 0.750559 | 1: `mcm-2024-a-lamprey` | ¥189.88 |
| 5 | Kimi K3 | 60.76% | -11.64% | 86.88% | 12.19% | 0.607556 | 3: `mcm-2024-a-lamprey`, `mcm-2025-b-juneau-tourism`, `mcm-2025-c-olympic-medals` | ¥179.76 |
| 6 | v4 pro | 60.56% | -4.26% | 61.87% | 2.28% | 0.605647 | 1: `mcm-2024-a-lamprey` | ¥44.83 |
| 7 | GLM-5.3 | 59.12% | -0.43% | 59.82% | 5.45% | 0.591244 | 1: `mcm-2024-a-lamprey` | ¥258.05 |
| 8 | Gemini 3.7 Flash high primary+retry | 56.59% | -20.87% | 57.86% | -14.37% | 0.565890 | 1: `mcm-2024-a-lamprey` | ¥82.93 |
| 9 | Qwen3.8 Flash (Bailian) | 55.89% | -13.12% | 56.49% | -7.33% | 0.558881 | 1: `mcm-2024-a-lamprey` | ¥59.34 |
| 10 | GLM-5.3-Flash (ox-alpha) | 51.41% | -7.19% | 65.59% | -1.46% | 0.514071 | 1: `cumcm-2025-a-smoke-screen` | ¥19.62 |

## Hard Gate Decisions

| Model | Task | Raw before gate | Gated raw | O-Eval before | Hard-gated O-Eval | Robust before | Hard-gated Robust | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|
| GLM-5.3-Flash (ox-alpha) | `cumcm-2025-a-smoke-screen` | 2.552664 | 0.000000 | 255.27% | 0.00% | 10.00% | -100.00% | independent smoke-screen replay gives 0.00s coverage under O-reference line-of-sight geometry |
| v4 flash baseline | `mcm-2024-a-lamprey` | 0.070175 | 0.000000 | 7.02% | 0.00% | 0.00% | 0.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.final_parasite_index, experiment_result.parasite_coexistence_case.host_fish_index |
| v4 pro | `mcm-2024-a-lamprey` | 0.235294 | 0.000000 | 23.53% | 0.00% | 17.76% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.final_parasite_index, experiment_result.parasite_coexistence_case.host_fish_index |
| GLM-5.3 | `mcm-2024-a-lamprey` | 0.125000 | 0.000000 | 12.50% | 0.00% | 5.90% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.final_parasite_index, experiment_result.parasite_coexistence_case.host_fish_index |
| GPT-5.6 SOL high | `mcm-2024-a-lamprey` | 0.070175 | 0.000000 | 7.02% | 0.00% | 0.00% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.final_parasite_index, experiment_result.parasite_coexistence_case.host_fish_index |
| Kimi K3 | `mcm-2024-a-lamprey` | 0.246711 | 0.000000 | 24.67% | 0.00% | 18.99% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.host_fish_index |
| Gemini 3.7 Flash high primary+retry | `mcm-2024-a-lamprey` | 0.228957 | 0.000000 | 22.90% | 0.00% | 17.08% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.host_fish_index |
| Qwen3.8-27B-FP8 thinking | `mcm-2024-a-lamprey` | 0.070175 | 0.000000 | 7.02% | 0.00% | 0.00% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.final_parasite_index, experiment_result.parasite_coexistence_case.host_fish_index |
| Qwen3.8 Flash (Bailian) | `mcm-2024-a-lamprey` | 0.108108 | 0.000000 | 10.81% | 0.00% | 4.08% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.final_parasite_index, experiment_result.parasite_coexistence_case.host_fish_index |
| Tencent Hy4 Preview | `mcm-2024-a-lamprey` | 0.015564 | 0.000000 | 1.56% | 0.00% | -5.87% | -100.00% | score-config hard-invalid metric(s): experiment_result.parasite_coexistence_case.final_parasite_index, experiment_result.parasite_coexistence_case.host_fish_index |
| Kimi K3 | `mcm-2025-b-juneau-tourism` | 1.460140 | 0.000000 | 146.01% | 0.00% | 100.00% | -100.00% | unit/scale invalid: resident_acceptance_index=1.5 and sustainability_score=232.2 on a unit-scale score |
| Kimi K3 | `mcm-2025-c-olympic-medals` | 2.995504 | 0.000000 | 299.55% | 0.00% | 10.00% | -100.00% | invalid high coach-effect result: only three scored recommendations and endpoint verifier reward is negative/BO 0 |

## Primary Readout

- 18-task primary O-Eval ranking: Kimi K3 (86.88%) > Tencent Hy4 Preview (86.52%) > GPT-5.6 SOL high (84.16%) > Qwen3.8-27B-FP8 thinking (75.45%) > GLM-5.3-Flash (ox-alpha) (65.59%) > v4 pro (61.87%) > GLM-5.3 (59.82%) > Gemini 3.7 Flash high primary+retry (57.86%) > Qwen3.8 Flash (Bailian) (56.49%).
- Tempered hard-gated O-Eval ranking: Tencent Hy4 Preview (86.43%) > GPT-5.6 SOL high (83.77%) > Qwen3.8-27B-FP8 thinking (75.06%) > Kimi K3 (60.76%) > v4 pro (60.56%) > GLM-5.3 (59.12%) > Gemini 3.7 Flash high primary+retry (56.59%) > Qwen3.8 Flash (Bailian) (55.89%) > GLM-5.3-Flash (ox-alpha) (51.41%).
- Secondary Robust BO-Eval ranking: Kimi K3 (12.19%) > Tencent Hy4 Preview (11.70%) > Qwen3.8-27B-FP8 thinking (9.94%) > GPT-5.6 SOL high (8.08%) > GLM-5.3 (5.45%) > v4 pro (2.28%) > GLM-5.3-Flash (ox-alpha) (-1.46%) > Qwen3.8 Flash (Bailian) (-7.33%) > Gemini 3.7 Flash high primary+retry (-14.37%).
- Tempered hard-gated Robust BO-Eval ranking: Tencent Hy4 Preview (6.47%) > Qwen3.8-27B-FP8 thinking (4.38%) > GPT-5.6 SOL high (2.53%) > GLM-5.3 (-0.43%) > v4 pro (-4.26%) > GLM-5.3-Flash (ox-alpha) (-7.19%) > Kimi K3 (-11.64%) > Qwen3.8 Flash (Bailian) (-13.12%) > Gemini 3.7 Flash high primary+retry (-20.87%).
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
| v4 flash baseline | `deepseek/deepseek-v4-flash-0731` | OpenRouter live | ¥0.4379/M | ¥0.1078/M | N/A | ¥1.2127/M |
| v4 pro | `deepseek/deepseek-v4-pro` | OpenRouter live | ¥7.0217/M | ¥0.5851/M | N/A | ¥14.0434/M |
| GLM-5.3 | `z-ai/glm-5.3` | OpenRouter live | ¥9.4318/M | ¥1.7516/M | N/A | ¥29.6429/M |
| GPT-5.6 SOL high | `openai/gpt-5.6-sol` | OpenRouter live | ¥13.4740/M | ¥1.3474/M | ¥16.8425/M | ¥67.3701/M |
| Kimi K3 | `moonshotai/kimi-k3` | OpenRouter live | ¥20.2110/M | ¥2.0211/M | N/A | ¥101.0552/M |
| Gemini 3.7 Flash high primary+retry | `google/gemini-3.7-flash` | OpenRouter live | ¥5.0528/M | ¥0.5053/M | ¥0.2807/M | ¥25.2638/M |
| Qwen3.8-27B-FP8 thinking | `qwen/qwen3.8-27b` | OpenRouter live | ¥2.8632/M | ¥0.5726/M | ¥3.5790/M | ¥17.1794/M |
| GLM-5.3-Flash (ox-alpha) | `z-ai/glm-5.3-flash` | user-supplied fixed snapshot | ¥0.5053/M | ¥0.1011/M | N/A | ¥1.6843/M |
| Qwen3.8 Flash (Bailian) | `qwen/qwen3.8-flash` | user-supplied fixed snapshot | ¥1.0106/M | ¥0.1078/M | ¥1.3474/M | ¥3.1664/M |
| Tencent Hy4 Preview | `tencent/hy4-preview` | OpenRouter live | ¥5.6187/M | ¥0.2830/M | N/A | ¥16.8493/M |

## Figures

- Clickable dashboard: `terminus2-bo-eval-aa-dashboard-2023-2025.html`
- Qwen feasibility audit: `terminus2-qwen27b-feasibility-audit-2023-2025.md`
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
| v4 flash baseline | 112.32% | 28.62% | 86.01% |
| v4 pro | 78.64% | 33.58% | 73.39% |
| GLM-5.3 | 89.77% | 32.36% | 57.32% |
| GPT-5.6 SOL high | 118.46% | 34.99% | 99.01% |
| Kimi K3 | 71.09% | 38.29% | 151.26% |
| Gemini 3.7 Flash high primary+retry | 93.29% | 22.24% | 58.05% |
| Qwen3.8-27B-FP8 thinking | 95.23% | 52.82% | 78.29% |
| GLM-5.3-Flash (ox-alpha) | 83.77% | 44.31% | 68.69% |
| Qwen3.8 Flash (Bailian) | 86.92% | 24.96% | 57.58% |
| Tencent Hy4 Preview | 117.99% | 32.15% | 109.41% |

## Suite Mean O-Eval

| Model | CUMCM | MCM |
|---|---:|---:|
| v4 flash baseline | 100.85% | 50.45% |
| v4 pro | 82.94% | 40.80% |
| GLM-5.3 | 69.19% | 50.45% |
| GPT-5.6 SOL high | 125.95% | 42.36% |
| Kimi K3 | 103.81% | 69.95% |
| Gemini 3.7 Flash high primary+retry | 96.53% | 19.20% |
| Qwen3.8-27B-FP8 thinking | 112.91% | 37.98% |
| GLM-5.3-Flash (ox-alpha) | 92.30% | 38.88% |
| Qwen3.8 Flash (Bailian) | 78.14% | 34.84% |
| Tencent Hy4 Preview | 124.04% | 49.00% |

## Year Mean Robust BO-Eval

| Model | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 0.00% |
| v4 pro | 9.43% | -2.00% | -0.58% |
| GLM-5.3 | 19.52% | -0.26% | -2.90% |
| GPT-5.6 SOL high | 22.65% | 1.11% | 0.49% |
| Kimi K3 | 9.51% | 5.34% | 21.73% |
| Gemini 3.7 Flash high primary+retry | -4.74% | -28.71% | -9.66% |
| Qwen3.8-27B-FP8 thinking | 19.69% | 13.71% | -3.59% |
| GLM-5.3-Flash (ox-alpha) | -12.77% | 15.47% | -7.08% |
| Qwen3.8 Flash (Bailian) | 9.30% | -27.00% | -4.30% |
| Tencent Hy4 Preview | 29.83% | -1.68% | 6.94% |

## Suite Mean Robust BO-Eval

| Model | CUMCM | MCM | CUMCM artifacts | MCM artifacts |
|---|---:|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 8 | 9 |
| v4 pro | 2.14% | 2.42% | 9 | 9 |
| GLM-5.3 | 0.41% | 10.49% | 9 | 9 |
| GPT-5.6 SOL high | 8.53% | 7.63% | 9 | 9 |
| Kimi K3 | 8.86% | 15.53% | 9 | 9 |
| Gemini 3.7 Flash high primary+retry | 0.89% | -29.63% | 9 | 6 |
| Qwen3.8-27B-FP8 thinking | 8.66% | 11.21% | 9 | 9 |
| GLM-5.3-Flash (ox-alpha) | -13.86% | 10.94% | 8 | 9 |
| Qwen3.8 Flash (Bailian) | -20.16% | 5.49% | 7 | 9 |
| Tencent Hy4 Preview | 5.45% | 17.94% | 9 | 9 |

## Saturated Or Near-Zero Gap Cases

| Year | Suite | Problem | Task | flash raw | O raw |
|---:|---|---|---|---:|---:|
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.492402 | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.550299 | 1.000000 |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 1.527989 | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.506359 | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.632029 | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.575307 | 1.000000 |

## Per-Task Values

Cells are `direction-aware raw / O-Eval % / B-Eval vs flash / Robust BO-Eval %`.

| Year | Suite | Problem | Task | v4 flash baseline | v4 pro | GLM-5.3 | GPT-5.6 SOL high | Kimi K3 | Gemini 3.7 Flash high primary+retry | Qwen3.8-27B-FP8 thinking | GLM-5.3-Flash (ox-alpha) | Qwen3.8 Flash (Bailian) | Tencent Hy4 Preview | O raw |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 0.738213 / 73.82% / 0.00% / 0.00% | 1.312936 / 131.29% / 219.54% / 100.00% | 1.393536 / 139.35% / 250.33% / 100.00% | 0.971969 / 97.20% / 89.29% / 89.29% | 0.975341 / 97.53% / 90.58% / 90.58% | 0.969010 / 96.90% / 88.16% / 88.16% | 1.244533 / 124.45% / 193.41% / 100.00% | 0.000000 / 0.00% / 0.00% / -100.00% | 1.455864 / 145.59% / 274.14% / 100.00% | 1.464003 / 146.40% / 277.24% / 100.00% | 1.000000 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.492402 / 149.24% / 0.00% / 0.00% | 1.496072 / 149.61% / N/A / 0.37% | 1.500666 / 150.07% / N/A / 0.83% | 2.425664 / 242.57% / N/A / 10.00% | 1.410390 / 141.04% / N/A / -8.20% | 1.496423 / 149.64% / N/A / 0.40% | 1.501820 / 150.18% / N/A / 0.94% | 1.500621 / 150.06% / N/A / 0.82% | 1.542730 / 154.27% / N/A / 5.03% | 2.349865 / 234.99% / N/A / 10.00% | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.550299 / 255.03% / 0.00% / 0.00% | 0.597918 / 59.79% / N/A / -10.00% | 0.355098 / 35.51% / N/A / -10.00% | 1.589944 / 158.99% / N/A / -10.00% | 1.134708 / 113.47% / N/A / -10.00% | 2.523435 / 252.34% / N/A / -2.69% | 1.292870 / 129.29% / N/A / -10.00% | 1.707570 / 170.76% / N/A / -10.00% | 1.755009 / 175.50% / N/A / -10.00% | 0.963631 / 96.36% / N/A / -10.00% | 1.000000 |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 0.722875 / 72.29% / 0.00% / 0.00% | 0.254589 / 25.46% / 0.00% / -100.00% | 0.203536 / 20.35% / 0.00% / -100.00% | 0.203536 / 20.35% / 0.00% / -100.00% | 0.068138 / 6.81% / 0.00% / -100.00% | 0.254590 / 25.46% / 0.00% / -100.00% | 0.203541 / 20.35% / 0.00% / -100.00% | 0.203536 / 20.35% / 0.00% / -100.00% | 0.203536 / 20.35% / 0.00% / -100.00% | 0.203536 / 20.35% / 0.00% / -100.00% | 1.000000 |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.318573 / 31.86% / 31.86% / 31.86% | 0.257329 / 25.73% / 25.73% / 25.73% | 0.444542 / 44.45% / 44.45% / 44.45% | 0.943081 / 94.31% / 94.31% / 94.31% | 0.469069 / 46.91% / 46.91% / 46.91% | 1.445692 / 144.57% / 144.57% / 100.00% | 0.390214 / 39.02% / 39.02% / 39.02% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.366504 / 36.65% / 36.65% / 36.65% | 1.000000 |
| 2024 | CUMCM | C | `cumcm-2024-c-crop-planting` | 0.246679 / 24.67% / 0.00% / 0.00% | 0.345043 / 34.50% / 13.06% / 13.06% | 0.285151 / 28.52% / 5.11% / 5.11% | 0.588775 / 58.88% / 45.41% / 45.41% | 0.191121 / 19.11% / 0.00% / -7.38% | 0.193549 / 19.35% / 0.00% / -7.05% | 0.172944 / 17.29% / 0.00% / -9.79% | 0.569595 / 56.96% / 42.87% / 42.87% | 0.448288 / 44.83% / 26.76% / 26.76% | 0.264186 / 26.42% / 2.32% / 2.32% | 1.000000 |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 1.527989 / 152.80% / 0.00% / 0.00% | 1.532372 / 153.24% / N/A / 0.44% | 0.854445 / 85.44% / N/A / -10.00% | 3.416382 / 341.64% / N/A / 10.00% | 2.894037 / 289.40% / N/A / 10.00% | 1.239279 / 123.93% / N/A / -10.00% | 2.591825 / 259.18% / N/A / 10.00% | 2.552664 / 255.27% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 4.004026 / 400.40% / N/A / 10.00% | 1.000000 |
| 2025 | CUMCM | B | `cumcm-2025-b-sic-thickness` | 0.291621 / 29.16% / 0.00% / 0.00% | 0.246099 / 24.61% / 0.00% / -6.43% | 0.306245 / 30.62% / 2.06% / 2.06% | 0.242011 / 24.20% / 0.00% / -7.00% | 0.436145 / 43.61% / 20.40% / 20.40% | 0.307888 / 30.79% / 2.30% / 2.30% | 0.187085 / 18.71% / 0.00% / -14.76% | 0.309492 / 30.95% / 2.52% / 2.52% | 0.339399 / 33.94% / 6.74% / 6.74% | 0.363177 / 36.32% / 10.10% / 10.10% | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.506359 / 150.64% / 0.00% / 0.00% | 1.360909 / 136.09% / N/A / -10.00% | 1.071182 / 107.12% / N/A / -10.00% | 1.452420 / 145.24% / N/A / -5.39% | 1.289804 / 128.98% / N/A / -10.00% | 1.234068 / 123.41% / N/A / -10.00% | 1.521520 / 152.15% / N/A / 1.52% | 1.073057 / 107.31% / N/A / -10.00% | 1.287680 / 128.77% / N/A / -10.00% | 1.184644 / 118.46% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.632029 / 163.20% / 0.00% / 0.00% | 1.179422 / 117.94% / N/A / -10.00% | 1.538784 / 153.88% / N/A / -9.32% | 1.364424 / 136.44% / N/A / -10.00% | 0.469546 / 46.95% / N/A / -10.00% | 0.545375 / 54.54% / N/A / -10.00% | 1.070439 / 107.04% / N/A / -10.00% | 1.163407 / 116.34% / N/A / -10.00% | 0.373162 / 37.32% / N/A / -10.00% | 1.296434 / 129.64% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | 0.102093 / 10.21% / 0.00% / 0.00% | 0.034371 / 3.44% / 0.00% / -7.54% | 0.068142 / 6.81% / 0.00% / -3.78% | 0.032355 / 3.24% / 0.00% / -7.77% | 0.028745 / 2.87% / 0.00% / -8.17% | 0.063352 / 6.34% / 0.00% / -4.31% | 0.024041 / 2.40% / 0.00% / -8.69% | 0.088569 / 8.86% / 0.00% / -1.51% | 0.023241 / 2.32% / 0.00% / -8.78% | 0.022503 / 2.25% / 0.00% / -8.86% | 1.000000 |
| 2023 | MCM | C | `mcm-2023-c-wordle` | 0.224201 / 22.42% / 0.00% / 0.00% | 0.097978 / 9.80% / 0.00% / -16.27% | 0.529999 / 53.00% / 39.42% / 39.42% | 0.723478 / 72.35% / 64.36% / 64.36% | 0.246521 / 24.65% / 2.88% / 2.88% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.580000 / 58.00% / 45.86% / 45.86% | 0.565840 / 56.58% / 44.04% / 44.04% | 0.065441 / 6.54% / 0.00% / -20.46% | 0.983080 / 98.31% / 97.82% / 97.82% | 1.000000 |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | 0.070175 / 7.02% / 0.00% / 0.00% | 0.235294 / 23.53% / 17.76% / 17.76% | 0.125000 / 12.50% / 5.90% / 5.90% | 0.070175 / 7.02% / 0.00% / 0.00% | 0.246711 / 24.67% / 18.99% / 18.99% | 0.228957 / 22.90% / 17.08% / 17.08% | 0.070175 / 7.02% / 0.00% / 0.00% | 0.089589 / 8.96% / 2.09% / 2.09% | 0.108108 / 10.81% / 4.08% / 4.08% | 0.015564 / 1.56% / 0.00% / -5.87% | 1.000000 |
| 2024 | MCM | B | `mcm-2024-b-submersible-search` | 0.371417 / 37.14% / 0.00% / 0.00% | 0.296505 / 29.65% / 0.00% / -11.92% | 0.709302 / 70.93% / 53.75% / 53.75% | 0.389026 / 38.90% / 2.80% / 2.80% | 0.470888 / 47.09% / 15.82% / 15.82% | 0.187946 / 18.79% / 0.00% / -29.19% | 0.753209 / 75.32% / 60.74% / 60.74% | 0.632353 / 63.24% / 41.51% / 41.51% | 0.272873 / 27.29% / 0.00% / -15.68% | 0.300348 / 30.03% / 0.00% / -11.31% | 1.000000 |
| 2024 | MCM | C | `mcm-2024-c-tennis-momentum` | 0.306291 / 30.63% / 0.00% / 0.00% | 0.564619 / 56.46% / 37.24% / 37.24% | 0.361433 / 36.14% / 7.95% / 7.95% | 0.403266 / 40.33% / 13.98% / 13.98% | 0.377542 / 37.75% / 10.27% / 10.27% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.523386 / 52.34% / 31.29% / 31.29% | 0.773319 / 77.33% / 67.32% / 67.32% | 0.464638 / 46.46% / 22.83% / 22.83% | 0.778964 / 77.90% / 68.14% / 68.14% | 1.000000 |
| 2025 | MCM | A | `mcm-2025-a-stair-wear` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.233333 / 23.33% / 23.33% / 23.33% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2025 | MCM | B | `mcm-2025-b-juneau-tourism` | 0.259364 / 25.94% / 0.00% / 0.00% | 0.426076 / 42.61% / 22.51% / 22.51% | 0.337214 / 33.72% / 10.51% / 10.51% | 0.372904 / 37.29% / 15.33% / 15.33% | 1.460140 / 146.01% / 162.13% / 100.00% | 0.702044 / 70.20% / 59.77% / 59.77% | 0.025227 / 2.52% / 0.00% / -31.61% | 0.000000 / 0.00% / 0.00% / -35.02% | 0.907133 / 90.71% / 87.46% / 87.46% | 0.567213 / 56.72% / 41.57% / 41.57% | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.575307 / 157.53% / 0.00% / 0.00% | 0.838169 / 83.82% / N/A / -10.00% | 0.870336 / 87.03% / N/A / -10.00% | 0.457106 / 45.71% / N/A / -10.00% | 2.995504 / 299.55% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 0.138589 / 13.86% / N/A / -10.00% | 0.186115 / 18.61% / N/A / -10.00% | 0.920868 / 92.09% / N/A / -10.00% | 0.445610 / 44.56% / N/A / -10.00% | 1.000000 |