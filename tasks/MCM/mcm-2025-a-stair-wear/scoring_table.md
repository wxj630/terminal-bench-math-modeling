# MCM 2025 A: stair wear and historical traffic inference

- Task slug: `mcm-2025-a-stair-wear`
- Required output: `/root/results/mcm-2025-a-stair-wear_result.json`
- Scoring version: `tb-mathmodeling-v4-endpoint-target-minmax`
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
