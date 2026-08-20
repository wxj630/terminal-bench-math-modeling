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
