# O-Eval and Robust BO-Eval: 2023-2025

Generated: 2026-08-26

Scope: 2023, 2024, and 2025 terminal-bench-math-modeling tasks, 18 tasks total. This report rescored saved artifacts only; it does not rerun models or modify job result files.

Primary O-Eval rule: `model direction-aware raw / O raw`, averaged over all 18 tasks. Since the O-award reproduction is normalized near raw=1 on these tasks, O-Eval is the easiest-to-read absolute oracle-normalized score.

BO-only diagnostic rule: `max(0, (model raw - v4 flash raw) / (O raw - v4 flash raw))`, computed only when `O raw > v4 flash raw`. Missing artifacts are treated as raw 0 for that task, matching the existing report convention.

Secondary Robust BO-Eval rule: let `gain = model raw - flash raw` and `gap = O raw - flash raw`. If `gap >= 0.10`, score `clip(gain / gap, -100%, +100%)`; otherwise score `clip(gain, -10pp, +10pp)`. This keeps bad tasks negative while preventing tiny denominators such as 37 vs 32 from exploding into 841%.

BO-only defined tasks: 12. Robust ratio tasks with gap >= 0.10: 11. Saturated or near-zero-gap tasks using clipped B-Eval: 7.

## Overall Mean

| Model | Artifacts | BO-defined tasks | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Mean BO-Eval vs flash on defined subset (%) | Tokens input/cache/output | Billable input/output | Est. cost RMB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v4 flash baseline | 18 | 12 | 0.719811 | 71.98% | +0.00 pp | 0.00% | 0.00% | 28,690,539 / 27,294,080 / 1,368,452 | 1,396,459 / 1,368,452 | ¥3.88 |
| v4 pro | 18 | 12 | 0.618719 | 61.87% | -10.11 pp | 8.98% | 121.72% | 21,309,105 / 20,096,768 / 1,748,356 | 1,212,337 / 1,748,356 | ¥37.42 |
| GLM-5.3 | 18 | 12 | 0.598189 | 59.82% | -12.16 pp | 7.82% | 127.83% | 92,056,972 / 89,637,696 / 2,638,779 | 2,419,276 / 2,638,779 | ¥258.05 |
| GPT-5.6 SOL high | 18 | 12 | 0.841554 | 84.16% | +12.17 pp | 11.68% | 99.37% | 8,774,606 / 7,566,848 / 497,473 | 1,207,758 / 497,473 | ¥59.98 |
| Kimi K3 | 18 | 12 | 0.868798 | 86.88% | +14.90 pp | 11.09% | 89.20% | 30,146,116 / 28,928,953 / 956,805 | 1,217,163 / 956,805 | ¥179.76 |
| Gemini 3.7 Flash high primary+retry | 15 | 12 | 0.578610 | 57.86% | -14.12 pp | 2.52% | 26.15% | 70,179,563 / 63,289,798 / 728,328 | 6,889,765 / 728,328 | ¥42.60 |
| Qwen3.8-27B-FP8 thinking | 18 | 12 | 0.754457 | 75.45% | +3.46 pp | 11.09% | 142.41% | 47,245,909 / 44,364,108 / 3,178,409 | 2,881,801 / 3,178,409 | ¥88.26 |
| OpenRouter ox-alpha | 0 | 12 | 0.000000 | 0.00% | -71.98 pp | -24.03% | 0.00% | 10,671,091 / 10,469,056 / 177,118 | 202,035 / 177,118 | N/A |

## Primary Readout

- 18-task primary O-Eval ranking: Kimi K3 (86.88%) > GPT-5.6 SOL high (84.16%) > Qwen3.8-27B-FP8 thinking (75.45%) > v4 pro (61.87%) > GLM-5.3 (59.82%) > Gemini 3.7 Flash high primary+retry (57.86%) > OpenRouter ox-alpha (0.00%).
- Secondary Robust BO-Eval ranking: GPT-5.6 SOL high (11.68%) > Kimi K3 (11.09%) > Qwen3.8-27B-FP8 thinking (11.09%) > v4 pro (8.98%) > GLM-5.3 (7.82%) > Gemini 3.7 Flash high primary+retry (2.52%) > OpenRouter ox-alpha (-24.03%).
- BO-only ranking is retained as a diagnostic, but it is not used as the main leaderboard because tiny denominators can create outliers.
- Cost is estimated from OpenRouter model catalog prices (`prompt`, `input_cache_read`, `input_cache_write`, `completion`) converted from USD/token to RMB/M tokens at USD/CNY=6.737012.
- Cache-hit input is charged for every model when OpenRouter exposes `input_cache_read`; explicit cache write/create is not included because these job `result.json` stats do not expose cache-write token fields.
- Qwen cache-hit input is imputed for comparable API-style cost: peer-average non-Qwen cache hit rate 93.90% is applied to Qwen input tokens. Raw Qwen `result.json` cache tokens were 0.
- OpenRouter ox-alpha is included for effect reporting only. Its current run has no standardized `/root/results/<task>_result.json` artifact yet, so missing tasks score raw 0 under the same artifact convention; cost is shown as N/A because no public price was available.
- Price snapshot used by this run: `openrouter-pricing-used-2023-2025.json`.
- Claude Opus 5 is not listed because no completed artifacts were present in the workspace for the 18-task scope.

## Price Table

| Model | OpenRouter model | Price source | Input | Cached read | Cache write/create | Output |
|---|---|---|---:|---:|---:|---:|
| v4 flash baseline | `deepseek/deepseek-v4-flash-0731` | OpenRouter live | ¥0.4042/M | ¥0.0808/M | N/A | ¥0.8084/M |
| v4 pro | `deepseek/deepseek-v4-pro` | OpenRouter live | ¥5.8612/M | ¥0.4884/M | N/A | ¥11.7224/M |
| GLM-5.3 | `z-ai/glm-5.3` | OpenRouter live | ¥9.4318/M | ¥1.7516/M | N/A | ¥29.6429/M |
| GPT-5.6 SOL high | `openai/gpt-5.6-sol` | OpenRouter live | ¥13.4740/M | ¥1.3474/M | ¥16.8425/M | ¥67.3701/M |
| Kimi K3 | `moonshotai/kimi-k3` | OpenRouter live | ¥20.2110/M | ¥2.0211/M | N/A | ¥101.0552/M |
| Gemini 3.7 Flash high primary+retry | `google/gemini-3.7-flash` | OpenRouter live | ¥2.5264/M | ¥0.2526/M | ¥0.1404/M | ¥12.6319/M |
| Qwen3.8-27B-FP8 thinking | `qwen/qwen3.8-27b` | OpenRouter live | ¥2.8632/M | ¥0.5726/M | ¥3.5790/M | ¥17.1794/M |
| OpenRouter ox-alpha | `openai/stealth/ox-alpha` | cost omitted | N/A | N/A | N/A | N/A |

## Figures

- Clickable dashboard: `terminus2-bo-eval-aa-dashboard-2023-2025.html`
- Qwen feasibility audit: `terminus2-qwen27b-feasibility-audit-2023-2025.md`
- Overall effect: `figures/aa-style-2023-2025-effect-bar.png`
- Score-cost: `figures/aa-style-2023-2025-effect-cost-scatter.png`
- O-Eval effect: `figures/aa-style-2023-2025-o-eval-bar.png`
- O-Eval score-cost: `figures/aa-style-2023-2025-o-eval-cost-scatter.png`
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
| OpenRouter ox-alpha | 0.00% | 0.00% | 0.00% |

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
| OpenRouter ox-alpha | 0.00% | 0.00% |

## Year Mean Robust BO-Eval

| Model | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 0.00% |
| v4 pro | 1.70% | 2.81% | 22.44% |
| GLM-5.3 | 11.11% | -0.87% | 13.21% |
| GPT-5.6 SOL high | 10.51% | 2.52% | 22.01% |
| Kimi K3 | 1.97% | -7.74% | 39.03% |
| Gemini 3.7 Flash high primary+retry | 2.27% | -22.95% | 28.24% |
| Qwen3.8-27B-FP8 thinking | 9.56% | 3.52% | 20.18% |
| OpenRouter ox-alpha | -7.19% | -42.13% | -22.79% |

## Suite Mean Robust BO-Eval

| Model | CUMCM | MCM | CUMCM artifacts | MCM artifacts |
|---|---:|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 9 | 9 |
| v4 pro | 11.40% | 6.57% | 9 | 9 |
| GLM-5.3 | 4.40% | 11.23% | 9 | 9 |
| GPT-5.6 SOL high | 15.24% | 8.11% | 9 | 9 |
| Kimi K3 | 7.13% | 15.05% | 9 | 9 |
| Gemini 3.7 Flash high primary+retry | 10.13% | -5.09% | 9 | 6 |
| Qwen3.8-27B-FP8 thinking | 9.40% | 12.77% | 9 | 9 |
| OpenRouter ox-alpha | -28.60% | -19.47% | 0 | 0 |

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

Cells are `direction-aware raw / O-Eval % / BO-only % / Robust BO-Eval %`.

| Year | Suite | Problem | Task | v4 flash baseline | v4 pro | GLM-5.3 | GPT-5.6 SOL high | Kimi K3 | Gemini 3.7 Flash high primary+retry | Qwen3.8-27B-FP8 thinking | OpenRouter ox-alpha | O raw |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 0.967004 / 96.70% / 0.00% / 0.00% | 1.312936 / 131.29% / 1048.41% / 10.00% | 1.393536 / 139.35% / 1292.69% / 10.00% | 0.971969 / 97.20% / 15.05% / 0.50% | 0.975341 / 97.53% / 25.27% / 0.83% | 0.969010 / 96.90% / 6.08% / 0.20% | 1.244533 / 124.45% / 841.10% / 10.00% | 0.000000 / 0.00% / 0.00% / -10.00% | 1.000000 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.345102 / 134.51% / 0.00% / 0.00% | 1.496072 / 149.61% / N/A / 10.00% | 1.500666 / 150.07% / N/A / 10.00% | 2.425664 / 242.57% / N/A / 10.00% | 1.410390 / 141.04% / N/A / 6.53% | 1.496423 / 149.64% / N/A / 10.00% | 1.501820 / 150.18% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -10.00% | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.135026 / 213.50% / 0.00% / 0.00% | 0.597918 / 59.79% / N/A / -10.00% | 0.355098 / 35.51% / N/A / -10.00% | 1.589944 / 158.99% / N/A / -10.00% | 1.134708 / 113.47% / N/A / -10.00% | 2.523435 / 252.34% / N/A / 10.00% | 1.292870 / 129.29% / N/A / -10.00% | 0.000000 / 0.00% / N/A / -10.00% | 1.000000 |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.254589 / 25.46% / 25.46% / 25.46% | 0.203536 / 20.35% / 20.35% / 20.35% | 0.203536 / 20.35% / 20.35% / 20.35% | 0.068138 / 6.81% / 6.81% / 6.81% | 0.254590 / 25.46% / 25.46% / 25.46% | 0.203541 / 20.35% / 20.35% / 20.35% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 1.378763 / 137.88% / 0.00% / 0.00% | 0.318573 / 31.86% / N/A / -10.00% | 0.257329 / 25.73% / N/A / -10.00% | 0.444542 / 44.45% / N/A / -10.00% | 0.943081 / 94.31% / N/A / -10.00% | 0.469069 / 46.91% / N/A / -10.00% | 1.445692 / 144.57% / N/A / 6.69% | 0.000000 / 0.00% / N/A / -10.00% | 1.000000 |
| 2024 | CUMCM | C | `cumcm-2024-c-crop-planting` | 0.475492 / 47.55% / 0.00% / 0.00% | 0.345043 / 34.50% / 0.00% / -24.87% | 0.285151 / 28.52% / 0.00% / -36.29% | 0.588775 / 58.88% / 21.60% / 21.60% | 0.191121 / 19.11% / 0.00% / -54.22% | 0.193549 / 19.35% / 0.00% / -53.75% | 0.172944 / 17.29% / 0.00% / -57.68% | 0.000000 / 0.00% / 0.00% / -90.65% | 1.000000 |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 0.727946 / 72.79% / 0.00% / 0.00% | 1.532372 / 153.24% / 295.69% / 100.00% | 0.854445 / 85.44% / 46.50% / 46.50% | 3.416382 / 341.64% / 988.20% / 100.00% | 2.894037 / 289.40% / 796.20% / 100.00% | 1.239279 / 123.93% / 187.95% / 100.00% | 2.591825 / 259.18% / 685.11% / 100.00% | 0.000000 / 0.00% / 0.00% / -100.00% | 1.000000 |
| 2025 | CUMCM | B | `cumcm-2025-b-sic-thickness` | 0.143179 / 14.32% / 0.00% / 0.00% | 0.246099 / 24.61% / 12.01% / 12.01% | 0.306245 / 30.62% / 19.03% / 19.03% | 0.242011 / 24.20% / 11.53% / 11.53% | 0.436145 / 43.61% / 34.19% / 34.19% | 0.307888 / 30.79% / 19.22% / 19.22% | 0.187085 / 18.71% / 5.12% / 5.12% | 0.000000 / 0.00% / 0.00% / -16.71% | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.520296 / 152.03% / 0.00% / 0.00% | 1.360909 / 136.09% / N/A / -10.00% | 1.071182 / 107.12% / N/A / -10.00% | 1.452420 / 145.24% / N/A / -6.79% | 1.289804 / 128.98% / N/A / -10.00% | 1.234068 / 123.41% / N/A / -10.00% | 1.521520 / 152.15% / N/A / 0.12% | 0.000000 / 0.00% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.541010 / 154.10% / 0.00% / 0.00% | 1.179422 / 117.94% / N/A / -10.00% | 1.538784 / 153.88% / N/A / -0.22% | 1.364424 / 136.44% / N/A / -10.00% | 0.469546 / 46.95% / N/A / -10.00% | 0.545375 / 54.54% / N/A / -10.00% | 1.070439 / 107.04% / N/A / -10.00% | 0.000000 / 0.00% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | 0.030363 / 3.04% / 0.00% / 0.00% | 0.034371 / 3.44% / 0.41% / 0.41% | 0.068142 / 6.81% / 3.90% / 3.90% | 0.032355 / 3.24% / 0.21% / 0.21% | 0.028745 / 2.87% / 0.00% / -0.17% | 0.063352 / 6.34% / 3.40% / 3.40% | 0.024041 / 2.40% / 0.00% / -0.65% | 0.000000 / 0.00% / 0.00% / -3.13% | 1.000000 |
| 2023 | MCM | C | `mcm-2023-c-wordle` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.097978 / 9.80% / 9.80% / 9.80% | 0.529999 / 53.00% / 53.00% / 53.00% | 0.723478 / 72.35% / 72.35% / 72.35% | 0.246521 / 24.65% / 24.65% / 24.65% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.580000 / 58.00% / 58.00% / 58.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | 0.235294 / 23.53% / 0.00% / 0.00% | 0.235294 / 23.53% / 0.00% / 0.00% | 0.125000 / 12.50% / 0.00% / -14.42% | 0.070175 / 7.02% / 0.00% / -21.59% | 0.246711 / 24.67% / 1.49% / 1.49% | 0.228957 / 22.90% / 0.00% / -0.83% | 0.070175 / 7.02% / 0.00% / -21.59% | 0.000000 / 0.00% / 0.00% / -30.77% | 1.000000 |
| 2024 | MCM | B | `mcm-2024-b-submersible-search` | 0.176025 / 17.60% / 0.00% / 0.00% | 0.296505 / 29.65% / 14.62% / 14.62% | 0.709302 / 70.93% / 64.72% / 64.72% | 0.389026 / 38.90% / 25.85% / 25.85% | 0.470888 / 47.09% / 35.79% / 35.79% | 0.187946 / 18.79% / 1.45% / 1.45% | 0.753209 / 75.32% / 70.05% / 70.05% | 0.000000 / 0.00% / 0.00% / -21.36% | 1.000000 |
| 2024 | MCM | C | `mcm-2024-c-tennis-momentum` | 0.507190 / 50.72% / 0.00% / 0.00% | 0.564619 / 56.46% / 11.65% / 11.65% | 0.361433 / 36.14% / 0.00% / -29.58% | 0.403266 / 40.33% / 0.00% / -21.09% | 0.377542 / 37.75% / 0.00% / -26.31% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.523386 / 52.34% / 3.29% / 3.29% | 0.000000 / 0.00% / 0.00% / -100.00% | 1.000000 |
| 2025 | MCM | A | `mcm-2025-a-stair-wear` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.233333 / 23.33% / 23.33% / 23.33% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2025 | MCM | B | `mcm-2025-b-juneau-tourism` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.426076 / 42.61% / 42.61% / 42.61% | 0.337214 / 33.72% / 33.72% / 33.72% | 0.372904 / 37.29% / 37.29% / 37.29% | 1.460140 / 146.01% / 146.01% / 100.00% | 0.702044 / 70.20% / 70.20% / 70.20% | 0.025227 / 2.52% / 2.52% / 2.52% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.773903 / 177.39% / 0.00% / 0.00% | 0.838169 / 83.82% / N/A / -10.00% | 0.870336 / 87.03% / N/A / -10.00% | 0.457106 / 45.71% / N/A / -10.00% | 2.995504 / 299.55% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -10.00% | 0.138589 / 13.86% / N/A / -10.00% | 0.000000 / 0.00% / N/A / -10.00% | 1.000000 |