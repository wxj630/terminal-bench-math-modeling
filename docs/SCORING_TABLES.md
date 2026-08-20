# Scoring Tables

Each original contest problem has one scoring table. `B-Eval` is the default verifier reward and reports gain over the baseline panel score; `BO-Eval` is available as a verifier hyperparameter for baseline-to-outstanding normalization. For endpoint tasks, the table shows the real baseline value, the real outstanding-paper value, and whether moving toward the outstanding endpoint is higher-is-better or lower-is-better. Legacy tasks list the oracle metric panel and keep per-metric baseline values blank because those tasks still use a legacy baseline-panel endpoint. The generated `test.sh` accepts the eval method as its first argument, and `score_result.py` also exposes `score_result(eval_method=...)`, so tests can select the scoring method directly instead of relying only on shell-level configuration.

## Contents

- [CUMCM 2023 A: heliostat field design](#cumcm-2023-a-heliostat-field)
- [CUMCM 2023 B: multibeam survey-line layout](#cumcm-2023-b-multibeam-lines)
- [CUMCM 2023 C: vegetable pricing and replenishment](#cumcm-2023-c-vegetable-pricing)
- [CUMCM 2024 A: dragon-dance bench kinematics](#cumcm-2024-a-dragon-dance)
- [CUMCM 2024 B: production-process decision optimization](#cumcm-2024-b-production-decision)
- [CUMCM 2024 C: crop-planting strategy optimization](#cumcm-2024-c-crop-planting)
- [CUMCM 2025 A: UAV smoke-screen strategy](#cumcm-2025-a-smoke-screen)
- [CUMCM 2025 B: SiC epitaxial-layer thickness inversion](#cumcm-2025-b-sic-thickness)
- [CUMCM 2025 C: NIPT timing and fetal abnormality modeling](#cumcm-2025-c-nipt)
- [MCM 2023 A: drought-stricken plant communities](#mcm-2023-a-plant-community)
- [MCM 2023 B: reimagining Maasai Mara](#mcm-2023-b-maasai-mara)
- [MCM 2023 C: predicting Wordle results](#mcm-2023-c-wordle)
- [MCM 2024 A: lamprey sex-ratio ecology](#mcm-2024-a-lamprey)
- [MCM 2024 B: submersible localization and search planning](#mcm-2024-b-submersible-search)
- [MCM 2024 C: momentum in tennis](#mcm-2024-c-tennis-momentum)
- [MCM 2025 A: stair wear and historical traffic inference](#mcm-2025-a-stair-wear)
- [MCM 2025 B: sustainable tourism management in Juneau](#mcm-2025-b-juneau-tourism)
- [MCM 2025 C: Olympic medal prediction](#mcm-2025-c-olympic-medals)

<a id="cumcm-2023-a-heliostat-field"></a>

# CUMCM 2023 A: heliostat field design

- Task slug: `cumcm-2023-a-heliostat-field`
- Required output: `/root/results/cumcm-2023-a-heliostat-field_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 29
- Effective scored metric count: 29
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `reproduced.design_summary[0].annual_optical_efficiency` |  | 0.536230167 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `reproduced.design_summary[0].annual_thermal_power_mw` |  | 32.76117051 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `reproduced.design_summary[0].mirror_count` |  | 1745 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `reproduced.design_summary[0].tower_xy[0]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `reproduced.design_summary[0].tower_xy[1]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `reproduced.design_summary[0].unit_area_power_kw_m2` |  | 0.521508604 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `reproduced.design_summary[1].annual_optical_efficiency` |  | 0.591643667 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `reproduced.design_summary[1].annual_thermal_power_mw` |  | 68.24427914 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `reproduced.design_summary[1].installation_height_m` |  | 4 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `reproduced.design_summary[1].mirror_area_m2` |  | 119196 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `reproduced.design_summary[1].mirror_count` |  | 3311 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `reproduced.design_summary[1].mirror_height_m` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `reproduced.design_summary[1].mirror_width_m` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `reproduced.design_summary[1].tower_xy[0]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `reproduced.design_summary[1].tower_xy[1]` |  | -250 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `reproduced.design_summary[1].unit_area_power_kw_m2` |  | 0.572538333 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `reproduced.design_summary[2].annual_optical_efficiency` |  | 0.496428083 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `reproduced.design_summary[2].annual_thermal_power_mw` |  | 60.336111 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `reproduced.design_summary[2].mirror_area_m2` |  | 119196 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `reproduced.design_summary[2].mirror_count` |  | 3311 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `reproduced.design_summary[2].tower_xy[0]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `reproduced.design_summary[2].tower_xy[1]` |  | -250 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `reproduced.design_summary[2].unit_area_power_kw_m2` |  | 0.506192417 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `reproduced.official_coordinate_count` |  | 1745 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `reproduced.q1_monthly_efficiency_mean` |  | 0.536230167 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `target_comparison.q1_annual_optical_efficiency.actual` |  | 0.536230167 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `target_comparison.q2_annual_thermal_power_mw.actual` |  | 68.244279 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `target_comparison.q2_mirror_count.actual` |  | 3311 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `target_comparison.q3_annual_thermal_power_mw.actual` |  | 60.336111 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2023-b-multibeam-lines"></a>

# CUMCM 2023 B: multibeam survey-line layout

- Task slug: `cumcm-2023-b-multibeam-lines`
- Required output: `/root/results/cumcm-2023-b-multibeam-lines_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 21
- Effective scored metric count: 21
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `reproduced.problem3_last_position_m` |  | 7226.14 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `reproduced.problem3_line_count` |  | 34 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `reproduced.problem3_total_length_m` |  | 125936 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `reproduced.problem4_summary.avg_position_error_m` |  | 9.27 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `reproduced.problem4_summary.greedy_avg_overlap_pct` |  | 10.35 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `reproduced.problem4_summary.missed_area_pct` |  | 3.48 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles` |  | 30 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `reproduced.problem4_summary.sa_avg_overlap_pct` |  | 10.48 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `reproduced.problem4_summary.total_length_nautical_miles` |  | 622 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `reproduced.seabed_grid_summary.max_depth_m` |  | 197.2 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `reproduced.seabed_grid_summary.mean_depth_m` |  | 62.539 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `reproduced.seabed_grid_summary.min_depth_m` |  | 20 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `reproduced.seabed_grid_summary.x_count` |  | 201 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `reproduced.seabed_grid_summary.x_range_nm` |  | 4 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `reproduced.seabed_grid_summary.y_count` |  | 251 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `reproduced.seabed_grid_summary.y_range_nm` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `target_comparison.problem3_last_position_m.actual` |  | 7226.14 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `target_comparison.problem3_line_count.actual` |  | 34 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `target_comparison.problem3_total_length_m.actual` |  | 125936 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `target_comparison.problem4_missed_area_pct.actual` |  | 3.48 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `target_comparison.problem4_total_length_nm.actual` |  | 622 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2023-c-vegetable-pricing"></a>

# CUMCM 2023 C: vegetable pricing and replenishment

- Task slug: `cumcm-2023-c-vegetable-pricing`
- Required output: `/root/results/cumcm-2023-c-vegetable-pricing_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 38
- Effective scored metric count: 38
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `reproduced.category_count` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `reproduced.cluster_center_comparison[0].avg_daily_sales_kg_actual` |  | 2.52916556634 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `reproduced.cluster_center_comparison[0].max_daily_sales_kg_actual` |  | 8.89412 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `reproduced.cluster_center_comparison[0].total_sales_kg_actual` |  | 258.426462857 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `reproduced.cluster_center_comparison[1].avg_daily_sales_kg_actual` |  | 9.10524135797 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `reproduced.cluster_center_comparison[1].max_daily_sales_kg_actual` |  | 56.0392826087 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `reproduced.cluster_center_comparison[1].total_sales_kg_actual` |  | 3149.22293478 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `reproduced.cluster_center_comparison[2].avg_daily_sales_kg_actual` |  | 20.808494683 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `reproduced.cluster_center_comparison[2].max_daily_sales_kg_actual` |  | 144.071684211 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `reproduced.cluster_center_comparison[2].total_sales_kg_actual` |  | 7849.98494737 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `reproduced.cluster_center_comparison[3].avg_daily_sales_kg_actual` |  | 32.7257670152 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `reproduced.cluster_center_comparison[3].max_daily_sales_kg_actual` |  | 205.939666667 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `reproduced.cluster_center_comparison[3].total_sales_kg_actual` |  | 22006.2065 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `reproduced.correlation_comparison[0].actual_sales_markup_corr` |  | -0.1579 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `reproduced.correlation_comparison[1].actual_sales_markup_corr` |  | -0.0287 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `reproduced.correlation_comparison[2].actual_sales_markup_corr` |  | 0.1977 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `reproduced.correlation_comparison[3].actual_sales_markup_corr` |  | 0.0418 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `reproduced.correlation_comparison[4].actual_sales_markup_corr` |  | 0.0259 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `reproduced.correlation_comparison[5].actual_sales_markup_corr` |  | -0.2332 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `reproduced.future_week_profit_yuan` |  | 5105.6 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `reproduced.item_count` |  | 246 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `reproduced.july1_profit_yuan` |  | 1282.2631 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `reproduced.regression_comparison[0].actual_intercept` |  | 11.2959 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `reproduced.regression_comparison[0].actual_slope` |  | -0.041909 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `reproduced.regression_comparison[1].actual_intercept` |  | 6.3512 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `reproduced.regression_comparison[1].actual_slope` |  | -0.004092 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `reproduced.regression_comparison[2].actual_intercept` |  | 10.6597 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `reproduced.regression_comparison[2].actual_slope` |  | -0.032044 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `reproduced.regression_comparison[3].actual_intercept` |  | 9.5925 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `reproduced.regression_comparison[3].actual_slope` |  | -0.036359 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `reproduced.regression_comparison[4].actual_intercept` |  | 9.6747 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `reproduced.regression_comparison[4].actual_slope` |  | -0.012185 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `reproduced.regression_comparison[5].actual_intercept` |  | 9.4799 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `reproduced.regression_comparison[5].actual_slope` |  | -0.012872 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `reproduced.selected_item_count` |  | 29 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `target_comparison.future_week_max_profit_yuan.actual` |  | 5105.6 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `target_comparison.problem3_july1_profit_yuan.actual` |  | 1282.2631 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `target_comparison.problem3_selected_item_count.actual` |  | 29 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2024-a-dragon-dance"></a>

# CUMCM 2024 A: dragon-dance bench kinematics

- Task slug: `cumcm-2024-a-dragon-dance`
- Required output: `/root/results/cumcm-2024-a-dragon-dance_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 9
- Effective scored metric count: 9
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q1.handles` |  | 224 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q2.terminal_min_margin_m` |  | 0.249958 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.q2.terminal_time_s` |  | 464 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.q3.minimum_pitch_m` |  | 0.4 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.q4.base_ratio_2_to_1_length_m` |  | 14.1372 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.q4.shortest_candidate_length_m` |  | 14.1372 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.q4.shortest_candidate_ratio` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.q5.max_head_speed_mps` |  | 2.00002 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.q5.max_speed_ratio_when_head_1mps` |  | 0.99999 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2024-b-production-decision"></a>

# CUMCM 2024 B: production-process decision optimization

- Task slug: `cumcm-2024-b-production-decision`
- Required output: `/root/results/cumcm-2024-b-production-decision_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 69
- Effective scored metric count: 69
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q1_sampling[0].c` |  | 36 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q1_sampling[0].false_alarm` |  | 0.046596 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.q1_sampling[0].n` |  | 270 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.q1_sampling[0].power` |  | 0.801472 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.q1_sampling[1].accept_bad` |  | 0.195466 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.q1_sampling[1].accept_good` |  | 0.903863 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.q1_sampling[1].c` |  | 25 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.q1_sampling[1].n` |  | 199 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.q2.best_decisions[0].case` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `experiment_result.q2.best_decisions[0].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `experiment_result.q2.best_decisions[0].expected_profit` |  | 26.374 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `experiment_result.q2.best_decisions[0].good_probability` |  | 0.729 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `experiment_result.q2.best_decisions[0].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `experiment_result.q2.best_decisions[0].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `experiment_result.q2.best_decisions[0].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `experiment_result.q2.best_decisions[1].case` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `experiment_result.q2.best_decisions[1].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `experiment_result.q2.best_decisions[1].expected_profit` |  | 25.072 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `experiment_result.q2.best_decisions[1].good_probability` |  | 0.512 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `experiment_result.q2.best_decisions[1].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `experiment_result.q2.best_decisions[1].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `experiment_result.q2.best_decisions[1].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `experiment_result.q2.best_decisions[2].case` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `experiment_result.q2.best_decisions[2].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `experiment_result.q2.best_decisions[2].expected_profit` |  | 19.87 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `experiment_result.q2.best_decisions[2].good_probability` |  | 0.729 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `experiment_result.q2.best_decisions[2].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `experiment_result.q2.best_decisions[2].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `experiment_result.q2.best_decisions[2].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `experiment_result.q2.best_decisions[3].case` |  | 4 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `experiment_result.q2.best_decisions[3].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `experiment_result.q2.best_decisions[3].expected_profit` |  | 14.95 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `experiment_result.q2.best_decisions[3].good_probability` |  | 0.64 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `experiment_result.q2.best_decisions[3].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `experiment_result.q2.best_decisions[3].inspect_part1` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `experiment_result.q2.best_decisions[3].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `experiment_result.q2.best_decisions[4].case` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `experiment_result.q2.best_decisions[4].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 39 | `experiment_result.q2.best_decisions[4].expected_profit` |  | 24.48 | `closeness_to_outstanding` | yes | 1 |  |
| 40 | `experiment_result.q2.best_decisions[4].good_probability` |  | 0.648 | `closeness_to_outstanding` | yes | 1 |  |
| 41 | `experiment_result.q2.best_decisions[4].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 42 | `experiment_result.q2.best_decisions[4].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 43 | `experiment_result.q2.best_decisions[4].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 44 | `experiment_result.q2.best_decisions[5].case` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 45 | `experiment_result.q2.best_decisions[5].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 46 | `experiment_result.q2.best_decisions[5].expected_profit` |  | 26.5738 | `closeness_to_outstanding` | yes | 1 |  |
| 47 | `experiment_result.q2.best_decisions[5].good_probability` |  | 0.85737 | `closeness_to_outstanding` | yes | 1 |  |
| 48 | `experiment_result.q2.best_decisions[5].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 49 | `experiment_result.q2.best_decisions[5].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 50 | `experiment_result.q2.best_decisions[5].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 51 | `experiment_result.q2.best_profit_mean` |  | 22.8866 | `closeness_to_outstanding` | yes | 1 |  |
| 52 | `experiment_result.q3.best_expected_profit` |  | 88 | `closeness_to_outstanding` | yes | 1 |  |
| 53 | `experiment_result.q3.decision_bits[0]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 54 | `experiment_result.q3.decision_bits[10]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 55 | `experiment_result.q3.decision_bits[11]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 56 | `experiment_result.q3.decision_bits[12]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 57 | `experiment_result.q3.decision_bits[13]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 58 | `experiment_result.q3.decision_bits[14]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 59 | `experiment_result.q3.decision_bits[15]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 60 | `experiment_result.q3.decision_bits[1]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 61 | `experiment_result.q3.decision_bits[2]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 62 | `experiment_result.q3.decision_bits[3]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 63 | `experiment_result.q3.decision_bits[4]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 64 | `experiment_result.q3.decision_bits[5]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 65 | `experiment_result.q3.decision_bits[6]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 66 | `experiment_result.q3.decision_bits[7]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 67 | `experiment_result.q3.decision_bits[8]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 68 | `experiment_result.q3.decision_bits[9]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 69 | `experiment_result.q3.generations` |  | 70 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2024-c-crop-planting"></a>

# CUMCM 2024 C: crop-planting strategy optimization

- Task slug: `cumcm-2024-c-crop-planting`
- Required output: `/root/results/cumcm-2024-c-crop-planting_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 20
- Effective scored metric count: 20
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q1.discount_gain_pct` |  | 8.1067954e+18 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q1.discount_profit_yuan` |  | 75678478 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.q1.waste_profit_yuan` |  | -5389476 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.q2_q3.best_correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.q2_q3.risk_summary[0].correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.q2_q3.risk_summary[0].cvar10_profit_yuan` |  | 118937552.19 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.q2_q3.risk_summary[0].deterministic_profit_yuan` |  | -5389476 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.q2_q3.risk_summary[0].mean_profit_yuan` |  | 119827636.74 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.q2_q3.risk_summary[0].q10_profit_yuan` |  | 119159280.66 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `experiment_result.q2_q3.risk_summary[1].correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `experiment_result.q2_q3.risk_summary[1].cvar10_profit_yuan` |  | 118937552.19 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `experiment_result.q2_q3.risk_summary[1].deterministic_profit_yuan` |  | 75678478 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `experiment_result.q2_q3.risk_summary[1].mean_profit_yuan` |  | 119827636.74 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `experiment_result.q2_q3.risk_summary[1].q10_profit_yuan` |  | 119159280.66 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `experiment_result.q2_q3.risk_summary[2].correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `experiment_result.q2_q3.risk_summary[2].cvar10_profit_yuan` |  | 118937552.19 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `experiment_result.q2_q3.risk_summary[2].deterministic_profit_yuan` |  | 75678478 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `experiment_result.q2_q3.risk_summary[2].mean_profit_yuan` |  | 119827636.74 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `experiment_result.q2_q3.risk_summary[2].q10_profit_yuan` |  | 119159280.66 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `experiment_result.q2_q3.spearman_price_cost` |  | 0.2551 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2025-a-smoke-screen"></a>

# CUMCM 2025 A: UAV smoke-screen strategy

- Task slug: `cumcm-2025-a-smoke-screen`
- Required output: `/root/results/cumcm-2025-a-smoke-screen_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 164
- Effective scored metric count: 164
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q1_duration_s` |  | 1.5 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q2_duration_s` |  | 4.5 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.q3_union_duration_s.M1` |  | 6.8 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.q3_union_duration_s.total` |  | 6.8 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.q4_union_duration_s.M1` |  | 8.1 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.q4_union_duration_s.total` |  | 8.1 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.q5_union_duration_s.M1` |  | 10.3 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.q5_union_duration_s.M2` |  | 6.2 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.q5_union_duration_s.M3` |  | 3.4 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `experiment_result.q5_union_duration_s.total` |  | 19.9 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `q1.effective_duration_s` |  | 1.5 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `q1.strategy.drop_time_s` |  | 1.5 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `q1.strategy.drop_x` |  | 17620 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `q1.strategy.drop_y` |  | -0 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `q1.strategy.drop_z` |  | 1800 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `q1.strategy.explode_time_s` |  | 5.1 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `q1.strategy.explode_x` |  | 17188 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `q1.strategy.explode_y` |  | -0 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `q1.strategy.explode_z` |  | 1736.496 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `q1.strategy.fuse_time_s` |  | 3.6 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `q1.strategy.heading_deg` |  | 180 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `q1.strategy.individual_duration_s` |  | 1.5 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `q1.strategy.speed_mps` |  | 120 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `q2.effective_duration_s` |  | 4.5 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `q2.strategy.drop_time_s` |  | 0.5 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `q2.strategy.drop_x` |  | 17740.004 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `q2.strategy.drop_y` |  | 0.674 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `q2.strategy.drop_z` |  | 1800 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `q2.strategy.explode_time_s` |  | 4.1 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `q2.strategy.explode_x` |  | 17308.031 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `q2.strategy.explode_y` |  | 5.528 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `q2.strategy.explode_z` |  | 1736.496 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `q2.strategy.fuse_time_s` |  | 3.6 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `q2.strategy.heading_deg` |  | 179.356 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `q2.strategy.individual_duration_s` |  | 4.5 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `q2.strategy.speed_mps` |  | 120 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `q3.strategies[0].drop_time_s` |  | 0.5 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `q3.strategies[0].drop_x` |  | 17740.004 | `closeness_to_outstanding` | yes | 1 |  |
| 39 | `q3.strategies[0].drop_y` |  | 0.674 | `closeness_to_outstanding` | yes | 1 |  |
| 40 | `q3.strategies[0].drop_z` |  | 1800 | `closeness_to_outstanding` | yes | 1 |  |
| 41 | `q3.strategies[0].explode_time_s` |  | 4.1 | `closeness_to_outstanding` | yes | 1 |  |
| 42 | `q3.strategies[0].explode_x` |  | 17308.031 | `closeness_to_outstanding` | yes | 1 |  |
| 43 | `q3.strategies[0].explode_y` |  | 5.528 | `closeness_to_outstanding` | yes | 1 |  |
| 44 | `q3.strategies[0].explode_z` |  | 1736.496 | `closeness_to_outstanding` | yes | 1 |  |
| 45 | `q3.strategies[0].fuse_time_s` |  | 3.6 | `closeness_to_outstanding` | yes | 1 |  |
| 46 | `q3.strategies[0].heading_deg` |  | 179.356 | `closeness_to_outstanding` | yes | 1 |  |
| 47 | `q3.strategies[0].individual_duration_s` |  | 4.5 | `closeness_to_outstanding` | yes | 1 |  |
| 48 | `q3.strategies[0].speed_mps` |  | 120 | `closeness_to_outstanding` | yes | 1 |  |
| 49 | `q3.strategies[1].drop_time_s` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 50 | `q3.strategies[1].drop_x` |  | 17380 | `closeness_to_outstanding` | yes | 1 |  |
| 51 | `q3.strategies[1].drop_y` |  | -0 | `closeness_to_outstanding` | yes | 1 |  |
| 52 | `q3.strategies[1].drop_z` |  | 1800 | `closeness_to_outstanding` | yes | 1 |  |
| 53 | `q3.strategies[1].explode_time_s` |  | 8 | `closeness_to_outstanding` | yes | 1 |  |
| 54 | `q3.strategies[1].explode_x` |  | 16680 | `closeness_to_outstanding` | yes | 1 |  |
| 55 | `q3.strategies[1].explode_y` |  | -0 | `closeness_to_outstanding` | yes | 1 |  |
| 56 | `q3.strategies[1].explode_z` |  | 1677.5 | `closeness_to_outstanding` | yes | 1 |  |
| 57 | `q3.strategies[1].fuse_time_s` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 58 | `q3.strategies[1].heading_deg` |  | 180 | `closeness_to_outstanding` | yes | 1 |  |
| 59 | `q3.strategies[1].individual_duration_s` |  | 2.3 | `closeness_to_outstanding` | yes | 1 |  |
| 60 | `q3.strategies[1].speed_mps` |  | 140 | `closeness_to_outstanding` | yes | 1 |  |
| 61 | `q3.union_duration_s.M1` |  | 6.8 | `closeness_to_outstanding` | yes | 1 |  |
| 62 | `q3.union_duration_s.total` |  | 6.8 | `closeness_to_outstanding` | yes | 1 |  |
| 63 | `q4.strategies[0].drop_time_s` |  | 0.5 | `closeness_to_outstanding` | yes | 1 |  |
| 64 | `q4.strategies[0].drop_x` |  | 17740.004 | `closeness_to_outstanding` | yes | 1 |  |
| 65 | `q4.strategies[0].drop_y` |  | 0.674 | `closeness_to_outstanding` | yes | 1 |  |
| 66 | `q4.strategies[0].drop_z` |  | 1800 | `closeness_to_outstanding` | yes | 1 |  |
| 67 | `q4.strategies[0].explode_time_s` |  | 4.1 | `closeness_to_outstanding` | yes | 1 |  |
| 68 | `q4.strategies[0].explode_x` |  | 17308.031 | `closeness_to_outstanding` | yes | 1 |  |
| 69 | `q4.strategies[0].explode_y` |  | 5.528 | `closeness_to_outstanding` | yes | 1 |  |
| 70 | `q4.strategies[0].explode_z` |  | 1736.496 | `closeness_to_outstanding` | yes | 1 |  |
| 71 | `q4.strategies[0].fuse_time_s` |  | 3.6 | `closeness_to_outstanding` | yes | 1 |  |
| 72 | `q4.strategies[0].heading_deg` |  | 179.356 | `closeness_to_outstanding` | yes | 1 |  |
| 73 | `q4.strategies[0].individual_duration_s` |  | 4.5 | `closeness_to_outstanding` | yes | 1 |  |
| 74 | `q4.strategies[0].speed_mps` |  | 120 | `closeness_to_outstanding` | yes | 1 |  |
| 75 | `q4.strategies[1].drop_time_s` |  | 31.977 | `closeness_to_outstanding` | yes | 1 |  |
| 76 | `q4.strategies[1].drop_x` |  | 2283.971 | `closeness_to_outstanding` | yes | 1 |  |
| 77 | `q4.strategies[1].drop_y` |  | -641.153 | `closeness_to_outstanding` | yes | 1 |  |
| 78 | `q4.strategies[1].drop_z` |  | 700 | `closeness_to_outstanding` | yes | 1 |  |
| 79 | `q4.strategies[1].explode_time_s` |  | 43 | `closeness_to_outstanding` | yes | 1 |  |
| 80 | `q4.strategies[1].explode_x` |  | 1002.963 | `closeness_to_outstanding` | yes | 1 |  |
| 81 | `q4.strategies[1].explode_y` |  | 172 | `closeness_to_outstanding` | yes | 1 |  |
| 82 | `q4.strategies[1].explode_z` |  | 104.596 | `closeness_to_outstanding` | yes | 1 |  |
| 83 | `q4.strategies[1].fuse_time_s` |  | 11.023 | `closeness_to_outstanding` | yes | 1 |  |
| 84 | `q4.strategies[1].heading_deg` |  | 147.594 | `closeness_to_outstanding` | yes | 1 |  |
| 85 | `q4.strategies[1].individual_duration_s` |  | 3.6 | `closeness_to_outstanding` | yes | 1 |  |
| 86 | `q4.strategies[1].speed_mps` |  | 137.646 | `closeness_to_outstanding` | yes | 1 |  |
| 87 | `q4.union_duration_s.M1` |  | 8.1 | `closeness_to_outstanding` | yes | 1 |  |
| 88 | `q4.union_duration_s.total` |  | 8.1 | `closeness_to_outstanding` | yes | 1 |  |
| 89 | `q5.strategies[0].drop_time_s` |  | 32.892 | `closeness_to_outstanding` | yes | 1 |  |
| 90 | `q5.strategies[0].drop_x` |  | 2130.79 | `closeness_to_outstanding` | yes | 1 |  |
| 91 | `q5.strategies[0].drop_y` |  | -609.343 | `closeness_to_outstanding` | yes | 1 |  |
| 92 | `q5.strategies[0].drop_z` |  | 700 | `closeness_to_outstanding` | yes | 1 |  |
| 93 | `q5.strategies[0].explode_time_s` |  | 44 | `closeness_to_outstanding` | yes | 1 |  |
| 94 | `q5.strategies[0].explode_x` |  | 824.089 | `closeness_to_outstanding` | yes | 1 |  |
| 95 | `q5.strategies[0].explode_y` |  | 198.024 | `closeness_to_outstanding` | yes | 1 |  |
| 96 | `q5.strategies[0].explode_z` |  | 95.384 | `closeness_to_outstanding` | yes | 1 |  |
| 97 | `q5.strategies[0].fuse_time_s` |  | 11.108 | `closeness_to_outstanding` | yes | 1 |  |
| 98 | `q5.strategies[0].heading_deg` |  | 148.289 | `closeness_to_outstanding` | yes | 1 |  |
| 99 | `q5.strategies[0].individual_duration_s` |  | 3.5 | `closeness_to_outstanding` | yes | 1 |  |
| 100 | `q5.strategies[0].speed_mps` |  | 138.277 | `closeness_to_outstanding` | yes | 1 |  |
| 101 | `q5.strategies[1].drop_time_s` |  | 34.64 | `closeness_to_outstanding` | yes | 1 |  |
| 102 | `q5.strategies[1].drop_x` |  | 1933.416 | `closeness_to_outstanding` | yes | 1 |  |
| 103 | `q5.strategies[1].drop_y` |  | -626.432 | `closeness_to_outstanding` | yes | 1 |  |
| 104 | `q5.strategies[1].drop_z` |  | 700 | `closeness_to_outstanding` | yes | 1 |  |
| 105 | `q5.strategies[1].explode_time_s` |  | 46 | `closeness_to_outstanding` | yes | 1 |  |
| 106 | `q5.strategies[1].explode_x` |  | 599.729 | `closeness_to_outstanding` | yes | 1 |  |
| 107 | `q5.strategies[1].explode_y` |  | 152.009 | `closeness_to_outstanding` | yes | 1 |  |
| 108 | `q5.strategies[1].explode_z` |  | 67.605 | `closeness_to_outstanding` | yes | 1 |  |
| 109 | `q5.strategies[1].fuse_time_s` |  | 11.36 | `closeness_to_outstanding` | yes | 1 |  |
| 110 | `q5.strategies[1].heading_deg` |  | 149.729 | `closeness_to_outstanding` | yes | 1 |  |
| 111 | `q5.strategies[1].individual_duration_s` |  | 3.4 | `closeness_to_outstanding` | yes | 1 |  |
| 112 | `q5.strategies[1].speed_mps` |  | 135.931 | `closeness_to_outstanding` | yes | 1 |  |
| 113 | `q5.strategies[2].drop_time_s` |  | 0.5 | `closeness_to_outstanding` | yes | 1 |  |
| 114 | `q5.strategies[2].drop_x` |  | 17740.004 | `closeness_to_outstanding` | yes | 1 |  |
| 115 | `q5.strategies[2].drop_y` |  | 0.674 | `closeness_to_outstanding` | yes | 1 |  |
| 116 | `q5.strategies[2].drop_z` |  | 1800 | `closeness_to_outstanding` | yes | 1 |  |
| 117 | `q5.strategies[2].explode_time_s` |  | 4.1 | `closeness_to_outstanding` | yes | 1 |  |
| 118 | `q5.strategies[2].explode_x` |  | 17308.031 | `closeness_to_outstanding` | yes | 1 |  |
| 119 | `q5.strategies[2].explode_y` |  | 5.528 | `closeness_to_outstanding` | yes | 1 |  |
| 120 | `q5.strategies[2].explode_z` |  | 1736.496 | `closeness_to_outstanding` | yes | 1 |  |
| 121 | `q5.strategies[2].fuse_time_s` |  | 3.6 | `closeness_to_outstanding` | yes | 1 |  |
| 122 | `q5.strategies[2].heading_deg` |  | 179.356 | `closeness_to_outstanding` | yes | 1 |  |
| 123 | `q5.strategies[2].individual_duration_s` |  | 4.5 | `closeness_to_outstanding` | yes | 1 |  |
| 124 | `q5.strategies[2].speed_mps` |  | 120 | `closeness_to_outstanding` | yes | 1 |  |
| 125 | `q5.strategies[3].drop_time_s` |  | 23.606 | `closeness_to_outstanding` | yes | 1 |  |
| 126 | `q5.strategies[3].drop_x` |  | 3595.615 | `closeness_to_outstanding` | yes | 1 |  |
| 127 | `q5.strategies[3].drop_y` |  | -748.142 | `closeness_to_outstanding` | yes | 1 |  |
| 128 | `q5.strategies[3].drop_z` |  | 700 | `closeness_to_outstanding` | yes | 1 |  |
| 129 | `q5.strategies[3].explode_time_s` |  | 33 | `closeness_to_outstanding` | yes | 1 |  |
| 130 | `q5.strategies[3].explode_x` |  | 2638.774 | `closeness_to_outstanding` | yes | 1 |  |
| 131 | `q5.strategies[3].explode_y` |  | 148 | `closeness_to_outstanding` | yes | 1 |  |
| 132 | `q5.strategies[3].explode_z` |  | 267.577 | `closeness_to_outstanding` | yes | 1 |  |
| 133 | `q5.strategies[3].fuse_time_s` |  | 9.394 | `closeness_to_outstanding` | yes | 1 |  |
| 134 | `q5.strategies[3].heading_deg` |  | 136.876 | `closeness_to_outstanding` | yes | 1 |  |
| 135 | `q5.strategies[3].individual_duration_s` |  | 3.5 | `closeness_to_outstanding` | yes | 1 |  |
| 136 | `q5.strategies[3].speed_mps` |  | 139.551 | `closeness_to_outstanding` | yes | 1 |  |
| 137 | `q5.strategies[4].drop_time_s` |  | 8 | `closeness_to_outstanding` | yes | 1 |  |
| 138 | `q5.strategies[4].drop_x` |  | 11079.087 | `closeness_to_outstanding` | yes | 1 |  |
| 139 | `q5.strategies[4].drop_y` |  | 835.803 | `closeness_to_outstanding` | yes | 1 |  |
| 140 | `q5.strategies[4].drop_z` |  | 1400 | `closeness_to_outstanding` | yes | 1 |  |
| 141 | `q5.strategies[4].explode_time_s` |  | 15 | `closeness_to_outstanding` | yes | 1 |  |
| 142 | `q5.strategies[4].explode_x` |  | 10273.287 | `closeness_to_outstanding` | yes | 1 |  |
| 143 | `q5.strategies[4].explode_y` |  | 342.13 | `closeness_to_outstanding` | yes | 1 |  |
| 144 | `q5.strategies[4].explode_z` |  | 1159.9 | `closeness_to_outstanding` | yes | 1 |  |
| 145 | `q5.strategies[4].fuse_time_s` |  | 7 | `closeness_to_outstanding` | yes | 1 |  |
| 146 | `q5.strategies[4].heading_deg` |  | 211.494 | `closeness_to_outstanding` | yes | 1 |  |
| 147 | `q5.strategies[4].individual_duration_s` |  | 2.7 | `closeness_to_outstanding` | yes | 1 |  |
| 148 | `q5.strategies[4].speed_mps` |  | 135 | `closeness_to_outstanding` | yes | 1 |  |
| 149 | `q5.strategies[5].drop_time_s` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 150 | `q5.strategies[5].drop_x` |  | 17380 | `closeness_to_outstanding` | yes | 1 |  |
| 151 | `q5.strategies[5].drop_y` |  | -0 | `closeness_to_outstanding` | yes | 1 |  |
| 152 | `q5.strategies[5].drop_z` |  | 1800 | `closeness_to_outstanding` | yes | 1 |  |
| 153 | `q5.strategies[5].explode_time_s` |  | 8 | `closeness_to_outstanding` | yes | 1 |  |
| 154 | `q5.strategies[5].explode_x` |  | 16680 | `closeness_to_outstanding` | yes | 1 |  |
| 155 | `q5.strategies[5].explode_y` |  | -0 | `closeness_to_outstanding` | yes | 1 |  |
| 156 | `q5.strategies[5].explode_z` |  | 1677.5 | `closeness_to_outstanding` | yes | 1 |  |
| 157 | `q5.strategies[5].fuse_time_s` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 158 | `q5.strategies[5].heading_deg` |  | 180 | `closeness_to_outstanding` | yes | 1 |  |
| 159 | `q5.strategies[5].individual_duration_s` |  | 2.3 | `closeness_to_outstanding` | yes | 1 |  |
| 160 | `q5.strategies[5].speed_mps` |  | 140 | `closeness_to_outstanding` | yes | 1 |  |
| 161 | `q5.union_duration_s.M1` |  | 10.3 | `closeness_to_outstanding` | yes | 1 |  |
| 162 | `q5.union_duration_s.M2` |  | 6.2 | `closeness_to_outstanding` | yes | 1 |  |
| 163 | `q5.union_duration_s.M3` |  | 3.4 | `closeness_to_outstanding` | yes | 1 |  |
| 164 | `q5.union_duration_s.total` |  | 19.9 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2025-b-sic-thickness"></a>

# CUMCM 2025 B: SiC epitaxial-layer thickness inversion

- Task slug: `cumcm-2025-b-sic-thickness`
- Required output: `/root/results/cumcm-2025-b-sic-thickness_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 2
- Effective scored metric count: 2
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.si_recommended_thickness_um` |  | 10.5145 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.sic_recommended_thickness_um` |  | 8.9815 | `closeness_to_outstanding` | yes | 1 |  |

<a id="cumcm-2025-c-nipt"></a>

# CUMCM 2025 C: NIPT timing and fetal abnormality modeling

- Task slug: `cumcm-2025-c-nipt`
- Required output: `/root/results/cumcm-2025-c-nipt_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 8
- Effective scored metric count: 8
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.earliest_recommended_week` |  | 12 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.female_loo_accuracy` |  | 0.8659 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.latest_recommended_week` |  | 20 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.male_pseudo_r2` |  | 0.90064 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `male_lmm.mother_count` |  | 267 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `male_lmm.pseudo_r2` |  | 0.90064 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `male_lmm.residual_sigma_logit` |  | 0.47707 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `male_lmm.rmse_fetal_fraction` |  | 0.01056 | `closeness_to_outstanding` | yes | 1 |  |

<a id="mcm-2023-a-plant-community"></a>

# MCM 2023 A: drought-stricken plant communities

- Task slug: `mcm-2023-a-plant-community`
- Required output: `/root/results/mcm-2023-a-plant-community_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 41
- Effective scored metric count: 41
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.502804666667`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `reproduced.beta_decline_pct` |  | 32 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `reproduced.coefficient_of_variation_1_to_5[0]` |  | 0.1864 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `reproduced.coefficient_of_variation_1_to_5[1]` |  | 0.0653 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `reproduced.drought_buffer[0].diversity_buffer_gain_pct` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `reproduced.drought_buffer[0].drought_frequency_per_50y` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `reproduced.drought_buffer[0].five_species_biomass_index` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `reproduced.drought_buffer[0].monoculture_biomass_index` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `reproduced.drought_buffer[1].diversity_buffer_gain_pct` |  | 7.92 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `reproduced.drought_buffer[1].drought_frequency_per_50y` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `reproduced.drought_buffer[1].five_species_biomass_index` |  | 0.8992 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `reproduced.drought_buffer[1].monoculture_biomass_index` |  | 0.82 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `reproduced.drought_buffer[2].diversity_buffer_gain_pct` |  | 14.96 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `reproduced.drought_buffer[2].drought_frequency_per_50y` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `reproduced.drought_buffer[2].five_species_biomass_index` |  | 0.8096 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `reproduced.drought_buffer[2].monoculture_biomass_index` |  | 0.66 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `reproduced.five_species_pielou_evenness` |  | 0.8826 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `reproduced.optimal_species_count` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `reproduced.species_count_summary[0].coefficient_of_variation` |  | 0.1864 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `reproduced.species_count_summary[0].mean_total_biomass_last20y` |  | 371.5034 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `reproduced.species_count_summary[0].pielou_evenness` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `reproduced.species_count_summary[0].species_count` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `reproduced.species_count_summary[1].coefficient_of_variation` |  | 0.1419 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `reproduced.species_count_summary[1].mean_total_biomass_last20y` |  | 500.0073 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `reproduced.species_count_summary[1].pielou_evenness` |  | 0.958 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `reproduced.species_count_summary[1].species_count` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `reproduced.species_count_summary[2].coefficient_of_variation` |  | 0.1037 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `reproduced.species_count_summary[2].mean_total_biomass_last20y` |  | 452.1233 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `reproduced.species_count_summary[2].pielou_evenness` |  | 0.9285 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `reproduced.species_count_summary[2].species_count` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `reproduced.species_count_summary[3].coefficient_of_variation` |  | 0.0788 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `reproduced.species_count_summary[3].mean_total_biomass_last20y` |  | 394.0814 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `reproduced.species_count_summary[3].pielou_evenness` |  | 0.9066 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `reproduced.species_count_summary[3].species_count` |  | 4 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `reproduced.species_count_summary[4].coefficient_of_variation` |  | 0.0653 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `reproduced.species_count_summary[4].mean_total_biomass_last20y` |  | 335.2487 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `reproduced.species_count_summary[4].pielou_evenness` |  | 0.8826 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `reproduced.species_count_summary[4].species_count` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `target_comparison.beta_decline_pct.actual` |  | 32 | `closeness_to_outstanding` | yes | 1 |  |
| 39 | `target_comparison.cov_decrease_1_to_5.actual` |  | 0.1211 | `closeness_to_outstanding` | yes | 1 |  |
| 40 | `target_comparison.five_species_pielou_evenness.actual` |  | 0.8826 | `closeness_to_outstanding` | yes | 1 |  |
| 41 | `target_comparison.optimal_species_count.actual` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |

<a id="mcm-2023-b-maasai-mara"></a>

# MCM 2023 B: reimagining Maasai Mara

- Task slug: `mcm-2023-b-maasai-mara`
- Required output: `/root/results/mcm-2023-b-maasai-mara_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 11
- Effective scored metric count: 11
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.60265725`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `reproduced.best_scenario_benefit_million` |  | 154948.974 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `reproduced.mean_sanctuary_to_tourism_interaction_distance` |  | 2.7376 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `reproduced.scenario2_counts.agricultural_area` |  | 12 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `reproduced.scenario2_counts.hunting_area` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `reproduced.scenario2_counts.tourism_area` |  | 9 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `reproduced.scenario2_counts.wildlife_sanctuary` |  | 13 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `target_comparison.scenario2_agriculture_cells.actual` |  | 12 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `target_comparison.scenario2_benefit_million.actual` |  | 154948.974 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `target_comparison.scenario2_hunting_cells.actual` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `target_comparison.scenario2_tourism_cells.actual` |  | 9 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `target_comparison.scenario2_wildlife_cells.actual` |  | 13 | `closeness_to_outstanding` | yes | 1 |  |

<a id="mcm-2023-c-wordle"></a>

# MCM 2023 C: predicting Wordle results

- Task slug: `mcm-2023-c-wordle`
- Required output: `/root/results/mcm-2023-c-wordle_result.json`
- Scoring version: `tb-mathmodeling-v4-endpoint-target-minmax`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 23
- Effective scored metric count: 17
- Baseline endpoint: `question_result_minmax_endpoint`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction_metric_values`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `reproduced.best_tree_holdout_accuracy` | 0.422222 | 1 | `higher_is_better` | yes | 1 | `difficulty_model.holdout_accuracy` |
| 2 | `reproduced.calibrated_lightgbm_like_accuracy` | 0.422222 | 0.7 | `higher_is_better` | yes | 1 | `difficulty_model.holdout_accuracy` |
| 3 | `reproduced.difficulty_metrics[0].holdout_accuracy` | 0.422222 | 1 | `higher_is_better` | yes | 1 | `difficulty_model.holdout_accuracy` |
| 4 | `reproduced.difficulty_metrics[0].train_accuracy` |  | 1 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 5 | `reproduced.difficulty_metrics[1].holdout_accuracy` | 0.422222 | 1 | `higher_is_better` | yes | 1 | `difficulty_model.holdout_accuracy` |
| 6 | `reproduced.difficulty_metrics[1].train_accuracy` |  | 1 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 7 | `reproduced.eerie.difficulty_group` | 2 | 2 | `exact_value` | no: exact value | 0 | `difficulty_model.eerie_classifier_class` |
| 8 | `reproduced.eerie.paper_aligned_distribution_pct[0]` | 0.245 | 0.649 | `higher_is_better` | yes | 1 | `eerie_prediction.predicted_distribution_percent.1 try` |
| 9 | `reproduced.eerie.paper_aligned_distribution_pct[1]` | 7.01 | 7.5792 | `higher_is_better` | yes | 1 | `eerie_prediction.predicted_distribution_percent.2 tries` |
| 10 | `reproduced.eerie.paper_aligned_distribution_pct[2]` | 22.062 | 26.2985 | `higher_is_better` | yes | 1 | `eerie_prediction.predicted_distribution_percent.3 tries` |
| 11 | `reproduced.eerie.paper_aligned_distribution_pct[3]` | 30.668 | 32.6147 | `higher_is_better` | yes | 1 | `eerie_prediction.predicted_distribution_percent.4 tries` |
| 12 | `reproduced.eerie.paper_aligned_distribution_pct[4]` | 22.491 | 20.9304 | `lower_is_better` | yes | 1 | `eerie_prediction.predicted_distribution_percent.5 tries` |
| 13 | `reproduced.eerie.paper_aligned_distribution_pct[5]` | 11.839 | 9.6302 | `lower_is_better` | yes | 1 | `eerie_prediction.predicted_distribution_percent.6 tries` |
| 14 | `reproduced.eerie.paper_aligned_distribution_pct[6]` | 5.685 | 2.298 | `lower_is_better` | yes | 1 | `eerie_prediction.predicted_distribution_percent.7 or more tries (X)` |
| 15 | `reproduced.forecast_record.horizon_days` | 60 | 60 | `exact_value` | no: exact value | 0 | `data_source.date_max -> report_count_model.prediction_date` |
| 16 | `reproduced.forecast_record.raw_80_lower` | 20365 | 0 | `lower_is_better` | yes | 1 | `report_count_model.prediction_interval_80[0]` |
| 17 | `reproduced.forecast_record.raw_80_upper` | 30713 | 59621.565 | `higher_is_better` | yes | 1 | `report_count_model.prediction_interval_80[1]` |
| 18 | `reproduced.forecast_record.raw_ma_forecast` | 23612 | 16662.852 | `lower_is_better` | yes | 1 | `report_count_model.predicted_reported_results` |
| 19 | `target_comparison.eerie_distribution_sum_pct.actual` | 100 | 100 | `exact_value` | no: exact value | 0 | `eerie_prediction.predicted_distribution_percent` |
| 20 | `target_comparison.eerie_group.actual` | 2 | 2 | `exact_value` | no: exact value | 0 | `difficulty_model.eerie_classifier_class` |
| 21 | `target_comparison.forecast_lower.actual` | 20365 | 10139.23 | `lower_is_better` | yes | 1 | `report_count_model.prediction_interval_80[0]` |
| 22 | `target_comparison.forecast_upper.actual` | 30713 | 30808.07 | `higher_is_better` | yes | 1 | `report_count_model.prediction_interval_80[1]` |
| 23 | `target_comparison.lightgbm_like_accuracy.actual` | 0.422222 | 0.7 | `higher_is_better` | yes | 1 | `difficulty_model.holdout_accuracy` |

<a id="mcm-2024-a-lamprey"></a>

# MCM 2024 A: lamprey sex-ratio ecology

- Task slug: `mcm-2024-a-lamprey`
- Required output: `/root/results/mcm-2024-a-lamprey_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 105
- Effective scored metric count: 105
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.45683575`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.adaptive_vs_fixed[0].adaptive_gain_pct` |  | 3.26 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.adaptive_vs_fixed[0].adaptive_stability` |  | 0.9144 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.adaptive_vs_fixed[0].fixed_stability` |  | 0.8855 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.adaptive_vs_fixed[1].adaptive_gain_pct` |  | 1.04 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.adaptive_vs_fixed[1].adaptive_stability` |  | 0.8824 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.adaptive_vs_fixed[1].fixed_stability` |  | 0.8733 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.adaptive_vs_fixed[2].adaptive_gain_pct` |  | 0.31 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.adaptive_vs_fixed[2].adaptive_stability` |  | 0.8659 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.adaptive_vs_fixed[2].fixed_stability` |  | 0.8632 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `experiment_result.adaptive_vs_fixed[3].adaptive_gain_pct` |  | 3.08 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `experiment_result.adaptive_vs_fixed[3].adaptive_stability` |  | 0.8566 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `experiment_result.adaptive_vs_fixed[3].fixed_stability` |  | 0.831 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `experiment_result.largest_stability_gain.adaptive_gain_pct` |  | 3.26 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `experiment_result.largest_stability_gain.adaptive_stability` |  | 0.9144 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `experiment_result.largest_stability_gain.fixed_stability` |  | 0.8855 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `experiment_result.parasite_coexistence_case.final_parasite_index` |  | 8.562 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `experiment_result.parasite_coexistence_case.host_fish_index` |  | 1080.356 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `experiment_result.scenario_summary[0].composite_stability` |  | 0.8855 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `experiment_result.scenario_summary[0].final_host_fish` |  | 1052.013 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `experiment_result.scenario_summary[0].final_lamprey` |  | 2079.718 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `experiment_result.scenario_summary[0].final_parasite` |  | 5.506 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `experiment_result.scenario_summary[0].mean_biomass` |  | 3187.261 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `experiment_result.scenario_summary[0].normalized_diversity` |  | 0.8213 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `experiment_result.scenario_summary[0].resilience` |  | 0.8693 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `experiment_result.scenario_summary[0].resistance` |  | 0.8979 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `experiment_result.scenario_summary[0].shannon_diversity` |  | 1.4715 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `experiment_result.scenario_summary[0].species_persistence` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `experiment_result.scenario_summary[0].sustainability` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `experiment_result.scenario_summary[1].composite_stability` |  | 0.9144 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `experiment_result.scenario_summary[1].final_host_fish` |  | 1163.941 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `experiment_result.scenario_summary[1].final_lamprey` |  | 1262.576 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `experiment_result.scenario_summary[1].final_parasite` |  | 38.764 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `experiment_result.scenario_summary[1].mean_biomass` |  | 2482.149 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `experiment_result.scenario_summary[1].normalized_diversity` |  | 0.7913 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `experiment_result.scenario_summary[1].resilience` |  | 0.9732 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `experiment_result.scenario_summary[1].resistance` |  | 0.9155 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `experiment_result.scenario_summary[1].shannon_diversity` |  | 1.4177 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `experiment_result.scenario_summary[1].species_persistence` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 39 | `experiment_result.scenario_summary[1].sustainability` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 40 | `experiment_result.scenario_summary[2].composite_stability` |  | 0.8733 | `closeness_to_outstanding` | yes | 1 |  |
| 41 | `experiment_result.scenario_summary[2].final_host_fish` |  | 987.127 | `closeness_to_outstanding` | yes | 1 |  |
| 42 | `experiment_result.scenario_summary[2].final_lamprey` |  | 2588.436 | `closeness_to_outstanding` | yes | 1 |  |
| 43 | `experiment_result.scenario_summary[2].final_parasite` |  | 1.737 | `closeness_to_outstanding` | yes | 1 |  |
| 44 | `experiment_result.scenario_summary[2].mean_biomass` |  | 3646.292 | `closeness_to_outstanding` | yes | 1 |  |
| 45 | `experiment_result.scenario_summary[2].normalized_diversity` |  | 0.8169 | `closeness_to_outstanding` | yes | 1 |  |
| 46 | `experiment_result.scenario_summary[2].resilience` |  | 0.8536 | `closeness_to_outstanding` | yes | 1 |  |
| 47 | `experiment_result.scenario_summary[2].resistance` |  | 0.8768 | `closeness_to_outstanding` | yes | 1 |  |
| 48 | `experiment_result.scenario_summary[2].shannon_diversity` |  | 1.4637 | `closeness_to_outstanding` | yes | 1 |  |
| 49 | `experiment_result.scenario_summary[2].species_persistence` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 50 | `experiment_result.scenario_summary[2].sustainability` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 51 | `experiment_result.scenario_summary[3].composite_stability` |  | 0.8824 | `closeness_to_outstanding` | yes | 1 |  |
| 52 | `experiment_result.scenario_summary[3].final_host_fish` |  | 1080.356 | `closeness_to_outstanding` | yes | 1 |  |
| 53 | `experiment_result.scenario_summary[3].final_lamprey` |  | 1900.454 | `closeness_to_outstanding` | yes | 1 |  |
| 54 | `experiment_result.scenario_summary[3].final_parasite` |  | 8.562 | `closeness_to_outstanding` | yes | 1 |  |
| 55 | `experiment_result.scenario_summary[3].mean_biomass` |  | 3041.299 | `closeness_to_outstanding` | yes | 1 |  |
| 56 | `experiment_result.scenario_summary[3].normalized_diversity` |  | 0.8077 | `closeness_to_outstanding` | yes | 1 |  |
| 57 | `experiment_result.scenario_summary[3].resilience` |  | 0.8953 | `closeness_to_outstanding` | yes | 1 |  |
| 58 | `experiment_result.scenario_summary[3].resistance` |  | 0.873 | `closeness_to_outstanding` | yes | 1 |  |
| 59 | `experiment_result.scenario_summary[3].shannon_diversity` |  | 1.4471 | `closeness_to_outstanding` | yes | 1 |  |
| 60 | `experiment_result.scenario_summary[3].species_persistence` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 61 | `experiment_result.scenario_summary[3].sustainability` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 62 | `experiment_result.scenario_summary[4].composite_stability` |  | 0.8632 | `closeness_to_outstanding` | yes | 1 |  |
| 63 | `experiment_result.scenario_summary[4].final_host_fish` |  | 930.367 | `closeness_to_outstanding` | yes | 1 |  |
| 64 | `experiment_result.scenario_summary[4].final_lamprey` |  | 3056.291 | `closeness_to_outstanding` | yes | 1 |  |
| 65 | `experiment_result.scenario_summary[4].final_parasite` |  | 0.616 | `closeness_to_outstanding` | yes | 1 |  |
| 66 | `experiment_result.scenario_summary[4].mean_biomass` |  | 4074.932 | `closeness_to_outstanding` | yes | 1 |  |
| 67 | `experiment_result.scenario_summary[4].normalized_diversity` |  | 0.8076 | `closeness_to_outstanding` | yes | 1 |  |
| 68 | `experiment_result.scenario_summary[4].resilience` |  | 0.8431 | `closeness_to_outstanding` | yes | 1 |  |
| 69 | `experiment_result.scenario_summary[4].resistance` |  | 0.8612 | `closeness_to_outstanding` | yes | 1 |  |
| 70 | `experiment_result.scenario_summary[4].shannon_diversity` |  | 1.4471 | `closeness_to_outstanding` | yes | 1 |  |
| 71 | `experiment_result.scenario_summary[4].species_persistence` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 72 | `experiment_result.scenario_summary[4].sustainability` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 73 | `experiment_result.scenario_summary[5].composite_stability` |  | 0.8659 | `closeness_to_outstanding` | yes | 1 |  |
| 74 | `experiment_result.scenario_summary[5].final_host_fish` |  | 1007.488 | `closeness_to_outstanding` | yes | 1 |  |
| 75 | `experiment_result.scenario_summary[5].final_lamprey` |  | 2469.707 | `closeness_to_outstanding` | yes | 1 |  |
| 76 | `experiment_result.scenario_summary[5].final_parasite` |  | 2.354 | `closeness_to_outstanding` | yes | 1 |  |
| 77 | `experiment_result.scenario_summary[5].mean_biomass` |  | 3554.691 | `closeness_to_outstanding` | yes | 1 |  |
| 78 | `experiment_result.scenario_summary[5].normalized_diversity` |  | 0.8073 | `closeness_to_outstanding` | yes | 1 |  |
| 79 | `experiment_result.scenario_summary[5].resilience` |  | 0.8628 | `closeness_to_outstanding` | yes | 1 |  |
| 80 | `experiment_result.scenario_summary[5].resistance` |  | 0.8507 | `closeness_to_outstanding` | yes | 1 |  |
| 81 | `experiment_result.scenario_summary[5].shannon_diversity` |  | 1.4465 | `closeness_to_outstanding` | yes | 1 |  |
| 82 | `experiment_result.scenario_summary[5].species_persistence` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 83 | `experiment_result.scenario_summary[5].sustainability` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 84 | `experiment_result.scenario_summary[6].composite_stability` |  | 0.831 | `closeness_to_outstanding` | yes | 1 |  |
| 85 | `experiment_result.scenario_summary[6].final_host_fish` |  | 892.229 | `closeness_to_outstanding` | yes | 1 |  |
| 86 | `experiment_result.scenario_summary[6].final_lamprey` |  | 3383.705 | `closeness_to_outstanding` | yes | 1 |  |
| 87 | `experiment_result.scenario_summary[6].final_parasite` |  | 0.302 | `closeness_to_outstanding` | yes | 1 |  |
| 88 | `experiment_result.scenario_summary[6].mean_biomass` |  | 4378.203 | `closeness_to_outstanding` | yes | 1 |  |
| 89 | `experiment_result.scenario_summary[6].normalized_diversity` |  | 0.7992 | `closeness_to_outstanding` | yes | 1 |  |
| 90 | `experiment_result.scenario_summary[6].resilience` |  | 0.8381 | `closeness_to_outstanding` | yes | 1 |  |
| 91 | `experiment_result.scenario_summary[6].resistance` |  | 0.8493 | `closeness_to_outstanding` | yes | 1 |  |
| 92 | `experiment_result.scenario_summary[6].shannon_diversity` |  | 1.4321 | `closeness_to_outstanding` | yes | 1 |  |
| 93 | `experiment_result.scenario_summary[6].species_persistence` |  | 0.8333 | `closeness_to_outstanding` | yes | 1 |  |
| 94 | `experiment_result.scenario_summary[6].sustainability` |  | 0.8333 | `closeness_to_outstanding` | yes | 1 |  |
| 95 | `experiment_result.scenario_summary[7].composite_stability` |  | 0.8566 | `closeness_to_outstanding` | yes | 1 |  |
| 96 | `experiment_result.scenario_summary[7].final_host_fish` |  | 959.411 | `closeness_to_outstanding` | yes | 1 |  |
| 97 | `experiment_result.scenario_summary[7].final_lamprey` |  | 2862.114 | `closeness_to_outstanding` | yes | 1 |  |
| 98 | `experiment_result.scenario_summary[7].final_parasite` |  | 0.999 | `closeness_to_outstanding` | yes | 1 |  |
| 99 | `experiment_result.scenario_summary[7].mean_biomass` |  | 3910.166 | `closeness_to_outstanding` | yes | 1 |  |
| 100 | `experiment_result.scenario_summary[7].normalized_diversity` |  | 0.8019 | `closeness_to_outstanding` | yes | 1 |  |
| 101 | `experiment_result.scenario_summary[7].resilience` |  | 0.8513 | `closeness_to_outstanding` | yes | 1 |  |
| 102 | `experiment_result.scenario_summary[7].resistance` |  | 0.8358 | `closeness_to_outstanding` | yes | 1 |  |
| 103 | `experiment_result.scenario_summary[7].shannon_diversity` |  | 1.4369 | `closeness_to_outstanding` | yes | 1 |  |
| 104 | `experiment_result.scenario_summary[7].species_persistence` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 105 | `experiment_result.scenario_summary[7].sustainability` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |

<a id="mcm-2024-b-submersible-search"></a>

# MCM 2024 B: submersible localization and search planning

- Task slug: `mcm-2024-b-submersible-search`
- Required output: `/root/results/mcm-2024-b-submersible-search_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 13
- Effective scored metric count: 13
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.57862125`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.caribbean_adaptation.current_multiplier` |  | 1.35 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.caribbean_adaptation.terrain_uncertainty_multiplier` |  | 1.2 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.equipment_selection.top_score` |  | 0.8357 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.location_model.final_mean_x_m` |  | 7698.65 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.location_model.final_mean_y_m` |  | -2324.78 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.location_model.final_p95_area_km2` |  | 0.9722 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.search_strategy.calibrated_detection_multiplier` |  | 0.8557 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.search_strategy.find_probability_10h_start_1h` |  | 0.43 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.search_strategy.find_probability_10h_start_3h` |  | 0.2338 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `experiment_result.search_strategy.find_probability_10h_start_5h` |  | 0.1158 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `experiment_result.search_strategy.find_probability_18h` |  | 0.4377 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `experiment_result.search_strategy.find_probability_6h` |  | 0.4068 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `experiment_result.search_strategy.searched_cells` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |

<a id="mcm-2024-c-tennis-momentum"></a>

# MCM 2024 C: momentum in tennis

- Task slug: `mcm-2024-c-tennis-momentum`
- Required output: `/root/results/mcm-2024-c-tennis-momentum_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 22
- Effective scored metric count: 22
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.5912914`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.dual_temporal_bayes.final_match_warning_rate` |  | 0.006 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.dual_temporal_bayes.strongest_transition.probability` |  | 0.6726 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.dual_temporal_bayes.swing_warning_rate` |  | 0.0032 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.momentum_model.final_momentum_range` |  | 0.7895 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.randomness_tests.matches_rejecting_iid_at_5pct` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.randomness_tests.median_ljung_box_p` |  | 0.712832 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.randomness_tests.median_runs_p` |  | 0.290172 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.top_swing_features[0].mean_otherwise` |  | 0.1257 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.top_swing_features[0].mean_when_warning` |  | 0.3043 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `experiment_result.top_swing_features[0].warning_correlation` |  | 0.0302 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `experiment_result.top_swing_features[1].mean_otherwise` |  | 0.1363 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `experiment_result.top_swing_features[1].mean_when_warning` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `experiment_result.top_swing_features[1].warning_correlation` |  | -0.0223 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `experiment_result.top_swing_features[2].mean_otherwise` |  | 100.773 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `experiment_result.top_swing_features[2].mean_when_warning` |  | 110.7391 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `experiment_result.top_swing_features[2].warning_correlation` |  | 0.0154 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `experiment_result.top_swing_features[3].mean_otherwise` |  | 0.1719 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `experiment_result.top_swing_features[3].mean_when_warning` |  | 0.087 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `experiment_result.top_swing_features[3].warning_correlation` |  | -0.0126 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `experiment_result.top_swing_features[4].mean_otherwise` |  | 0.0313 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `experiment_result.top_swing_features[4].mean_when_warning` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `experiment_result.top_swing_features[4].warning_correlation` |  | -0.0101 | `closeness_to_outstanding` | yes | 1 |  |

<a id="mcm-2025-a-stair-wear"></a>

# MCM 2025 A: stair wear and historical traffic inference

- Task slug: `mcm-2025-a-stair-wear`
- Required output: `/root/results/mcm-2025-a-stair-wear_result.json`
- Scoring version: `tb-mathmodeling-v4-endpoint-target-minmax`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 21
- Effective scored metric count: 5
- Baseline endpoint: `question_result_minmax_endpoint`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction_metric_values`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `daily_use_pattern.peak_period_share_of_daily_use` | 0.376 | 0.376 | `exact_value` | no: exact value | 0 | `daily_use_pattern.peak_period_share_of_daily_use` |
| 2 | `daily_use_pattern.peak_period_users` | 27.3 | 27.6 | `higher_is_better` | yes | 1 | `daily_use_pattern.peak_period_users` |
| 3 | `daily_use_pattern.regular_hour_users_if_spread_over_10_hours` | 4.5 | 4.6 | `higher_is_better` | yes | 1 | `daily_use_pattern.regular_hour_users_if_spread_over_10_hours` |
| 4 | `experiment_result.age_interval_years[0]` | 283.6 | 283.6 | `exact_value` | no: exact value | 0 | `age_reliability.plausible_interval_years[0]` |
| 5 | `experiment_result.age_interval_years[1]` | 397 | 397 | `exact_value` | no: exact value | 0 | `age_reliability.plausible_interval_years[1]` |
| 6 | `experiment_result.estimated_age_years` | 340.3 | 340.3 | `exact_value` | no: exact value | 0 | `age_reliability.estimated_age_years` |
| 7 | `experiment_result.estimated_daily_users` | 72.67 | 73.52 | `higher_is_better` | yes | 1 | `inverse_wear_model.usage_frequency.estimated_daily_users` |
| 8 | `experiment_result.estimated_passages_per_tread` | 9555556 | 9666667 | `higher_is_better` | yes | 1 | `inverse_wear_model.usage_frequency.estimated_passages_per_tread` |
| 9 | `experiment_result.lateral_centroid` |  | -0.0261 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 10 | `experiment_result.median_center_wear_depth_mm` | 4.3 | 4.35 | `higher_is_better` | yes | 1 | `inverse_wear_model.usage_frequency.median_center_wear_depth_mm` |
| 11 | `material_consistency.worked_example_material_proxy.material_density_proxy_g_cm3` | 2.35 | 2.35 | `exact_value` | no: exact value | 0 | `material_source_guidance.worked_example_material_proxy.material_density_proxy` |
| 12 | `material_consistency.worked_example_material_proxy.surface_hardness_proxy` | 4 | 4 | `exact_value` | no: exact value | 0 | `material_source_guidance.worked_example_material_proxy.surface_hardness_proxy` |
| 13 | `renovation_detection.repair_candidates[0].candidate_score` | 5.35 | 5.35 | `exact_value` | no: exact value | 0 | `renovation_detection.repair_candidates[0].candidate_score` |
| 14 | `renovation_detection.repair_candidates[0].patch_boundary_score` | 5 | 5 | `exact_value` | no: exact value | 0 | `renovation_detection.repair_candidates[0].patch_boundary_score` |
| 15 | `renovation_detection.repair_candidates[0].wear_jump_mm` | -2.4 | -2.4 | `exact_value` | no: exact value | 0 | `renovation_detection.repair_candidates[0].wear_jump_mm` |
| 16 | `renovation_detection.repair_candidates[1].candidate_score` | 3 | 3 | `exact_value` | no: exact value | 0 | `renovation_detection.repair_candidates[1].candidate_score` |
| 17 | `renovation_detection.repair_candidates[1].patch_boundary_score` | 2 | 2 | `exact_value` | no: exact value | 0 | `renovation_detection.repair_candidates[1].patch_boundary_score` |
| 18 | `renovation_detection.repair_candidates[1].wear_jump_mm` | 1.4 | 1.4 | `exact_value` | no: exact value | 0 | `renovation_detection.repair_candidates[1].wear_jump_mm` |
| 19 | `wdm.front_to_back_rounding_ratio` | 1.497 | 1.497 | `exact_value` | no: exact value | 0 | `inverse_wear_model.direction_preference.front_to_back_rounding_ratio` |
| 20 | `wdm.side_to_center_wear_ratio` | 0.526 | 0.526 | `exact_value` | no: exact value | 0 | `inverse_wear_model.simultaneous_use.side_to_center_wear_ratio` |
| 21 | `wdm.simultaneous_use_index_0_1` | 0.391 | 0.391 | `exact_value` | no: exact value | 0 | `inverse_wear_model.simultaneous_use.simultaneous_use_index_0_1` |

<a id="mcm-2025-b-juneau-tourism"></a>

# MCM 2025 B: sustainable tourism management in Juneau

- Task slug: `mcm-2025-b-juneau-tourism`
- Required output: `/root/results/mcm-2025-b-juneau-tourism_result.json`
- Scoring version: `tb-mathmodeling-v4-endpoint-target-minmax`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 27
- Effective scored metric count: 19
- Baseline endpoint: `question_result_minmax_endpoint`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction_metric_values`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `destination_adaptation.district_population_reference` | 180000 | 180000 | `exact_value` | no: exact value | 0 | `destination_adaptation.adapted_constraints.district_level_planning_population` |
| 2 | `destination_adaptation.scaled_annual_visitor_target` | 8448000 | 8949156 | `higher_is_better` | yes | 1 | `destination_adaptation.adapted_constraints.recommended_annual_visitor_target_for_district` |
| 3 | `dynamic_programming.best_cumulative_score` |  | 4.793367 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 4 | `dynamic_programming.horizon_years[0]` |  | 2024 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 5 | `dynamic_programming.horizon_years[1]` |  | 2028 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 6 | `dynamic_programming.optimal_terminal_policy.annual_visitors` | 1408000 | 1491526 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.annual_visitors` |
| 7 | `dynamic_programming.optimal_terminal_policy.conservation_share` | 0.35 | 0.35 | `exact_value` | no: exact value | 0 | `sustainability_model.optimal_policy.conservation_share` |
| 8 | `dynamic_programming.optimal_terminal_policy.daily_cap` | 10000 | 11000 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.daily_cap` |
| 9 | `dynamic_programming.optimal_terminal_policy.glacier_pressure_fields_per_year` | 0.3353 | 0.3319 | `lower_is_better` | yes | 1 | `sustainability_model.optimal_policy.projected_glacier_recession_fields_per_year` |
| 10 | `dynamic_programming.optimal_terminal_policy.net_benefit_usd` | 313532032 | 341049399.55 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.net_benefit_usd` |
| 11 | `dynamic_programming.optimal_terminal_policy.resident_acceptance_index` | 0.78 | 1 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.resident_acceptance_index` |
| 12 | `dynamic_programming.optimal_terminal_policy.sustainability_score` | 0.908447 | 1.007 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.sustainability_score` |
| 13 | `dynamic_programming.optimal_terminal_policy.total_revenue_usd` | 400400000 | 431610327.83 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.total_revenue_usd` |
| 14 | `dynamic_programming.optimal_terminal_policy.visitor_fee_usd` | 50 | 55 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.visitor_fee_usd` |
| 15 | `dynamic_programming.optimal_terminal_policy.year` |  | 2028 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 16 | `experiment_result.annual_visitors` | 1408000 | 1491526 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.annual_visitors` |
| 17 | `experiment_result.optimal_conservation_share` | 0.35 | 0.35 | `exact_value` | no: exact value | 0 | `sustainability_model.optimal_policy.conservation_share` |
| 18 | `experiment_result.optimal_daily_cap` | 10000 | 11000 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.daily_cap` |
| 19 | `experiment_result.optimal_visitor_fee_usd` | 50 | 55 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.visitor_fee_usd` |
| 20 | `experiment_result.resident_acceptance_index` | 0.78 | 1 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.resident_acceptance_index` |
| 21 | `experiment_result.sustainability_score` | 0.908447 | 1.007 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.sustainability_score` |
| 22 | `experiment_result.terminal_year` |  | 2028 | `unscored_missing_baseline` | no: missing baseline | 0 |  |
| 23 | `experiment_result.total_revenue_usd` | 400400000 | 431610327.83 | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.total_revenue_usd` |
| 24 | `sensitivity_analysis[0].correlation_with_score` | 0.909965 | 0.59522 | `lower_is_better` | yes | 1 | `sensitivity_analysis.top_factors[1].correlation_with_score` |
| 25 | `sensitivity_analysis[2].correlation_with_score` | -0.868509 | -0.19619 | `higher_is_better` | yes | 1 | `sensitivity_analysis.top_factors[2].correlation_with_score` |
| 26 | `sensitivity_analysis[3].correlation_with_score` | 0.227667 | 0.11805 | `lower_is_better` | yes | 1 | `sensitivity_analysis.top_factors[4].correlation_with_score` |
| 27 | `sensitivity_analysis[4].correlation_with_score` | -0.117707 | 0.00598 | `higher_is_better` | yes | 1 | `sensitivity_analysis.top_factors[5].correlation_with_score` |

<a id="mcm-2025-c-olympic-medals"></a>

# MCM 2025 C: Olympic medal prediction

- Task slug: `mcm-2025-c-olympic-medals`
- Required output: `/root/results/mcm-2025-c-olympic-medals_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 96
- Effective scored metric count: 96
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.584014166667`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `great_coach_model.global_top_jump_75pct` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `great_coach_model.lang_ping_validation[0].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `great_coach_model.lang_ping_validation[0].estimated_jump_score` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `great_coach_model.lang_ping_validation[0].medal_score` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `great_coach_model.lang_ping_validation[0].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `great_coach_model.lang_ping_validation[1].Year` |  | 2016 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `great_coach_model.lang_ping_validation[1].estimated_jump_score` |  | 1.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `great_coach_model.lang_ping_validation[1].medal_score` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `great_coach_model.lang_ping_validation[1].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `great_coach_model.recommendations[0].benchmark_jump_score` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `great_coach_model.recommendations[0].estimated_medal_count_gain` |  | 1.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `great_coach_model.recommendations[0].latest_medal_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `great_coach_model.recommendations[0].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `great_coach_model.recommendations[0].recent_baseline_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `great_coach_model.recommendations[1].benchmark_jump_score` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `great_coach_model.recommendations[1].estimated_medal_count_gain` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `great_coach_model.recommendations[1].latest_medal_score` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `great_coach_model.recommendations[1].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `great_coach_model.recommendations[1].recent_baseline_score` |  | 0.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `great_coach_model.recommendations[2].benchmark_jump_score` |  | 9.416667 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `great_coach_model.recommendations[2].estimated_medal_count_gain` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `great_coach_model.recommendations[2].latest_medal_score` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `great_coach_model.recommendations[2].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `great_coach_model.recommendations[2].recent_baseline_score` |  | 2.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `great_coach_model.recommendations[3].benchmark_jump_score` |  | 5.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `great_coach_model.recommendations[3].estimated_medal_count_gain` |  | 1.777778 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `great_coach_model.recommendations[3].latest_medal_score` |  | 12 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `great_coach_model.recommendations[3].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `great_coach_model.recommendations[3].recent_baseline_score` |  | 2.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `great_coach_model.top_historical_jump_candidates[0].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `great_coach_model.top_historical_jump_candidates[0].coach_like_jump` |  | 28 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `great_coach_model.top_historical_jump_candidates[0].medal_score` |  | 34 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `great_coach_model.top_historical_jump_candidates[0].prev3_score` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `great_coach_model.top_historical_jump_candidates[10].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `great_coach_model.top_historical_jump_candidates[10].coach_like_jump` |  | 17.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `great_coach_model.top_historical_jump_candidates[10].medal_score` |  | 31 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `great_coach_model.top_historical_jump_candidates[10].prev3_score` |  | 13.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `great_coach_model.top_historical_jump_candidates[11].Year` |  | 2020 | `closeness_to_outstanding` | yes | 1 |  |
| 39 | `great_coach_model.top_historical_jump_candidates[11].coach_like_jump` |  | 17 | `closeness_to_outstanding` | yes | 1 |  |
| 40 | `great_coach_model.top_historical_jump_candidates[11].medal_score` |  | 17 | `closeness_to_outstanding` | yes | 1 |  |
| 41 | `great_coach_model.top_historical_jump_candidates[11].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 42 | `great_coach_model.top_historical_jump_candidates[1].Year` |  | 2000 | `closeness_to_outstanding` | yes | 1 |  |
| 43 | `great_coach_model.top_historical_jump_candidates[1].coach_like_jump` |  | 23.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 44 | `great_coach_model.top_historical_jump_candidates[1].medal_score` |  | 37 | `closeness_to_outstanding` | yes | 1 |  |
| 45 | `great_coach_model.top_historical_jump_candidates[1].prev3_score` |  | 13.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 46 | `great_coach_model.top_historical_jump_candidates[2].Year` |  | 2004 | `closeness_to_outstanding` | yes | 1 |  |
| 47 | `great_coach_model.top_historical_jump_candidates[2].coach_like_jump` |  | 23 | `closeness_to_outstanding` | yes | 1 |  |
| 48 | `great_coach_model.top_historical_jump_candidates[2].medal_score` |  | 38 | `closeness_to_outstanding` | yes | 1 |  |
| 49 | `great_coach_model.top_historical_jump_candidates[2].prev3_score` |  | 15 | `closeness_to_outstanding` | yes | 1 |  |
| 50 | `great_coach_model.top_historical_jump_candidates[3].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 51 | `great_coach_model.top_historical_jump_candidates[3].coach_like_jump` |  | 22.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 52 | `great_coach_model.top_historical_jump_candidates[3].medal_score` |  | 33 | `closeness_to_outstanding` | yes | 1 |  |
| 53 | `great_coach_model.top_historical_jump_candidates[3].prev3_score` |  | 10.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 54 | `great_coach_model.top_historical_jump_candidates[4].Year` |  | 2000 | `closeness_to_outstanding` | yes | 1 |  |
| 55 | `great_coach_model.top_historical_jump_candidates[4].coach_like_jump` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 56 | `great_coach_model.top_historical_jump_candidates[4].medal_score` |  | 30 | `closeness_to_outstanding` | yes | 1 |  |
| 57 | `great_coach_model.top_historical_jump_candidates[4].prev3_score` |  | 8 | `closeness_to_outstanding` | yes | 1 |  |
| 58 | `great_coach_model.top_historical_jump_candidates[5].Year` |  | 1996 | `closeness_to_outstanding` | yes | 1 |  |
| 59 | `great_coach_model.top_historical_jump_candidates[5].coach_like_jump` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 60 | `great_coach_model.top_historical_jump_candidates[5].medal_score` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 61 | `great_coach_model.top_historical_jump_candidates[5].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 62 | `great_coach_model.top_historical_jump_candidates[6].Year` |  | 1996 | `closeness_to_outstanding` | yes | 1 |  |
| 63 | `great_coach_model.top_historical_jump_candidates[6].coach_like_jump` |  | 20.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 64 | `great_coach_model.top_historical_jump_candidates[6].medal_score` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 65 | `great_coach_model.top_historical_jump_candidates[6].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 66 | `great_coach_model.top_historical_jump_candidates[7].Year` |  | 1996 | `closeness_to_outstanding` | yes | 1 |  |
| 67 | `great_coach_model.top_historical_jump_candidates[7].coach_like_jump` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 68 | `great_coach_model.top_historical_jump_candidates[7].medal_score` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 69 | `great_coach_model.top_historical_jump_candidates[7].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 70 | `great_coach_model.top_historical_jump_candidates[8].Year` |  | 2020 | `closeness_to_outstanding` | yes | 1 |  |
| 71 | `great_coach_model.top_historical_jump_candidates[8].coach_like_jump` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 72 | `great_coach_model.top_historical_jump_candidates[8].medal_score` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 73 | `great_coach_model.top_historical_jump_candidates[8].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 74 | `great_coach_model.top_historical_jump_candidates[9].Year` |  | 2000 | `closeness_to_outstanding` | yes | 1 |  |
| 75 | `great_coach_model.top_historical_jump_candidates[9].coach_like_jump` |  | 17.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 76 | `great_coach_model.top_historical_jump_candidates[9].medal_score` |  | 19 | `closeness_to_outstanding` | yes | 1 |  |
| 77 | `great_coach_model.top_historical_jump_candidates[9].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 78 | `host_effect_model.Gold.event_count_coefficient` |  | 0.000147 | `closeness_to_outstanding` | yes | 1 |  |
| 79 | `host_effect_model.Gold.host_bonus_coefficient` |  | 14.341156 | `closeness_to_outstanding` | yes | 1 |  |
| 80 | `host_effect_model.Gold.prev3_coefficient` |  | 0.950866 | `closeness_to_outstanding` | yes | 1 |  |
| 81 | `host_effect_model.Gold.r2` |  | 0.752918 | `closeness_to_outstanding` | yes | 1 |  |
| 82 | `host_effect_model.Total.event_count_coefficient` |  | -0.000215 | `closeness_to_outstanding` | yes | 1 |  |
| 83 | `host_effect_model.Total.host_bonus_coefficient` |  | 36.422317 | `closeness_to_outstanding` | yes | 1 |  |
| 84 | `host_effect_model.Total.prev3_coefficient` |  | 0.952921 | `closeness_to_outstanding` | yes | 1 |  |
| 85 | `host_effect_model.Total.r2` |  | 0.765819 | `closeness_to_outstanding` | yes | 1 |  |
| 86 | `model_evaluation.holdout_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 87 | `model_evaluation.mean_accuracy_2024` |  | 0.850591 | `closeness_to_outstanding` | yes | 1 |  |
| 88 | `model_evaluation.mean_brier_2024` |  | 0.142806 | `closeness_to_outstanding` | yes | 1 |  |
| 89 | `model_evaluation.mean_f1_2024` |  | 0.287348 | `closeness_to_outstanding` | yes | 1 |  |
| 90 | `model_evaluation.sport_models` |  | 50 | `closeness_to_outstanding` | yes | 1 |  |
| 91 | `model_evaluation.status_counts.GoldBinary:fallback_mean` |  | 7 | `closeness_to_outstanding` | yes | 1 |  |
| 92 | `model_evaluation.status_counts.GoldBinary:random_forest` |  | 43 | `closeness_to_outstanding` | yes | 1 |  |
| 93 | `model_evaluation.status_counts.MedalBinary:fallback_mean` |  | 7 | `closeness_to_outstanding` | yes | 1 |  |
| 94 | `model_evaluation.status_counts.MedalBinary:random_forest` |  | 43 | `closeness_to_outstanding` | yes | 1 |  |
| 95 | `monte_carlo.simulations` |  | 500 | `closeness_to_outstanding` | yes | 1 |  |
| 96 | `monte_carlo.weight_power` |  | 4 | `closeness_to_outstanding` | yes | 1 |  |
