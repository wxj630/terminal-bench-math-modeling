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
| 1 | claude-code + Fable 5.1 | **64.67%** | 69.60% | -4.93pp | -3.20% |
| 2 | opencode + DeepSeek V4.1 Flash | **62.87%** | 73.36% | -10.49pp | 0.00% |
| 3 | codex + GPT-6 Astra | **59.66%** | 60.01% | -0.35pp | -19.17% |
| 4 | codex + GPT-5.5 xhigh | **58.57%** | 63.46% | -4.90pp | -5.15% |
| 5 | opencode + DeepSeek V4.1 Flash (max) | **52.36%** | 60.31% | -7.95pp | -15.19% |

## Aggregation sensitivity

The headline is the task-equal mean over all 18 tasks. The other columns are
diagnostics rather than alternate headline scores: they show whether the ordering
depends on single-reference tasks or on giving tasks rather than papers equal weight.

| Model | All 18 tasks (task-equal) | Tasks with ≥2 refs (n=14) | Tasks with ≥3 refs (n=12) | All panels paper-equal (n=67) |
|---|---:|---:|---:|---:|
| claude-code + Fable 5.1 | 64.67% | 61.38% | 60.19% | 58.75% |
| opencode + DeepSeek V4.1 Flash | 62.87% | 58.48% | 56.74% | 56.67% |
| codex + GPT-6 Astra | 59.66% | 54.79% | 53.89% | 51.38% |
| codex + GPT-5.5 xhigh | 58.57% | 53.63% | 53.82% | 52.80% |
| opencode + DeepSeek V4.1 Flash (max) | 52.36% | 52.82% | 51.36% | 49.96% |

## Oracle coverage per task

| Task | Papers found | Papers usable | Scored fields covered | Fallback |
|---|---:|---:|---:|---|
| `cumcm-2023-a-heliostat-field` | 4 | 4 | 20 field-reports | — |
| `cumcm-2023-b-multibeam-lines` | 3 | 3 | 10 field-reports | — |
| `cumcm-2023-c-vegetable-pricing` | 3 | 3 | 5 field-reports | — |
| `cumcm-2024-a-dragon-dance` | 5 | 5 | 7 field-reports | — |
| `cumcm-2024-b-production-decision` | 3 | 1 | 2 field-reports | — |
| `cumcm-2024-c-crop-planting` | 4 | 4 | 8 field-reports | — |
| `cumcm-2025-a-smoke-screen` | 1 | 1 | 1 field-reports | — |
| `cumcm-2025-b-sic-thickness` | 2 | 2 | 4 field-reports | — |
| `cumcm-2025-c-nipt` | 2 | 2 | 4 field-reports | — |
| `mcm-2023-a-plant-community` | 7 | 6 | 8 field-reports | — |
| `mcm-2023-b-maasai-mara` | 3 | 1 | 5 field-reports | — |
| `mcm-2023-c-wordle` | 12 | 7 | 7 field-reports | — |
| `mcm-2024-a-lamprey` | 5 | 4 | 4 field-reports | — |
| `mcm-2024-b-submersible-search` | 4 | 1 | 2 field-reports | — |
| `mcm-2024-c-tennis-momentum` | 11 | 6 | 9 field-reports | — |
| `mcm-2025-a-stair-wear` | 5 | 3 | 3 field-reports | — |
| `mcm-2025-b-juneau-tourism` | 7 | 7 | 11 field-reports | — |
| `mcm-2025-c-olympic-medals` | 18 | 7 | 21 field-reports | — |

## Caveats a reader must know

1. **Coverage is uneven.** The 99 O-award papers were extracted from OCR of
   the PDFs; 67 papers form usable panels with 131 numeric field-reports. Every
   task now has at least one human panel, but four tasks still rest on one paper:
   production decision, smoke screen, Maasai Mara, and submersible search.
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

| Task | claude-code + Fable 5.1 | opencode + DeepSeek V4.1 Flash | codex + GPT-6 Astra | codex + GPT-5.5 xhigh | opencode + DeepSeek V4.1 Flash (max) |
|---|---:|---:|---:|---:|---:|
| `cumcm-2023-a-heliostat-field` | 68.2 | 73.8 | 85.1 | 73.8 | 76.3 |
| `cumcm-2023-b-multibeam-lines` | 100.0 | 73.5 | 100.0 | 100.0 | 72.7 |
| `cumcm-2023-c-vegetable-pricing` | 69.1 | 70.4 | 48.2 | 69.8 | 75.0 |
| `cumcm-2024-a-dragon-dance` | 83.4 | 83.4 | 83.4 | 83.4 | 83.4 |
| `cumcm-2024-b-production-decision` | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| `cumcm-2024-c-crop-planting` | 89.2 | 100.0 | 89.3 | 96.6 | 88.0 |
| `cumcm-2025-a-smoke-screen` | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| `cumcm-2025-b-sic-thickness` | 79.3 | 77.1 | 81.2 | 76.5 | 79.8 |
| `cumcm-2025-c-nipt` | 57.8 | 60.7 | 39.2 | 28.5 | 43.4 |
| `mcm-2023-a-plant-community` | 17.9 | 46.6 | 19.0 | 41.9 | 37.7 |
| `mcm-2023-b-maasai-mara` | 4.6 | 13.0 | 6.8 | 3.3 | 3.1 |
| `mcm-2023-c-wordle` | 48.9 | 43.7 | 32.3 | 33.9 | 40.8 |
| `mcm-2024-a-lamprey` | 100.0 | 60.9 | 84.2 | 10.7 | 14.4 |
| `mcm-2024-b-submersible-search` | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| `mcm-2024-c-tennis-momentum` | 13.5 | 13.9 | 16.1 | 14.0 | 15.9 |
| `mcm-2025-a-stair-wear` | 12.8 | 12.8 | 15.4 | 12.9 | 17.2 |
| `mcm-2025-b-juneau-tourism` | 77.4 | 60.0 | 60.8 | 53.1 | 53.0 |
| `mcm-2025-c-olympic-medals` | 41.8 | 41.9 | 13.0 | 55.7 | 41.9 |

## Overall Mean

| Model | Artifacts | Mean direction-aware raw | Mean O-Eval on all 18 (%) | Mean B-Eval vs flash (pp) | Mean Robust BO-Eval on all 18 (%) | Tokens input/cache/output | Billable input/output | Est. cost USD | Est. cost RMB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| claude-code + Fable 5.1 | 18 | 1.349180 | 64.67% | +0.00 pp | -3.20% | 51,903,796 / 0 / 3,795,512 | 51,903,796 / 3,795,512 | $272.800916 | N/A |
| opencode + DeepSeek V4.1 Flash | 18 | 1.295249 | 62.87% | +0.00 pp | 0.00% | 89,376,395 / 88,668,288 / 569,862 | 708,107 / 569,862 | $2.535912 | ¥17.08 |
| codex + GPT-6 Astra | 18 | 1.222997 | 59.66% | +0.00 pp | -19.17% | 84,337,603 / 0 / 2,132,173 | 84,337,603 / 2,132,173 | $246.410839 | N/A |
| codex + GPT-5.5 xhigh | 18 | 0.940640 | 58.57% | +0.00 pp | -5.15% | 108,584,170 / 105,199,744 / 994,910 | 3,384,426 / 994,910 | $99.369234 | ¥669.45 |
| opencode + DeepSeek V4.1 Flash (max) | 17 | 0.838241 | 52.36% | +0.00 pp | -15.19% | 105,481,424 / 104,781,440 / 610,561 | 699,984 / 610,561 | $2.783484 | ¥18.75 |
