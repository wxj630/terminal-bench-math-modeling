# CUMCM 2025 C: NIPT timing and fetal abnormality modeling

- Task slug: `cumcm-2025-c-nipt`
- Required output: `/root/results/cumcm-2025-c-nipt_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 按 BMI 分组后，各组的最佳 NIPT 检测时点应定在什么孕周，才能把孕妇的潜在风险降到最低。
- Final answer: O 奖复现按 BMI 分成 4 组，前三组最佳时点 12.0 周、最高 BMI 组 20.0 周；因此推荐时点区间为 12.0 到 20.0 周（Q4 的女胎异常判定本身是分类方法，论文普遍只报判定例数或不同交叉验证协议下的指标，不可比，故回退到 Q2/Q3 的时点核心）。
- Baseline model: baseline 用混合效应/生存模型估计各 BMI 组 Y 染色体浓度达标时间，再在风险函数下优化每组统一检测时点。
- Note: 回退说明：Q4（女胎异常判定）是方法题，人类论文报的 accuracy/F1 取决于各自的分组数、交叉验证协议（留一法 vs 5 折）与阈值，彼此不可比；一篇甚至不给数值。Q2/Q3 要求的每组最佳 NIPT 时点才是本题真正的数值核心，两篇论文都报告了孕周区间。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 8
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 2
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Semantic direction | Normalization mode | Normalization direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---|---|---:|---|
| 1 | `experiment_result.earliest_recommended_week` |  | 12 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
| 2 | `experiment_result.latest_recommended_week` |  | 20 | `target_value` | `legacy_target_distance_to_outstanding` |  | yes | 1 |  |
