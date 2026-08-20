# CUMCM 2024 A: dragon-dance bench kinematics

- Task slug: `cumcm-2024-a-dragon-dance`
- Required output: `/root/results/cumcm-2024-a-dragon-dance_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 9
- Effective scored metric count: 9
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q1.handles` |  | 224 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q2.terminal_min_margin_m` |  | 0.249958 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.q2.terminal_time_s` |  | 464 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.q3.minimum_pitch_m` |  | 0.4 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.q4.base_ratio_2_to_1_length_m` |  | 14.1372 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.q4.shortest_candidate_length_m` |  | 14.1372 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.q4.shortest_candidate_ratio` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.q5.max_head_speed_mps` |  | 2.00002 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.q5.max_speed_ratio_when_head_1mps` |  | 0.99999 | `closeness_to_outstanding` | yes | 1 |  |
