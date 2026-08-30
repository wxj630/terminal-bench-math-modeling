# Qwen3.8-27B-FP8 Thinking Feasibility Audit: 2023-2025

Generated: 2026-08-30

Scope: Qwen3.8-27B-FP8 thinking artifacts for all 18 terminal-bench-math-modeling tasks. This audit checks saved JSON artifacts against the current task score_config hard validity gates and review-warning heuristics. It does not independently rerun every mathematical model from raw data.

## Verdict

- Artifacts: 18/18 present and parseable.
- Scored fields: 60/60 present and numeric.
- Hard-invalid tasks: 1 task, with 2 invalid metrics.
- Needs-review tasks: 1 task, with 2 scale-warning metrics.
- Score-config-clean tasks: 16 tasks.
- Bottom line: Qwen's Robust BO-Eval is 11.09% after denominator and outlier clipping. It is not safe to call all 18 answers feasible: MCM 2024 A is hard-invalid under the current scorer, and MCM 2023 B has a strong grid-scale mismatch warning.

## Strict Rejudge

If hard-invalid tasks are treated as whole-task zero instead of letting still-valid fields contribute, the overall mean barely moves because the worst task was already clipped to 0. Robust BO-Eval still moves because invalid tasks remain negative or capped instead of disappearing.

| Policy | Raw mean | B-Eval vs flash mean | Robust BO-Eval main metric | Changed tasks |
|---|---:|---:|---:|---|
| Original scorer | 0.754457 | +3.46 pp | 11.09% | none |
| Hard-invalid tasks as whole-task zero | 0.750559 | +3.07 pp | 10.58% | `mcm-2024-a-lamprey` |
| Hard-invalid + needs-review tasks as whole-task zero | 0.749223 | +2.94 pp | 10.44% | `mcm-2023-b-maasai-mara`, `mcm-2024-a-lamprey` |

Interpretation: the old ratio-style comparator can hide bad tasks because it clips negative recovery to 0 or drops denominator-failed tasks. The final leaderboard now uses Robust BO-Eval, so invalid/review tasks reduce Qwen's average while tiny-denominator wins are capped.

## Why High-Score Tasks Look High

- CUMCM 2023 A heliostat: no hard warnings. The artifact claims a 60.08 MW Q3 design with fewer mirrors and smaller area than the O reference, so direction-aware scoring rewards it above O on efficiency/area/count while keeping thermal power close to the 60 MW target.
- CUMCM 2025 A smoke screen: no score-config warning. A basic operational schedule check for Q5 passed. The big BO-Eval comes from reported M2/M3/total shielding durations far above the O reference.
- These checks still rely on the artifact's reported final numbers. A stronger audit would rerun each artifact's generation code or reconstruct each physics/optimization model from raw files.

## Smoke-Screen Basic Schedule Check

- Q5 basic schedule check passed: 15 bombs, <=3 per UAV, speed/heading fixed per UAV, >=1s drop gaps, positive burst height.

## Per-Task Status

| Year | Suite | Problem | Task | Qwen raw | Robust BO-Eval | Status | Notes |
|---:|---|---|---|---:|---:|---|---|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 1.24453 | 10.00% | score-config-clean | Q3: power 60.08 MW, unit-area 0.5134 kW/m2, mirrors 2,786, area 117,012 m2 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.50182 | 10.00% | score-config-clean |  |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 1.29287 | -10.00% | score-config-clean |  |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 0.203541 | 20.35% | score-config-clean |  |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 1.44569 | 6.69% | score-config-clean |  |
| 2024 | CUMCM | C | `cumcm-2024-c-crop-planting` | 0.172944 | -57.68% | score-config-clean |  |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 2.59182 | 100.00% | score-config-clean | Q5 durations: M1 7.703s, M2 12.0755s, M3 11.874s, total 31.6525s |
| 2025 | CUMCM | B | `cumcm-2025-b-sic-thickness` | 0.187085 | 5.12% | score-config-clean |  |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.52152 | 0.12% | score-config-clean |  |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.07044 | -10.00% | score-config-clean |  |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | 0.0240411 | -0.65% | needs-review | target_comparison.scenario2_agriculture_cells.actual=872, O=12, ratio=72.66667 (review_extreme_actual_oracle_ratio); target_comparison.scenario2_tourism_cells.actual=1,080, O=9, ratio=120 (review_extreme_actual_oracle_ratio); scenario2 cells: agri 872, hunting 100, tourism 1,080, wildlife 448 |
| 2023 | MCM | C | `mcm-2023-c-wordle` | 0.58 | 58.00% | score-config-clean |  |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | 0.0701754 | -21.59% | hard-invalid | experiment_result.parasite_coexistence_case.final_parasite_index=0.523833 (invalid_normalized_value_for_raw_population_index); experiment_result.parasite_coexistence_case.host_fish_index=0.843327 (invalid_normalized_value_for_raw_population_index); parasite_index 0.523833, host_fish_index 0.843327, resource 1 |
| 2024 | MCM | B | `mcm-2024-b-submersible-search` | 0.753209 | 70.05% | score-config-clean |  |
| 2024 | MCM | C | `mcm-2024-c-tennis-momentum` | 0.523386 | 3.29% | score-config-clean |  |
| 2025 | MCM | A | `mcm-2025-a-stair-wear` | 0.233333 | 23.33% | score-config-clean |  |
| 2025 | MCM | B | `mcm-2025-b-juneau-tourism` | 0.0252273 | 2.52% | score-config-clean |  |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 0.138589 | -10.00% | score-config-clean |  |

## Hard Invalid Metrics

| Year | Suite | Problem | Task | Metric | Actual | O value | Reason |
|---:|---|---|---|---|---:|---:|---|
| 2024 | MCM | A | `mcm-2024-a-lamprey` | `experiment_result.parasite_coexistence_case.final_parasite_index` | 0.523833 | 8.562 | invalid_normalized_value_for_raw_population_index |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | `experiment_result.parasite_coexistence_case.host_fish_index` | 0.843327 | 1,080.356 | invalid_normalized_value_for_raw_population_index |

## Review-Warning Metrics

| Year | Suite | Problem | Task | Metric | Actual | O value | Actual/O | Warning |
|---:|---|---|---|---|---:|---:|---:|---|
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | `target_comparison.scenario2_agriculture_cells.actual` | 872 | 12 | 72.66667 | review_extreme_actual_oracle_ratio |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | `target_comparison.scenario2_tourism_cells.actual` | 1,080 | 9 | 120 | review_extreme_actual_oracle_ratio |

## Score-Config Exclusions

| Year | Suite | Problem | Task | Metric | Reason |
|---:|---|---|---|---|---|
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | `great_coach_model.recommendations[3].estimated_medal_count_gain` | excluded_prompt_asks_three_countries_not_four_recommendation_rows |