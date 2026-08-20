# MCM 2024 C: momentum in tennis

- Task slug: `mcm-2024-c-tennis-momentum`
- Required output: `/root/results/mcm-2024-c-tennis-momentum_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 把势头模型转成教练能用的赛中提示：什么时候可能发生势头转换，应重点监控哪些指标。
- Final answer: O 奖复现的最终比赛预警率为 0.006；前三个势头预警特征相关系数约为 0.0302、-0.0223、0.0154。
- Baseline model: baseline 用势头时间序列、随机性检验和贝叶斯/分类预警模型，把比赛数据转成教练提示。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 22
- Final-answer numeric field count: 4
- Scored final-answer numeric field count: 4
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.5912914`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.dual_temporal_bayes.final_match_warning_rate` |  | 0.006 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.top_swing_features[0].warning_correlation` |  | 0.0302 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.top_swing_features[1].warning_correlation` |  | -0.0223 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.top_swing_features[2].warning_correlation` |  | 0.0154 | `closeness_to_outstanding` | yes | 1 |  |
