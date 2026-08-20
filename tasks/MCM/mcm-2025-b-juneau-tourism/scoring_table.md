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
