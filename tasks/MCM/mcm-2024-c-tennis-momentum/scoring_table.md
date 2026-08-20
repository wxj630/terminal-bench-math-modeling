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
