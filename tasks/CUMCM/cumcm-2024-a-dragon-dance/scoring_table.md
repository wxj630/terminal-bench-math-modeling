# CUMCM 2024 A: dragon-dance bench kinematics

- Task slug: `cumcm-2024-a-dragon-dance`
- Required output: `/root/results/cumcm-2024-a-dragon-dance_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 沿着前面求出的调头路径行进时，求龙头最大能跑多快，才能保证所有把手速度都不超过 2 m/s。
- Final answer: O 奖复现给出的最大龙头速度约 2.00002 m/s；当龙头速度为 1 m/s 时，全队最大速度比例约 0.99999。
- Baseline model: baseline 用几何解析和运动学参数方程，沿路径传播各把手位置，再由速度约束反推龙头速度上限。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 9
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 2
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Semantic direction | Normalization mode | Normalization direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---|---|---:|---|
| 1 | `experiment_result.q5.max_head_speed_mps` |  | 2.00002 | `higher_is_better` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 2 | `experiment_result.q5.max_speed_ratio_when_head_1mps` |  | 0.99999 | `lower_is_better` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
