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
