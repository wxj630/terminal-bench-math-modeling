# MCM 2024 A: lamprey sex-ratio ecology

- Task slug: `mcm-2024-a-lamprey`
- Required output: `/root/results/mcm-2024-a-lamprey_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 判断七鳃鳗可变性别比例是否也会让生态系统中的其他生物受益，尤其是寄生者/宿主相关指标。
- Final answer: O 奖复现的共存情景资源水平为 0.55，寄生者指数 8.562，宿主鱼指数 1080.356。
- Baseline model: baseline 用生态动力系统仿真，把资源水平、性别比例、七鳃鳗、宿主鱼和寄生者一起演化。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 105
- Final-answer numeric field count: 3
- Scored final-answer numeric field count: 3
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.45683575`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Semantic direction | Normalization mode | Normalization direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---|---|---:|---|
| 1 | `experiment_result.parasite_coexistence_case.final_parasite_index` |  | 8.562 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 2 | `experiment_result.parasite_coexistence_case.host_fish_index` |  | 1080.356 | `higher_is_better` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 3 | `experiment_result.parasite_coexistence_case.resource_level` |  | 0.55 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
