# Multimodal board — multi-oracle O-Eval

Generated: 2026-10-20

## What changed

Each task is now anchored to **every O-award paper** for that problem, not just
one reproduced answer. For a task, every paper that reports at least one of the
task's scored fields contributes one oracle panel; the model's O-Eval on that
task is the mean over those papers, and the board averages over 18 tasks.
A missing artifact scores 0 and stays in the denominator (same protocol as the
single-anchor board). Where no paper reports any scored field, the task falls
back to the reproduced anchor and is flagged below.

## Leaderboard

| Rank | Model | Multi-O Eval | Single-O Eval | Δ | Robust BO-Eval (single anchor) |
|---:|---|---:|---:|---:|---:|
| 1 | claude-code + Fable 5.1 | **64.62%** | 76.31% | -11.69pp | 17.62% |
| 2 | codex + GPT-6 Astra | **61.47%** | 72.65% | -11.18pp | 7.66% |
| 3 | opencode + DeepSeek V4.1 Flash | **59.81%** | 75.33% | -15.53pp | 0.00% |
| 4 | codex + GPT-5.5 xhigh | **59.75%** | 71.73% | -11.99pp | 0.22% |
| 5 | opencode + DeepSeek V4.1 Flash (max) | **48.11%** | 64.17% | -16.07pp | -6.20% |

## Aggregation sensitivity

The headline is the task-equal mean over all 18 tasks. The other columns are
diagnostics rather than alternate headline scores: they show whether the ordering
depends on single-reference tasks or on giving tasks rather than papers equal weight.

| Model | All 18 tasks (task-equal) | Tasks with ≥2 refs (n=17) | Tasks with ≥3 refs (n=14) | All panels paper-equal (n=94) |
|---|---:|---:|---:|---:|
| claude-code + Fable 5.1 | 64.62% | 62.54% | 57.20% | 51.15% |
| codex + GPT-6 Astra | 61.47% | 59.20% | 56.91% | 52.50% |
| opencode + DeepSeek V4.1 Flash | 59.81% | 57.44% | 51.53% | 47.46% |
| codex + GPT-5.5 xhigh | 59.75% | 57.38% | 54.67% | 52.82% |
| opencode + DeepSeek V4.1 Flash (max) | 48.11% | 50.94% | 45.25% | 44.89% |

## Oracle coverage per task

| Task | Papers found | Papers usable | Scored fields covered | Fallback |
|---|---:|---:|---:|---|
| `cumcm-2023-a-heliostat-field` | 4 | 4 | 4 field-reports | — |
| `cumcm-2023-b-multibeam-lines` | 3 | 3 | 3 field-reports | — |
| `cumcm-2023-c-vegetable-pricing` | 3 | 3 | 3 field-reports | — |
| `cumcm-2024-a-dragon-dance` | 5 | 5 | 5 field-reports | — |
| `cumcm-2024-b-production-decision` | 3 | 3 | 3 field-reports | — |
| `cumcm-2024-c-crop-planting` | 4 | 4 | 4 field-reports | — |
| `cumcm-2025-a-smoke-screen` | 1 | 1 | 1 field-reports | — |
| `cumcm-2025-b-sic-thickness` | 2 | 2 | 2 field-reports | — |
| `cumcm-2025-c-nipt` | 2 | 2 | 2 field-reports | — |
| `mcm-2023-a-plant-community` | 7 | 7 | 7 field-reports | — |
| `mcm-2023-b-maasai-mara` | 3 | 3 | 3 field-reports | — |
| `mcm-2023-c-wordle` | 12 | 12 | 12 field-reports | — |
| `mcm-2024-a-lamprey` | 5 | 4 | 4 field-reports | — |
| `mcm-2024-b-submersible-search` | 4 | 2 | 2 field-reports | — |
| `mcm-2024-c-tennis-momentum` | 11 | 11 | 11 field-reports | — |
| `mcm-2025-a-stair-wear` | 5 | 3 | 3 field-reports | — |
| `mcm-2025-b-juneau-tourism` | 7 | 7 | 7 field-reports | — |
| `mcm-2025-c-olympic-medals` | 18 | 18 | 18 field-reports | — |

## Human papers not in any panel

Every one of the 99 papers is either used or listed here with a structured
reason. These five cannot answer the task's single core scalar without
inventing a conversion.

| Task | Paper | Reason |
|---|---|---|
| `mcm-2024-a-lamprey` | 2424371 | number_only_in_figure: the paper reports the 3-R index only as Figure 17 and gives no fixed-vs-adaptive numeric pair or percentage. |
| `mcm-2024-b-submersible-search` | 2411570 | figure_only_logistic_prior: plots P=1/(1+exp(at-bS'/S)), whose value at t=0 is 0.5; it is not a cumulative discovery probability from zero and cannot be mapped to the scored curve. |
| `mcm-2024-b-submersible-search` | 2425792 | figure_only: gives P(found/t)=1/(alpha t) and a probability heatmap, with no numeric cumulative probability at the scored time point. |
| `mcm-2025-a-stair-wear` | 2504218 | no_numeric_estimate: reports only relative uncertainties (peak traffic 30-40%, usage +/-5-10%) and no calibrated daily-user count. |
| `mcm-2025-a-stair-wear` | 2511565 | different_unit_of_analysis: reports daily traffic for 11 distinct staircases, not a single estimate for the benchmark staircase. |

## Caveats a reader must know

1. **Coverage is uneven.** The 99 O-award papers were extracted from OCR of
   the PDFs; 94 papers form usable panels with 94 numeric field-reports.
   Every task has at least one human panel. Fourteen tasks are fully covered; smoke
   screen has one paper available, submersible 2 of 4, lamprey 4 of 5, stair-wear 3 of 5.
2. **A paper may not report the reproduction's numbers.** MCM answers are often
   prose, figures, or defined on a different grid or scale. Where the current
   anchor came from the reproduction rather than the paper text (for example,
   Olympic's 75th-percentile jump), the paper contributes only fields it states.
3. **Papers that report few fields act as partial checks.** One human answer gets
   one vote. Missing model fields score zero inside that vote; they never remove
   the paper from the denominator.
4. **Robust BO-Eval is still single-anchor.** It is shown only for continuity and
   must not be interpreted as a multi-reference robustness score.

## Per-task detail (multimodal entries)

| Task | claude-code + Fable 5.1 | codex + GPT-6 Astra | opencode + DeepSeek V4.1 Flash | codex + GPT-5.5 xhigh | opencode + DeepSeek V4.1 Flash (max) |
|---|---:|---:|---:|---:|---:|
| `cumcm-2023-a-heliostat-field` | 72.3 | 85.3 | 80.2 | 80.5 | 81.6 |
| `cumcm-2023-b-multibeam-lines` | 78.7 | 100.0 | 59.3 | 91.7 | 65.8 |
| `cumcm-2023-c-vegetable-pricing` | 64.3 | 64.3 | 64.3 | 64.3 | 64.3 |
| `cumcm-2024-a-dragon-dance` | 83.4 | 83.4 | 83.4 | 83.4 | 83.4 |
| `cumcm-2024-b-production-decision` | 100.0 | 100.0 | 87.2 | 87.2 | 87.2 |
| `cumcm-2024-c-crop-planting` | 89.1 | 88.9 | 63.8 | 99.7 | 0.0 |
| `cumcm-2025-a-smoke-screen` | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| `cumcm-2025-b-sic-thickness` | 87.2 | 85.7 | 78.7 | 80.3 | 88.2 |
| `cumcm-2025-c-nipt` | 75.2 | 23.9 | 76.4 | 29.7 | 44.2 |
| `mcm-2023-a-plant-community` | 12.3 | 2.3 | 27.7 | 27.7 | 30.8 |
| `mcm-2023-b-maasai-mara` | 45.4 | 17.2 | 43.1 | 43.1 | 43.1 |
| `mcm-2023-c-wordle` | 49.5 | 35.3 | 56.4 | 40.9 | 30.4 |
| `mcm-2024-a-lamprey` | 100.0 | 84.2 | 60.9 | 10.7 | 14.4 |
| `mcm-2024-b-submersible-search` | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| `mcm-2024-c-tennis-momentum` | 9.1 | 9.1 | 9.1 | 9.1 | 9.1 |
| `mcm-2025-a-stair-wear` | 12.8 | 15.4 | 12.8 | 12.9 | 17.2 |
| `mcm-2025-b-juneau-tourism` | 42.9 | 42.9 | 42.9 | 42.9 | 42.9 |
| `mcm-2025-c-olympic-medals` | 40.9 | 68.6 | 30.1 | 71.2 | 63.4 |

## Overall Mean

| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| claude-code + Fable 5.1 | 18 | 1.573861 | 64.62% | +0.00 pp | 17.62% | 51,903,796 / 0 / 3,795,512 | 51,903,796 / 3,795,512 | $272.800916 | N/A |
| codex + GPT-6 Astra | 18 | 1.544800 | 61.47% | +0.00 pp | 7.66% | 84,337,603 / 0 / 2,132,173 | 84,337,603 / 2,132,173 | $246.410839 | N/A |
| opencode + DeepSeek V4.1 Flash | 18 | 1.384117 | 59.81% | +0.00 pp | 0.00% | 89,376,395 / 88,668,288 / 569,862 | 708,107 / 569,862 | $2.535912 | ¥17.08 |
| codex + GPT-5.5 xhigh | 18 | 1.121491 | 59.75% | +0.00 pp | 0.22% | 108,584,170 / 105,199,744 / 994,910 | 3,384,426 / 994,910 | $99.369234 | ¥669.45 |
| opencode + DeepSeek V4.1 Flash (max) | 17 | 0.891236 | 48.11% | +0.00 pp | -6.20% | 105,481,424 / 104,781,440 / 610,561 | 699,984 / 610,561 | $2.783484 | ¥18.75 |
