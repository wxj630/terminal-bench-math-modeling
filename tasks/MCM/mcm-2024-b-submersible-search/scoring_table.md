# MCM 2024 B: submersible localization and search planning

- Task slug: `mcm-2024-b-submersible-search`
- Required output: `/root/results/mcm-2024-b-submersible-search_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 把潜水器搜索模型迁移到加勒比海场景，并说明洋流、海底地形和多潜水器协同时需要怎样调整。
- Final answer: O 奖复现给出的加勒比海调整为洋流不确定性乘数 1.35、地形不确定性乘数 1.2。
- Baseline model: baseline 用贝叶斯搜索规划，先估计位置后验，再按海流和地形不确定性调整搜索区域。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 13
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 2
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.57862125`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Semantic direction | Normalization mode | Normalization direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---|---|---:|---|
| 1 | `experiment_result.caribbean_adaptation.current_multiplier` |  | 1.35 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 2 | `experiment_result.caribbean_adaptation.terrain_uncertainty_multiplier` |  | 1.2 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
