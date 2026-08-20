# MCM 2023 A: drought-stricken plant communities

- Task slug: `mcm-2023-a-plant-community`
- Required output: `/root/results/mcm-2023-a-plant-community_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 综合物种数、干旱、污染和栖息地压力，说明怎样保证植物群落长期可生存。
- Final answer: O 奖复现的核心量化结论包括最优/阈值物种数 2，beta 压力下生物量下降 32.0%，五物种均匀度 0.8826。
- Baseline model: baseline 把物种数阈值、功能性状、干旱敏感性和污染/栖息地压力合成为管理前沿。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 41
- Final-answer numeric field count: 3
- Scored final-answer numeric field count: 3
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.502804666667`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `target_comparison.beta_decline_pct.actual` |  | 32 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `target_comparison.five_species_pielou_evenness.actual` |  | 0.8826 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `target_comparison.optimal_species_count.actual` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
