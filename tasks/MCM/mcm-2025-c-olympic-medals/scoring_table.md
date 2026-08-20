# MCM 2025 C: Olympic medal prediction

- Task slug: `mcm-2025-c-olympic-medals`
- Required output: `/root/results/mcm-2025-c-olympic-medals_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 说明模型还能发现哪些原创奖牌规律，以及这些规律怎样指导国家奥委会分配项目和教练资源。
- Final answer: O 奖复现的教练效应建议中，四个候选投资的预计奖牌增益为 1.666667、2.0、3.0、1.777778，全局强教练效应 75 分位跳升为 6.0。
- Baseline model: baseline 用奥运奖牌预测、项目重要性分析和滚动三届历史成绩跳升来筛选可能的强教练效应。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 96
- Final-answer numeric field count: 5
- Scored final-answer numeric field count: 5
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.584014166667`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `great_coach_model.global_top_jump_75pct` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `great_coach_model.recommendations[0].estimated_medal_count_gain` |  | 1.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `great_coach_model.recommendations[1].estimated_medal_count_gain` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `great_coach_model.recommendations[2].estimated_medal_count_gain` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `great_coach_model.recommendations[3].estimated_medal_count_gain` |  | 1.777778 | `closeness_to_outstanding` | yes | 1 |  |
