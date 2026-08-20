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
