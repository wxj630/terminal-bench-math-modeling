# O-Eval and Robust BO-Eval: 2023-2025

Generated: 2026-10-08

Scope: 2023, 2024, and 2025 terminal-bench-math-modeling tasks, 18 tasks total. This report rescored saved artifacts only; it does not rerun models or modify job result files.

Primary O-Eval rule: `clamp(model direction-aware raw / O raw, 0, 1)`, averaged over all 18 tasks. Since the O-award reproduction is normalized near raw=1 on these tasks, O-Eval is the easiest-to-read absolute oracle-normalized score, and overshoots are capped at 100%.

Secondary Robust BO-Eval rule: let `gain = model raw - flash raw` and `gap = O raw - flash raw`. If `gap >= 0.10`, score `clip(gain / gap, -100%, +100%)`; otherwise score `clip(gain, -10pp, +10pp)`. Normal completed tasks still use the clipped fallback on tiny-gap cases, but any missing or non-scoreable artifact is assigned `-100%` so a completely unfinished task gets the worst possible score.

Tempered hard-gated rule: only clearly non-feasible cells are whole-task penalized. Automatic scorer hard-invalid metrics and manually replay-proven invalid high-score cells receive gated raw `0` for O-Eval and `-100%` for Robust BO-Eval. Needs-review/proxy cells remain scored but are not used as stronger-than-O claims without a better replay verifier.

Robust ratio tasks with gap >= 0.10: 12. Saturated or near-zero-gap tasks using clipped B-Eval: 6.

## Overall Mean

| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB | Canonical valid/running/error/pending | Excluded retries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| v4 flash baseline | 17 | 0.783920 | 54.59% | +0.00 pp | 0.00% | 33,032,997 / 31,802,112 / 1,896,174 | 1,230,885 / 1,896,174 | $0.683019 | ¥4.60 | 18/0/0/0 | 0 |
| opencode + deepseek-flash | 18 | 0.942707 | 65.76% | +15.88 pp | 18.36% | 89,376,395 / 88,668,288 / 569,862 | 708,107 / 569,862 | $2.535912 | ¥17.08 | 18/0/0/0 | 6 |
| opencode + deepseek-flash (max) | 17 | 0.651325 | 54.93% | -13.26 pp | 12.74% | 105,481,424 / 104,781,440 / 610,561 | 699,984 / 610,561 | $2.783484 | ¥18.75 | 17/0/1/0 | 0 |
| codex + GPT-6 Astra | 18 | 0.775532 | 52.85% | -0.84 pp | 16.03% | 84,337,603 / 0 / 2,132,173 | 84,337,603 / 2,132,173 | $246.410839 | N/A | 18/0/0/0 | 0 |
| claude-code + Fable 5.1 | 18 | 0.890061 | 62.62% | +10.61 pp | 20.22% | 51,903,796 / 0 / 3,795,512 | 51,903,796 / 3,795,512 | $272.800916 | N/A | 18/0/0/0 | 0 |
| codex + gpt-5.5 xhigh | 18 | 0.892105 | 68.07% | +10.82 pp | 23.62% | 108,584,170 / 105,199,744 / 994,910 | 3,384,426 / 994,910 | $99.369234 | ¥669.45 | 18/0/0/0 | 0 |
| v4 pro | 18 | 0.715620 | 58.62% | -6.83 pp | 12.30% | 21,309,105 / 20,096,768 / 1,748,356 | 1,212,337 / 1,748,356 | $5.553888 | ¥37.42 | 18/0/0/0 | 0 |
| GLM-5.3 | 18 | 0.687859 | 60.43% | -9.61 pp | 12.97% | 92,056,972 / 89,637,696 / 2,638,779 | 2,419,276 / 2,638,779 | $38.303415 | ¥258.05 | 18/0/0/0 | 0 |
| GPT-5.6 SOL high | 18 | 0.928319 | 63.67% | +14.44 pp | 16.12% | 8,774,606 / 7,566,848 / 497,473 | 1,207,758 / 497,473 | $8.903616 | ¥59.98 | 18/0/0/0 | 0 |
| GPT-5.6 SOL xhigh | 17 | 0.735805 | 60.40% | -4.81 pp | 9.79% | 16,596,399 / 14,928,768 / 841,198 | 1,667,631 / 841,198 | $14.732996 | ¥99.26 | 17/0/1/0 | 3 |
| Kimi K3 | 18 | 0.945874 | 65.36% | +16.20 pp | 21.41% | 30,146,116 / 28,928,953 / 956,805 | 1,217,163 / 956,805 | $26.682250 | ¥179.76 | 17/0/1/0 | 0 |
| Gemini 3.7 Flash high primary+retry | 15 | 0.658446 | 51.99% | -12.55 pp | -4.91% | 69,131,259 / 62,497,004 / 705,776 | 6,634,255 / 705,776 | $6.154813 | ¥41.47 | 18/0/0/0 | 1 |
| Qwen3.8-27B-FP8 thinking | 18 | 0.866389 | 65.81% | +8.25 pp | 22.41% | 47,245,909 / 0 / 3,178,409 | 47,245,909 / 3,178,409 | $28.184454 | ¥189.88 | 17/0/1/0 | 0 |
| GLM-5.3-Flash (ox-alpha) | 18 | 0.752552 | 57.93% | -3.14 pp | 10.13% | 107,726,029 / 101,466,688 / 3,683,366 | 6,259,341 / 3,683,366 | $2.912292 | ¥19.62 | 17/0/1/0 | 20 |
| Qwen3.8 Flash (Bailian) | 18 | 0.666536 | 55.31% | -11.74 pp | 4.86% | 299,616,972 / 293,563,264 / 6,814,374 | 6,053,708 / 6,814,374 | $8.807824 | ¥59.34 | 16/0/2/0 | 0 |
| Tencent Hy4 Preview | 18 | 0.942218 | 64.78% | +15.83 pp | 16.50% | 133,731,323 / 128,999,040 / 2,068,825 | 4,732,283 / 2,068,825 | $14.538815 | ¥97.95 | 18/0/0/0 | 0 |

## Tempered Hard-Gated Leaderboard

| Rank | Model | Hard-gated O-Eval | Hard-gated Robust BO-Eval | Original O-Eval | Original Robust BO-Eval | Hard-gated raw mean | Hard gates | Est. cost RMB |
|---:|---|---:|---:|---:|---:|---:|---|---:|
| 1 | codex + gpt-5.5 xhigh | 68.07% | 23.62% | 68.07% | 23.62% | 0.892105 | 0 | ¥669.45 |
| 2 | Qwen3.8-27B-FP8 thinking | 65.81% | 22.41% | 65.81% | 22.41% | 0.866389 | 0 | ¥189.88 |
| 3 | opencode + deepseek-flash | 65.76% | 18.36% | 65.76% | 18.36% | 0.942707 | 0 | ¥17.08 |
| 4 | Tencent Hy4 Preview | 64.78% | 16.50% | 64.78% | 16.50% | 0.942218 | 0 | ¥97.95 |
| 5 | GPT-5.6 SOL high | 63.67% | 16.56% | 63.67% | 16.12% | 0.928319 | 0 | ¥59.98 |
| 6 | claude-code + Fable 5.1 | 62.62% | 20.98% | 62.62% | 20.22% | 0.890061 | 0 | N/A |
| 7 | GPT-5.6 SOL xhigh | 60.40% | 9.79% | 60.40% | 9.79% | 0.735805 | 0 | ¥99.26 |
| 8 | v4 pro | 58.62% | 12.30% | 58.62% | 12.30% | 0.715620 | 0 | ¥37.42 |
| 9 | Qwen3.8 Flash (Bailian) | 55.31% | 4.86% | 55.31% | 4.86% | 0.666536 | 0 | ¥59.34 |
| 10 | GLM-5.3 | 54.87% | 1.86% | 60.43% | 12.97% | 0.610440 | 1: `cumcm-2023-a-heliostat-field` | ¥258.05 |
| 11 | Kimi K3 | 54.25% | 4.57% | 65.36% | 21.41% | 0.698339 | 2: `mcm-2025-b-juneau-tourism`, `mcm-2025-c-olympic-medals` | ¥179.76 |
| 12 | codex + GPT-6 Astra | 52.85% | 16.03% | 52.85% | 16.03% | 0.775532 | 0 | N/A |
| 13 | GLM-5.3-Flash (ox-alpha) | 52.37% | 4.02% | 57.93% | 10.13% | 0.610737 | 1: `cumcm-2025-a-smoke-screen` | ¥19.62 |
| 14 | v4 flash baseline | 50.49% | 0.00% | 54.59% | 0.00% | 0.742908 | 1: `cumcm-2023-a-heliostat-field` | ¥4.60 |
| 15 | opencode + deepseek-flash (max) | 49.38% | 1.63% | 54.93% | 12.74% | 0.586406 | 1: `cumcm-2023-a-heliostat-field` | ¥18.75 |
| 16 | Gemini 3.7 Flash high primary+retry | 46.61% | -15.36% | 51.99% | -4.91% | 0.604612 | 1: `cumcm-2023-a-heliostat-field` | ¥41.47 |

## Hard Gate Decisions

| Model | Task | Raw before gate | Gated raw | O-Eval before | Hard-gated O-Eval | Robust before | Hard-gated Robust | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|
| v4 flash baseline | `cumcm-2023-a-heliostat-field` | 0.738213 | 0.000000 | 73.82% | 0.00% | 0.00% | 0.00% | hard-invalid/heliostat-constraint: Q2 rated-power constraint violation: 53.795541 MW is below the required approximately 60 MW; Q3 rated-power constraint violation: 53.795541 MW is below the required approximately 60 MW; Q3 does not expose numeric mirror dimensions |
| opencode + deepseek-flash (max) | `cumcm-2023-a-heliostat-field` | 1.168550 | 0.000000 | 100.00% | 0.00% | 100.00% | -100.00% | hard-invalid/heliostat-constraint: Q2 rated-power constraint violation: 59.997149 MW is below the required approximately 60 MW; Q3 rated-power constraint violation: 59.997149 MW is below the required approximately 60 MW |
| GLM-5.3 | `cumcm-2023-a-heliostat-field` | 1.393536 | 0.000000 | 100.00% | 0.00% | 100.00% | -100.00% | explicit Q3 design note violates heliostat installation-height bound: one tail mirror uses z=1.9024 m, below the required 2 m minimum |
| Gemini 3.7 Flash high primary+retry | `cumcm-2023-a-heliostat-field` | 0.969010 | 0.000000 | 96.90% | 0.00% | 88.16% | -100.00% | hard-invalid/heliostat-constraint: Question 2 rated-power constraint violation: 55.460000 MW is below the required approximately 60 MW; Question 3 rated-power constraint violation: 54.966000 MW is below the required approximately 60 MW |
| GLM-5.3-Flash (ox-alpha) | `cumcm-2025-a-smoke-screen` | 2.552664 | 0.000000 | 100.00% | 0.00% | 10.00% | -100.00% | independent smoke-screen replay gives 0.00s coverage under O-reference line-of-sight geometry |
| Kimi K3 | `mcm-2025-b-juneau-tourism` | 1.460140 | 0.000000 | 100.00% | 0.00% | 100.00% | -100.00% | unit/scale invalid: resident_acceptance_index=1.5 and sustainability_score=232.2 on a unit-scale score |
| Kimi K3 | `mcm-2025-c-olympic-medals` | 2.995504 | 0.000000 | 100.00% | 0.00% | 10.00% | -100.00% | invalid high coach-effect result: only three scored recommendations and endpoint verifier reward is negative/BO 0 |

## Primary Readout

- 18-task primary O-Eval ranking: codex + gpt-5.5 xhigh (68.07%) > Qwen3.8-27B-FP8 thinking (65.81%) > opencode + deepseek-flash (65.76%) > Kimi K3 (65.36%) > Tencent Hy4 Preview (64.78%) > GPT-5.6 SOL high (63.67%) > claude-code + Fable 5.1 (62.62%) > GLM-5.3 (60.43%) > GPT-5.6 SOL xhigh (60.40%) > v4 pro (58.62%) > GLM-5.3-Flash (ox-alpha) (57.93%) > Qwen3.8 Flash (Bailian) (55.31%) > opencode + deepseek-flash (max) (54.93%) > codex + GPT-6 Astra (52.85%) > Gemini 3.7 Flash high primary+retry (51.99%).
- Tempered hard-gated O-Eval ranking: codex + gpt-5.5 xhigh (68.07%) > Qwen3.8-27B-FP8 thinking (65.81%) > opencode + deepseek-flash (65.76%) > Tencent Hy4 Preview (64.78%) > GPT-5.6 SOL high (63.67%) > claude-code + Fable 5.1 (62.62%) > GPT-5.6 SOL xhigh (60.40%) > v4 pro (58.62%) > Qwen3.8 Flash (Bailian) (55.31%) > GLM-5.3 (54.87%) > Kimi K3 (54.25%) > codex + GPT-6 Astra (52.85%) > GLM-5.3-Flash (ox-alpha) (52.37%) > opencode + deepseek-flash (max) (49.38%) > Gemini 3.7 Flash high primary+retry (46.61%).
- Secondary Robust BO-Eval ranking: codex + gpt-5.5 xhigh (23.62%) > Qwen3.8-27B-FP8 thinking (22.41%) > Kimi K3 (21.41%) > claude-code + Fable 5.1 (20.22%) > opencode + deepseek-flash (18.36%) > Tencent Hy4 Preview (16.50%) > GPT-5.6 SOL high (16.12%) > codex + GPT-6 Astra (16.03%) > GLM-5.3 (12.97%) > opencode + deepseek-flash (max) (12.74%) > v4 pro (12.30%) > GLM-5.3-Flash (ox-alpha) (10.13%) > GPT-5.6 SOL xhigh (9.79%) > Qwen3.8 Flash (Bailian) (4.86%) > Gemini 3.7 Flash high primary+retry (-4.91%).
- Tempered hard-gated Robust BO-Eval ranking: codex + gpt-5.5 xhigh (23.62%) > Qwen3.8-27B-FP8 thinking (22.41%) > claude-code + Fable 5.1 (20.98%) > opencode + deepseek-flash (18.36%) > GPT-5.6 SOL high (16.56%) > Tencent Hy4 Preview (16.50%) > codex + GPT-6 Astra (16.03%) > v4 pro (12.30%) > GPT-5.6 SOL xhigh (9.79%) > Qwen3.8 Flash (Bailian) (4.86%) > Kimi K3 (4.57%) > GLM-5.3-Flash (ox-alpha) (4.02%) > GLM-5.3 (1.86%) > opencode + deepseek-flash (max) (1.63%) > Gemini 3.7 Flash high primary+retry (-15.36%).
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
| v4 flash baseline | `deepseek/deepseek-v4-flash-0731` | model_config (fixed) | ¥0.4042/M | ¥0.0808/M | N/A | ¥0.8084/M |
| opencode + deepseek-flash | `deepseek/deepseek-v4.1-flash` | model_config (fixed) | ¥2.0211/M | ¥0.0404/M | N/A | ¥8.0844/M |
| opencode + deepseek-flash (max) | `deepseek/deepseek-v4.1-flash` | model_config (fixed) | ¥2.0211/M | ¥0.0404/M | N/A | ¥8.0844/M |
| codex + GPT-6 Astra | `N/A` | cost omitted | N/A | N/A | N/A | N/A |
| claude-code + Fable 5.1 | `N/A` | cost omitted | N/A | N/A | N/A | N/A |
| codex + gpt-5.5 xhigh | `openai/gpt-5.5` | model_config (fixed) | ¥33.6851/M | ¥3.3685/M | N/A | ¥202.1104/M |
| v4 pro | `deepseek/deepseek-v4-pro` | model_config (fixed) | ¥5.8612/M | ¥0.4884/M | N/A | ¥11.7224/M |
| GLM-5.3 | `z-ai/glm-5.3` | model_config (fixed) | ¥9.4318/M | ¥1.7516/M | N/A | ¥29.6429/M |
| GPT-5.6 SOL high | `openai/gpt-5.6-sol` | model_config (fixed) | ¥13.4740/M | ¥1.3474/M | N/A | ¥67.3701/M |
| GPT-5.6 SOL xhigh | `openai/gpt-5.6-sol` | model_config (fixed) | ¥13.4740/M | ¥1.3474/M | N/A | ¥67.3701/M |
| Kimi K3 | `moonshotai/kimi-k3` | model_config (fixed) | ¥20.2110/M | ¥2.0211/M | N/A | ¥101.0552/M |
| Gemini 3.7 Flash high primary+retry | `google/gemini-3.7-flash` | model_config (fixed) | ¥2.5264/M | ¥0.2526/M | N/A | ¥12.6319/M |
| Qwen3.8-27B-FP8 thinking | `qwen/qwen3.8-27b` | model_config (fixed) | ¥2.8632/M | ¥0.5726/M | ¥3.5790/M | ¥17.1794/M |
| GLM-5.3-Flash (ox-alpha) | `z-ai/glm-5.3-flash` | user-supplied fixed snapshot | ¥0.5053/M | ¥0.1011/M | N/A | ¥1.6843/M |
| Qwen3.8 Flash (Bailian) | `qwen/qwen3.8-flash` | user-supplied fixed snapshot | ¥1.0106/M | ¥0.1078/M | ¥1.3474/M | ¥3.1664/M |
| Tencent Hy4 Preview | `tencent/hy4-preview` | model_config (fixed) | ¥5.6187/M | ¥0.2830/M | N/A | ¥16.8493/M |

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
| v4 flash baseline | 67.74% | 29.00% | 67.03% |
| opencode + deepseek-flash | 77.94% | 59.10% | 60.23% |
| opencode + deepseek-flash (max) | 63.56% | 62.23% | 39.01% |
| codex + GPT-6 Astra | 61.55% | 56.25% | 40.75% |
| claude-code + Fable 5.1 | 65.20% | 53.71% | 68.94% |
| codex + gpt-5.5 xhigh | 66.93% | 74.88% | 62.39% |
| v4 pro | 62.17% | 56.40% | 57.28% |
| GLM-5.3 | 65.89% | 52.65% | 62.76% |
| GPT-5.6 SOL high | 78.80% | 56.10% | 56.12% |
| GPT-5.6 SOL xhigh | 55.56% | 67.76% | 57.90% |
| Kimi K3 | 62.00% | 55.25% | 78.83% |
| Gemini 3.7 Flash high primary+retry | 59.63% | 39.27% | 57.08% |
| Qwen3.8-27B-FP8 thinking | 76.73% | 74.78% | 45.90% |
| GLM-5.3-Flash (ox-alpha) | 60.91% | 64.90% | 47.97% |
| Qwen3.8 Flash (Bailian) | 57.70% | 50.03% | 58.22% |
| Tencent Hy4 Preview | 82.82% | 51.96% | 59.57% |

## Suite Mean O-Eval

| Model | CUMCM | MCM |
|---|---:|---:|
| v4 flash baseline | 70.58% | 38.60% |
| opencode + deepseek-flash | 93.40% | 38.11% |
| opencode + deepseek-flash (max) | 81.88% | 27.98% |
| codex + GPT-6 Astra | 76.66% | 29.04% |
| claude-code + Fable 5.1 | 89.08% | 36.15% |
| codex + gpt-5.5 xhigh | 93.80% | 42.33% |
| v4 pro | 72.49% | 44.74% |
| GLM-5.3 | 73.62% | 47.24% |
| GPT-5.6 SOL high | 87.47% | 39.87% |
| GPT-5.6 SOL xhigh | 74.47% | 46.34% |
| Kimi K3 | 85.86% | 44.86% |
| Gemini 3.7 Flash high primary+retry | 82.40% | 21.59% |
| Qwen3.8-27B-FP8 thinking | 92.85% | 38.76% |
| GLM-5.3-Flash (ox-alpha) | 78.69% | 37.16% |
| Qwen3.8 Flash (Bailian) | 73.39% | 37.24% |
| Tencent Hy4 Preview | 83.52% | 46.05% |

## Year Mean Robust BO-Eval

| Model | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 0.00% |
| opencode + deepseek-flash | 22.00% | 43.32% | -10.25% |
| opencode + deepseek-flash (max) | 17.52% | 46.60% | -25.90% |
| codex + GPT-6 Astra | 14.23% | 42.65% | -8.79% |
| claude-code + Fable 5.1 | 19.86% | 37.59% | 3.20% |
| codex + gpt-5.5 xhigh | 14.93% | 65.47% | -9.55% |
| v4 pro | 9.43% | 42.59% | -15.13% |
| GLM-5.3 | 19.52% | 26.76% | -7.38% |
| GPT-5.6 SOL high | 22.65% | 39.85% | -14.13% |
| GPT-5.6 SOL xhigh | -20.25% | 58.82% | -9.21% |
| Kimi K3 | 9.51% | 38.65% | 16.06% |
| Gemini 3.7 Flash high primary+retry | -4.74% | 2.83% | -12.83% |
| Qwen3.8-27B-FP8 thinking | 19.69% | 65.34% | -17.79% |
| GLM-5.3-Flash (ox-alpha) | -12.77% | 55.61% | -12.44% |
| Qwen3.8 Flash (Bailian) | 9.30% | 17.53% | -12.25% |
| Tencent Hy4 Preview | 29.83% | 28.50% | -8.84% |

## Suite Mean Robust BO-Eval

| Model | CUMCM | MCM | CUMCM artifacts | MCM artifacts |
|---|---:|---:|---:|---:|
| v4 flash baseline | 0.00% | 0.00% | 8 | 9 |
| opencode + deepseek-flash | 36.84% | -0.13% | 9 | 9 |
| opencode + deepseek-flash (max) | 23.12% | 2.36% | 8 | 9 |
| codex + GPT-6 Astra | 34.08% | -2.02% | 9 | 9 |
| claude-code + Fable 5.1 | 32.53% | 7.90% | 9 | 9 |
| codex + gpt-5.5 xhigh | 39.38% | 7.85% | 9 | 9 |
| v4 pro | 16.48% | 8.12% | 9 | 9 |
| GLM-5.3 | 13.78% | 12.15% | 9 | 9 |
| GPT-5.6 SOL high | 24.62% | 7.63% | 9 | 9 |
| GPT-5.6 SOL xhigh | 7.87% | 11.70% | 8 | 9 |
| Kimi K3 | 26.10% | 16.71% | 9 | 9 |
| Gemini 3.7 Flash high primary+retry | 18.41% | -28.23% | 9 | 6 |
| Qwen3.8-27B-FP8 thinking | 33.60% | 11.21% | 9 | 9 |
| GLM-5.3-Flash (ox-alpha) | 11.14% | 9.13% | 8 | 9 |
| Qwen3.8 Flash (Bailian) | 3.08% | 6.64% | 7 | 9 |
| Tencent Hy4 Preview | 16.70% | 16.29% | 9 | 9 |

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

| Year | Suite | Problem | Task | v4 flash baseline | opencode + deepseek-flash | opencode + deepseek-flash (max) | codex + GPT-6 Astra | claude-code + Fable 5.1 | codex + gpt-5.5 xhigh | v4 pro | GLM-5.3 | GPT-5.6 SOL high | GPT-5.6 SOL xhigh | Kimi K3 | Gemini 3.7 Flash high primary+retry | Qwen3.8-27B-FP8 thinking | GLM-5.3-Flash (ox-alpha) | Qwen3.8 Flash (Bailian) | Tencent Hy4 Preview | O raw |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 0.738213 / 73.82% / 0.00% / 0.00% | 1.103930 / 100.00% / 139.70% / 100.00% | 1.168550 / 100.00% / 164.38% / 100.00% | 1.370825 / 100.00% / 241.65% / 100.00% | 0.951569 / 95.16% / 81.50% / 81.50% | 1.097346 / 100.00% / 137.19% / 100.00% | 1.312936 / 100.00% / 219.54% / 100.00% | 1.393536 / 100.00% / 250.33% / 100.00% | 0.971969 / 97.20% / 89.29% / 89.29% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.975341 / 97.53% / 90.58% / 90.58% | 0.969010 / 96.90% / 88.16% / 88.16% | 1.244533 / 100.00% / 193.41% / 100.00% | 0.000000 / 0.00% / 0.00% / -100.00% | 1.455864 / 100.00% / 274.14% / 100.00% | 1.464003 / 100.00% / 277.24% / 100.00% | 1.000000 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.492402 / 100.00% / 0.00% / 0.00% | 1.566098 / 100.00% / N/A / 7.37% | 1.493015 / 100.00% / N/A / 0.06% | 2.330462 / 100.00% / N/A / 10.00% | 2.358966 / 100.00% / N/A / 10.00% | 2.542996 / 100.00% / N/A / 10.00% | 1.496072 / 100.00% / N/A / 0.37% | 1.500666 / 100.00% / N/A / 0.83% | 2.425664 / 100.00% / N/A / 10.00% | 1.463138 / 100.00% / N/A / -2.93% | 1.410390 / 100.00% / N/A / -8.20% | 1.496423 / 100.00% / N/A / 0.40% | 1.501820 / 100.00% / N/A / 0.94% | 1.500621 / 100.00% / N/A / 0.82% | 1.542730 / 100.00% / N/A / 5.03% | 2.349865 / 100.00% / N/A / 10.00% | 1.000000 |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 2.550299 / 100.00% / 0.00% / 0.00% | 1.714187 / 100.00% / N/A / -10.00% | 1.940776 / 100.00% / N/A / -10.00% | 0.407264 / 40.73% / N/A / -10.00% | 1.448011 / 100.00% / N/A / -10.00% | 1.635081 / 100.00% / N/A / -10.00% | 0.597918 / 59.79% / N/A / -10.00% | 0.355098 / 35.51% / N/A / -10.00% | 1.589944 / 100.00% / N/A / -10.00% | 1.427361 / 100.00% / N/A / -10.00% | 1.134708 / 100.00% / N/A / -10.00% | 2.523435 / 100.00% / N/A / -2.69% | 1.292870 / 100.00% / N/A / -10.00% | 1.707570 / 100.00% / N/A / -10.00% | 1.755009 / 100.00% / N/A / -10.00% | 0.963631 / 96.36% / N/A / -10.00% | 1.000000 |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 0.220263 / 22.03% / 0.00% / 0.00% | 0.999998 / 100.00% / 100.00% / 100.00% | 0.999895 / 99.99% / 99.99% / 99.99% | 0.999998 / 100.00% / 100.00% / 100.00% | 0.999998 / 100.00% / 100.00% / 100.00% | 0.999998 / 100.00% / 100.00% / 100.00% | 0.498202 / 49.82% / 35.65% / 35.65% | 1.000000 / 100.00% / 100.00% / 100.00% | 0.999998 / 100.00% / 100.00% / 100.00% | 0.999998 / 100.00% / 100.00% / 100.00% | 0.078771 / 7.88% / 0.00% / -18.15% | 0.498202 / 49.82% / 35.65% / 35.65% | 0.999883 / 99.99% / 99.98% / 99.98% | 0.999998 / 100.00% / 100.00% / 100.00% | 1.000000 / 100.00% / 100.00% / 100.00% | 0.999998 / 100.00% / 100.00% / 100.00% | 1.000000 |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.737706 / 73.77% / 73.77% / 73.77% | 0.750214 / 75.02% / 75.02% / 75.02% | 0.297261 / 29.73% / 29.73% / 29.73% | 0.362732 / 36.27% / 36.27% / 36.27% | 0.788883 / 78.89% / 78.89% / 78.89% | 0.318573 / 31.86% / 31.86% / 31.86% | 0.257329 / 25.73% / 25.73% / 25.73% | 0.444542 / 44.45% / 44.45% / 44.45% | 0.479172 / 47.92% / 47.92% / 47.92% | 0.943081 / 94.31% / 94.31% / 94.31% | 0.469069 / 46.91% / 46.91% / 46.91% | 1.445692 / 100.00% / 144.57% / 100.00% | 0.390214 / 39.02% / 39.02% / 39.02% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.366504 / 36.65% / 36.65% / 36.65% | 1.000000 |
| 2024 | CUMCM | C | `cumcm-2024-c-crop-planting` | 0.631481 / 63.15% / 0.00% / 0.00% | 1.593766 / 100.00% / 261.12% / 100.00% | 0.911223 / 91.12% / 75.91% / 75.91% | 1.089400 / 100.00% / 124.26% / 100.00% | 1.075121 / 100.00% / 120.38% / 100.00% | 1.361571 / 100.00% / 198.11% / 100.00% | 1.448533 / 100.00% / 221.71% / 100.00% | 0.455660 / 45.57% / 0.00% / -47.71% | 0.918474 / 91.85% / 77.88% / 77.88% | 1.015015 / 100.00% / 104.07% / 100.00% | 1.076446 / 100.00% / 120.74% / 100.00% | 0.756826 / 75.68% / 34.01% / 34.01% | 1.081087 / 100.00% / 122.00% / 100.00% | 1.121885 / 100.00% / 133.07% / 100.00% | 0.939687 / 93.97% / 83.63% / 83.63% | 0.625186 / 62.52% / 0.00% / -1.71% | 1.000000 |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 1.527989 / 100.00% / 0.00% / 0.00% | 3.578239 / 100.00% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 3.572965 / 100.00% / N/A / 10.00% | 3.609138 / 100.00% / N/A / 10.00% | 1.829285 / 100.00% / N/A / 10.00% | 1.532372 / 100.00% / N/A / 0.44% | 0.854445 / 85.44% / N/A / -10.00% | 3.416382 / 100.00% / N/A / 10.00% | 0.939201 / 93.92% / N/A / -10.00% | 2.894037 / 100.00% / N/A / 10.00% | 1.239279 / 100.00% / N/A / -10.00% | 2.591825 / 100.00% / N/A / 10.00% | 2.552664 / 100.00% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 4.004026 / 100.00% / N/A / 10.00% | 1.000000 |
| 2025 | CUMCM | B | `cumcm-2025-b-sic-thickness` | 0.762319 / 76.23% / 0.00% / 0.00% | 0.668246 / 66.82% / 0.00% / -39.58% | 0.707946 / 70.79% / 0.00% / -22.88% | 0.707683 / 70.77% / 0.00% / -22.99% | 0.702963 / 70.30% / 0.00% / -24.97% | 0.704257 / 70.43% / 0.00% / -24.43% | 0.109821 / 10.98% / 0.00% / -100.00% | 0.703334 / 70.33% / 0.00% / -24.82% | 0.537264 / 53.73% / 0.00% / -94.69% | 0.657456 / 65.75% / 0.00% / -44.12% | 0.729831 / 72.98% / 0.00% / -13.67% | 0.722558 / 72.26% / 0.00% / -16.73% | 0.357013 / 35.70% / 0.00% / -100.00% | 0.691962 / 69.20% / 0.00% / -29.60% | 0.664995 / 66.50% / 0.00% / -40.95% | 0.561223 / 56.12% / 0.00% / -84.61% | 1.000000 |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.506359 / 100.00% / 0.00% / 0.00% | 1.235518 / 100.00% / N/A / -10.00% | 1.233863 / 100.00% / N/A / -10.00% | 0.487255 / 48.73% / N/A / -10.00% | 1.258849 / 100.00% / N/A / -10.00% | 0.949136 / 94.91% / N/A / -10.00% | 1.360909 / 100.00% / N/A / -10.00% | 1.071182 / 100.00% / N/A / -10.00% | 1.452420 / 100.00% / N/A / -5.39% | 0.626050 / 62.60% / N/A / -10.00% | 1.289804 / 100.00% / N/A / -10.00% | 1.234068 / 100.00% / N/A / -10.00% | 1.521520 / 100.00% / N/A / 1.52% | 1.073057 / 100.00% / N/A / -10.00% | 1.287680 / 100.00% / N/A / -10.00% | 1.184644 / 100.00% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.632029 / 100.00% / 0.00% / 0.00% | 1.340862 / 100.00% / N/A / -10.00% | 0.302446 / 30.24% / N/A / -10.00% | 1.082519 / 100.00% / N/A / -10.00% | 0.271790 / 27.18% / N/A / -10.00% | 0.702577 / 70.26% / N/A / -10.00% | 1.179422 / 100.00% / N/A / -10.00% | 1.538784 / 100.00% / N/A / -9.32% | 1.364424 / 100.00% / N/A / -10.00% | 1.364410 / 100.00% / N/A / -10.00% | 0.469546 / 46.95% / N/A / -10.00% | 0.545375 / 54.54% / N/A / -10.00% | 1.070439 / 100.00% / N/A / -10.00% | 1.163407 / 100.00% / N/A / -10.00% | 0.373162 / 37.32% / N/A / -10.00% | 1.296434 / 100.00% / N/A / -10.00% | 1.000000 |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | 0.102093 / 10.21% / 0.00% / 0.00% | 0.130340 / 13.03% / 3.15% / 3.15% | 0.030738 / 3.07% / 0.00% / -7.95% | 0.068085 / 6.81% / 0.00% / -3.79% | 0.046482 / 4.65% / 0.00% / -6.19% | 0.033496 / 3.35% / 0.00% / -7.64% | 0.034371 / 3.44% / 0.00% / -7.54% | 0.068142 / 6.81% / 0.00% / -3.78% | 0.032355 / 3.24% / 0.00% / -7.77% | 0.073712 / 7.37% / 0.00% / -3.16% | 0.028745 / 2.87% / 0.00% / -8.17% | 0.063352 / 6.34% / 0.00% / -4.31% | 0.024041 / 2.40% / 0.00% / -8.69% | 0.088569 / 8.86% / 0.00% / -1.51% | 0.023241 / 2.32% / 0.00% / -8.78% | 0.022503 / 2.25% / 0.00% / -8.86% | 1.000000 |
| 2023 | MCM | C | `mcm-2023-c-wordle` | 0.224201 / 22.42% / 0.00% / 0.00% | 0.546040 / 54.60% / 41.48% / 41.48% | 0.480160 / 48.02% / 32.99% / 32.99% | 0.217932 / 21.79% / 0.00% / -0.81% | 0.642197 / 64.22% / 53.88% / 53.88% | 0.280001 / 28.00% / 7.19% / 7.19% | 0.097978 / 9.80% / 0.00% / -16.27% | 0.529999 / 53.00% / 39.42% / 39.42% | 0.723478 / 72.35% / 64.36% / 64.36% | 0.259776 / 25.98% / 4.59% / 4.59% | 0.246521 / 24.65% / 2.88% / 2.88% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.580000 / 58.00% / 45.86% / 45.86% | 0.565840 / 56.58% / 44.04% / 44.04% | 0.065441 / 6.54% / 0.00% / -20.46% | 0.983080 / 98.31% / 97.82% / 97.82% | 1.000000 |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | 0.210526 / 21.05% / 0.00% / 0.00% | 0.210526 / 21.05% / 0.00% / 0.00% | 0.210526 / 21.05% / 0.00% / 0.00% | 0.210526 / 21.05% / 0.00% / 0.00% | 0.375000 / 37.50% / 20.83% / 20.83% | 0.444444 / 44.44% / 29.63% / 29.63% | 0.705882 / 70.59% / 62.75% / 62.75% | 0.375000 / 37.50% / 20.83% / 20.83% | 0.210526 / 21.05% / 0.00% / 0.00% | 0.210526 / 21.05% / 0.00% / 0.00% | 0.444444 / 44.44% / 29.63% / 29.63% | 0.444444 / 44.44% / 29.63% / 29.63% | 0.210526 / 21.05% / 0.00% / 0.00% | 0.098361 / 9.84% / 0.00% / -14.21% | 0.324324 / 32.43% / 14.41% / 14.41% | 0.046693 / 4.67% / 0.00% / -20.75% | 1.000000 |
| 2024 | MCM | B | `mcm-2024-b-submersible-search` | 0.371417 / 37.14% / 0.00% / 0.00% | 0.212392 / 21.24% / 0.00% / -25.30% | 0.514568 / 51.46% / 22.77% / 22.77% | 0.294515 / 29.45% / 0.00% / -12.23% | 0.120973 / 12.10% / 0.00% / -39.84% | 0.403101 / 40.31% / 5.04% / 5.04% | 0.296505 / 29.65% / 0.00% / -11.92% | 0.709302 / 70.93% / 53.75% / 53.75% | 0.389026 / 38.90% / 2.80% / 2.80% | 0.662162 / 66.22% / 46.25% / 46.25% | 0.470888 / 47.09% / 15.82% / 15.82% | 0.187946 / 18.79% / 0.00% / -29.19% | 0.753209 / 75.32% / 60.74% / 60.74% | 0.632353 / 63.24% / 41.51% / 41.51% | 0.272873 / 27.29% / 0.00% / -15.68% | 0.300348 / 30.03% / 0.00% / -11.31% | 1.000000 |
| 2024 | MCM | C | `mcm-2024-c-tennis-momentum` | 0.306291 / 30.63% / 0.00% / 0.00% | 0.385581 / 38.56% / 11.43% / 11.43% | 0.347473 / 34.75% / 5.94% / 5.94% | 0.572641 / 57.26% / 38.40% / 38.40% | 0.363804 / 36.38% / 8.29% / 8.29% | 0.856263 / 85.63% / 79.28% / 79.28% | 0.564619 / 56.46% / 37.24% / 37.24% | 0.361433 / 36.14% / 7.95% / 7.95% | 0.403266 / 40.33% / 13.98% / 13.98% | 0.713777 / 71.38% / 58.74% / 58.74% | 0.377542 / 37.75% / 10.27% / 10.27% | 0.000000 / 0.00% / 0.00% / -100.00% | 0.523386 / 52.34% / 31.29% / 31.29% | 0.773319 / 77.33% / 67.32% / 67.32% | 0.464638 / 46.46% / 22.83% / 22.83% | 0.778964 / 77.90% / 68.14% / 68.14% | 1.000000 |
| 2025 | MCM | A | `mcm-2025-a-stair-wear` | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.062802 / 6.28% / 6.28% / 6.28% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.233333 / 23.33% / 23.33% / 23.33% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 0.000000 / 0.00% / 0.00% / 0.00% | 1.000000 |
| 2025 | MCM | B | `mcm-2025-b-juneau-tourism` | 0.259364 / 25.94% / 0.00% / 0.00% | 0.171015 / 17.10% / 0.00% / -11.93% | 0.166667 / 16.67% / 0.00% / -12.52% | 0.113282 / 11.33% / 0.00% / -19.72% | 0.660616 / 66.06% / 54.18% / 54.18% | 0.090096 / 9.01% / 0.00% / -22.85% | 0.426076 / 42.61% / 22.51% / 22.51% | 0.337214 / 33.72% / 10.51% / 10.51% | 0.372904 / 37.29% / 15.33% / 15.33% | 0.251056 / 25.11% / 0.00% / -1.12% | 1.460140 / 100.00% / 162.13% / 100.00% | 0.702044 / 70.20% / 59.77% / 59.77% | 0.025227 / 2.52% / 0.00% / -31.61% | 0.000000 / 0.00% / 0.00% / -35.02% | 0.907133 / 90.71% / 87.46% / 87.46% | 0.567213 / 56.72% / 41.57% / 41.57% | 1.000000 |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 1.575307 / 100.00% / 0.00% / 0.00% | 0.774277 / 77.43% / N/A / -10.00% | 0.465799 / 46.58% / N/A / -10.00% | 0.136955 / 13.70% / N/A / -10.00% | 0.772885 / 77.29% / N/A / -10.00% | 1.339365 / 100.00% / N/A / -10.00% | 0.838169 / 83.82% / N/A / -10.00% | 0.870336 / 87.03% / N/A / -10.00% | 0.457106 / 45.71% / N/A / -10.00% | 2.101688 / 100.00% / N/A / 10.00% | 2.995504 / 100.00% / N/A / 10.00% | 0.000000 / 0.00% / N/A / -100.00% | 0.138589 / 13.86% / N/A / -10.00% | 0.186115 / 18.61% / N/A / -10.00% | 0.920868 / 92.09% / N/A / -10.00% | 0.445610 / 44.56% / N/A / -10.00% | 1.000000 |