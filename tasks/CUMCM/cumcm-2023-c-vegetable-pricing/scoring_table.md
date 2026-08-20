# CUMCM 2023 C: vegetable pricing and replenishment

- Task slug: `cumcm-2023-c-vegetable-pricing`
- Required output: `/root/results/cumcm-2023-c-vegetable-pricing_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 最后一问本身是让商超说明还应采集哪些数据、这些数据怎样帮助补货和定价；它主要是文字建议。
- Final answer: 当前数值 verifier 只看支撑这些建议的最后可量化补货定价结果：未来一周最大利润 5105.6 元，并选择 29 个单品进入补货定价方案。
- Baseline model: baseline 用规划优化和资源配置模型，把可售空间、补货量和价格决策转成利润最大化问题。
- Note: Q4 is qualitative, so this benchmark records the last quantifiable pricing/replenishment answer that Q4 asks to improve with more data.
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 38
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 2
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `target_comparison.future_week_max_profit_yuan.actual` |  | 5105.6 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `target_comparison.problem3_selected_item_count.actual` |  | 29 | `closeness_to_outstanding` | yes | 1 |  |
