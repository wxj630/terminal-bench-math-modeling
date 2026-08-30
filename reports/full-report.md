# O-Eval and Robust BO-Eval: 2023-2025

Generated: 2026-08-30

Scope: 2023, 2024, and 2025 terminal-bench-math-modeling tasks, 18 tasks total. This report rescored saved artifacts only; it does not rerun models or modify job result files.

Primary O-Eval rule: `model direction-aware raw / O raw`, averaged over all 18 tasks. Since the O-award reproduction is normalized near raw=1 on these tasks, O-Eval is the easiest-to-read absolute oracle-normalized score.

Secondary Robust BO-Eval rule: let `gain = model raw - flash raw` and `gap = O raw - flash raw`. If `gap >= 0.10`, score `clip(gain / gap, -100%, +100%)`; otherwise score `clip(gain, -10pp, +10pp)`. Normal completed tasks still use the clipped fallback on tiny-gap cases, but any final error or missing artifact is assigned `-100%` so a completely unfinished task gets the worst possible score.

Robust ratio tasks with gap >= 0.10: 11. Saturated or near-zero-gap tasks using clipped B-Eval: 7.

## Overall Mean

| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB | Canonical valid/running/error/pending | Excluded retries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| v4 flash baseline | 18 | 0.719811 | 71.98% | +0.00 pp | 0.00% | 28,690,539 / 27,294,080 / 1,368,452 | 1,396,459 / 1,368,452 | $0.773796 | ¥5.21 | 11/0/7/0 | 0 |
| v4 pro | 18 | 0.618719 | 61.87% | -10.11 pp | 8.98% | 21,309,105 / 20,096,768 / 1,748,356 | 1,212,337 / 1,748,356 | $3.181267 | ¥21.43 | 18/0/0/0 | 0 |
| GLM-5.3 | 18 | 0.598189 | 59.82% | -12.16 pp | 7.82% | 92,056,972 / 89,637,696 / 2,638,779 | 2,419,276 / 2,638,779 | $38.303415 | ¥258.05 | 18/0/0/0 | 0 |
| GPT-5.6 SOL high | 18 | 0.841554 | 84.16% | +12.17 pp | 11.68% | 8,774,606 / 7,566,848 / 497,473 | 1,207,758 / 497,473 | $8.903616 | ¥59.98 | 18/0/0/0 | 0 |
| Kimi K3 | 18 | 0.868798 | 86.88% | +14.90 pp | 11.09% | 30,146,116 / 28,928,953 / 956,805 | 1,217,163 / 956,805 | $26.682250 | ¥179.76 | 17/0/1/0 | 0 |
| Gemini 3.7 Flash high primary+retry | 15 | 0.578610 | 57.86% | -14.12 pp | -8.04% | 69,131,259 / 62,497,004 / 705,776 | 6,634,255 / 705,776 | $12.309627 | ¥82.93 | 18/0/0/0 | 1 |
| Qwen3.8-27B-FP8 thinking | 18 | 0.754457 | 75.45% | +3.46 pp | 11.09% | 47,245,909 / 0 / 3,178,409 | 47,245,909 / 3,178,409 | $28.184454 | ¥189.88 | 17/0/1/0 | 0 |
| GLM-5.3-Flash (ox-alpha) | 18 | 0.655886 | 65.59% | -6.39 pp | 9.48% | 107,726,029 / 101,466,688 / 3,683,366 | 6,259,341 / 3,683,366 | $2.912292 | ¥19.62 | 17/0/1/0 | 20 |
| Qwen3.8 Flash (Bailian) | 18 | 0.564887 | 56.49% | -15.49 pp | -5.50% | 299,616,972 / 293,563,264 / 6,814,374 | 6,053,708 / 6,814,374 | $8.807824 | ¥59.34 | 16/0/2/0 | 0 |

## Primary Readout

- 18-task primary O-Eval ranking: Kimi K3 (86.88%) > GPT-5.6 SOL high (84.16%) > Qwen3.8-27B-FP8 thinking (75.45%) > GLM-5.3-Flash (ox-alpha) (65.59%) > v4 pro (61.87%) > GLM-5.3 (59.82%) > Gemini 3.7 Flash high primary+retry (57.86%) > Qwen3.8 Flash (Bailian) (56.49%).
- Secondary Robust BO-Eval ranking: GPT-5.6 SOL high (11.68%) > Kimi K3 (11.09%) > Qwen3.8-27B-FP8 thinking (11.09%) > GLM-5.3-Flash (ox-alpha) (9.48%) > v4 pro (8.98%) > GLM-5.3 (7.82%) > Qwen3.8 Flash (Bailian) (-5.50%) > Gemini 3.7 Flash high primary+retry (-8.04%).
- These two metrics are complementary, not competing: O-Eval is the absolute oracle-normalized score for the headline leaderboard, while Robust BO-Eval is the baseline-relative gain view. If the rankings disagree, it usually means a model is closer to O in absolute terms but does not pull as far ahead of flash, or it gains a lot on a few weak-baseline tasks without being closest overall. This report therefore uses O-Eval as the final ranking and Robust BO-Eval as a diagnostic view.
- The GLM-5.3-Flash vs DeepSeek flash difference is a good example: Robust can favor the model that moves farther above flash, while O-Eval still favors the model that lands closer to the oracle anchor.
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
| v4 pro | `deepseek/deepseek-v4-pro` | OpenRouter live | ¥3.3573/M | ¥0.2798/M | N/A | ¥6.7146/M |
| GLM-5.3 | `z-ai/glm-5.3` | OpenRouter live | ¥9.4318/M | ¥1.7516/M | N/A | ¥29.6429/M |
| GPT-5.6 SOL high | `openai/gpt-5.6-sol` | OpenRouter live | ¥13.4740/M | ¥1.3474/M | ¥16.8425/M | ¥67.3701/M |
| Kimi K3 | `moonshotai/kimi-k3` | OpenRouter live | ¥20.2110/M | ¥2.0211/M | N/A | ¥101.0552/M |
| Gemini 3.7 Flash high primary+retry | `google/gemini-3.7-flash` | OpenRouter live | ¥5.0528/M | ¥0.5053/M | ¥0.2807/M | ¥25.2638/M |
| Qwen3.8-27B-FP8 thinking | `qwen/qwen3.8-27b` | OpenRouter live | ¥2.8632/M | ¥0.5726/M | ¥3.5790/M | ¥17.1794/M |
| GLM-5.3-Flash (ox-alpha) | `z-ai/glm-5.3-flash` | user-supplied fixed snapshot | ¥0.5053/M | ¥0.1011/M | N/A | ¥1.6843/M |
| Qwen3.8 Flash (Bailian) | `qwen/qwen3.8-flash` | user-supplied fixed snapshot | ¥1.0106/M | ¥0.1078/M | ¥1.3474/M | ¥3.1664/M |

## Figures

- Leaderboard homepage: `../index.html`
- Qwen feasibility audit: `terminus2-qwen27b-feasibility-audit-2023-2025.md`
- O-Eval effect: `figures/aa-style-2023-2025-o-eval-bar.png`
- O-Eval score-cost: `figures/aa-style-2023-2025-o-eval-cost-scatter.png`
- Robust BO-Eval effect: `figures/aa-style-2023-2025-boeval-effect-bar.png`
- Robust BO-Eval score-cost: `figures/aa-style-2023-2025-boeval-score-cost.png`
- Token usage: `figures/aa-style-2023-2025-token-usage.png`
- Cost: `figures/aa-style-2023-2025-cost.png`
- Diagnostic year split: `figures/aa-style-2023-2025-boeval-year-split.png`
- Diagnostic suite split: `figures/aa-style-2023-2025-boeval-suite-split.png`

## Year Mean O-Eval

| Model | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| v4 flash baseline | 100.31% | 46.21% | 69.42% |
| v4 pro | 78.64% | 33.58% | 73.39% |
| GLM-5.3 | 89.77% | 32.36% | 57.32% |
| GPT-5.6 SOL high | 118.46% | 34.99% | 99.01% |
| Kimi K3 | 71.09% | 38.29% | 151.26% |
| Gemini 3.7 Flash high primary+retry | 93.29% | 22.24% | 58.05% |
| Qwen3.8-27B-FP8 thinking | 95.23% | 52.82% | 78.29% |
| GLM-5.3-Flash (ox-alpha) | 83.77% | 44.31% | 68.69% |
| Qwen3.8 Flash (Bailian) | 86.92% | 24.96% | 57.58% |

## Suite Mean O-Eval

| Model | CUMCM | MCM |
|---|---:|---:|
| v4 flash baseline | 96.59% | 47.38% |
| v4 pro | 82.94% | 40.80% |
| GLM-5.3 | 69.19% | 50.45% |
| GPT-5.6 SOL high | 125.95% | 42.36% |
| Kimi K3 | 103.81% | 69.95% |
| Gemini 3.7 Flash high primary+retry | 96.53% | 19.20% |
| Qwen3.8-27B-FP8 thinking | 112.91% | 37.98% |
| GLM-5.3-Flash (ox-alpha) | 92.30% | 38.88% |
| Qwen3.8 Flash (Bailian) | 78.14% | 34.84% |

## Year Mean Robust BO-Eval

| Model | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 0.00% |
| v4 pro | 1.70% | 2.81% | 22.44% |
| GLM-5.3 | 11.11% | -0.87% | 13.21% |
| GPT-5.6 SOL high | 10.51% | 2.52% | 22.01% |
| Kimi K3 | 1.97% | -7.74% | 39.03% |
| Gemini 3.7 Flash high primary+retry | -14.40% | -22.95% | 13.24% |
| Qwen3.8-27B-FP8 thinking | 9.56% | 3.52% | 20.18% |
| GLM-5.3-Flash (ox-alpha) | -7.90% | 19.77% | 16.57% |
| Qwen3.8 Flash (Bailian) | 0.97% | -16.39% | -1.06% |

## Suite Mean Robust BO-Eval

| Model | CUMCM | MCM | CUMCM artifacts | MCM artifacts |
|---|---:|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 9 | 9 |
| v4 pro | 11.40% | 6.57% | 9 | 9 |
| GLM-5.3 | 4.40% | 11.23% | 9 | 9 |
| GPT-5.6 SOL high | 15.24% | 8.11% | 9 | 9 |
| Kimi K3 | 7.13% | 15.05% | 9 | 9 |
| Gemini 3.7 Flash high primary+retry | 10.13% | -26.20% | 9 | 6 |
| Qwen3.8-27B-FP8 thinking | 9.40% | 12.77% | 9 | 9 |
| GLM-5.3-Flash (ox-alpha) | 4.19% | 14.77% | 8 | 9 |
| Qwen3.8 Flash (Bailian) | -17.99% | 7.00% | 7 | 9 |

## Saturated Or Near-Zero Gap Cases

| Year | Suite | Problem | Task | flash raw | O raw |
|---:|---|---|---|---:|---:|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 0.967004 | 1.000000 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.345102 | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.135026 | 1.000000 |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 1.378763 | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.520296 | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.541010 | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.773903 | 1.000000 |

## Per-Task Values

Cells are `direction-aware raw / O-Eval % / B-Eval vs flash / Robust BO-Eval %`.

| Year | Suite | Problem | Task | v4 flash baseline | v4 pro | GLM-5.3 | GPT-5.6 SOL high | Kimi K3 | Gemini 3.7 Flash high primary+retry | Qwen3.8-27B-FP8 thinking | GLM-5.3-Flash (ox-alpha) | Qwen3.8 Flash (Bailian) | O raw |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 0.967004 / 96.70% / 0.00% / 0.00% | 1.312936 / 131.29% / 1048.41% / 10.00% | 1.393536 / 139.35% / 1292.69% / 10.00% | 0.971969 / 97.20% / 15.05% / 0.50% | 0.975341 / 97.53% / 25.27% / 0.83% | 0.969010 / 96.90% / 6.08% / 0.20% | 1.244533 / 124.45% / 841.10% / 10.00% | 0.000000 / 0.00% / 0.00% / -100.00% | 1.455864 / 145.59% / 1481.58% / 10.00% | 1.000000 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.345102 / 134.51% / 0.00% / 0.00% | 1.496072 / 149.61% / N/A / 10.00% | 1.500666 / 150.07% / N/A / 10.00% | 2.425664 / 242.57% / N/A / 10.00% | 1.410390 / 141.04% / N/A / 6.53% | 1.496423 / 149.64% / N/A / 10.00% | 1.501820 / 150.18% / N/A / 10.00% | 1.500621 / 150.06% / N/A / 10.00% | 1.542730 / 154.27% / N/A / 10.00% | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.135026 / 213.50% / 0.00% / 0.00% | 0.597918 / 59.79% / N/A / -10.00% | 0.355098 / 35.51% / N/A / -10.00% | 1.589944 / 158.99% / N/A / -10.00% | 1.134708 / 113.47% / N/A / -10.00% | 2.523435 / 252.34% / N/A / 10.00% | 1.292870 / 129.29% / N/A / -10.00% | 1.707570 / 170.76% / N/A / -10.00% | 1.755009 / 175.50% / N/A / -10.00% | 1.000000 |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.254589 / 25.46% / 25.46% / 25.46% | 0.203536 / 20.35% / 20.35% / 20.35% | 0.203536 / 20.35% / 20.35% / 20.35% | 0.068138 / 6.81% / 6.81% / 6.81% | 0.254590 / 25.46% / 25.46% / 25.46% | 0.203541 / 20.35% / 20.35% / 20.35% | 0.203536 / 20.35% / 20.35% / 20.35% | 0.203536 / 20.35% / 20.35% / 20.35% | 1.000000 |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 1.378763 / 137.88% / 0.00% / 0.00% | 0.318573 / 31.86% / N/A / -10.00% | 0.257329 / 25.73% / N/A / -10.00% | 0.444542 / 44.45% / N/A / -10.00% | 0.943081 / 94.31% / N/A / -10.00% | 0.469069 / 46.91% / N/A / -10.00% | 1.445692 / 144.57% / N/A / 6.69% | 0.390214 / 39.02% / N/A / -10.00% | 0.000000 / 0.00% / N/A / -100.00% | 1.000000 |
| 2024 | CUMCM | C | `cumcm-2024-c-crop-planting` | 0.475492 / 47.55% / 0.00% / 0.00% | 0.345043 / 34.50% / 0.00% / -24.87% | 0.285151 / 28.52% / 0.00% / -36.29% | 0.588775 / 58.88% / 21.60% / 21.60% | 0.191121 / 19.11% / 0.00% / -54.22% | 0.193549 / 19.35% / 0.00% / -53.75% | 0.172944 / 17.29% / 0.00% / -57.68% | 0.569595 / 56.96% / 17.94% / 17.94% | 0.448288 / 44.83% / 0.00% / -5.19% | 1.000000 |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 0.727946 / 72.79% / 0.00% / 0.00% | 1.532372 / 153.24% / 295.69% / 100.00% | 0.854445 / 85.44% / 46.50% / 46.50% | 3.416382 / 341.64% / 988.20% / 100.00% | 2.894037 / 289.40% / 796.20% / 100.00% | 1.239279 / 123.93% / 187.95% / 100.00% | 2.591825 / 259.18% / 685.11% / 100.00% | 2.552664 / 255.27% / 670.72% / 100.00% | 0.000000 / 0.00% / 0.00% / -100.00% | 1.000000 |
| 2025 | CUMCM | B | `cumcm-2025-b-sic-thickness` | 0.143179 / 14.32% / 0.00% / 0.00% | 0.246099 / 24.61% / 12.01% / 12.01% | 0.306245 / 30.62% / 19.03% / 19.03% | 0.242011 / 24.20% / 11.53% / 11.53% | 0.436145 / 43.61% / 34.19% / 34.19% | 0.307888 / 30.79% / 19.22% / 19.22% | 0.187085 / 18.71% / 5.12% / 5.12% | 0.309492 / 30.95% / 19.41% / 19.41% | 0.339399 / 33.94% / 22.90% / 22.90% | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.520296 / 152.03% / 0.00% / 0.00% | 1.360909 / 136.09% / N/A / -10.00% | 1.071182 / 107.12% / N/A / -10.00% | 1.452420 / 145.24% / N/A / -6.79% | 1.289804 / 128.98% / N/A / -10.00% | 1.234068 / 123.41% / N/A / -10.00% | 1.521520 / 152.15% / N/A / 0.12% | 1.073057 / 107.31% / N/A / -10.00% | 1.287680 / 128.77% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.541010 / 154.10% / 0.00% / 0.00% | 1.179422 / 117.94% / N/A / -10.00% | 1.538784 / 153.88% / N/A / -0.22% | 1.364424 / 136.44% / N/A / -10.00% | 0.469546 / 46.95% / N/A / -10.00% | 0.545375 / 54.54% / N/A / -10.00% | 1.070439 / 107.04% / N/A / -10.00% | 1.163407 / 116.34% / N/A / -10.00% | 0.373162 / 37.32% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | 0.030363 / 3.04% / 0.00% / 0.00% | 0.034371 / 3.44% / 0.41% / 0.41% | 0.068142 / 6.81% / 3.90% / 3.90% | 0.032355 / 3.24% / 0.21% / 0.21% | 0.028745 / 2.87% / 0.00% / -0.17% | 0.063352 / 6.34% / 3.40% / 3.40% | 0.024041 / 2.40% / 0.00% / -0.65% | 0.088569 / 8.86% / 6.00% / 6.00% | 0.023241 / 2.32% / 0.00% / -0.73% | 1.000000 |
| 2023 | MCM | C | `mcm-2023-c-wordle` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.097978 / 9.80% / 9.80% / 9.80% | 0.529999 / 53.00% / 53.00% / 53.00% | 0.723478 / 72.35% / 72.35% / 72.35% | 0.246521 / 24.65% / 24.65% / 24.65% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.580000 / 58.00% / 58.00% / 58.00% | 0.565840 / 56.58% / 56.58% / 56.58% | 0.065441 / 6.54% / 6.54% / 6.54% | 1.000000 |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | 0.235294 / 23.53% / 0.00% / 0.00% | 0.235294 / 23.53% / 0.00% / 0.00% | 0.125000 / 12.50% / 0.00% / -14.42% | 0.070175 / 7.02% / 0.00% / -21.59% | 0.246711 / 24.67% / 1.49% / 1.49% | 0.228957 / 22.90% / 0.00% / -0.83% | 0.070175 / 7.02% / 0.00% / -21.59% | 0.089589 / 8.96% / 0.00% / -19.05% | 0.108108 / 10.81% / 0.00% / -16.63% | 1.000000 |
| 2024 | MCM | B | `mcm-2024-b-submersible-search` | 0.176025 / 17.60% / 0.00% / 0.00% | 0.296505 / 29.65% / 14.62% / 14.62% | 0.709302 / 70.93% / 64.72% / 64.72% | 0.389026 / 38.90% / 25.85% / 25.85% | 0.470888 / 47.09% / 35.79% / 35.79% | 0.187946 / 18.79% / 1.45% / 1.45% | 0.753209 / 75.32% / 70.05% / 70.05% | 0.632353 / 63.24% / 55.38% / 55.38% | 0.272873 / 27.29% / 11.75% / 11.75% | 1.000000 |
| 2024 | MCM | C | `mcm-2024-c-tennis-momentum` | 0.507190 / 50.72% / 0.00% / 0.00% | 0.564619 / 56.46% / 11.65% / 11.65% | 0.361433 / 36.14% / 0.00% / -29.58% | 0.403266 / 40.33% / 0.00% / -21.09% | 0.377542 / 37.75% / 0.00% / -26.31% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.523386 / 52.34% / 3.29% / 3.29% | 0.773319 / 77.33% / 54.00% / 54.00% | 0.464638 / 46.46% / 0.00% / -8.63% | 1.000000 |
| 2025 | MCM | A | `mcm-2025-a-stair-wear` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.233333 / 23.33% / 23.33% / 23.33% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2025 | MCM | B | `mcm-2025-b-juneau-tourism` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.426076 / 42.61% / 42.61% / 42.61% | 0.337214 / 33.72% / 33.72% / 33.72% | 0.372904 / 37.29% / 37.29% / 37.29% | 1.460140 / 146.01% / 146.01% / 100.00% | 0.702044 / 70.20% / 70.20% / 70.20% | 0.025227 / 2.52% / 2.52% / 2.52% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.907133 / 90.71% / 90.71% / 90.71% | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.773903 / 177.39% / 0.00% / 0.00% | 0.838169 / 83.82% / N/A / -10.00% | 0.870336 / 87.03% / N/A / -10.00% | 0.457106 / 45.71% / N/A / -10.00% | 2.995504 / 299.55% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 0.138589 / 13.86% / N/A / -10.00% | 0.186115 / 18.61% / N/A / -10.00% | 0.920868 / 92.09% / N/A / -10.00% | 1.000000 |
