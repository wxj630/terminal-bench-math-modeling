# MCM 2023 C: predicting Wordle results

- Task slug: `mcm-2023-c-wordle`
- Required output: `/root/results/mcm-2023-c-wordle_result.json`
- Scoring version: `tb-mathmodeling-v5-final-question-endpoint-target-minmax`
- Scoring scope: `final_question_only`
- Final question: 在给纽约时报编辑的总结信之前，最后一个可量化核心是判断 EERIE 的难度，并给出难度分类模型准确率。
- Final answer: O 奖复现把 EERIE 判为中等难度组 2，难度分类模型 holdout accuracy 为 0.7。
- Baseline model: baseline 用报告量时间序列、单词属性特征和分类模型来预测 Wordle 分布及难度等级。
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Candidate metric count before final-question filter: 23
- Final-answer numeric field count: 2
- Scored final-answer numeric field count: 1
- Baseline endpoint: `question_result_minmax_endpoint`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction_metric_values`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `target_comparison.eerie_group.actual` | 2 | 2 | `exact_value` | no: exact value | 0 | `difficulty_model.eerie_classifier_class` |
| 2 | `target_comparison.lightgbm_like_accuracy.actual` | 0.422222 | 0.7 | `higher_is_better` | yes | 1 | `difficulty_model.holdout_accuracy` |
