# MCM 2025 B: sustainable tourism management in Juneau

- Task slug: `mcm-2025-b-juneau-tourism`
- Required output: `/root/results/mcm-2025-b-juneau-tourism_result.json`
- Scoring version: `tb-mathmodeling-v5-final-question-endpoint-target-minmax`
- Scoring scope: `final_question_only`
- Final question: 给朱诺旅游委员会写一页备忘录，概括预测、各种限制/收费措施的效果，并推荐最优可持续旅游政策。
- Final answer: O 奖复现推荐终端政策：日容量 11000 人，游客费 55 USD，年游客 1491526，总收入 431610327.83 USD，居民接受度 1.0，可持续得分 1.007。
- Baseline model: baseline 用可持续旅游政策优化，把游客量、收费、保护投入、居民接受度和冰川压力一起做动态规划。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 27
- Final-answer numeric field count: 6
- Scored final-answer numeric field count: 6
- Baseline endpoint: `question_result_minmax_endpoint`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction_metric_values`, score `1`

| # | Metric path | Baseline value | Outstanding value | Semantic direction | Normalization mode | Normalization direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---|---|---:|---|
| 1 | `experiment_result.annual_visitors` | 1408000 | 1491526 | `higher_is_better` | `baseline_to_outstanding_target_minmax` | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.annual_visitors` |
| 2 | `experiment_result.optimal_daily_cap` | 10000 | 11000 | `target_value` | `baseline_to_outstanding_target_minmax` | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.daily_cap` |
| 3 | `experiment_result.optimal_visitor_fee_usd` | 50 | 55 | `target_value` | `baseline_to_outstanding_target_minmax` | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.visitor_fee_usd` |
| 4 | `experiment_result.resident_acceptance_index` | 0.78 | 1 | `higher_is_better` | `baseline_to_outstanding_target_minmax` | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.resident_acceptance_index` |
| 5 | `experiment_result.sustainability_score` | 0.908447 | 1.007 | `higher_is_better` | `baseline_to_outstanding_target_minmax` | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.sustainability_score` |
| 6 | `experiment_result.total_revenue_usd` | 400400000 | 431610327.83 | `higher_is_better` | `baseline_to_outstanding_target_minmax` | `higher_is_better` | yes | 1 | `sustainability_model.optimal_policy.total_revenue_usd` |
