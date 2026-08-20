# CUMCM 2024 C: crop-planting strategy optimization

- Task slug: `cumcm-2024-c-crop-planting`
- Required output: `/root/results/cumcm-2024-c-crop-planting_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 在问题 2 的基础上加入作物之间的替代、互补和价格/成本/销量相关性，求 2024-2030 年的稳健种植策略。
- Final answer: O 奖复现的相关性稳健方案给出 best correlated CVaR10 利润 118550698.19 元，价格和成本的 Spearman 相关系数约 0.2551。
- Baseline model: baseline 用规划优化和资源配置模型，在随机场景下比较候选种植方案的收益和风险。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 20
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 2
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q2_q3.best_correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q2_q3.spearman_price_cost` |  | 0.2551 | `closeness_to_outstanding` | yes | 1 |  |
