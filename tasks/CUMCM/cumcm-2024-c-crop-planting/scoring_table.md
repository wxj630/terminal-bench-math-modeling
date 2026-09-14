# CUMCM 2024 C: crop-planting strategy optimization

- Task slug: `cumcm-2024-c-crop-planting`
- Required output: `/root/results/cumcm-2024-c-crop-planting_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 2024-2030 年最优种植方案：超产分别按（1）滞销浪费、（2）按 2023 年价格 50% 降价出售，求两种情形下七年总利润最大的种植策略。
- Final answer: 本题为 special case：O 奖论文的完整约束集（含其自创的“实际产量≥0.9×预期销量”）在官方附件上不可行，且论文使用未公开的启发式，其汇报值无法忠实复现。评分锚点改为一套可复现的精确求解结果：按论文式(19)的逐地块销量封顶建模（min(x·y, d) 在逐地块求和之内），用 HiGHS 混合整数规划求解，滞销情境七年总利润约 36271603 元、50% 降价情境约 43282389 元（MIP gap < 1%）。
- Baseline model: baseline 用规划优化和资源配置模型，在候选种植方案间比较收益与风险。
- Note: special case：O 奖论文的完整约束集在官方附件上无可行解（“分散度≤5 块地”与“实际产量≥0.9×预期销量”联立冲突），论文亦使用未公开的 DEGA 启发式，其汇报值无法忠实复现。本题锚点改为论文式(19)口径下用 HiGHS 求得的可复现解（脚本：outstanding_solutions/2024/C/C038/solution.py）。
- Special case: yes
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 20
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 2
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Semantic direction | Normalization mode | Normalization direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---|---|---:|---|
| 1 | `experiment_result.q1.discount_profit_yuan` |  | 58718967.38 | `higher_is_better` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 2 | `experiment_result.q1.waste_profit_yuan` |  | 40418876.72 | `higher_is_better` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
