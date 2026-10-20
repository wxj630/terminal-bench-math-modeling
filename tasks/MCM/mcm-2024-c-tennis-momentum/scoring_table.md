# MCM 2024 C: momentum in tennis

- Task slug: `mcm-2024-c-tennis-momentum`
- Required output: `/root/results/mcm-2024-c-tennis-momentum_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 教练认为比赛中的起伏是随机的。用统计检验评估这个说法：有多大比例的比赛在 5% 水平上拒绝了"走势独立同分布"的原假设（即数据支持动量存在）。
- Final answer: O 奖复现的结果：中位 Ljung-Box p = 0.7128、中位 Runs p = 0.2902，按 Ljung-Box 或 Runs 任一在 5% 水平拒绝 iid 的比赛比例为 0.0000——即数据并不支持动量存在。
- Baseline model: baseline 用服务器调整后的得失分残差序列，对每场比赛做 Ljung-Box 与 Runs 检验，统计拒绝随机原假设的比赛比例。
- Note: 回退说明：Q5（给教练的赛中提示）是定性建议，原计分的 warning_rate 由复现自设阈值产生，论文普遍不报告。这里回退到 Q2——题面明确要求评估"起伏是否随机"，这是本题唯一的统计检验型数值核心。方向说明：share_rejecting_iid_at_5pct 越高越支持动量存在；median p 值则是 target-like（论文间的 p 值不可比，仅作辅助项）。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 23
- Final-answer numeric field count: 3
- Scored final-answer numeric field count: 3
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.5912914`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Semantic direction | Normalization mode | Normalization direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---|---|---:|---|
| 1 | `experiment_result.randomness_tests.median_ljung_box_p` |  | 0.712832 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 2 | `experiment_result.randomness_tests.median_runs_p` |  | 0.290172 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 3 | `experiment_result.randomness_tests.share_rejecting_iid_at_5pct` |  | 0.16129 | `higher_is_better` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
