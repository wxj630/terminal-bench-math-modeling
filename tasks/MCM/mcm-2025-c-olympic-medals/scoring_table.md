# MCM 2025 C: Olympic medal prediction

- Task slug: `mcm-2025-c-olympic-medals`
- Required output: `/root/results/mcm-2025-c-olympic-medals_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Primary evaluation: `B-Eval`
- Secondary evaluation: `BO-Eval`
- Metric count: 96
- Effective scored metric count: 96
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`, score `0.584014166667`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `great_coach_model.global_top_jump_75pct` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `great_coach_model.lang_ping_validation[0].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `great_coach_model.lang_ping_validation[0].estimated_jump_score` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `great_coach_model.lang_ping_validation[0].medal_score` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `great_coach_model.lang_ping_validation[0].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `great_coach_model.lang_ping_validation[1].Year` |  | 2016 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `great_coach_model.lang_ping_validation[1].estimated_jump_score` |  | 1.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `great_coach_model.lang_ping_validation[1].medal_score` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `great_coach_model.lang_ping_validation[1].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `great_coach_model.recommendations[0].benchmark_jump_score` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `great_coach_model.recommendations[0].estimated_medal_count_gain` |  | 1.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `great_coach_model.recommendations[0].latest_medal_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `great_coach_model.recommendations[0].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `great_coach_model.recommendations[0].recent_baseline_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `great_coach_model.recommendations[1].benchmark_jump_score` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `great_coach_model.recommendations[1].estimated_medal_count_gain` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `great_coach_model.recommendations[1].latest_medal_score` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `great_coach_model.recommendations[1].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `great_coach_model.recommendations[1].recent_baseline_score` |  | 0.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `great_coach_model.recommendations[2].benchmark_jump_score` |  | 9.416667 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `great_coach_model.recommendations[2].estimated_medal_count_gain` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `great_coach_model.recommendations[2].latest_medal_score` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `great_coach_model.recommendations[2].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `great_coach_model.recommendations[2].recent_baseline_score` |  | 2.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `great_coach_model.recommendations[3].benchmark_jump_score` |  | 5.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `great_coach_model.recommendations[3].estimated_medal_count_gain` |  | 1.777778 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `great_coach_model.recommendations[3].latest_medal_score` |  | 12 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `great_coach_model.recommendations[3].latest_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `great_coach_model.recommendations[3].recent_baseline_score` |  | 2.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `great_coach_model.top_historical_jump_candidates[0].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `great_coach_model.top_historical_jump_candidates[0].coach_like_jump` |  | 28 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `great_coach_model.top_historical_jump_candidates[0].medal_score` |  | 34 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `great_coach_model.top_historical_jump_candidates[0].prev3_score` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `great_coach_model.top_historical_jump_candidates[10].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `great_coach_model.top_historical_jump_candidates[10].coach_like_jump` |  | 17.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `great_coach_model.top_historical_jump_candidates[10].medal_score` |  | 31 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `great_coach_model.top_historical_jump_candidates[10].prev3_score` |  | 13.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `great_coach_model.top_historical_jump_candidates[11].Year` |  | 2020 | `closeness_to_outstanding` | yes | 1 |  |
| 39 | `great_coach_model.top_historical_jump_candidates[11].coach_like_jump` |  | 17 | `closeness_to_outstanding` | yes | 1 |  |
| 40 | `great_coach_model.top_historical_jump_candidates[11].medal_score` |  | 17 | `closeness_to_outstanding` | yes | 1 |  |
| 41 | `great_coach_model.top_historical_jump_candidates[11].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 42 | `great_coach_model.top_historical_jump_candidates[1].Year` |  | 2000 | `closeness_to_outstanding` | yes | 1 |  |
| 43 | `great_coach_model.top_historical_jump_candidates[1].coach_like_jump` |  | 23.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 44 | `great_coach_model.top_historical_jump_candidates[1].medal_score` |  | 37 | `closeness_to_outstanding` | yes | 1 |  |
| 45 | `great_coach_model.top_historical_jump_candidates[1].prev3_score` |  | 13.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 46 | `great_coach_model.top_historical_jump_candidates[2].Year` |  | 2004 | `closeness_to_outstanding` | yes | 1 |  |
| 47 | `great_coach_model.top_historical_jump_candidates[2].coach_like_jump` |  | 23 | `closeness_to_outstanding` | yes | 1 |  |
| 48 | `great_coach_model.top_historical_jump_candidates[2].medal_score` |  | 38 | `closeness_to_outstanding` | yes | 1 |  |
| 49 | `great_coach_model.top_historical_jump_candidates[2].prev3_score` |  | 15 | `closeness_to_outstanding` | yes | 1 |  |
| 50 | `great_coach_model.top_historical_jump_candidates[3].Year` |  | 2008 | `closeness_to_outstanding` | yes | 1 |  |
| 51 | `great_coach_model.top_historical_jump_candidates[3].coach_like_jump` |  | 22.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 52 | `great_coach_model.top_historical_jump_candidates[3].medal_score` |  | 33 | `closeness_to_outstanding` | yes | 1 |  |
| 53 | `great_coach_model.top_historical_jump_candidates[3].prev3_score` |  | 10.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 54 | `great_coach_model.top_historical_jump_candidates[4].Year` |  | 2000 | `closeness_to_outstanding` | yes | 1 |  |
| 55 | `great_coach_model.top_historical_jump_candidates[4].coach_like_jump` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 56 | `great_coach_model.top_historical_jump_candidates[4].medal_score` |  | 30 | `closeness_to_outstanding` | yes | 1 |  |
| 57 | `great_coach_model.top_historical_jump_candidates[4].prev3_score` |  | 8 | `closeness_to_outstanding` | yes | 1 |  |
| 58 | `great_coach_model.top_historical_jump_candidates[5].Year` |  | 1996 | `closeness_to_outstanding` | yes | 1 |  |
| 59 | `great_coach_model.top_historical_jump_candidates[5].coach_like_jump` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 60 | `great_coach_model.top_historical_jump_candidates[5].medal_score` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 61 | `great_coach_model.top_historical_jump_candidates[5].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 62 | `great_coach_model.top_historical_jump_candidates[6].Year` |  | 1996 | `closeness_to_outstanding` | yes | 1 |  |
| 63 | `great_coach_model.top_historical_jump_candidates[6].coach_like_jump` |  | 20.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 64 | `great_coach_model.top_historical_jump_candidates[6].medal_score` |  | 22 | `closeness_to_outstanding` | yes | 1 |  |
| 65 | `great_coach_model.top_historical_jump_candidates[6].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 66 | `great_coach_model.top_historical_jump_candidates[7].Year` |  | 1996 | `closeness_to_outstanding` | yes | 1 |  |
| 67 | `great_coach_model.top_historical_jump_candidates[7].coach_like_jump` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 68 | `great_coach_model.top_historical_jump_candidates[7].medal_score` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 69 | `great_coach_model.top_historical_jump_candidates[7].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 70 | `great_coach_model.top_historical_jump_candidates[8].Year` |  | 2020 | `closeness_to_outstanding` | yes | 1 |  |
| 71 | `great_coach_model.top_historical_jump_candidates[8].coach_like_jump` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 72 | `great_coach_model.top_historical_jump_candidates[8].medal_score` |  | 18 | `closeness_to_outstanding` | yes | 1 |  |
| 73 | `great_coach_model.top_historical_jump_candidates[8].prev3_score` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 74 | `great_coach_model.top_historical_jump_candidates[9].Year` |  | 2000 | `closeness_to_outstanding` | yes | 1 |  |
| 75 | `great_coach_model.top_historical_jump_candidates[9].coach_like_jump` |  | 17.666667 | `closeness_to_outstanding` | yes | 1 |  |
| 76 | `great_coach_model.top_historical_jump_candidates[9].medal_score` |  | 19 | `closeness_to_outstanding` | yes | 1 |  |
| 77 | `great_coach_model.top_historical_jump_candidates[9].prev3_score` |  | 1.333333 | `closeness_to_outstanding` | yes | 1 |  |
| 78 | `host_effect_model.Gold.event_count_coefficient` |  | 0.000147 | `closeness_to_outstanding` | yes | 1 |  |
| 79 | `host_effect_model.Gold.host_bonus_coefficient` |  | 14.341156 | `closeness_to_outstanding` | yes | 1 |  |
| 80 | `host_effect_model.Gold.prev3_coefficient` |  | 0.950866 | `closeness_to_outstanding` | yes | 1 |  |
| 81 | `host_effect_model.Gold.r2` |  | 0.752918 | `closeness_to_outstanding` | yes | 1 |  |
| 82 | `host_effect_model.Total.event_count_coefficient` |  | -0.000215 | `closeness_to_outstanding` | yes | 1 |  |
| 83 | `host_effect_model.Total.host_bonus_coefficient` |  | 36.422317 | `closeness_to_outstanding` | yes | 1 |  |
| 84 | `host_effect_model.Total.prev3_coefficient` |  | 0.952921 | `closeness_to_outstanding` | yes | 1 |  |
| 85 | `host_effect_model.Total.r2` |  | 0.765819 | `closeness_to_outstanding` | yes | 1 |  |
| 86 | `model_evaluation.holdout_year` |  | 2024 | `closeness_to_outstanding` | yes | 1 |  |
| 87 | `model_evaluation.mean_accuracy_2024` |  | 0.850591 | `closeness_to_outstanding` | yes | 1 |  |
| 88 | `model_evaluation.mean_brier_2024` |  | 0.142806 | `closeness_to_outstanding` | yes | 1 |  |
| 89 | `model_evaluation.mean_f1_2024` |  | 0.287348 | `closeness_to_outstanding` | yes | 1 |  |
| 90 | `model_evaluation.sport_models` |  | 50 | `closeness_to_outstanding` | yes | 1 |  |
| 91 | `model_evaluation.status_counts.GoldBinary:fallback_mean` |  | 7 | `closeness_to_outstanding` | yes | 1 |  |
| 92 | `model_evaluation.status_counts.GoldBinary:random_forest` |  | 43 | `closeness_to_outstanding` | yes | 1 |  |
| 93 | `model_evaluation.status_counts.MedalBinary:fallback_mean` |  | 7 | `closeness_to_outstanding` | yes | 1 |  |
| 94 | `model_evaluation.status_counts.MedalBinary:random_forest` |  | 43 | `closeness_to_outstanding` | yes | 1 |  |
| 95 | `monte_carlo.simulations` |  | 500 | `closeness_to_outstanding` | yes | 1 |  |
| 96 | `monte_carlo.weight_power` |  | 4 | `closeness_to_outstanding` | yes | 1 |  |
