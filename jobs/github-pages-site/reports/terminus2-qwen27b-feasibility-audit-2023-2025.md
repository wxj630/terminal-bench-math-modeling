# Qwen3.8-27B-FP8 Thinking Feasibility Audit: 2023-2025

Generated: 2026-09-04

Scope: Qwen3.8-27B-FP8 thinking artifacts for all 18 terminal-bench-math-modeling tasks. This audit checks saved JSON artifacts against the current task score_config hard validity gates and review-warning heuristics. It does not independently rerun every mathematical model from raw data.

## Verdict

- Artifacts: 18/18 present and parseable.
- Scored fields: 60/60 present and numeric.
- Hard-invalid tasks: 0 task, with 0 invalid metrics.
- Needs-review tasks: 2 tasks, with 4 review-warning metrics.
- Score-config-clean tasks: 16 tasks.
- Bottom line: Qwen's original O-Eval is 55.06% and original Robust BO-Eval is 9.94%. Under the tempered hard-gated public view, Qwen becomes 55.06% hard-gated O-Eval and 9.94% hard-gated Robust BO-Eval.
- It is not safe to call all 18 answers independently verified feasible: MCM 2024 A has a score-config scale mismatch that is retained as a review warning, and MCM 2023 B has a strong grid-scale mismatch warning.

## Strict Rejudge

The strict rows below are sensitivity analyses: a hard-invalid task would be zeroed as a whole, while a needs-review task is zeroed only in the deliberately conservative stress test. In the current Qwen run there are no hard-invalid tasks; the conservative drop comes from the two review-warning tasks.

| Policy | Raw mean | B-Eval vs flash mean | Robust BO-Eval main metric | Changed tasks |
|---|---:|---:|---:|---|
| Original scorer | 0.754457 | -0.21 pp | 9.94% | none |
| Tempered hard-gated leaderboard | 0.754457 | N/A | 9.94% |  |
| Hard-invalid tasks as whole-task zero | 0.754457 | -0.21 pp | 9.94% |  |
| Hard-invalid + needs-review tasks as whole-task zero | 0.749223 | -0.73 pp | 9.37% | `mcm-2023-b-maasai-mara`, `mcm-2024-a-lamprey` |

Interpretation: the old ratio-style comparator can hide bad tasks because it clips negative recovery to 0 or drops denominator-failed tasks. The public report now keeps O-Eval as the main score and adds a tempered hard-gated view, so clearly invalid tasks reduce Qwen's average while tiny-denominator wins are capped.

## Why High-Score Tasks Look High

- CUMCM 2023 A heliostat: the reported Q3 design is 60.08 MW, 2,786 mirrors and 117,012 m2 of mirror area, with installation height 4 m and mirror height 6 m. Those values pass the available boundary checks and explain the high score, but the collected artifact has no per-mirror coordinate/layout file, so the optical result is not independently replayable.
- CUMCM 2023 B multibeam: the saved Q4 coordinates replay to 100% grid coverage. However, only about 14.8% of local overlaps fall in the suggested 10%-20% band, about 36.2% are below 10% and 51.0% are above 20%; the last Q3 center is about 4.17 m beyond the 4 NM boundary. This is executable coverage, not a clean proof that every quality constraint is satisfied.
- CUMCM 2024 B production decision: binary decisions, positive sample counts and probability ranges pass the structural checks; the artifact still needs a full independent rerun to establish optimality and statistical calibration.
- CUMCM 2025 A smoke screen: independent replay gives 32.62 s versus the reported 31.65 s, and the 15-bomb schedule passes the per-UAV, timing, speed, heading and burst-height checks under the common O-reference geometry. This high score has physical replay support.
- CUMCM 2025 C NIPT: five BMI groups cover 20-28, 28-32, 32-36, 36-40 and 40+, with recommended weeks 10, 11, 12, 14 and 16 and qualified probabilities around 0.91-0.93. Basic timing and probability checks pass, but this does not replace validation on held-out data.
- These checks separate score-config validity from independent feasibility: a clean JSON/artifact can explain a high score, but only a replayable code/data package can support a strong claim that the mathematical solution is executable.

## Smoke-Screen Basic Schedule Check

- Q5 basic schedule check passed: 15 bombs, <=3 per UAV, speed/heading fixed per UAV, >=1s drop gaps, positive burst height.

## Per-Task Status

| Year | Suite | Problem | Task | Qwen raw | Robust BO-Eval | Status | Notes |
|---:|---|---|---|---:|---:|---|---|
| 2023 | CUMCM | A | `cumcm-2023-a-heliostat-field` | 1.24453 | 100.00% | score-config-clean | Q3: power 60.08 MW, unit-area 0.5134 kW/m2, mirrors 2,786, area 117,012 m2 |
| 2023 | CUMCM | B | `cumcm-2023-b-multibeam-lines` | 1.50182 | 0.94% | score-config-clean |  |
| 2023 | CUMCM | C | `cumcm-2023-c-vegetable-pricing` | 1.29287 | -10.00% | score-config-clean |  |
| 2024 | CUMCM | A | `cumcm-2024-a-dragon-dance` | 0.203541 | -100.00% | score-config-clean |  |
| 2024 | CUMCM | B | `cumcm-2024-b-production-decision` | 1.44569 | 100.00% | score-config-clean |  |
| 2024 | CUMCM | C | `cumcm-2024-c-crop-planting` | 0.172944 | -9.79% | score-config-clean |  |
| 2025 | CUMCM | A | `cumcm-2025-a-smoke-screen` | 2.59182 | 10.00% | score-config-clean | Q5 durations: M1 7.703s, M2 12.0755s, M3 11.874s, total 31.6525s |
| 2025 | CUMCM | B | `cumcm-2025-b-sic-thickness` | 0.187085 | -14.76% | score-config-clean |  |
| 2025 | CUMCM | C | `cumcm-2025-c-nipt` | 1.52152 | 1.52% | score-config-clean |  |
| 2023 | MCM | A | `mcm-2023-a-plant-community` | 1.07044 | -10.00% | score-config-clean |  |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | 0.0240411 | -8.69% | needs-review | target_comparison.scenario2_agriculture_cells.actual=872, O=12, ratio=72.66667 (review_extreme_actual_oracle_ratio); target_comparison.scenario2_tourism_cells.actual=1,080, O=9, ratio=120 (review_extreme_actual_oracle_ratio); scenario2 cells: agri 872, hunting 100, tourism 1,080, wildlife 448 |
| 2023 | MCM | C | `mcm-2023-c-wordle` | 0.58 | 45.86% | score-config-clean |  |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | 0.0701754 | 0.00% | needs-review | experiment_result.parasite_coexistence_case.final_parasite_index=0.523833 (score-config scale mismatch; not a biological boundary check); experiment_result.parasite_coexistence_case.host_fish_index=0.843327 (score-config scale mismatch; not a biological boundary check); parasite_index 0.523833, host_fish_index 0.843327, resource 1 |
| 2024 | MCM | B | `mcm-2024-b-submersible-search` | 0.753209 | 60.74% | score-config-clean |  |
| 2024 | MCM | C | `mcm-2024-c-tennis-momentum` | 0.523386 | 31.29% | score-config-clean |  |
| 2025 | MCM | A | `mcm-2025-a-stair-wear` | 0.233333 | 23.33% | score-config-clean |  |
| 2025 | MCM | B | `mcm-2025-b-juneau-tourism` | 0.0252273 | -31.61% | score-config-clean |  |
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | 0.138589 | -10.00% | score-config-clean |  |

## Hard Invalid Metrics

None.

## Review-Warning Metrics

| Year | Suite | Problem | Task | Metric | Actual | O value | Actual/O | Warning |
|---:|---|---|---|---|---:|---:|---:|---|
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | `target_comparison.scenario2_agriculture_cells.actual` | 872 | 12 | 72.66667 | review_extreme_actual_oracle_ratio |
| 2023 | MCM | B | `mcm-2023-b-maasai-mara` | `target_comparison.scenario2_tourism_cells.actual` | 1,080 | 9 | 120 | review_extreme_actual_oracle_ratio |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | `experiment_result.parasite_coexistence_case.final_parasite_index` | 0.523833 | 8.562 | N/A | score-config scale mismatch; not a biological boundary check |
| 2024 | MCM | A | `mcm-2024-a-lamprey` | `experiment_result.parasite_coexistence_case.host_fish_index` | 0.843327 | 1,080.356 | N/A | score-config scale mismatch; not a biological boundary check |

## Score-Config Exclusions

| Year | Suite | Problem | Task | Metric | Reason |
|---:|---|---|---|---|---|
| 2025 | MCM | C | `mcm-2025-c-olympic-medals` | `great_coach_model.recommendations[3].estimated_medal_count_gain` | excluded_prompt_asks_three_countries_not_four_recommendation_rows |