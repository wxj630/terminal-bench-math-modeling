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
