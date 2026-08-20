# CUMCM 2024 B: production-process decision optimization

- Task slug: `cumcm-2024-b-production-decision`
- Required output: `/root/results/cumcm-2024-b-production-decision_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 把零配件和成品次品率看成抽样估出来的不确定量，然后重新求问题 2 和问题 3 的最优检测、装配、拆解决策。
- Final answer: O 奖复现用 3 组后验缺陷率情景重算利润：Q2 case1 利润约 25.9691、25.8694、25.7715；Q3 最优策略后验利润约 86.8529、86.5588、86.2647。
- Baseline model: baseline 用二项抽样/贝叶斯后验估计次品率，再用期望利润枚举和多阶段决策搜索求最优策略。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 69
- Final-answer numeric field count: 6
- Scored final-answer numeric field count: 6
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q4.posterior_rows[0].q2_best_profit_case1` |  | 25.9691 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q4.posterior_rows[0].q3_best_policy_profit_under_posterior` |  | 86.8529 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.q4.posterior_rows[1].q2_best_profit_case1` |  | 25.8694 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.q4.posterior_rows[1].q3_best_policy_profit_under_posterior` |  | 86.5588 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.q4.posterior_rows[2].q2_best_profit_case1` |  | 25.7715 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.q4.posterior_rows[2].q3_best_policy_profit_under_posterior` |  | 86.2647 | `closeness_to_outstanding` | yes | 1 |  |
