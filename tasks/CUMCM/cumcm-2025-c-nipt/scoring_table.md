# CUMCM 2025 C: NIPT timing and fetal abnormality modeling

- Task slug: `cumcm-2025-c-nipt`
- Required output: `/root/results/cumcm-2025-c-nipt_result.json`
- Scoring version: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- Scoring scope: `final_question_only`
- Final question: 对女胎样本，用染色体 Z 值、GC 含量、读段数、BMI 等指标判断胎儿是否异常。
- Final answer: O 奖复现的女胎异常判定模型 leave-one-out accuracy 为 0.8659，F1 为 0.3721。
- Baseline model: baseline 用综合评价和权重决策，把多项检测指标合成风险分数，再给出异常判定。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 8
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 2
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.female_loo_accuracy` |  | 0.8659 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `female_abnormality.leave_one_out_f1` |  | 0.3721 | `closeness_to_outstanding` | yes | 1 |  |
