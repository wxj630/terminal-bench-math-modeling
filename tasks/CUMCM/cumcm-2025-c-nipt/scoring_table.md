# CUMCM 2025 C: NIPT timing and fetal abnormality modeling

- Task slug: `cumcm-2025-c-nipt`
- Required output: `/root/results/cumcm-2025-c-nipt_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 8
- Effective scored metric count: 8
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.earliest_recommended_week` |  | 12 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.female_loo_accuracy` |  | 0.8659 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.latest_recommended_week` |  | 20 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.male_pseudo_r2` |  | 0.90064 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `male_lmm.mother_count` |  | 267 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `male_lmm.pseudo_r2` |  | 0.90064 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `male_lmm.residual_sigma_logit` |  | 0.47707 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `male_lmm.rmse_fetal_fraction` |  | 0.01056 | `closeness_to_outstanding` | yes | 1 |  |
