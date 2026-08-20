# MCM 2023 B: reimagining Maasai Mara

- Task slug: `mcm-2023-b-maasai-mara`
- Required output: `/root/results/mcm-2023-b-maasai-mara_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 把土地分区和政策方案整理成给当地管理者的非技术报告，说明推荐方案的收益和用地分配。
- Final answer: O 奖复现的方案 2 收益指标值约 154948.974，农业/狩猎/旅游/保护区格点数分别为 12、2、9、13。
- Baseline model: baseline 用空间土地利用优化，把农业、狩猎、旅游和野生动物保护的格点分配成收益最大化问题。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 11
- Final-answer numeric field count: 5
- Scored final-answer numeric field count: 5
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.60265725`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `target_comparison.scenario2_agriculture_cells.actual` |  | 12 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `target_comparison.scenario2_benefit_million.actual` |  | 154948.974 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `target_comparison.scenario2_hunting_cells.actual` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `target_comparison.scenario2_tourism_cells.actual` |  | 9 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `target_comparison.scenario2_wildlife_cells.actual` |  | 13 | `closeness_to_outstanding` | yes | 1 |  |
