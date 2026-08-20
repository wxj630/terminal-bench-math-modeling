# Evaluation Results

This report is generated from local Harbor jobs and task `score_config.json` files.

- Total tasks: 18
- Default eval method for regenerated tasks: `B-Eval`
- v4 endpoint target-minmax tasks: 3
- legacy fallback tasks: 15
- Oracle jobs found: 18
- Oracle mean reward: 0.998107872466
- DeepSeek/Terminus-2 jobs found: 18
- DeepSeek/Terminus-2 mean job reward: 0.112880297733
- DeepSeek/Terminus-2 mean B-Eval: -0.0107674556435
- DeepSeek/Terminus-2 mean BO-Eval: 0.13545635728

`B-Eval` is the default baseline-only score: `raw_panel_score - baseline_panel_score`, so negative means worse than the baseline. `BO-Eval` is the optional baseline-to-outstanding normalized score. `v4 endpoint target-minmax` means the task has real per-metric `baseline_value` and `outstanding_value` endpoints. `legacy fallback` means no semantically comparable per-metric question-result endpoint has been mapped yet, so the task still uses the older baseline-panel normalization.

| Contest | Year | Problem | Task | Scoring status | Default eval | Metrics | Effective | Exact-value | Missing baseline | Baseline kind | Oracle reward | Oracle status | DeepSeek job reward | DeepSeek B-Eval | DeepSeek BO-Eval | DeepSeek status |
|---|---:|---|---|---|---|---:|---:|---:|---:|---|---:|---|---:|---:|---:|---|
| CUMCM | 2023 | A | `cumcm-2023-a-heliostat-field` | legacy fallback | B-Eval | 29 | 29 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0 |  |  | error: AgentTimeoutError(1) |
| CUMCM | 2023 | B | `cumcm-2023-b-multibeam-lines` | legacy fallback | B-Eval | 21 | 21 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0 |  |  | error: CancelledError(1) |
| CUMCM | 2023 | C | `cumcm-2023-c-vegetable-pricing` | legacy fallback | B-Eval | 38 | 38 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.093365864843 | 0.093365864843 | 0.093365864843 | error: AgentTimeoutError(1) |
| CUMCM | 2024 | A | `cumcm-2024-a-dragon-dance` | legacy fallback | B-Eval | 9 | 9 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.206349206349 | 0.206349206349 | 0.206349206349 | error: AgentTimeoutError(1) |
| CUMCM | 2024 | B | `cumcm-2024-b-production-decision` | legacy fallback | B-Eval | 69 | 69 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.633378428946 | 0.633378428946 | 0.633378428946 | error: AgentTimeoutError(1) |
| CUMCM | 2024 | C | `cumcm-2024-c-crop-planting` | legacy fallback | B-Eval | 20 | 20 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.207024231145 | 0.207024231145 | 0.207024231145 | error: AgentTimeoutError(1) |
| CUMCM | 2025 | A | `cumcm-2025-a-smoke-screen` | legacy fallback | B-Eval | 164 | 164 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0 |  |  | error: AgentTimeoutError(1) |
| CUMCM | 2025 | B | `cumcm-2025-b-sic-thickness` | legacy fallback | B-Eval | 2 | 2 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.143178654302 | 0.143178654302 | 0.143178654302 | error: AgentTimeoutError(1) |
| CUMCM | 2025 | C | `cumcm-2025-c-nipt` | legacy fallback | B-Eval | 8 | 8 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 0.967571343045 | scored | 0.524882309574 | 0.524882309574 | 0.524882309574 | scored |
| MCM | 2023 | A | `mcm-2023-a-plant-community` | legacy fallback | B-Eval | 41 | 41 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 1 | scored | 0 | -0.137723472028 | 0 | error: AgentTimeoutError(1) |
| MCM | 2023 | B | `mcm-2023-b-maasai-mara` | legacy fallback | B-Eval | 11 | 11 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 1 | scored | 0 | -0.570725974269 | 0 | scored |
| MCM | 2023 | C | `mcm-2023-c-wordle` | v4 endpoint target-minmax | B-Eval | 23 | 17 | 4 | 2 | `question_result_minmax_endpoint` | 1 | scored | 0.143159490288 | 0.143159490288 | 0.143159490288 | scored |
| MCM | 2024 | A | `mcm-2024-a-lamprey` | legacy fallback | B-Eval | 105 | 105 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 1 | scored | 0 | -0.24548365989 | 0 | scored |
| MCM | 2024 | B | `mcm-2024-b-submersible-search` | legacy fallback | B-Eval | 13 | 13 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 1 | scored | 0 | -0.437625067352 | 0 | scored |
| MCM | 2024 | C | `mcm-2024-c-tennis-momentum` | legacy fallback | B-Eval | 22 | 22 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 1 | scored | 0 | -0.508413940348 | 0 | scored |
| MCM | 2025 | A | `mcm-2025-a-stair-wear` | v4 endpoint target-minmax | B-Eval | 21 | 5 | 15 | 1 | `question_result_minmax_endpoint` | 1 | scored | 0 | 0 | 0 | scored |
| MCM | 2025 | B | `mcm-2025-b-juneau-tourism` | v4 endpoint target-minmax | B-Eval | 27 | 19 | 3 | 5 | `question_result_minmax_endpoint` | 1 | scored | 0.0805071737516 | 0.0805071737516 | 0.0805071737516 | scored |
| MCM | 2025 | C | `mcm-2025-c-olympic-medals` | legacy fallback | B-Eval | 96 | 96 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 0.998370361347 | scored | 0 | -0.293385079963 | 0 | error: AgentTimeoutError(1) |

# Per-Task Tables

## CUMCM 2023 A: `cumcm-2023-a-heliostat-field`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 29 total, 29 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: N/A
- DeepSeek/Terminus-2 BO-Eval: N/A

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.design_summary[0].annual_optical_efficiency` |  | 0.536230167 | `closeness_to_outstanding` |  |  |  | yes |  |
| 2 | `reproduced.design_summary[0].annual_thermal_power_mw` |  | 32.76117051 | `closeness_to_outstanding` |  |  |  | yes |  |
| 3 | `reproduced.design_summary[0].mirror_count` |  | 1745 | `closeness_to_outstanding` |  |  |  | yes |  |
| 4 | `reproduced.design_summary[0].tower_xy[0]` |  | 0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 5 | `reproduced.design_summary[0].tower_xy[1]` |  | 0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 6 | `reproduced.design_summary[0].unit_area_power_kw_m2` |  | 0.521508604 | `closeness_to_outstanding` |  |  |  | yes |  |
| 7 | `reproduced.design_summary[1].annual_optical_efficiency` |  | 0.591643667 | `closeness_to_outstanding` |  |  |  | yes |  |
| 8 | `reproduced.design_summary[1].annual_thermal_power_mw` |  | 68.24427914 | `closeness_to_outstanding` |  |  |  | yes |  |
| 9 | `reproduced.design_summary[1].installation_height_m` |  | 4 | `closeness_to_outstanding` |  |  |  | yes |  |
| 10 | `reproduced.design_summary[1].mirror_area_m2` |  | 119196 | `closeness_to_outstanding` |  |  |  | yes |  |
| 11 | `reproduced.design_summary[1].mirror_count` |  | 3311 | `closeness_to_outstanding` |  |  |  | yes |  |
| 12 | `reproduced.design_summary[1].mirror_height_m` |  | 6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 13 | `reproduced.design_summary[1].mirror_width_m` |  | 6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 14 | `reproduced.design_summary[1].tower_xy[0]` |  | 0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 15 | `reproduced.design_summary[1].tower_xy[1]` |  | -250 | `closeness_to_outstanding` |  |  |  | yes |  |
| 16 | `reproduced.design_summary[1].unit_area_power_kw_m2` |  | 0.572538333 | `closeness_to_outstanding` |  |  |  | yes |  |
| 17 | `reproduced.design_summary[2].annual_optical_efficiency` |  | 0.496428083 | `closeness_to_outstanding` |  |  |  | yes |  |
| 18 | `reproduced.design_summary[2].annual_thermal_power_mw` |  | 60.336111 | `closeness_to_outstanding` |  |  |  | yes |  |
| 19 | `reproduced.design_summary[2].mirror_area_m2` |  | 119196 | `closeness_to_outstanding` |  |  |  | yes |  |
| 20 | `reproduced.design_summary[2].mirror_count` |  | 3311 | `closeness_to_outstanding` |  |  |  | yes |  |
| 21 | `reproduced.design_summary[2].tower_xy[0]` |  | 0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 22 | `reproduced.design_summary[2].tower_xy[1]` |  | -250 | `closeness_to_outstanding` |  |  |  | yes |  |
| 23 | `reproduced.design_summary[2].unit_area_power_kw_m2` |  | 0.506192417 | `closeness_to_outstanding` |  |  |  | yes |  |
| 24 | `reproduced.official_coordinate_count` |  | 1745 | `closeness_to_outstanding` |  |  |  | yes |  |
| 25 | `reproduced.q1_monthly_efficiency_mean` |  | 0.536230167 | `closeness_to_outstanding` |  |  |  | yes |  |
| 26 | `target_comparison.q1_annual_optical_efficiency.actual` |  | 0.536230167 | `closeness_to_outstanding` |  |  |  | yes |  |
| 27 | `target_comparison.q2_annual_thermal_power_mw.actual` |  | 68.244279 | `closeness_to_outstanding` |  |  |  | yes |  |
| 28 | `target_comparison.q2_mirror_count.actual` |  | 3311 | `closeness_to_outstanding` |  |  |  | yes |  |
| 29 | `target_comparison.q3_annual_thermal_power_mw.actual` |  | 60.336111 | `closeness_to_outstanding` |  |  |  | yes |  |
## CUMCM 2023 B: `cumcm-2023-b-multibeam-lines`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 21 total, 21 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: CancelledError(1))
- DeepSeek/Terminus-2 B-Eval: N/A
- DeepSeek/Terminus-2 BO-Eval: N/A

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.problem3_last_position_m` |  | 7226.14 | `closeness_to_outstanding` |  |  |  | yes |  |
| 2 | `reproduced.problem3_line_count` |  | 34 | `closeness_to_outstanding` |  |  |  | yes |  |
| 3 | `reproduced.problem3_total_length_m` |  | 125936 | `closeness_to_outstanding` |  |  |  | yes |  |
| 4 | `reproduced.problem4_summary.avg_position_error_m` |  | 9.27 | `closeness_to_outstanding` |  |  |  | yes |  |
| 5 | `reproduced.problem4_summary.greedy_avg_overlap_pct` |  | 10.35 | `closeness_to_outstanding` |  |  |  | yes |  |
| 6 | `reproduced.problem4_summary.missed_area_pct` |  | 3.48 | `closeness_to_outstanding` |  |  |  | yes |  |
| 7 | `reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles` |  | 30 | `closeness_to_outstanding` |  |  |  | yes |  |
| 8 | `reproduced.problem4_summary.sa_avg_overlap_pct` |  | 10.48 | `closeness_to_outstanding` |  |  |  | yes |  |
| 9 | `reproduced.problem4_summary.total_length_nautical_miles` |  | 622 | `closeness_to_outstanding` |  |  |  | yes |  |
| 10 | `reproduced.seabed_grid_summary.max_depth_m` |  | 197.2 | `closeness_to_outstanding` |  |  |  | yes |  |
| 11 | `reproduced.seabed_grid_summary.mean_depth_m` |  | 62.539 | `closeness_to_outstanding` |  |  |  | yes |  |
| 12 | `reproduced.seabed_grid_summary.min_depth_m` |  | 20 | `closeness_to_outstanding` |  |  |  | yes |  |
| 13 | `reproduced.seabed_grid_summary.x_count` |  | 201 | `closeness_to_outstanding` |  |  |  | yes |  |
| 14 | `reproduced.seabed_grid_summary.x_range_nm` |  | 4 | `closeness_to_outstanding` |  |  |  | yes |  |
| 15 | `reproduced.seabed_grid_summary.y_count` |  | 251 | `closeness_to_outstanding` |  |  |  | yes |  |
| 16 | `reproduced.seabed_grid_summary.y_range_nm` |  | 5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 17 | `target_comparison.problem3_last_position_m.actual` |  | 7226.14 | `closeness_to_outstanding` |  |  |  | yes |  |
| 18 | `target_comparison.problem3_line_count.actual` |  | 34 | `closeness_to_outstanding` |  |  |  | yes |  |
| 19 | `target_comparison.problem3_total_length_m.actual` |  | 125936 | `closeness_to_outstanding` |  |  |  | yes |  |
| 20 | `target_comparison.problem4_missed_area_pct.actual` |  | 3.48 | `closeness_to_outstanding` |  |  |  | yes |  |
| 21 | `target_comparison.problem4_total_length_nm.actual` |  | 622 | `closeness_to_outstanding` |  |  |  | yes |  |
## CUMCM 2023 C: `cumcm-2023-c-vegetable-pricing`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 38 total, 38 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.093365864843 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.093365864843
- DeepSeek/Terminus-2 BO-Eval: 0.093365864843

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.category_count` |  | 6 | `closeness_to_outstanding` | 6 | 1 |  | yes |  |
| 2 | `reproduced.cluster_center_comparison[0].avg_daily_sales_kg_actual` |  | 2.52916556634 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 3 | `reproduced.cluster_center_comparison[0].max_daily_sales_kg_actual` |  | 8.89412 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 4 | `reproduced.cluster_center_comparison[0].total_sales_kg_actual` |  | 258.426462857 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 5 | `reproduced.cluster_center_comparison[1].avg_daily_sales_kg_actual` |  | 9.10524135797 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 6 | `reproduced.cluster_center_comparison[1].max_daily_sales_kg_actual` |  | 56.0392826087 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 7 | `reproduced.cluster_center_comparison[1].total_sales_kg_actual` |  | 3149.22293478 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 8 | `reproduced.cluster_center_comparison[2].avg_daily_sales_kg_actual` |  | 20.808494683 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 9 | `reproduced.cluster_center_comparison[2].max_daily_sales_kg_actual` |  | 144.071684211 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 10 | `reproduced.cluster_center_comparison[2].total_sales_kg_actual` |  | 7849.98494737 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 11 | `reproduced.cluster_center_comparison[3].avg_daily_sales_kg_actual` |  | 32.7257670152 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 12 | `reproduced.cluster_center_comparison[3].max_daily_sales_kg_actual` |  | 205.939666667 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 13 | `reproduced.cluster_center_comparison[3].total_sales_kg_actual` |  | 22006.2065 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 14 | `reproduced.correlation_comparison[0].actual_sales_markup_corr` |  | -0.1579 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 15 | `reproduced.correlation_comparison[1].actual_sales_markup_corr` |  | -0.0287 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 16 | `reproduced.correlation_comparison[2].actual_sales_markup_corr` |  | 0.1977 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 17 | `reproduced.correlation_comparison[3].actual_sales_markup_corr` |  | 0.0418 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 18 | `reproduced.correlation_comparison[4].actual_sales_markup_corr` |  | 0.0259 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 19 | `reproduced.correlation_comparison[5].actual_sales_markup_corr` |  | -0.2332 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 20 | `reproduced.future_week_profit_yuan` |  | 5105.6 | `closeness_to_outstanding` | 14616.69 | 0.060518214474 |  | yes |  |
| 21 | `reproduced.item_count` |  | 246 | `closeness_to_outstanding` | 246 | 1 |  | yes |  |
| 22 | `reproduced.july1_profit_yuan` |  | 1282.2631 | `closeness_to_outstanding` | 1748.36 | 0.248192575832 |  | yes |  |
| 23 | `reproduced.regression_comparison[0].actual_intercept` |  | 11.2959 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 24 | `reproduced.regression_comparison[0].actual_slope` |  | -0.041909 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 25 | `reproduced.regression_comparison[1].actual_intercept` |  | 6.3512 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 26 | `reproduced.regression_comparison[1].actual_slope` |  | -0.004092 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 27 | `reproduced.regression_comparison[2].actual_intercept` |  | 10.6597 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 28 | `reproduced.regression_comparison[2].actual_slope` |  | -0.032044 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 29 | `reproduced.regression_comparison[3].actual_intercept` |  | 9.5925 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 30 | `reproduced.regression_comparison[3].actual_slope` |  | -0.036359 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 31 | `reproduced.regression_comparison[4].actual_intercept` |  | 9.6747 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 32 | `reproduced.regression_comparison[4].actual_slope` |  | -0.012185 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 33 | `reproduced.regression_comparison[5].actual_intercept` |  | 9.4799 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 34 | `reproduced.regression_comparison[5].actual_slope` |  | -0.012872 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 35 | `reproduced.selected_item_count` |  | 29 | `closeness_to_outstanding` | 33 | 0.465240641711 |  | yes |  |
| 36 | `target_comparison.future_week_max_profit_yuan.actual` |  | 5105.6 | `closeness_to_outstanding` | 14616.69 | 0.060518214474 |  | yes |  |
| 37 | `target_comparison.problem3_july1_profit_yuan.actual` |  | 1282.2631 | `closeness_to_outstanding` | 1748.36 | 0.248192575832 |  | yes |  |
| 38 | `target_comparison.problem3_selected_item_count.actual` |  | 29 | `closeness_to_outstanding` | 33 | 0.465240641711 |  | yes |  |
## CUMCM 2024 A: `cumcm-2024-a-dragon-dance`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 9 total, 9 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.206349206349 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.206349206349
- DeepSeek/Terminus-2 BO-Eval: 0.206349206349

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q1.handles` |  | 224 | `closeness_to_outstanding` | 224 | 1 |  | yes |  |
| 2 | `experiment_result.q2.terminal_min_margin_m` |  | 0.249958 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 3 | `experiment_result.q2.terminal_time_s` |  | 464 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 4 | `experiment_result.q3.minimum_pitch_m` |  | 0.4 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 5 | `experiment_result.q4.base_ratio_2_to_1_length_m` |  | 14.1372 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 6 | `experiment_result.q4.shortest_candidate_length_m` |  | 14.1372 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 7 | `experiment_result.q4.shortest_candidate_ratio` |  | 1 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 8 | `experiment_result.q5.max_head_speed_mps` |  | 2.00002 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 9 | `experiment_result.q5.max_speed_ratio_when_head_1mps` |  | 0.99999 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
## CUMCM 2024 B: `cumcm-2024-b-production-decision`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 69 total, 69 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.633378428946 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.633378428946
- DeepSeek/Terminus-2 BO-Eval: 0.633378428946

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q1_sampling[0].c` |  | 36 | `closeness_to_outstanding` | 1 | 0.10986775178 |  | yes |  |
| 2 | `experiment_result.q1_sampling[0].false_alarm` |  | 0.046596 | `closeness_to_outstanding` | 0.01 | 0.1325396705 |  | yes |  |
| 3 | `experiment_result.q1_sampling[0].n` |  | 270 | `closeness_to_outstanding` | 2 | 0.107856191744 |  | yes |  |
| 4 | `experiment_result.q1_sampling[0].power` |  | 0.801472 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 5 | `experiment_result.q1_sampling[1].accept_bad` |  | 0.195466 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 6 | `experiment_result.q1_sampling[1].accept_good` |  | 0.903863 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 7 | `experiment_result.q1_sampling[1].c` |  | 25 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 8 | `experiment_result.q1_sampling[1].n` |  | 199 | `closeness_to_outstanding` | 1 | 0.107625743645 |  | yes |  |
| 9 | `experiment_result.q2.best_decisions[0].case` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 10 | `experiment_result.q2.best_decisions[0].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 11 | `experiment_result.q2.best_decisions[0].expected_profit` |  | 26.374 | `closeness_to_outstanding` | 21.6804 | 0.402734371023 |  | yes |  |
| 12 | `experiment_result.q2.best_decisions[0].good_probability` |  | 0.729 | `closeness_to_outstanding` | 0.729 | 1 |  | yes |  |
| 13 | `experiment_result.q2.best_decisions[0].inspect_final` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 14 | `experiment_result.q2.best_decisions[0].inspect_part1` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 15 | `experiment_result.q2.best_decisions[0].inspect_part2` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 16 | `experiment_result.q2.best_decisions[1].case` |  | 2 | `closeness_to_outstanding` | 2 | 1 |  | yes |  |
| 17 | `experiment_result.q2.best_decisions[1].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 18 | `experiment_result.q2.best_decisions[1].expected_profit` |  | 25.072 | `closeness_to_outstanding` | 14.9375 | 0.228913334257 |  | yes |  |
| 19 | `experiment_result.q2.best_decisions[1].good_probability` |  | 0.512 | `closeness_to_outstanding` | 0.64 | 0.324324324324 |  | yes |  |
| 20 | `experiment_result.q2.best_decisions[1].inspect_final` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 21 | `experiment_result.q2.best_decisions[1].inspect_part1` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 22 | `experiment_result.q2.best_decisions[1].inspect_part2` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 23 | `experiment_result.q2.best_decisions[2].case` |  | 3 | `closeness_to_outstanding` | 3 | 1 |  | yes |  |
| 24 | `experiment_result.q2.best_decisions[2].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 25 | `experiment_result.q2.best_decisions[2].expected_profit` |  | 19.87 | `closeness_to_outstanding` | 19.7956 | 0.969741337238 |  | yes |  |
| 26 | `experiment_result.q2.best_decisions[2].good_probability` |  | 0.729 | `closeness_to_outstanding` | 0.729 | 1 |  | yes |  |
| 27 | `experiment_result.q2.best_decisions[2].inspect_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 28 | `experiment_result.q2.best_decisions[2].inspect_part1` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 29 | `experiment_result.q2.best_decisions[2].inspect_part2` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 30 | `experiment_result.q2.best_decisions[3].case` |  | 4 | `closeness_to_outstanding` | 4 | 1 |  | yes |  |
| 31 | `experiment_result.q2.best_decisions[3].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 32 | `experiment_result.q2.best_decisions[3].expected_profit` |  | 14.95 | `closeness_to_outstanding` | 16.4375 | 0.546701203718 |  | yes |  |
| 33 | `experiment_result.q2.best_decisions[3].good_probability` |  | 0.64 | `closeness_to_outstanding` | 0.64 | 1 |  | yes |  |
| 34 | `experiment_result.q2.best_decisions[3].inspect_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 35 | `experiment_result.q2.best_decisions[3].inspect_part1` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 36 | `experiment_result.q2.best_decisions[3].inspect_part2` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 37 | `experiment_result.q2.best_decisions[4].case` |  | 5 | `closeness_to_outstanding` | 5 | 1 |  | yes |  |
| 38 | `experiment_result.q2.best_decisions[4].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 39 | `experiment_result.q2.best_decisions[4].expected_profit` |  | 24.48 | `closeness_to_outstanding` | 18.9383 | 0.346443692286 |  | yes |  |
| 40 | `experiment_result.q2.best_decisions[4].good_probability` |  | 0.648 | `closeness_to_outstanding` | 0.648 | 1 |  | yes |  |
| 41 | `experiment_result.q2.best_decisions[4].inspect_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 42 | `experiment_result.q2.best_decisions[4].inspect_part1` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 43 | `experiment_result.q2.best_decisions[4].inspect_part2` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 44 | `experiment_result.q2.best_decisions[5].case` |  | 6 | `closeness_to_outstanding` | 6 | 1 |  | yes |  |
| 45 | `experiment_result.q2.best_decisions[5].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 46 | `experiment_result.q2.best_decisions[5].expected_profit` |  | 26.5738 | `closeness_to_outstanding` | 19.6343 | 0.314844383432 |  | yes |  |
| 47 | `experiment_result.q2.best_decisions[5].good_probability` |  | 0.85737 | `closeness_to_outstanding` | 0.9025 | 0.695097233783 |  | yes |  |
| 48 | `experiment_result.q2.best_decisions[5].inspect_final` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 49 | `experiment_result.q2.best_decisions[5].inspect_part1` |  | 0 | `closeness_to_outstanding` | 1 | 9.99900009999e-05 |  | yes |  |
| 50 | `experiment_result.q2.best_decisions[5].inspect_part2` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 51 | `experiment_result.q2.best_profit_mean` |  | 22.8866 | `closeness_to_outstanding` | 18.5706 | 0.388875610416 |  | yes |  |
| 52 | `experiment_result.q3.best_expected_profit` |  | 88 | `closeness_to_outstanding` | 85.5556 | 0.81203285042 |  | yes |  |
| 53 | `experiment_result.q3.decision_bits[0]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 54 | `experiment_result.q3.decision_bits[10]` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 55 | `experiment_result.q3.decision_bits[11]` |  | 1 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 56 | `experiment_result.q3.decision_bits[12]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 57 | `experiment_result.q3.decision_bits[13]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 58 | `experiment_result.q3.decision_bits[14]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 59 | `experiment_result.q3.decision_bits[15]` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 60 | `experiment_result.q3.decision_bits[1]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 61 | `experiment_result.q3.decision_bits[2]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 62 | `experiment_result.q3.decision_bits[3]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 63 | `experiment_result.q3.decision_bits[4]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 64 | `experiment_result.q3.decision_bits[5]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 65 | `experiment_result.q3.decision_bits[6]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 66 | `experiment_result.q3.decision_bits[7]` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 67 | `experiment_result.q3.decision_bits[8]` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 68 | `experiment_result.q3.decision_bits[9]` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 69 | `experiment_result.q3.generations` |  | 70 | `closeness_to_outstanding` | 65536 | 0.00012829441736 |  | yes |  |
## CUMCM 2024 C: `cumcm-2024-c-crop-planting`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 20 total, 20 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.207024231145 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.207024231145
- DeepSeek/Terminus-2 BO-Eval: 0.207024231145

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q1.discount_gain_pct` |  | 8.1067954e+18 | `closeness_to_outstanding` | 12.18 | 0.107142857143 |  | yes |  |
| 2 | `experiment_result.q1.discount_profit_yuan` |  | 75678478 | `closeness_to_outstanding` | 74663211.25 | 0.899445526973 |  | yes |  |
| 3 | `experiment_result.q1.waste_profit_yuan` |  | -5389476 | `closeness_to_outstanding` | 66558138.75 | 0.00890891788879 |  | yes |  |
| 4 | `experiment_result.q2_q3.best_correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | 69059695.53 | 0.223269527485 |  | yes |  |
| 5 | `experiment_result.q2_q3.risk_summary[0].correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | 76732995.04 | 0.253838731488 |  | yes |  |
| 6 | `experiment_result.q2_q3.risk_summary[0].cvar10_profit_yuan` |  | 118937552.19 | `closeness_to_outstanding` | 78592899.47 | 0.261319089616 |  | yes |  |
| 7 | `experiment_result.q2_q3.risk_summary[0].deterministic_profit_yuan` |  | -5389476 | `closeness_to_outstanding` | 74663211.25 | 0.00801414787093 |  | yes |  |
| 8 | `experiment_result.q2_q3.risk_summary[0].mean_profit_yuan` |  | 119827636.74 | `closeness_to_outstanding` | 81840993.96 | 0.27459282006 |  | yes |  |
| 9 | `experiment_result.q2_q3.risk_summary[0].q10_profit_yuan` |  | 119159280.66 | `closeness_to_outstanding` | 79051026.67 | 0.262815759919 |  | yes |  |
| 10 | `experiment_result.q2_q3.risk_summary[1].correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | 69059695.53 | 0.223269527485 |  | yes |  |
| 11 | `experiment_result.q2_q3.risk_summary[1].cvar10_profit_yuan` |  | 118937552.19 | `closeness_to_outstanding` | 70733609.52 | 0.228446182627 |  | yes |  |
| 12 | `experiment_result.q2_q3.risk_summary[1].deterministic_profit_yuan` |  | 75678478 | `closeness_to_outstanding` | 67196890.12 | 0.517076504613 |  | yes |  |
| 13 | `experiment_result.q2_q3.risk_summary[1].mean_profit_yuan` |  | 119827636.74 | `closeness_to_outstanding` | 73656894.56 | 0.237478158468 |  | yes |  |
| 14 | `experiment_result.q2_q3.risk_summary[1].q10_profit_yuan` |  | 119159280.66 | `closeness_to_outstanding` | 71145924.01 | 0.229474350859 |  | yes |  |
| 15 | `experiment_result.q2_q3.risk_summary[2].correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 16 | `experiment_result.q2_q3.risk_summary[2].cvar10_profit_yuan` |  | 118937552.19 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 17 | `experiment_result.q2_q3.risk_summary[2].deterministic_profit_yuan` |  | 75678478 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 18 | `experiment_result.q2_q3.risk_summary[2].mean_profit_yuan` |  | 119827636.74 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 19 | `experiment_result.q2_q3.risk_summary[2].q10_profit_yuan` |  | 119159280.66 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 20 | `experiment_result.q2_q3.spearman_price_cost` |  | 0.2551 | `closeness_to_outstanding` | 0.3 | 0.405392520394 |  | yes |  |
## CUMCM 2025 A: `cumcm-2025-a-smoke-screen`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 164 total, 164 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: N/A
- DeepSeek/Terminus-2 BO-Eval: N/A

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q1_duration_s` |  | 1.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 2 | `experiment_result.q2_duration_s` |  | 4.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 3 | `experiment_result.q3_union_duration_s.M1` |  | 6.8 | `closeness_to_outstanding` |  |  |  | yes |  |
| 4 | `experiment_result.q3_union_duration_s.total` |  | 6.8 | `closeness_to_outstanding` |  |  |  | yes |  |
| 5 | `experiment_result.q4_union_duration_s.M1` |  | 8.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 6 | `experiment_result.q4_union_duration_s.total` |  | 8.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 7 | `experiment_result.q5_union_duration_s.M1` |  | 10.3 | `closeness_to_outstanding` |  |  |  | yes |  |
| 8 | `experiment_result.q5_union_duration_s.M2` |  | 6.2 | `closeness_to_outstanding` |  |  |  | yes |  |
| 9 | `experiment_result.q5_union_duration_s.M3` |  | 3.4 | `closeness_to_outstanding` |  |  |  | yes |  |
| 10 | `experiment_result.q5_union_duration_s.total` |  | 19.9 | `closeness_to_outstanding` |  |  |  | yes |  |
| 11 | `q1.effective_duration_s` |  | 1.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 12 | `q1.strategy.drop_time_s` |  | 1.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 13 | `q1.strategy.drop_x` |  | 17620 | `closeness_to_outstanding` |  |  |  | yes |  |
| 14 | `q1.strategy.drop_y` |  | -0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 15 | `q1.strategy.drop_z` |  | 1800 | `closeness_to_outstanding` |  |  |  | yes |  |
| 16 | `q1.strategy.explode_time_s` |  | 5.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 17 | `q1.strategy.explode_x` |  | 17188 | `closeness_to_outstanding` |  |  |  | yes |  |
| 18 | `q1.strategy.explode_y` |  | -0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 19 | `q1.strategy.explode_z` |  | 1736.496 | `closeness_to_outstanding` |  |  |  | yes |  |
| 20 | `q1.strategy.fuse_time_s` |  | 3.6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 21 | `q1.strategy.heading_deg` |  | 180 | `closeness_to_outstanding` |  |  |  | yes |  |
| 22 | `q1.strategy.individual_duration_s` |  | 1.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 23 | `q1.strategy.speed_mps` |  | 120 | `closeness_to_outstanding` |  |  |  | yes |  |
| 24 | `q2.effective_duration_s` |  | 4.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 25 | `q2.strategy.drop_time_s` |  | 0.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 26 | `q2.strategy.drop_x` |  | 17740.004 | `closeness_to_outstanding` |  |  |  | yes |  |
| 27 | `q2.strategy.drop_y` |  | 0.674 | `closeness_to_outstanding` |  |  |  | yes |  |
| 28 | `q2.strategy.drop_z` |  | 1800 | `closeness_to_outstanding` |  |  |  | yes |  |
| 29 | `q2.strategy.explode_time_s` |  | 4.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 30 | `q2.strategy.explode_x` |  | 17308.031 | `closeness_to_outstanding` |  |  |  | yes |  |
| 31 | `q2.strategy.explode_y` |  | 5.528 | `closeness_to_outstanding` |  |  |  | yes |  |
| 32 | `q2.strategy.explode_z` |  | 1736.496 | `closeness_to_outstanding` |  |  |  | yes |  |
| 33 | `q2.strategy.fuse_time_s` |  | 3.6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 34 | `q2.strategy.heading_deg` |  | 179.356 | `closeness_to_outstanding` |  |  |  | yes |  |
| 35 | `q2.strategy.individual_duration_s` |  | 4.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 36 | `q2.strategy.speed_mps` |  | 120 | `closeness_to_outstanding` |  |  |  | yes |  |
| 37 | `q3.strategies[0].drop_time_s` |  | 0.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 38 | `q3.strategies[0].drop_x` |  | 17740.004 | `closeness_to_outstanding` |  |  |  | yes |  |
| 39 | `q3.strategies[0].drop_y` |  | 0.674 | `closeness_to_outstanding` |  |  |  | yes |  |
| 40 | `q3.strategies[0].drop_z` |  | 1800 | `closeness_to_outstanding` |  |  |  | yes |  |
| 41 | `q3.strategies[0].explode_time_s` |  | 4.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 42 | `q3.strategies[0].explode_x` |  | 17308.031 | `closeness_to_outstanding` |  |  |  | yes |  |
| 43 | `q3.strategies[0].explode_y` |  | 5.528 | `closeness_to_outstanding` |  |  |  | yes |  |
| 44 | `q3.strategies[0].explode_z` |  | 1736.496 | `closeness_to_outstanding` |  |  |  | yes |  |
| 45 | `q3.strategies[0].fuse_time_s` |  | 3.6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 46 | `q3.strategies[0].heading_deg` |  | 179.356 | `closeness_to_outstanding` |  |  |  | yes |  |
| 47 | `q3.strategies[0].individual_duration_s` |  | 4.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 48 | `q3.strategies[0].speed_mps` |  | 120 | `closeness_to_outstanding` |  |  |  | yes |  |
| 49 | `q3.strategies[1].drop_time_s` |  | 3 | `closeness_to_outstanding` |  |  |  | yes |  |
| 50 | `q3.strategies[1].drop_x` |  | 17380 | `closeness_to_outstanding` |  |  |  | yes |  |
| 51 | `q3.strategies[1].drop_y` |  | -0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 52 | `q3.strategies[1].drop_z` |  | 1800 | `closeness_to_outstanding` |  |  |  | yes |  |
| 53 | `q3.strategies[1].explode_time_s` |  | 8 | `closeness_to_outstanding` |  |  |  | yes |  |
| 54 | `q3.strategies[1].explode_x` |  | 16680 | `closeness_to_outstanding` |  |  |  | yes |  |
| 55 | `q3.strategies[1].explode_y` |  | -0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 56 | `q3.strategies[1].explode_z` |  | 1677.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 57 | `q3.strategies[1].fuse_time_s` |  | 5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 58 | `q3.strategies[1].heading_deg` |  | 180 | `closeness_to_outstanding` |  |  |  | yes |  |
| 59 | `q3.strategies[1].individual_duration_s` |  | 2.3 | `closeness_to_outstanding` |  |  |  | yes |  |
| 60 | `q3.strategies[1].speed_mps` |  | 140 | `closeness_to_outstanding` |  |  |  | yes |  |
| 61 | `q3.union_duration_s.M1` |  | 6.8 | `closeness_to_outstanding` |  |  |  | yes |  |
| 62 | `q3.union_duration_s.total` |  | 6.8 | `closeness_to_outstanding` |  |  |  | yes |  |
| 63 | `q4.strategies[0].drop_time_s` |  | 0.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 64 | `q4.strategies[0].drop_x` |  | 17740.004 | `closeness_to_outstanding` |  |  |  | yes |  |
| 65 | `q4.strategies[0].drop_y` |  | 0.674 | `closeness_to_outstanding` |  |  |  | yes |  |
| 66 | `q4.strategies[0].drop_z` |  | 1800 | `closeness_to_outstanding` |  |  |  | yes |  |
| 67 | `q4.strategies[0].explode_time_s` |  | 4.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 68 | `q4.strategies[0].explode_x` |  | 17308.031 | `closeness_to_outstanding` |  |  |  | yes |  |
| 69 | `q4.strategies[0].explode_y` |  | 5.528 | `closeness_to_outstanding` |  |  |  | yes |  |
| 70 | `q4.strategies[0].explode_z` |  | 1736.496 | `closeness_to_outstanding` |  |  |  | yes |  |
| 71 | `q4.strategies[0].fuse_time_s` |  | 3.6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 72 | `q4.strategies[0].heading_deg` |  | 179.356 | `closeness_to_outstanding` |  |  |  | yes |  |
| 73 | `q4.strategies[0].individual_duration_s` |  | 4.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 74 | `q4.strategies[0].speed_mps` |  | 120 | `closeness_to_outstanding` |  |  |  | yes |  |
| 75 | `q4.strategies[1].drop_time_s` |  | 31.977 | `closeness_to_outstanding` |  |  |  | yes |  |
| 76 | `q4.strategies[1].drop_x` |  | 2283.971 | `closeness_to_outstanding` |  |  |  | yes |  |
| 77 | `q4.strategies[1].drop_y` |  | -641.153 | `closeness_to_outstanding` |  |  |  | yes |  |
| 78 | `q4.strategies[1].drop_z` |  | 700 | `closeness_to_outstanding` |  |  |  | yes |  |
| 79 | `q4.strategies[1].explode_time_s` |  | 43 | `closeness_to_outstanding` |  |  |  | yes |  |
| 80 | `q4.strategies[1].explode_x` |  | 1002.963 | `closeness_to_outstanding` |  |  |  | yes |  |
| 81 | `q4.strategies[1].explode_y` |  | 172 | `closeness_to_outstanding` |  |  |  | yes |  |
| 82 | `q4.strategies[1].explode_z` |  | 104.596 | `closeness_to_outstanding` |  |  |  | yes |  |
| 83 | `q4.strategies[1].fuse_time_s` |  | 11.023 | `closeness_to_outstanding` |  |  |  | yes |  |
| 84 | `q4.strategies[1].heading_deg` |  | 147.594 | `closeness_to_outstanding` |  |  |  | yes |  |
| 85 | `q4.strategies[1].individual_duration_s` |  | 3.6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 86 | `q4.strategies[1].speed_mps` |  | 137.646 | `closeness_to_outstanding` |  |  |  | yes |  |
| 87 | `q4.union_duration_s.M1` |  | 8.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 88 | `q4.union_duration_s.total` |  | 8.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 89 | `q5.strategies[0].drop_time_s` |  | 32.892 | `closeness_to_outstanding` |  |  |  | yes |  |
| 90 | `q5.strategies[0].drop_x` |  | 2130.79 | `closeness_to_outstanding` |  |  |  | yes |  |
| 91 | `q5.strategies[0].drop_y` |  | -609.343 | `closeness_to_outstanding` |  |  |  | yes |  |
| 92 | `q5.strategies[0].drop_z` |  | 700 | `closeness_to_outstanding` |  |  |  | yes |  |
| 93 | `q5.strategies[0].explode_time_s` |  | 44 | `closeness_to_outstanding` |  |  |  | yes |  |
| 94 | `q5.strategies[0].explode_x` |  | 824.089 | `closeness_to_outstanding` |  |  |  | yes |  |
| 95 | `q5.strategies[0].explode_y` |  | 198.024 | `closeness_to_outstanding` |  |  |  | yes |  |
| 96 | `q5.strategies[0].explode_z` |  | 95.384 | `closeness_to_outstanding` |  |  |  | yes |  |
| 97 | `q5.strategies[0].fuse_time_s` |  | 11.108 | `closeness_to_outstanding` |  |  |  | yes |  |
| 98 | `q5.strategies[0].heading_deg` |  | 148.289 | `closeness_to_outstanding` |  |  |  | yes |  |
| 99 | `q5.strategies[0].individual_duration_s` |  | 3.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 100 | `q5.strategies[0].speed_mps` |  | 138.277 | `closeness_to_outstanding` |  |  |  | yes |  |
| 101 | `q5.strategies[1].drop_time_s` |  | 34.64 | `closeness_to_outstanding` |  |  |  | yes |  |
| 102 | `q5.strategies[1].drop_x` |  | 1933.416 | `closeness_to_outstanding` |  |  |  | yes |  |
| 103 | `q5.strategies[1].drop_y` |  | -626.432 | `closeness_to_outstanding` |  |  |  | yes |  |
| 104 | `q5.strategies[1].drop_z` |  | 700 | `closeness_to_outstanding` |  |  |  | yes |  |
| 105 | `q5.strategies[1].explode_time_s` |  | 46 | `closeness_to_outstanding` |  |  |  | yes |  |
| 106 | `q5.strategies[1].explode_x` |  | 599.729 | `closeness_to_outstanding` |  |  |  | yes |  |
| 107 | `q5.strategies[1].explode_y` |  | 152.009 | `closeness_to_outstanding` |  |  |  | yes |  |
| 108 | `q5.strategies[1].explode_z` |  | 67.605 | `closeness_to_outstanding` |  |  |  | yes |  |
| 109 | `q5.strategies[1].fuse_time_s` |  | 11.36 | `closeness_to_outstanding` |  |  |  | yes |  |
| 110 | `q5.strategies[1].heading_deg` |  | 149.729 | `closeness_to_outstanding` |  |  |  | yes |  |
| 111 | `q5.strategies[1].individual_duration_s` |  | 3.4 | `closeness_to_outstanding` |  |  |  | yes |  |
| 112 | `q5.strategies[1].speed_mps` |  | 135.931 | `closeness_to_outstanding` |  |  |  | yes |  |
| 113 | `q5.strategies[2].drop_time_s` |  | 0.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 114 | `q5.strategies[2].drop_x` |  | 17740.004 | `closeness_to_outstanding` |  |  |  | yes |  |
| 115 | `q5.strategies[2].drop_y` |  | 0.674 | `closeness_to_outstanding` |  |  |  | yes |  |
| 116 | `q5.strategies[2].drop_z` |  | 1800 | `closeness_to_outstanding` |  |  |  | yes |  |
| 117 | `q5.strategies[2].explode_time_s` |  | 4.1 | `closeness_to_outstanding` |  |  |  | yes |  |
| 118 | `q5.strategies[2].explode_x` |  | 17308.031 | `closeness_to_outstanding` |  |  |  | yes |  |
| 119 | `q5.strategies[2].explode_y` |  | 5.528 | `closeness_to_outstanding` |  |  |  | yes |  |
| 120 | `q5.strategies[2].explode_z` |  | 1736.496 | `closeness_to_outstanding` |  |  |  | yes |  |
| 121 | `q5.strategies[2].fuse_time_s` |  | 3.6 | `closeness_to_outstanding` |  |  |  | yes |  |
| 122 | `q5.strategies[2].heading_deg` |  | 179.356 | `closeness_to_outstanding` |  |  |  | yes |  |
| 123 | `q5.strategies[2].individual_duration_s` |  | 4.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 124 | `q5.strategies[2].speed_mps` |  | 120 | `closeness_to_outstanding` |  |  |  | yes |  |
| 125 | `q5.strategies[3].drop_time_s` |  | 23.606 | `closeness_to_outstanding` |  |  |  | yes |  |
| 126 | `q5.strategies[3].drop_x` |  | 3595.615 | `closeness_to_outstanding` |  |  |  | yes |  |
| 127 | `q5.strategies[3].drop_y` |  | -748.142 | `closeness_to_outstanding` |  |  |  | yes |  |
| 128 | `q5.strategies[3].drop_z` |  | 700 | `closeness_to_outstanding` |  |  |  | yes |  |
| 129 | `q5.strategies[3].explode_time_s` |  | 33 | `closeness_to_outstanding` |  |  |  | yes |  |
| 130 | `q5.strategies[3].explode_x` |  | 2638.774 | `closeness_to_outstanding` |  |  |  | yes |  |
| 131 | `q5.strategies[3].explode_y` |  | 148 | `closeness_to_outstanding` |  |  |  | yes |  |
| 132 | `q5.strategies[3].explode_z` |  | 267.577 | `closeness_to_outstanding` |  |  |  | yes |  |
| 133 | `q5.strategies[3].fuse_time_s` |  | 9.394 | `closeness_to_outstanding` |  |  |  | yes |  |
| 134 | `q5.strategies[3].heading_deg` |  | 136.876 | `closeness_to_outstanding` |  |  |  | yes |  |
| 135 | `q5.strategies[3].individual_duration_s` |  | 3.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 136 | `q5.strategies[3].speed_mps` |  | 139.551 | `closeness_to_outstanding` |  |  |  | yes |  |
| 137 | `q5.strategies[4].drop_time_s` |  | 8 | `closeness_to_outstanding` |  |  |  | yes |  |
| 138 | `q5.strategies[4].drop_x` |  | 11079.087 | `closeness_to_outstanding` |  |  |  | yes |  |
| 139 | `q5.strategies[4].drop_y` |  | 835.803 | `closeness_to_outstanding` |  |  |  | yes |  |
| 140 | `q5.strategies[4].drop_z` |  | 1400 | `closeness_to_outstanding` |  |  |  | yes |  |
| 141 | `q5.strategies[4].explode_time_s` |  | 15 | `closeness_to_outstanding` |  |  |  | yes |  |
| 142 | `q5.strategies[4].explode_x` |  | 10273.287 | `closeness_to_outstanding` |  |  |  | yes |  |
| 143 | `q5.strategies[4].explode_y` |  | 342.13 | `closeness_to_outstanding` |  |  |  | yes |  |
| 144 | `q5.strategies[4].explode_z` |  | 1159.9 | `closeness_to_outstanding` |  |  |  | yes |  |
| 145 | `q5.strategies[4].fuse_time_s` |  | 7 | `closeness_to_outstanding` |  |  |  | yes |  |
| 146 | `q5.strategies[4].heading_deg` |  | 211.494 | `closeness_to_outstanding` |  |  |  | yes |  |
| 147 | `q5.strategies[4].individual_duration_s` |  | 2.7 | `closeness_to_outstanding` |  |  |  | yes |  |
| 148 | `q5.strategies[4].speed_mps` |  | 135 | `closeness_to_outstanding` |  |  |  | yes |  |
| 149 | `q5.strategies[5].drop_time_s` |  | 3 | `closeness_to_outstanding` |  |  |  | yes |  |
| 150 | `q5.strategies[5].drop_x` |  | 17380 | `closeness_to_outstanding` |  |  |  | yes |  |
| 151 | `q5.strategies[5].drop_y` |  | -0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 152 | `q5.strategies[5].drop_z` |  | 1800 | `closeness_to_outstanding` |  |  |  | yes |  |
| 153 | `q5.strategies[5].explode_time_s` |  | 8 | `closeness_to_outstanding` |  |  |  | yes |  |
| 154 | `q5.strategies[5].explode_x` |  | 16680 | `closeness_to_outstanding` |  |  |  | yes |  |
| 155 | `q5.strategies[5].explode_y` |  | -0 | `closeness_to_outstanding` |  |  |  | yes |  |
| 156 | `q5.strategies[5].explode_z` |  | 1677.5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 157 | `q5.strategies[5].fuse_time_s` |  | 5 | `closeness_to_outstanding` |  |  |  | yes |  |
| 158 | `q5.strategies[5].heading_deg` |  | 180 | `closeness_to_outstanding` |  |  |  | yes |  |
| 159 | `q5.strategies[5].individual_duration_s` |  | 2.3 | `closeness_to_outstanding` |  |  |  | yes |  |
| 160 | `q5.strategies[5].speed_mps` |  | 140 | `closeness_to_outstanding` |  |  |  | yes |  |
| 161 | `q5.union_duration_s.M1` |  | 10.3 | `closeness_to_outstanding` |  |  |  | yes |  |
| 162 | `q5.union_duration_s.M2` |  | 6.2 | `closeness_to_outstanding` |  |  |  | yes |  |
| 163 | `q5.union_duration_s.M3` |  | 3.4 | `closeness_to_outstanding` |  |  |  | yes |  |
| 164 | `q5.union_duration_s.total` |  | 19.9 | `closeness_to_outstanding` |  |  |  | yes |  |
## CUMCM 2025 B: `cumcm-2025-b-sic-thickness`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 2 total, 2 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.143178654302 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.143178654302
- DeepSeek/Terminus-2 BO-Eval: 0.143178654302

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.si_recommended_thickness_um` |  | 10.5145 | `closeness_to_outstanding` | 4.82505875455 | 0.181514472929 |  | yes |  |
| 2 | `experiment_result.sic_recommended_thickness_um` |  | 8.9815 | `closeness_to_outstanding` | 18.1836785023 | 0.104842835674 |  | yes |  |
## CUMCM 2025 C: `cumcm-2025-c-nipt`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 8 total, 8 effective
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 0.967571343045 (scored)
- DeepSeek/Terminus-2 job reward: 0.524882309574 (scored)
- DeepSeek/Terminus-2 B-Eval: 0.524882309574
- DeepSeek/Terminus-2 BO-Eval: 0.524882309574

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.earliest_recommended_week` |  | 12 | `closeness_to_outstanding` | 12 | 1 |  | yes |  |
| 2 | `experiment_result.female_loo_accuracy` |  | 0.8659 | `closeness_to_outstanding` | 0.9174 | 0.668614228354 |  | yes |  |
| 3 | `experiment_result.latest_recommended_week` |  | 20 | `closeness_to_outstanding` | 22 | 0.545454545455 |  | yes |  |
| 4 | `experiment_result.male_pseudo_r2` |  | 0.90064 | `closeness_to_outstanding` | 0.04413 | 0.112044659952 |  | yes |  |
| 5 | `male_lmm.mother_count` |  | 267 | `closeness_to_outstanding` | 267 | 1 |  | yes |  |
| 6 | `male_lmm.pseudo_r2` |  | 0.90064 | `closeness_to_outstanding` | 0.04413 | 0.112044659952 |  | yes |  |
| 7 | `male_lmm.residual_sigma_logit` |  | 0.47707 | `closeness_to_outstanding` | 0.495318 | 0.758293110665 |  | yes |  |
| 8 | `male_lmm.rmse_fetal_fraction` |  | 0.01056 | `closeness_to_outstanding` | 0.495318 | 0.00260727221551 |  | yes |  |
## MCM 2023 A: `mcm-2023-a-plant-community`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 41 total, 41 effective
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: -0.137723472028
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.beta_decline_pct` |  | 32 | `closeness_to_outstanding` | 7.04 | 0.133333333333 |  | yes |  |
| 2 | `reproduced.coefficient_of_variation_1_to_5[0]` |  | 0.1864 | `closeness_to_outstanding` | 0.1561 | 0.424698108909 |  | yes |  |
| 3 | `reproduced.coefficient_of_variation_1_to_5[1]` |  | 0.0653 | `closeness_to_outstanding` | 0.1392 | 0.0958696290496 |  | yes |  |
| 4 | `reproduced.drought_buffer[0].diversity_buffer_gain_pct` |  | 0 | `closeness_to_outstanding` | 114.93 | 8.70094083273e-07 |  | yes |  |
| 5 | `reproduced.drought_buffer[0].drought_frequency_per_50y` |  | 0 | `closeness_to_outstanding` | 10 | 9.999900001e-06 |  | yes |  |
| 6 | `reproduced.drought_buffer[0].five_species_biomass_index` |  | 1 | `closeness_to_outstanding` | 2.0588 | 0.101798439091 |  | yes |  |
| 7 | `reproduced.drought_buffer[0].monoculture_biomass_index` |  | 1 | `closeness_to_outstanding` | 0.9579 | 0.740283775447 |  | yes |  |
| 8 | `reproduced.drought_buffer[1].diversity_buffer_gain_pct` |  | 7.92 | `closeness_to_outstanding` | 121.63 | 0.00828882508695 |  | yes |  |
| 9 | `reproduced.drought_buffer[1].drought_frequency_per_50y` |  | 3 | `closeness_to_outstanding` | 10 | 0.0489130434783 |  | yes |  |
| 10 | `reproduced.drought_buffer[1].five_species_biomass_index` |  | 0.8992 | `closeness_to_outstanding` | 1.9674 | 0.0917469883616 |  | yes |  |
| 11 | `reproduced.drought_buffer[1].monoculture_biomass_index` |  | 0.82 | `closeness_to_outstanding` | 0.8877 | 0.592414208308 |  | yes |  |
| 12 | `reproduced.drought_buffer[2].diversity_buffer_gain_pct` |  | 14.96 | `closeness_to_outstanding` | 112.8 | 0.0180177286742 |  | yes |  |
| 13 | `reproduced.drought_buffer[2].drought_frequency_per_50y` |  | 6 | `closeness_to_outstanding` | 2 | 0.152542372881 |  | yes |  |
| 14 | `reproduced.drought_buffer[2].five_species_biomass_index` |  | 0.8096 | `closeness_to_outstanding` | 2.1021 | 0.0699110280847 |  | yes |  |
| 15 | `reproduced.drought_buffer[2].monoculture_biomass_index` |  | 0.66 | `closeness_to_outstanding` | 0.9879 | 0.194546794399 |  | yes |  |
| 16 | `reproduced.five_species_pielou_evenness` |  | 0.8826 | `closeness_to_outstanding` | 0.9673 | 0.555641827377 |  | yes |  |
| 17 | `reproduced.optimal_species_count` |  | 2 | `closeness_to_outstanding` | 5 | 0.0740740740741 |  | yes |  |
| 18 | `reproduced.species_count_summary[0].coefficient_of_variation` |  | 0.1864 | `closeness_to_outstanding` | 0.1561 | 0.424698108909 |  | yes |  |
| 19 | `reproduced.species_count_summary[0].mean_total_biomass_last20y` |  | 371.5034 | `closeness_to_outstanding` | 983.46 | 0.0679023534954 |  | yes |  |
| 20 | `reproduced.species_count_summary[0].pielou_evenness` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 21 | `reproduced.species_count_summary[0].species_count` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 22 | `reproduced.species_count_summary[1].coefficient_of_variation` |  | 0.1419 | `closeness_to_outstanding` | 0.1392 | 0.863138686131 |  | yes |  |
| 23 | `reproduced.species_count_summary[1].mean_total_biomass_last20y` |  | 500.0073 | `closeness_to_outstanding` | 1532.16 | 0.054938130789 |  | yes |  |
| 24 | `reproduced.species_count_summary[1].pielou_evenness` |  | 0.958 | `closeness_to_outstanding` | 0.9442 | 0.892823858341 |  | yes |  |
| 25 | `reproduced.species_count_summary[1].species_count` |  | 2 | `closeness_to_outstanding` | 2 | 1 |  | yes |  |
| 26 | `reproduced.species_count_summary[2].coefficient_of_variation` |  | 0.1037 | `closeness_to_outstanding` | 0.1231 | 0.390780052757 |  | yes |  |
| 27 | `reproduced.species_count_summary[2].mean_total_biomass_last20y` |  | 452.1233 | `closeness_to_outstanding` | 1722.07 | 0.0409717072242 |  | yes |  |
| 28 | `reproduced.species_count_summary[2].pielou_evenness` |  | 0.9285 | `closeness_to_outstanding` | 0.9981 | 0.615512098111 |  | yes |  |
| 29 | `reproduced.species_count_summary[2].species_count` |  | 3 | `closeness_to_outstanding` | 3 | 1 |  | yes |  |
| 30 | `reproduced.species_count_summary[3].coefficient_of_variation` |  | 0.0788 | `closeness_to_outstanding` | 0.1136 | 0.213665943601 |  | yes |  |
| 31 | `reproduced.species_count_summary[3].mean_total_biomass_last20y` |  | 394.0814 | `closeness_to_outstanding` | 1851.48 | 0.0314282804371 |  | yes |  |
| 32 | `reproduced.species_count_summary[3].pielou_evenness` |  | 0.9066 | `closeness_to_outstanding` | 0.9939 | 0.554800807784 |  | yes |  |
| 33 | `reproduced.species_count_summary[3].species_count` |  | 4 | `closeness_to_outstanding` | 4 | 1 |  | yes |  |
| 34 | `reproduced.species_count_summary[4].coefficient_of_variation` |  | 0.0653 | `closeness_to_outstanding` | 0.1028 | 0.172842773954 |  | yes |  |
| 35 | `reproduced.species_count_summary[4].mean_total_biomass_last20y` |  | 335.2487 | `closeness_to_outstanding` | 1968.19 | 0.0240440699353 |  | yes |  |
| 36 | `reproduced.species_count_summary[4].pielou_evenness` |  | 0.8826 | `closeness_to_outstanding` | 0.9673 | 0.555641827377 |  | yes |  |
| 37 | `reproduced.species_count_summary[4].species_count` |  | 5 | `closeness_to_outstanding` | 5 | 1 |  | yes |  |
| 38 | `target_comparison.beta_decline_pct.actual` |  | 32 | `closeness_to_outstanding` | 7.04 | 0.133333333333 |  | yes |  |
| 39 | `target_comparison.cov_decrease_1_to_5.actual` |  | 0.1211 | `closeness_to_outstanding` | [0.1561, 0.1392, 0.1231, 0.1136, 0.1028] | 0 |  | yes |  |
| 40 | `target_comparison.five_species_pielou_evenness.actual` |  | 0.8826 | `closeness_to_outstanding` | 0.9673 | 0.555641827377 |  | yes |  |
| 41 | `target_comparison.optimal_species_count.actual` |  | 2 | `closeness_to_outstanding` | 5 | 0.0740740740741 |  | yes |  |
## MCM 2023 B: `mcm-2023-b-maasai-mara`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 11 total, 11 effective
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.570725974269
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.best_scenario_benefit_million` |  | 154948.974 | `closeness_to_outstanding` | 117.86 | 0.107215671661 |  | yes |  |
| 2 | `reproduced.mean_sanctuary_to_tourism_interaction_distance` |  | 2.7376 | `closeness_to_outstanding` | 9.3093 | 0.0476089720142 |  | yes |  |
| 3 | `reproduced.scenario2_counts.agricultural_area` |  | 12 | `closeness_to_outstanding` | 100 | 0.0161001788909 |  | yes |  |
| 4 | `reproduced.scenario2_counts.hunting_area` |  | 2 | `closeness_to_outstanding` | 40 | 0.00627615062762 |  | yes |  |
| 5 | `reproduced.scenario2_counts.tourism_area` |  | 9 | `closeness_to_outstanding` | 100 | 0.011728931364 |  | yes |  |
| 6 | `reproduced.scenario2_counts.wildlife_sanctuary` |  | 13 | `closeness_to_outstanding` | 160 | 0.0105008077544 |  | yes |  |
| 7 | `target_comparison.scenario2_agriculture_cells.actual` |  | 12 | `closeness_to_outstanding` | 100 | 0.0161001788909 |  | yes |  |
| 8 | `target_comparison.scenario2_benefit_million.actual` |  | 154948.974 | `closeness_to_outstanding` | 104.24 | 0.107207252097 |  | yes |  |
| 9 | `target_comparison.scenario2_hunting_cells.actual` |  | 2 | `closeness_to_outstanding` | 40 | 0.00627615062762 |  | yes |  |
| 10 | `target_comparison.scenario2_tourism_cells.actual` |  | 9 | `closeness_to_outstanding` | 100 | 0.011728931364 |  | yes |  |
| 11 | `target_comparison.scenario2_wildlife_cells.actual` |  | 13 | `closeness_to_outstanding` | 160 | 0.0105008077544 |  | yes |  |
## MCM 2023 C: `mcm-2023-c-wordle`

- Scoring status: v4 endpoint target-minmax
- Default eval method: `B-Eval`
- Metrics: 23 total, 17 effective
- Baseline endpoint: `question_result_minmax_endpoint`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.143159490288 (scored)
- DeepSeek/Terminus-2 B-Eval: 0.143159490288
- DeepSeek/Terminus-2 BO-Eval: 0.143159490288

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.best_tree_holdout_accuracy` | 0.422222 | 1 | `higher_is_better` | 0.3211 | 0 | -0.101122 | yes | difficulty_model.holdout_accuracy |
| 2 | `reproduced.calibrated_lightgbm_like_accuracy` | 0.422222 | 0.7 | `higher_is_better` | 0.3211 | 0 | -0.101122 | yes | difficulty_model.holdout_accuracy |
| 3 | `reproduced.difficulty_metrics[0].holdout_accuracy` | 0.422222 | 1 | `higher_is_better` | 0.3211 | 0 | -0.101122 | yes | difficulty_model.holdout_accuracy |
| 4 | `reproduced.difficulty_metrics[0].train_accuracy` |  | 1 | `unscored_missing_baseline` | 0.4011 | 0 |  | no |  |
| 5 | `reproduced.difficulty_metrics[1].holdout_accuracy` | 0.422222 | 1 | `higher_is_better` |  | 0 |  | yes | difficulty_model.holdout_accuracy |
| 6 | `reproduced.difficulty_metrics[1].train_accuracy` |  | 1 | `unscored_missing_baseline` |  | 0 |  | no |  |
| 7 | `reproduced.eerie.difficulty_group` | 2 | 2 | `exact_value` | 3 | 0 |  | no | difficulty_model.eerie_classifier_class |
| 8 | `reproduced.eerie.paper_aligned_distribution_pct[0]` | 0.245 | 0.649 | `higher_is_better` | 0.3 | 0.136138613861 | 0.055 | yes | eerie_prediction.predicted_distribution_percent.1 try |
| 9 | `reproduced.eerie.paper_aligned_distribution_pct[1]` | 7.01 | 7.5792 | `higher_is_better` | 4.7 | 0 | -2.31 | yes | eerie_prediction.predicted_distribution_percent.2 tries |
| 10 | `reproduced.eerie.paper_aligned_distribution_pct[2]` | 22.062 | 26.2985 | `higher_is_better` | 19.4 | 0 | -2.662 | yes | eerie_prediction.predicted_distribution_percent.3 tries |
| 11 | `reproduced.eerie.paper_aligned_distribution_pct[3]` | 30.668 | 32.6147 | `higher_is_better` | 33.4 | 0.596599373298 | 2.732 | yes | eerie_prediction.predicted_distribution_percent.4 tries |
| 12 | `reproduced.eerie.paper_aligned_distribution_pct[4]` | 22.491 | 20.9304 | `lower_is_better` | 27 | 0 | -4.509 | yes | eerie_prediction.predicted_distribution_percent.5 tries |
| 13 | `reproduced.eerie.paper_aligned_distribution_pct[5]` | 11.839 | 9.6302 | `lower_is_better` | 13 | 0 | -1.161 | yes | eerie_prediction.predicted_distribution_percent.6 tries |
| 14 | `reproduced.eerie.paper_aligned_distribution_pct[6]` | 5.685 | 2.298 | `lower_is_better` | 2.3 | 0.999409506938 | 3.385 | yes | eerie_prediction.predicted_distribution_percent.7 or more tries (X) |
| 15 | `reproduced.forecast_record.horizon_days` | 60 | 60 | `exact_value` | 60 | 0 |  | no | data_source.date_max -> report_count_model.prediction_date |
| 16 | `reproduced.forecast_record.raw_80_lower` | 20365 | 0 | `lower_is_better` | 6250 | 0.693100908421 | 14115 | yes | report_count_model.prediction_interval_80[0] |
| 17 | `reproduced.forecast_record.raw_80_upper` | 30713 | 59621.565 | `higher_is_better` | 13522 | 0 | -17191 | yes | report_count_model.prediction_interval_80[1] |
| 18 | `reproduced.forecast_record.raw_ma_forecast` | 23612 | 16662.852 | `lower_is_better` | 9193 | 0 | 14419 | yes | report_count_model.predicted_reported_results |
| 19 | `target_comparison.eerie_distribution_sum_pct.actual` | 100 | 100 | `exact_value` | 100 | 0 |  | no | eerie_prediction.predicted_distribution_percent |
| 20 | `target_comparison.eerie_group.actual` | 2 | 2 | `exact_value` | 3 | 0 |  | no | difficulty_model.eerie_classifier_class |
| 21 | `target_comparison.forecast_lower.actual` | 20365 | 10139.23 | `lower_is_better` | 0 | 0.00846293237575 | 20365 | yes | report_count_model.prediction_interval_80[0] |
| 22 | `target_comparison.forecast_upper.actual` | 30713 | 30808.07 | `higher_is_better` | 0 | 0 | -30713 | yes | report_count_model.prediction_interval_80[1] |
| 23 | `target_comparison.lightgbm_like_accuracy.actual` | 0.422222 | 0.7 | `higher_is_better` | 0.3211 | 0 | -0.101122 | yes | difficulty_model.holdout_accuracy |
## MCM 2024 A: `mcm-2024-a-lamprey`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 105 total, 105 effective
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.24548365989
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.adaptive_vs_fixed[0].adaptive_gain_pct` |  | 3.26 | `closeness_to_outstanding` | -0.1 | 0.104286628279 |  | yes |  |
| 2 | `experiment_result.adaptive_vs_fixed[0].adaptive_stability` |  | 0.9144 | `closeness_to_outstanding` | 0.3841 | 0.171442499391 |  | yes |  |
| 3 | `experiment_result.adaptive_vs_fixed[0].fixed_stability` |  | 0.8855 | `closeness_to_outstanding` | 0.3845 | 0.174982709218 |  | yes |  |
| 4 | `experiment_result.adaptive_vs_fixed[1].adaptive_gain_pct` |  | 1.04 | `closeness_to_outstanding` | -0.66 | 0.0683910565541 |  | yes |  |
| 5 | `experiment_result.adaptive_vs_fixed[1].adaptive_stability` |  | 0.8824 | `closeness_to_outstanding` | 0.3137 | 0.156966919068 |  | yes |  |
| 6 | `experiment_result.adaptive_vs_fixed[1].fixed_stability` |  | 0.8733 | `closeness_to_outstanding` | 0.3158 | 0.158231364828 |  | yes |  |
| 7 | `experiment_result.adaptive_vs_fixed[2].adaptive_gain_pct` |  | 0.31 | `closeness_to_outstanding` | 22.04 | 0.00170899334779 |  | yes |  |
| 8 | `experiment_result.adaptive_vs_fixed[2].adaptive_stability` |  | 0.8659 | `closeness_to_outstanding` | 0.4839 | 0.213842949694 |  | yes |  |
| 9 | `experiment_result.adaptive_vs_fixed[2].fixed_stability` |  | 0.8632 | `closeness_to_outstanding` | 0.3965 | 0.181635816541 |  | yes |  |
| 10 | `experiment_result.adaptive_vs_fixed[3].adaptive_gain_pct` |  | 3.08 | `closeness_to_outstanding` | 0.95 | 0.147863658185 |  | yes |  |
| 11 | `experiment_result.adaptive_vs_fixed[3].adaptive_stability` |  | 0.8566 | `closeness_to_outstanding` | 0.3612 | 0.171837804584 |  | yes |  |
| 12 | `experiment_result.adaptive_vs_fixed[3].fixed_stability` |  | 0.831 | `closeness_to_outstanding` | 0.3578 | 0.174055714585 |  | yes |  |
| 13 | `experiment_result.largest_stability_gain.adaptive_gain_pct` |  | 3.26 | `closeness_to_outstanding` | 22.04 | 0.0204056084126 |  | yes |  |
| 14 | `experiment_result.largest_stability_gain.adaptive_stability` |  | 0.9144 | `closeness_to_outstanding` | 0.4839 | 0.203114240654 |  | yes |  |
| 15 | `experiment_result.largest_stability_gain.fixed_stability` |  | 0.8855 | `closeness_to_outstanding` | 0.3965 | 0.178510230824 |  | yes |  |
| 16 | `experiment_result.parasite_coexistence_case.final_parasite_index` |  | 8.562 | `closeness_to_outstanding` | 0.3124 | 0.110750842941 |  | yes |  |
| 17 | `experiment_result.parasite_coexistence_case.host_fish_index` |  | 1080.356 | `closeness_to_outstanding` | 0.5981 | 0.107195843839 |  | yes |  |
| 18 | `experiment_result.scenario_summary[0].composite_stability` |  | 0.8855 | `closeness_to_outstanding` | 0.3841 | 0.174867524603 |  | yes |  |
| 19 | `experiment_result.scenario_summary[0].final_host_fish` |  | 1052.013 | `closeness_to_outstanding` | 432 | 0.169166885895 |  | yes |  |
| 20 | `experiment_result.scenario_summary[0].final_lamprey` |  | 2079.718 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 21 | `experiment_result.scenario_summary[0].final_parasite` |  | 5.506 | `closeness_to_outstanding` | 120 | 0.00573767189048 |  | yes |  |
| 22 | `experiment_result.scenario_summary[0].mean_biomass` |  | 3187.261 | `closeness_to_outstanding` | 552 | 0.126741300898 |  | yes |  |
| 23 | `experiment_result.scenario_summary[0].normalized_diversity` |  | 0.8213 | `closeness_to_outstanding` | 0.4766 | 0.222345552006 |  | yes |  |
| 24 | `experiment_result.scenario_summary[0].resilience` |  | 0.8693 | `closeness_to_outstanding` | 0.1595 | 0.12813407426 |  | yes |  |
| 25 | `experiment_result.scenario_summary[0].resistance` |  | 0.8979 | `closeness_to_outstanding` | 0.6436 | 0.297606947145 |  | yes |  |
| 26 | `experiment_result.scenario_summary[0].shannon_diversity` |  | 1.4715 | `closeness_to_outstanding` | 0.5236 | 0.15703258395 |  | yes |  |
| 27 | `experiment_result.scenario_summary[0].species_persistence` |  | 1 | `closeness_to_outstanding` | 0.6667 | 0.264725347452 |  | yes |  |
| 28 | `experiment_result.scenario_summary[0].sustainability` |  | 1 | `closeness_to_outstanding` | 0.552 | 0.211267605634 |  | yes |  |
| 29 | `experiment_result.scenario_summary[1].composite_stability` |  | 0.9144 | `closeness_to_outstanding` | 0.3845 | 0.171549713271 |  | yes |  |
| 30 | `experiment_result.scenario_summary[1].final_host_fish` |  | 1163.941 | `closeness_to_outstanding` | 432 | 0.160246316397 |  | yes |  |
| 31 | `experiment_result.scenario_summary[1].final_lamprey` |  | 1262.576 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 32 | `experiment_result.scenario_summary[1].final_parasite` |  | 38.764 | `closeness_to_outstanding` | 120 | 0.0541600378541 |  | yes |  |
| 33 | `experiment_result.scenario_summary[1].mean_biomass` |  | 2482.149 | `closeness_to_outstanding` | 552 | 0.13368804319 |  | yes |  |
| 34 | `experiment_result.scenario_summary[1].normalized_diversity` |  | 0.7913 | `closeness_to_outstanding` | 0.4766 | 0.231794481223 |  | yes |  |
| 35 | `experiment_result.scenario_summary[1].resilience` |  | 0.9732 | `closeness_to_outstanding` | 0.1601 | 0.12558985852 |  | yes |  |
| 36 | `experiment_result.scenario_summary[1].resistance` |  | 0.9155 | `closeness_to_outstanding` | 0.6431 | 0.287396013185 |  | yes |  |
| 37 | `experiment_result.scenario_summary[1].shannon_diversity` |  | 1.4177 | `closeness_to_outstanding` | 0.5236 | 0.15985732327 |  | yes |  |
| 38 | `experiment_result.scenario_summary[1].species_persistence` |  | 1 | `closeness_to_outstanding` | 0.6667 | 0.264725347452 |  | yes |  |
| 39 | `experiment_result.scenario_summary[1].sustainability` |  | 1 | `closeness_to_outstanding` | 0.552 | 0.211267605634 |  | yes |  |
| 40 | `experiment_result.scenario_summary[2].composite_stability` |  | 0.8733 | `closeness_to_outstanding` | 0.3137 | 0.157731232578 |  | yes |  |
| 41 | `experiment_result.scenario_summary[2].final_host_fish` |  | 987.127 | `closeness_to_outstanding` | 431.37 | 0.17569428879 |  | yes |  |
| 42 | `experiment_result.scenario_summary[2].final_lamprey` |  | 2588.436 | `closeness_to_outstanding` | 0.09 | 0.107146183461 |  | yes |  |
| 43 | `experiment_result.scenario_summary[2].final_parasite` |  | 1.737 | `closeness_to_outstanding` | 120 | 0.00175941138219 |  | yes |  |
| 44 | `experiment_result.scenario_summary[2].mean_biomass` |  | 3646.292 | `closeness_to_outstanding` | 550.52 | 0.123836552645 |  | yes |  |
| 45 | `experiment_result.scenario_summary[2].normalized_diversity` |  | 0.8169 | `closeness_to_outstanding` | 0.4783 | 0.22451148346 |  | yes |  |
| 46 | `experiment_result.scenario_summary[2].resilience` |  | 0.8536 | `closeness_to_outstanding` | 0.067 | 0.115217449991 |  | yes |  |
| 47 | `experiment_result.scenario_summary[2].resistance` |  | 0.8768 | `closeness_to_outstanding` | 0.8353 | 0.717140598162 |  | yes |  |
| 48 | `experiment_result.scenario_summary[2].shannon_diversity` |  | 1.4637 | `closeness_to_outstanding` | 0.5254 | 0.157677585229 |  | yes |  |
| 49 | `experiment_result.scenario_summary[2].species_persistence` |  | 1 | `closeness_to_outstanding` | 0.6667 | 0.264725347452 |  | yes |  |
| 50 | `experiment_result.scenario_summary[2].sustainability` |  | 1 | `closeness_to_outstanding` | 0.5515 | 0.211081794195 |  | yes |  |
| 51 | `experiment_result.scenario_summary[3].composite_stability` |  | 0.8824 | `closeness_to_outstanding` | 0.3158 | 0.157457084736 |  | yes |  |
| 52 | `experiment_result.scenario_summary[3].final_host_fish` |  | 1080.356 | `closeness_to_outstanding` | 431.63 | 0.166556950027 |  | yes |  |
| 53 | `experiment_result.scenario_summary[3].final_lamprey` |  | 1900.454 | `closeness_to_outstanding` | 0.05 | 0.107145374055 |  | yes |  |
| 54 | `experiment_result.scenario_summary[3].final_parasite` |  | 8.562 | `closeness_to_outstanding` | 120 | 0.0091356064583 |  | yes |  |
| 55 | `experiment_result.scenario_summary[3].mean_biomass` |  | 3041.299 | `closeness_to_outstanding` | 550.98 | 0.127818124467 |  | yes |  |
| 56 | `experiment_result.scenario_summary[3].normalized_diversity` |  | 0.8077 | `closeness_to_outstanding` | 0.4776 | 0.226975532991 |  | yes |  |
| 57 | `experiment_result.scenario_summary[3].resilience` |  | 0.8953 | `closeness_to_outstanding` | 0.0695 | 0.115122005581 |  | yes |  |
| 58 | `experiment_result.scenario_summary[3].resistance` |  | 0.873 | `closeness_to_outstanding` | 0.8209 | 0.667856687492 |  | yes |  |
| 59 | `experiment_result.scenario_summary[3].shannon_diversity` |  | 1.4471 | `closeness_to_outstanding` | 0.5247 | 0.158434088894 |  | yes |  |
| 60 | `experiment_result.scenario_summary[3].species_persistence` |  | 1 | `closeness_to_outstanding` | 0.6667 | 0.264725347452 |  | yes |  |
| 61 | `experiment_result.scenario_summary[3].sustainability` |  | 1 | `closeness_to_outstanding` | 0.5517 | 0.211156079535 |  | yes |  |
| 62 | `experiment_result.scenario_summary[4].composite_stability` |  | 0.8632 | `closeness_to_outstanding` | 0.4839 | 0.214511145534 |  | yes |  |
| 63 | `experiment_result.scenario_summary[4].final_host_fish` |  | 930.367 | `closeness_to_outstanding` | 298.38 | 0.150133646923 |  | yes |  |
| 64 | `experiment_result.scenario_summary[4].final_lamprey` |  | 3056.291 | `closeness_to_outstanding` | 13.46 | 0.107565824298 |  | yes |  |
| 65 | `experiment_result.scenario_summary[4].final_parasite` |  | 0.616 | `closeness_to_outstanding` | 120 | 0.000618795304656 |  | yes |  |
| 66 | `experiment_result.scenario_summary[4].mean_biomass` |  | 4074.932 | `closeness_to_outstanding` | 431.83 | 0.118339964903 |  | yes |  |
| 67 | `experiment_result.scenario_summary[4].normalized_diversity` |  | 0.8076 | `closeness_to_outstanding` | 0.6548 | 0.388095085539 |  | yes |  |
| 68 | `experiment_result.scenario_summary[4].resilience` |  | 0.8431 | `closeness_to_outstanding` | 0.2624 | 0.148373888354 |  | yes |  |
| 69 | `experiment_result.scenario_summary[4].resistance` |  | 0.8612 | `closeness_to_outstanding` | 1 | 0.426787366195 |  | yes |  |
| 70 | `experiment_result.scenario_summary[4].shannon_diversity` |  | 1.4471 | `closeness_to_outstanding` | 0.7194 | 0.19265725266 |  | yes |  |
| 71 | `experiment_result.scenario_summary[4].species_persistence` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 72 | `experiment_result.scenario_summary[4].sustainability` |  | 1 | `closeness_to_outstanding` | 0.4318 | 0.174367916303 |  | yes |  |
| 73 | `experiment_result.scenario_summary[5].composite_stability` |  | 0.8659 | `closeness_to_outstanding` | 0.3965 | 0.181242892128 |  | yes |  |
| 74 | `experiment_result.scenario_summary[5].final_host_fish` |  | 1007.488 | `closeness_to_outstanding` | 303.83 | 0.146622519139 |  | yes |  |
| 75 | `experiment_result.scenario_summary[5].final_lamprey` |  | 2469.707 | `closeness_to_outstanding` | 12.91 | 0.107645266506 |  | yes |  |
| 76 | `experiment_result.scenario_summary[5].final_parasite` |  | 2.354 | `closeness_to_outstanding` | 120 | 0.00239535013086 |  | yes |  |
| 77 | `experiment_result.scenario_summary[5].mean_biomass` |  | 3554.691 | `closeness_to_outstanding` | 436.77 | 0.120345565004 |  | yes |  |
| 78 | `experiment_result.scenario_summary[5].normalized_diversity` |  | 0.8073 | `closeness_to_outstanding` | 0.6476 | 0.377572337241 |  | yes |  |
| 79 | `experiment_result.scenario_summary[5].resilience` |  | 0.8628 | `closeness_to_outstanding` | 0.1428 | 0.125721279944 |  | yes |  |
| 80 | `experiment_result.scenario_summary[5].resistance` |  | 0.8507 | `closeness_to_outstanding` | 0.9999 | 0.406249502555 |  | yes |  |
| 81 | `experiment_result.scenario_summary[5].shannon_diversity` |  | 1.4465 | `closeness_to_outstanding` | 0.7115 | 0.191045367497 |  | yes |  |
| 82 | `experiment_result.scenario_summary[5].species_persistence` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 83 | `experiment_result.scenario_summary[5].sustainability` |  | 1 | `closeness_to_outstanding` | 0.4367 | 0.175618322845 |  | yes |  |
| 84 | `experiment_result.scenario_summary[6].composite_stability` |  | 0.831 | `closeness_to_outstanding` | 0.3612 | 0.175094816688 |  | yes |  |
| 85 | `experiment_result.scenario_summary[6].final_host_fish` |  | 892.229 | `closeness_to_outstanding` | 180.88 | 0.130822732211 |  | yes |  |
| 86 | `experiment_result.scenario_summary[6].final_lamprey` |  | 3383.705 | `closeness_to_outstanding` | 18.19 | 0.107659600554 |  | yes |  |
| 87 | `experiment_result.scenario_summary[6].final_parasite` |  | 0.302 | `closeness_to_outstanding` | 120 | 0.000302670313855 |  | yes |  |
| 88 | `experiment_result.scenario_summary[6].mean_biomass` |  | 4378.203 | `closeness_to_outstanding` | 319.01 | 0.114598210204 |  | yes |  |
| 89 | `experiment_result.scenario_summary[6].normalized_diversity` |  | 0.7992 | `closeness_to_outstanding` | 0.7763 | 0.807245547288 |  | yes |  |
| 90 | `experiment_result.scenario_summary[6].resilience` |  | 0.8381 | `closeness_to_outstanding` | 0.1481 | 0.127214219578 |  | yes |  |
| 91 | `experiment_result.scenario_summary[6].resistance` |  | 0.8493 | `closeness_to_outstanding` | 0.9974 | 0.407637911174 |  | yes |  |
| 92 | `experiment_result.scenario_summary[6].shannon_diversity` |  | 1.4321 | `closeness_to_outstanding` | 0.8529 | 0.228815048758 |  | yes |  |
| 93 | `experiment_result.scenario_summary[6].species_persistence` |  | 0.8333 | `closeness_to_outstanding` | 1 | 0.374943756187 |  | yes |  |
| 94 | `experiment_result.scenario_summary[6].sustainability` |  | 0.8333 | `closeness_to_outstanding` | 0.3191 | 0.162807963582 |  | yes |  |
| 95 | `experiment_result.scenario_summary[7].composite_stability` |  | 0.8566 | `closeness_to_outstanding` | 0.3578 | 0.170866633865 |  | yes |  |
| 96 | `experiment_result.scenario_summary[7].final_host_fish` |  | 959.411 | `closeness_to_outstanding` | 179.55 | 0.128637503029 |  | yes |  |
| 97 | `experiment_result.scenario_summary[7].final_lamprey` |  | 2862.114 | `closeness_to_outstanding` | 18.29 | 0.107757689942 |  | yes |  |
| 98 | `experiment_result.scenario_summary[7].final_parasite` |  | 0.999 | `closeness_to_outstanding` | 120 | 0.0010063726863 |  | yes |  |
| 99 | `experiment_result.scenario_summary[7].mean_biomass` |  | 3910.166 | `closeness_to_outstanding` | 317.79 | 0.115525997475 |  | yes |  |
| 100 | `experiment_result.scenario_summary[7].normalized_diversity` |  | 0.8019 | `closeness_to_outstanding` | 0.778 | 0.801045551412 |  | yes |  |
| 101 | `experiment_result.scenario_summary[7].resilience` |  | 0.8513 | `closeness_to_outstanding` | 0.1445 | 0.126281281059 |  | yes |  |
| 102 | `experiment_result.scenario_summary[7].resistance` |  | 0.8358 | `closeness_to_outstanding` | 0.9971 | 0.383400357804 |  | yes |  |
| 103 | `experiment_result.scenario_summary[7].shannon_diversity` |  | 1.4369 | `closeness_to_outstanding` | 0.8547 | 0.228494039447 |  | yes |  |
| 104 | `experiment_result.scenario_summary[7].species_persistence` |  | 1 | `closeness_to_outstanding` | 1 | 1 |  | yes |  |
| 105 | `experiment_result.scenario_summary[7].sustainability` |  | 1 | `closeness_to_outstanding` | 0.3178 | 0.149588631264 |  | yes |  |
## MCM 2024 B: `mcm-2024-b-submersible-search`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 13 total, 13 effective
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.437625067352
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.caribbean_adaptation.current_multiplier` |  | 1.35 | `closeness_to_outstanding` | 2 | 0.199507389163 |  | yes |  |
| 2 | `experiment_result.caribbean_adaptation.terrain_uncertainty_multiplier` |  | 1.2 | `closeness_to_outstanding` | 2 | 0.152542372881 |  | yes |  |
| 3 | `experiment_result.equipment_selection.top_score` |  | 0.8357 | `closeness_to_outstanding` | 7.3 | 0.0152765201877 |  | yes |  |
| 4 | `experiment_result.location_model.final_mean_x_m` |  | 7698.65 | `closeness_to_outstanding` | 6467.92 | 0.428781082797 |  | yes |  |
| 5 | `experiment_result.location_model.final_mean_y_m` |  | -2324.78 | `closeness_to_outstanding` | -8.09 | 0.107476793218 |  | yes |  |
| 6 | `experiment_result.location_model.final_p95_area_km2` |  | 0.9722 | `closeness_to_outstanding` | 29.47 | 0.00407709891054 |  | yes |  |
| 7 | `experiment_result.search_strategy.calibrated_detection_multiplier` |  | 0.8557 | `closeness_to_outstanding` | 1.3236 | 0.179962985292 |  | yes |  |
| 8 | `experiment_result.search_strategy.find_probability_10h_start_1h` |  | 0.43 | `closeness_to_outstanding` | 0.6412 | 0.196347031963 |  | yes |  |
| 9 | `experiment_result.search_strategy.find_probability_10h_start_3h` |  | 0.2338 | `closeness_to_outstanding` | 0.4153 | 0.133883067056 |  | yes |  |
| 10 | `experiment_result.search_strategy.find_probability_10h_start_5h` |  | 0.1158 | `closeness_to_outstanding` | 0.2488 | 0.0945975383945 |  | yes |  |
| 11 | `experiment_result.search_strategy.find_probability_18h` |  | 0.4377 | `closeness_to_outstanding` | 0.936 | 0.0953553222082 |  | yes |  |
| 12 | `experiment_result.search_strategy.find_probability_6h` |  | 0.4068 | `closeness_to_outstanding` | 0.6 | 0.201705672352 |  | yes |  |
| 13 | `experiment_result.search_strategy.searched_cells` |  | 18 | `closeness_to_outstanding` | 108 | 0.0234375 |  | yes |  |
## MCM 2024 C: `mcm-2024-c-tennis-momentum`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 22 total, 22 effective
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.508413940348
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.dual_temporal_bayes.final_match_warning_rate` |  | 0.006 | `closeness_to_outstanding` | 0.9632 | 0.000751628528478 |  | yes |  |
| 2 | `experiment_result.dual_temporal_bayes.strongest_transition.probability` |  | 0.6726 | `closeness_to_outstanding` | 0.3947 | 0.225067761257 |  | yes |  |
| 3 | `experiment_result.dual_temporal_bayes.swing_warning_rate` |  | 0.0032 | `closeness_to_outstanding` | 0.9632 | 0.000399840063974 |  | yes |  |
| 4 | `experiment_result.momentum_model.final_momentum_range` |  | 0.7895 | `closeness_to_outstanding` | 0.7212 | 0.581084396467 |  | yes |  |
| 5 | `experiment_result.randomness_tests.matches_rejecting_iid_at_5pct` |  | 0 | `closeness_to_outstanding` | 31 | 3.22579604582e-06 |  | yes |  |
| 6 | `experiment_result.randomness_tests.median_ljung_box_p` |  | 0.712832 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 7 | `experiment_result.randomness_tests.median_runs_p` |  | 0.290172 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 8 | `experiment_result.top_swing_features[0].mean_otherwise` |  | 0.1257 | `closeness_to_outstanding` | -0.1124 | 0.0595772244692 |  | yes |  |
| 9 | `experiment_result.top_swing_features[0].mean_when_warning` |  | 0.3043 | `closeness_to_outstanding` | 0.1821 | 0.230071322362 |  | yes |  |
| 10 | `experiment_result.top_swing_features[0].warning_correlation` |  | 0.0302 | `closeness_to_outstanding` | 0.1074 | 0.0448381668811 |  | yes |  |
| 11 | `experiment_result.top_swing_features[1].mean_otherwise` |  | 0.1363 | `closeness_to_outstanding` | -0.1208 | 0.0598121818501 |  | yes |  |
| 12 | `experiment_result.top_swing_features[1].mean_when_warning` |  | 0 | `closeness_to_outstanding` | -0.0073 | 0.0135135135135 |  | yes |  |
| 13 | `experiment_result.top_swing_features[1].warning_correlation` |  | -0.0223 | `closeness_to_outstanding` | 0.0809 | 0.0252748498243 |  | yes |  |
| 14 | `experiment_result.top_swing_features[2].mean_otherwise` |  | 100.773 | `closeness_to_outstanding` | 0.0728 | 0.107212010395 |  | yes |  |
| 15 | `experiment_result.top_swing_features[2].mean_when_warning` |  | 110.7391 | `closeness_to_outstanding` | -0.0301 | 0.107116861215 |  | yes |  |
| 16 | `experiment_result.top_swing_features[2].warning_correlation` |  | 0.0154 | `closeness_to_outstanding` | 0.051 | 0.0493484298227 |  | yes |  |
| 17 | `experiment_result.top_swing_features[3].mean_otherwise` |  | 0.1719 | `closeness_to_outstanding` | 1.5 | 0.0152944107337 |  | yes |  |
| 18 | `experiment_result.top_swing_features[3].mean_when_warning` |  | 0.087 | `closeness_to_outstanding` | 1.546 | 0.00710474738676 |  | yes |  |
| 19 | `experiment_result.top_swing_features[3].warning_correlation` |  | -0.0126 | `closeness_to_outstanding` | 0.046 | 0.0251530476444 |  | yes |  |
| 20 | `experiment_result.top_swing_features[4].mean_otherwise` |  | 0.0313 | `closeness_to_outstanding` | 1.52 | 0.00251665710748 |  | yes |  |
| 21 | `experiment_result.top_swing_features[4].mean_when_warning` |  | 0 | `closeness_to_outstanding` | 1.5092 | 6.62558802094e-05 |  | yes |  |
| 22 | `experiment_result.top_swing_features[4].warning_correlation` |  | -0.0101 | `closeness_to_outstanding` | 0.0108 | 0.0548118668596 |  | yes |  |
## MCM 2025 A: `mcm-2025-a-stair-wear`

- Scoring status: v4 endpoint target-minmax
- Default eval method: `B-Eval`
- Metrics: 21 total, 5 effective
- Baseline endpoint: `question_result_minmax_endpoint`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: 0
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `daily_use_pattern.peak_period_share_of_daily_use` | 0.376 | 0.376 | `exact_value` | 0.4 | 0 |  | no | daily_use_pattern.peak_period_share_of_daily_use |
| 2 | `daily_use_pattern.peak_period_users` | 27.3 | 27.6 | `higher_is_better` | 23.6 | 0 | -3.7 | yes | daily_use_pattern.peak_period_users |
| 3 | `daily_use_pattern.regular_hour_users_if_spread_over_10_hours` | 4.5 | 4.6 | `higher_is_better` | 7.1 | 0 | 2.6 | yes | daily_use_pattern.regular_hour_users_if_spread_over_10_hours |
| 4 | `experiment_result.age_interval_years[0]` | 283.6 | 283.6 | `exact_value` | 274 | 0 |  | no | age_reliability.plausible_interval_years[0] |
| 5 | `experiment_result.age_interval_years[1]` | 397 | 397 | `exact_value` | 510 | 0 |  | no | age_reliability.plausible_interval_years[1] |
| 6 | `experiment_result.estimated_age_years` | 340.3 | 340.3 | `exact_value` | 393 | 0 |  | no | age_reliability.estimated_age_years |
| 7 | `experiment_result.estimated_daily_users` | 72.67 | 73.52 | `higher_is_better` | 117.9 | 0 | 45.23 | yes | inverse_wear_model.usage_frequency.estimated_daily_users |
| 8 | `experiment_result.estimated_passages_per_tread` | 9555556 | 9666667 | `higher_is_better` | 21508000 | 0 | 11952444 | yes | inverse_wear_model.usage_frequency.estimated_passages_per_tread |
| 9 | `experiment_result.lateral_centroid` |  | -0.0261 | `unscored_missing_baseline` | 4.63 | 0 |  | no |  |
| 10 | `experiment_result.median_center_wear_depth_mm` | 4.3 | 4.35 | `higher_is_better` | 10.754 | 0 | 6.454 | yes | inverse_wear_model.usage_frequency.median_center_wear_depth_mm |
| 11 | `material_consistency.worked_example_material_proxy.material_density_proxy_g_cm3` | 2.35 | 2.35 | `exact_value` | 2.5 | 0 |  | no | material_source_guidance.worked_example_material_proxy.material_density_proxy |
| 12 | `material_consistency.worked_example_material_proxy.surface_hardness_proxy` | 4 | 4 | `exact_value` | 20 | 0 |  | no | material_source_guidance.worked_example_material_proxy.surface_hardness_proxy |
| 13 | `renovation_detection.repair_candidates[0].candidate_score` | 5.35 | 5.35 | `exact_value` | 0 | 0 |  | no | renovation_detection.repair_candidates[0].candidate_score |
| 14 | `renovation_detection.repair_candidates[0].patch_boundary_score` | 5 | 5 | `exact_value` | 0 | 0 |  | no | renovation_detection.repair_candidates[0].patch_boundary_score |
| 15 | `renovation_detection.repair_candidates[0].wear_jump_mm` | -2.4 | -2.4 | `exact_value` | 1.051 | 0 |  | no | renovation_detection.repair_candidates[0].wear_jump_mm |
| 16 | `renovation_detection.repair_candidates[1].candidate_score` | 3 | 3 | `exact_value` | 0 | 0 |  | no | renovation_detection.repair_candidates[1].candidate_score |
| 17 | `renovation_detection.repair_candidates[1].patch_boundary_score` | 2 | 2 | `exact_value` | 0 | 0 |  | no | renovation_detection.repair_candidates[1].patch_boundary_score |
| 18 | `renovation_detection.repair_candidates[1].wear_jump_mm` | 1.4 | 1.4 | `exact_value` | 0.799 | 0 |  | no | renovation_detection.repair_candidates[1].wear_jump_mm |
| 19 | `wdm.front_to_back_rounding_ratio` | 1.497 | 1.497 | `exact_value` | 1.67 | 0 |  | no | inverse_wear_model.direction_preference.front_to_back_rounding_ratio |
| 20 | `wdm.side_to_center_wear_ratio` | 0.526 | 0.526 | `exact_value` | 42.64 | 0 |  | no | inverse_wear_model.simultaneous_use.side_to_center_wear_ratio |
| 21 | `wdm.simultaneous_use_index_0_1` | 0.391 | 0.391 | `exact_value` | 0.3 | 0 |  | no | inverse_wear_model.simultaneous_use.simultaneous_use_index_0_1 |
## MCM 2025 B: `mcm-2025-b-juneau-tourism`

- Scoring status: v4 endpoint target-minmax
- Default eval method: `B-Eval`
- Metrics: 27 total, 19 effective
- Baseline endpoint: `question_result_minmax_endpoint`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.0805071737516 (scored)
- DeepSeek/Terminus-2 B-Eval: 0.0805071737516
- DeepSeek/Terminus-2 BO-Eval: 0.0805071737516

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `destination_adaptation.district_population_reference` | 180000 | 180000 | `exact_value` | 15500 | 0 |  | no | destination_adaptation.adapted_constraints.district_level_planning_population |
| 2 | `destination_adaptation.scaled_annual_visitor_target` | 8448000 | 8949156 | `higher_is_better` | 2380000 | 0 | -6068000 | yes | destination_adaptation.adapted_constraints.recommended_annual_visitor_target_for_district |
| 3 | `dynamic_programming.best_cumulative_score` |  | 4.793367 | `unscored_missing_baseline` | 0.5797 | 0 |  | no |  |
| 4 | `dynamic_programming.horizon_years[0]` |  | 2024 | `unscored_missing_baseline` | 2025 | 0 |  | no |  |
| 5 | `dynamic_programming.horizon_years[1]` |  | 2028 | `unscored_missing_baseline` | 2026 | 0 |  | no |  |
| 6 | `dynamic_programming.optimal_terminal_policy.annual_visitors` | 1408000 | 1491526 | `higher_is_better` | 1111429 | 0 | -296571 | yes | sustainability_model.optimal_policy.annual_visitors |
| 7 | `dynamic_programming.optimal_terminal_policy.conservation_share` | 0.35 | 0.35 | `exact_value` | 0.6 | 0 |  | no | sustainability_model.optimal_policy.conservation_share |
| 8 | `dynamic_programming.optimal_terminal_policy.daily_cap` | 10000 | 11000 | `higher_is_better` | 4000 | 0 | -6000 | yes | sustainability_model.optimal_policy.daily_cap |
| 9 | `dynamic_programming.optimal_terminal_policy.glacier_pressure_fields_per_year` | 0.3353 | 0.3319 | `lower_is_better` | 6.95 | 0 | -6.6147 | yes | sustainability_model.optimal_policy.projected_glacier_recession_fields_per_year |
| 10 | `dynamic_programming.optimal_terminal_policy.net_benefit_usd` | 313532032 | 341049399.55 | `higher_is_better` | 263158600 | 0 | -50373432 | yes | sustainability_model.optimal_policy.net_benefit_usd |
| 11 | `dynamic_programming.optimal_terminal_policy.resident_acceptance_index` | 0.78 | 1 | `higher_is_better` | 0.764 | 0 | -0.016 | yes | sustainability_model.optimal_policy.resident_acceptance_index |
| 12 | `dynamic_programming.optimal_terminal_policy.sustainability_score` | 0.908447 | 1.007 | `higher_is_better` | 0.5827 | 0 | -0.325747 | yes | sustainability_model.optimal_policy.sustainability_score |
| 13 | `dynamic_programming.optimal_terminal_policy.total_revenue_usd` | 400400000 | 431610327.83 | `higher_is_better` | 277162606 | 0 | -123237394 | yes | sustainability_model.optimal_policy.total_revenue_usd |
| 14 | `dynamic_programming.optimal_terminal_policy.visitor_fee_usd` | 50 | 55 | `higher_is_better` | 15 | 0 | -35 | yes | sustainability_model.optimal_policy.visitor_fee_usd |
| 15 | `dynamic_programming.optimal_terminal_policy.year` |  | 2028 | `unscored_missing_baseline` | 2034 | 0 |  | no |  |
| 16 | `experiment_result.annual_visitors` | 1408000 | 1491526 | `higher_is_better` | 1111429 | 0 | -296571 | yes | sustainability_model.optimal_policy.annual_visitors |
| 17 | `experiment_result.optimal_conservation_share` | 0.35 | 0.35 | `exact_value` | 0.6 | 0 |  | no | sustainability_model.optimal_policy.conservation_share |
| 18 | `experiment_result.optimal_daily_cap` | 10000 | 11000 | `higher_is_better` | 4000 | 0 | -6000 | yes | sustainability_model.optimal_policy.daily_cap |
| 19 | `experiment_result.optimal_visitor_fee_usd` | 50 | 55 | `higher_is_better` | 15 | 0 | -35 | yes | sustainability_model.optimal_policy.visitor_fee_usd |
| 20 | `experiment_result.resident_acceptance_index` | 0.78 | 1 | `higher_is_better` | 0.764 | 0 | -0.016 | yes | sustainability_model.optimal_policy.resident_acceptance_index |
| 21 | `experiment_result.sustainability_score` | 0.908447 | 1.007 | `higher_is_better` | 0.5827 | 0 | -0.325747 | yes | sustainability_model.optimal_policy.sustainability_score |
| 22 | `experiment_result.terminal_year` |  | 2028 | `unscored_missing_baseline` | 2034 | 0 |  | no |  |
| 23 | `experiment_result.total_revenue_usd` | 400400000 | 431610327.83 | `higher_is_better` | 277162606 | 0 | -123237394 | yes | sustainability_model.optimal_policy.total_revenue_usd |
| 24 | `sensitivity_analysis[0].correlation_with_score` | 0.909965 | 0.59522 | `lower_is_better` | -0.02 | 0 | 0.929965 | yes | sensitivity_analysis.top_factors[1].correlation_with_score |
| 25 | `sensitivity_analysis[2].correlation_with_score` | -0.868509 | -0.19619 | `higher_is_better` | 0.0047 | 0.701198389455 | 0.873209 | yes | sensitivity_analysis.top_factors[2].correlation_with_score |
| 26 | `sensitivity_analysis[3].correlation_with_score` | 0.227667 | 0.11805 | `lower_is_better` | -0.1087 | 0 | 0.336367 | yes | sensitivity_analysis.top_factors[4].correlation_with_score |
| 27 | `sensitivity_analysis[4].correlation_with_score` | -0.117707 | 0.00598 | `higher_is_better` | 0.0272 | 0.828437911826 | 0.144907 | yes | sensitivity_analysis.top_factors[5].correlation_with_score |
## MCM 2025 C: `mcm-2025-c-olympic-medals`

- Scoring status: legacy fallback
- Default eval method: `B-Eval`
- Metrics: 96 total, 96 effective
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 0.998370361347 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: -0.293385079963
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `great_coach_model.global_top_jump_75pct` |  | 6 | `closeness_to_outstanding` | 17.7 | 0.0579710144928 |  | yes |  |
| 2 | `great_coach_model.lang_ping_validation[0].Year` |  | 2008 | `closeness_to_outstanding` | 1984 | 0.909420289855 |  | yes |  |
| 3 | `great_coach_model.lang_ping_validation[0].estimated_jump_score` |  | 5 | `closeness_to_outstanding` | 30 | 0.0234375 |  | yes |  |
| 4 | `great_coach_model.lang_ping_validation[0].medal_score` |  | 5 | `closeness_to_outstanding` | 30 | 0.0234375 |  | yes |  |
| 5 | `great_coach_model.lang_ping_validation[0].prev3_score` |  | 0 | `closeness_to_outstanding` | 0 | 1 |  | yes |  |
| 6 | `great_coach_model.lang_ping_validation[1].Year` |  | 2016 | `closeness_to_outstanding` | 1988 | 0.896265560166 |  | yes |  |
| 7 | `great_coach_model.lang_ping_validation[1].estimated_jump_score` |  | 1.666667 | `closeness_to_outstanding` | -19 | 0.00958466628219 |  | yes |  |
| 8 | `great_coach_model.lang_ping_validation[1].medal_score` |  | 3 | `closeness_to_outstanding` | 11 | 0.0430622009569 |  | yes |  |
| 9 | `great_coach_model.lang_ping_validation[1].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | 30 | 0.00555041483714 |  | yes |  |
| 10 | `great_coach_model.recommendations[0].benchmark_jump_score` |  | 5 | `closeness_to_outstanding` | 0.7 | 0.122448979592 |  | yes |  |
| 11 | `great_coach_model.recommendations[0].estimated_medal_count_gain` |  | 1.666667 | `closeness_to_outstanding` | 0.4 | 0.136363628926 |  | yes |  |
| 12 | `great_coach_model.recommendations[0].latest_medal_score` |  | 0 | `closeness_to_outstanding` | 4 | 2.49993750156e-05 |  | yes |  |
| 13 | `great_coach_model.recommendations[0].latest_year` |  | 2024 | `closeness_to_outstanding` | 2024 | 1 |  | yes |  |
| 14 | `great_coach_model.recommendations[0].recent_baseline_score` |  | 1.333333 | `closeness_to_outstanding` | 2.7 | 0.104803447112 |  | yes |  |
| 15 | `great_coach_model.recommendations[1].benchmark_jump_score` |  | 6 | `closeness_to_outstanding` | 5.8 | 0.782608695652 |  | yes |  |
| 16 | `great_coach_model.recommendations[1].estimated_medal_count_gain` |  | 2 | `closeness_to_outstanding` | 3.5 | 0.137931034483 |  | yes |  |
| 17 | `great_coach_model.recommendations[1].latest_medal_score` |  | 1 | `closeness_to_outstanding` | 16 | 0.00793650793651 |  | yes |  |
| 18 | `great_coach_model.recommendations[1].latest_year` |  | 2024 | `closeness_to_outstanding` | 2024 | 1 |  | yes |  |
| 19 | `great_coach_model.recommendations[1].recent_baseline_score` |  | 0.333333 | `closeness_to_outstanding` | 4.3 | 0.00998335035064 |  | yes |  |
| 20 | `great_coach_model.recommendations[2].benchmark_jump_score` |  | 9.416667 | `closeness_to_outstanding` | 1 | 0.118365921349 |  | yes |  |
| 21 | `great_coach_model.recommendations[2].estimated_medal_count_gain` |  | 3 | `closeness_to_outstanding` | 0.6 | 0.130434782609 |  | yes |  |
| 22 | `great_coach_model.recommendations[2].latest_medal_score` |  | 6 | `closeness_to_outstanding` | 2 | 0.152542372881 |  | yes |  |
| 23 | `great_coach_model.recommendations[2].latest_year` |  | 2024 | `closeness_to_outstanding` | 2000 | 0.910071942446 |  | yes |  |
| 24 | `great_coach_model.recommendations[2].recent_baseline_score` |  | 2.666667 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 25 | `great_coach_model.recommendations[3].benchmark_jump_score` |  | 5.333333 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 26 | `great_coach_model.recommendations[3].estimated_medal_count_gain` |  | 1.777778 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 27 | `great_coach_model.recommendations[3].latest_medal_score` |  | 12 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 28 | `great_coach_model.recommendations[3].latest_year` |  | 2024 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 29 | `great_coach_model.recommendations[3].recent_baseline_score` |  | 2.666667 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 30 | `great_coach_model.top_historical_jump_candidates[0].Year` |  | 2008 | `closeness_to_outstanding` | 1920 | 0.732490272374 |  | yes |  |
| 31 | `great_coach_model.top_historical_jump_candidates[0].coach_like_jump` |  | 28 | `closeness_to_outstanding` | 121 | 0.0348692403487 |  | yes |  |
| 32 | `great_coach_model.top_historical_jump_candidates[0].medal_score` |  | 34 | `closeness_to_outstanding` | 164 | 0.0304295942721 |  | yes |  |
| 33 | `great_coach_model.top_historical_jump_candidates[0].prev3_score` |  | 6 | `closeness_to_outstanding` | 43 | 0.0190880169671 |  | yes |  |
| 34 | `great_coach_model.top_historical_jump_candidates[10].Year` |  | 2008 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 35 | `great_coach_model.top_historical_jump_candidates[10].coach_like_jump` |  | 17.333333 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 36 | `great_coach_model.top_historical_jump_candidates[10].medal_score` |  | 31 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 37 | `great_coach_model.top_historical_jump_candidates[10].prev3_score` |  | 13.666667 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 38 | `great_coach_model.top_historical_jump_candidates[11].Year` |  | 2020 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 39 | `great_coach_model.top_historical_jump_candidates[11].coach_like_jump` |  | 17 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 40 | `great_coach_model.top_historical_jump_candidates[11].medal_score` |  | 17 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 41 | `great_coach_model.top_historical_jump_candidates[11].prev3_score` |  | 0 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 42 | `great_coach_model.top_historical_jump_candidates[1].Year` |  | 2000 | `closeness_to_outstanding` | 1964 | 0.869565217391 |  | yes |  |
| 43 | `great_coach_model.top_historical_jump_candidates[1].coach_like_jump` |  | 23.666667 | `closeness_to_outstanding` | 94 | 0.038811954055 |  | yes |  |
| 44 | `great_coach_model.top_historical_jump_candidates[1].medal_score` |  | 37 | `closeness_to_outstanding` | 159 | 0.035115469788 |  | yes |  |
| 45 | `great_coach_model.top_historical_jump_candidates[1].prev3_score` |  | 13.333333 | `closeness_to_outstanding` | 65 | 0.0300375460173 |  | yes |  |
| 46 | `great_coach_model.top_historical_jump_candidates[2].Year` |  | 2004 | `closeness_to_outstanding` | 1980 | 0.909255898367 |  | yes |  |
| 47 | `great_coach_model.top_historical_jump_candidates[2].coach_like_jump` |  | 23 | `closeness_to_outstanding` | 90 | 0.0395642201835 |  | yes |  |
| 48 | `great_coach_model.top_historical_jump_candidates[2].medal_score` |  | 38 | `closeness_to_outstanding` | 127 | 0.0487387772552 |  | yes |  |
| 49 | `great_coach_model.top_historical_jump_candidates[2].prev3_score` |  | 15 | `closeness_to_outstanding` | 37 | 0.0756302521008 |  | yes |  |
| 50 | `great_coach_model.top_historical_jump_candidates[3].Year` |  | 2008 | `closeness_to_outstanding` | 1980 | 0.895895300416 |  | yes |  |
| 51 | `great_coach_model.top_historical_jump_candidates[3].coach_like_jump` |  | 22.333333 | `closeness_to_outstanding` | 84.3 | 0.0414561196428 |  | yes |  |
| 52 | `great_coach_model.top_historical_jump_candidates[3].medal_score` |  | 33 | `closeness_to_outstanding` | 159 | 0.0304709141274 |  | yes |  |
| 53 | `great_coach_model.top_historical_jump_candidates[3].prev3_score` |  | 10.666667 | `closeness_to_outstanding` | 74.7 | 0.0195978367727 |  | yes |  |
| 54 | `great_coach_model.top_historical_jump_candidates[4].Year` |  | 2000 | `closeness_to_outstanding` | 2000 | 1 |  | yes |  |
| 55 | `great_coach_model.top_historical_jump_candidates[4].coach_like_jump` |  | 22 | `closeness_to_outstanding` | 83.7 | 0.0410320174075 |  | yes |  |
| 56 | `great_coach_model.top_historical_jump_candidates[4].medal_score` |  | 30 | `closeness_to_outstanding` | 103 | 0.0469973890339 |  | yes |  |
| 57 | `great_coach_model.top_historical_jump_candidates[4].prev3_score` |  | 8 | `closeness_to_outstanding` | 19.3 | 0.0783034257749 |  | yes |  |
| 58 | `great_coach_model.top_historical_jump_candidates[5].Year` |  | 1996 | `closeness_to_outstanding` | 1920 | 0.759127789047 |  | yes |  |
| 59 | `great_coach_model.top_historical_jump_candidates[5].coach_like_jump` |  | 22 | `closeness_to_outstanding` | 77 | 0.0458015267176 |  | yes |  |
| 60 | `great_coach_model.top_historical_jump_candidates[5].medal_score` |  | 22 | `closeness_to_outstanding` | 83 | 0.0414833438089 |  | yes |  |
| 61 | `great_coach_model.top_historical_jump_candidates[5].prev3_score` |  | 0 | `closeness_to_outstanding` | 6 | 1.66663888935e-05 |  | yes |  |
| 62 | `great_coach_model.top_historical_jump_candidates[6].Year` |  | 1996 | `closeness_to_outstanding` | 2016 | 0.922934648582 |  | yes |  |
| 63 | `great_coach_model.top_historical_jump_candidates[6].coach_like_jump` |  | 20.666667 | `closeness_to_outstanding` | 71.3 | 0.0466926080149 |  | yes |  |
| 64 | `great_coach_model.top_historical_jump_candidates[6].medal_score` |  | 22 | `closeness_to_outstanding` | 88 | 0.0384615384615 |  | yes |  |
| 65 | `great_coach_model.top_historical_jump_candidates[6].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | 16.7 | 0.0103048490969 |  | yes |  |
| 66 | `great_coach_model.top_historical_jump_candidates[7].Year` |  | 1996 | `closeness_to_outstanding` | 1984 | 0.952290076336 |  | yes |  |
| 67 | `great_coach_model.top_historical_jump_candidates[7].coach_like_jump` |  | 18 | `closeness_to_outstanding` | 71 | 0.0391588107324 |  | yes |  |
| 68 | `great_coach_model.top_historical_jump_candidates[7].medal_score` |  | 18 | `closeness_to_outstanding` | 84 | 0.0316901408451 |  | yes |  |
| 69 | `great_coach_model.top_historical_jump_candidates[7].prev3_score` |  | 0 | `closeness_to_outstanding` | 13 | 7.69224852117e-06 |  | yes |  |
| 70 | `great_coach_model.top_historical_jump_candidates[8].Year` |  | 2020 | `closeness_to_outstanding` | 1984 | 0.870689655172 |  | yes |  |
| 71 | `great_coach_model.top_historical_jump_candidates[8].coach_like_jump` |  | 18 | `closeness_to_outstanding` | 67.7 | 0.0416505977632 |  | yes |  |
| 72 | `great_coach_model.top_historical_jump_candidates[8].medal_score` |  | 18 | `closeness_to_outstanding` | 75 | 0.0365111561866 |  | yes |  |
| 73 | `great_coach_model.top_historical_jump_candidates[8].prev3_score` |  | 0 | `closeness_to_outstanding` | 7.3 | 1.36984424871e-05 |  | yes |  |
| 74 | `great_coach_model.top_historical_jump_candidates[9].Year` |  | 2000 | `closeness_to_outstanding` | 1912 | 0.731707317073 |  | yes |  |
| 75 | `great_coach_model.top_historical_jump_candidates[9].coach_like_jump` |  | 17.666667 | `closeness_to_outstanding` | 65.3 | 0.0426102114263 |  | yes |  |
| 76 | `great_coach_model.top_historical_jump_candidates[9].medal_score` |  | 19 | `closeness_to_outstanding` | 75 | 0.0391214824983 |  | yes |  |
| 77 | `great_coach_model.top_historical_jump_candidates[9].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | 9.7 | 0.0187646545538 |  | yes |  |
| 78 | `host_effect_model.Gold.event_count_coefficient` |  | 0.000147 | `closeness_to_outstanding` | 0.00022 | 0.578034682081 |  | yes |  |
| 79 | `host_effect_model.Gold.host_bonus_coefficient` |  | 14.341156 | `closeness_to_outstanding` | 14.121 | 0.886581526532 |  | yes |  |
| 80 | `host_effect_model.Gold.prev3_coefficient` |  | 0.950866 | `closeness_to_outstanding` | 0.909 | 0.731576447561 |  | yes |  |
| 81 | `host_effect_model.Gold.r2` |  | 0.752918 | `closeness_to_outstanding` | 0.722 | 0.745044371086 |  | yes |  |
| 82 | `host_effect_model.Total.event_count_coefficient` |  | -0.000215 | `closeness_to_outstanding` | 1e-05 | 0.307692307692 |  | yes |  |
| 83 | `host_effect_model.Total.host_bonus_coefficient` |  | 36.422317 | `closeness_to_outstanding` | 35.277 | 0.792364389073 |  | yes |  |
| 84 | `host_effect_model.Total.prev3_coefficient` |  | 0.952921 | `closeness_to_outstanding` | 0.915 | 0.750964592722 |  | yes |  |
| 85 | `host_effect_model.Total.r2` |  | 0.765819 | `closeness_to_outstanding` | 0.721 | 0.672177503824 |  | yes |  |
| 86 | `model_evaluation.holdout_year` |  | 2024 | `closeness_to_outstanding` | 2024 | 1 |  | yes |  |
| 87 | `model_evaluation.mean_accuracy_2024` |  | 0.850591 | `closeness_to_outstanding` | 0.661 | 0.3499631354 |  | yes |  |
| 88 | `model_evaluation.mean_brier_2024` |  | 0.142806 | `closeness_to_outstanding` | 0.315 | 0.0905120943923 |  | yes |  |
| 89 | `model_evaluation.mean_f1_2024` |  | 0.287348 | `closeness_to_outstanding` | 0.627 | 0.0921642569759 |  | yes |  |
| 90 | `model_evaluation.sport_models` |  | 50 | `closeness_to_outstanding` | 44 | 0.5 |  | yes |  |
| 91 | `model_evaluation.status_counts.GoldBinary:fallback_mean` |  | 7 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 92 | `model_evaluation.status_counts.GoldBinary:random_forest` |  | 43 | `closeness_to_outstanding` | 44 | 0.837662337662 |  | yes |  |
| 93 | `model_evaluation.status_counts.MedalBinary:fallback_mean` |  | 7 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 94 | `model_evaluation.status_counts.MedalBinary:random_forest` |  | 43 | `closeness_to_outstanding` | 44 | 0.837662337662 |  | yes |  |
| 95 | `monte_carlo.simulations` |  | 500 | `closeness_to_outstanding` | 500 | 1 |  | yes |  |
| 96 | `monte_carlo.weight_power` |  | 4 | `closeness_to_outstanding` | 1 | 0.137931034483 |  | yes |  |
