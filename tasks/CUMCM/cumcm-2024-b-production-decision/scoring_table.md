# CUMCM 2024 B: production-process decision optimization

- Task slug: `cumcm-2024-b-production-decision`
- Required output: `/root/results/cumcm-2024-b-production-decision_result.json`
- Scoring version: `tb-mathmodeling-v2-legacy-baseline-panel`
- Metric count: 69
- Effective scored metric count: 69
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`, score `0`
- Outstanding endpoint: `outstanding_paper_reproduction`, score `1`

| # | Metric path | Baseline value | Outstanding value | Direction | Scored | Weight | Baseline source |
|---:|---|---:|---:|---|---|---:|---|
| 1 | `experiment_result.q1_sampling[0].c` |  | 36 | `closeness_to_outstanding` | yes | 1 |  |
| 2 | `experiment_result.q1_sampling[0].false_alarm` |  | 0.046596 | `closeness_to_outstanding` | yes | 1 |  |
| 3 | `experiment_result.q1_sampling[0].n` |  | 270 | `closeness_to_outstanding` | yes | 1 |  |
| 4 | `experiment_result.q1_sampling[0].power` |  | 0.801472 | `closeness_to_outstanding` | yes | 1 |  |
| 5 | `experiment_result.q1_sampling[1].accept_bad` |  | 0.195466 | `closeness_to_outstanding` | yes | 1 |  |
| 6 | `experiment_result.q1_sampling[1].accept_good` |  | 0.903863 | `closeness_to_outstanding` | yes | 1 |  |
| 7 | `experiment_result.q1_sampling[1].c` |  | 25 | `closeness_to_outstanding` | yes | 1 |  |
| 8 | `experiment_result.q1_sampling[1].n` |  | 199 | `closeness_to_outstanding` | yes | 1 |  |
| 9 | `experiment_result.q2.best_decisions[0].case` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 10 | `experiment_result.q2.best_decisions[0].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 11 | `experiment_result.q2.best_decisions[0].expected_profit` |  | 26.374 | `closeness_to_outstanding` | yes | 1 |  |
| 12 | `experiment_result.q2.best_decisions[0].good_probability` |  | 0.729 | `closeness_to_outstanding` | yes | 1 |  |
| 13 | `experiment_result.q2.best_decisions[0].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 14 | `experiment_result.q2.best_decisions[0].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 15 | `experiment_result.q2.best_decisions[0].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 16 | `experiment_result.q2.best_decisions[1].case` |  | 2 | `closeness_to_outstanding` | yes | 1 |  |
| 17 | `experiment_result.q2.best_decisions[1].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 18 | `experiment_result.q2.best_decisions[1].expected_profit` |  | 25.072 | `closeness_to_outstanding` | yes | 1 |  |
| 19 | `experiment_result.q2.best_decisions[1].good_probability` |  | 0.512 | `closeness_to_outstanding` | yes | 1 |  |
| 20 | `experiment_result.q2.best_decisions[1].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 21 | `experiment_result.q2.best_decisions[1].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 22 | `experiment_result.q2.best_decisions[1].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 23 | `experiment_result.q2.best_decisions[2].case` |  | 3 | `closeness_to_outstanding` | yes | 1 |  |
| 24 | `experiment_result.q2.best_decisions[2].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 25 | `experiment_result.q2.best_decisions[2].expected_profit` |  | 19.87 | `closeness_to_outstanding` | yes | 1 |  |
| 26 | `experiment_result.q2.best_decisions[2].good_probability` |  | 0.729 | `closeness_to_outstanding` | yes | 1 |  |
| 27 | `experiment_result.q2.best_decisions[2].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 28 | `experiment_result.q2.best_decisions[2].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 29 | `experiment_result.q2.best_decisions[2].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 30 | `experiment_result.q2.best_decisions[3].case` |  | 4 | `closeness_to_outstanding` | yes | 1 |  |
| 31 | `experiment_result.q2.best_decisions[3].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 32 | `experiment_result.q2.best_decisions[3].expected_profit` |  | 14.95 | `closeness_to_outstanding` | yes | 1 |  |
| 33 | `experiment_result.q2.best_decisions[3].good_probability` |  | 0.64 | `closeness_to_outstanding` | yes | 1 |  |
| 34 | `experiment_result.q2.best_decisions[3].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 35 | `experiment_result.q2.best_decisions[3].inspect_part1` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 36 | `experiment_result.q2.best_decisions[3].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 37 | `experiment_result.q2.best_decisions[4].case` |  | 5 | `closeness_to_outstanding` | yes | 1 |  |
| 38 | `experiment_result.q2.best_decisions[4].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 39 | `experiment_result.q2.best_decisions[4].expected_profit` |  | 24.48 | `closeness_to_outstanding` | yes | 1 |  |
| 40 | `experiment_result.q2.best_decisions[4].good_probability` |  | 0.648 | `closeness_to_outstanding` | yes | 1 |  |
| 41 | `experiment_result.q2.best_decisions[4].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 42 | `experiment_result.q2.best_decisions[4].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 43 | `experiment_result.q2.best_decisions[4].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 44 | `experiment_result.q2.best_decisions[5].case` |  | 6 | `closeness_to_outstanding` | yes | 1 |  |
| 45 | `experiment_result.q2.best_decisions[5].dismantle_bad_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 46 | `experiment_result.q2.best_decisions[5].expected_profit` |  | 26.5738 | `closeness_to_outstanding` | yes | 1 |  |
| 47 | `experiment_result.q2.best_decisions[5].good_probability` |  | 0.85737 | `closeness_to_outstanding` | yes | 1 |  |
| 48 | `experiment_result.q2.best_decisions[5].inspect_final` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 49 | `experiment_result.q2.best_decisions[5].inspect_part1` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 50 | `experiment_result.q2.best_decisions[5].inspect_part2` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 51 | `experiment_result.q2.best_profit_mean` |  | 22.8866 | `closeness_to_outstanding` | yes | 1 |  |
| 52 | `experiment_result.q3.best_expected_profit` |  | 88 | `closeness_to_outstanding` | yes | 1 |  |
| 53 | `experiment_result.q3.decision_bits[0]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 54 | `experiment_result.q3.decision_bits[10]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 55 | `experiment_result.q3.decision_bits[11]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 56 | `experiment_result.q3.decision_bits[12]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 57 | `experiment_result.q3.decision_bits[13]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 58 | `experiment_result.q3.decision_bits[14]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 59 | `experiment_result.q3.decision_bits[15]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 60 | `experiment_result.q3.decision_bits[1]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 61 | `experiment_result.q3.decision_bits[2]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 62 | `experiment_result.q3.decision_bits[3]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 63 | `experiment_result.q3.decision_bits[4]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 64 | `experiment_result.q3.decision_bits[5]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 65 | `experiment_result.q3.decision_bits[6]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 66 | `experiment_result.q3.decision_bits[7]` |  | 0 | `closeness_to_outstanding` | yes | 1 |  |
| 67 | `experiment_result.q3.decision_bits[8]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 68 | `experiment_result.q3.decision_bits[9]` |  | 1 | `closeness_to_outstanding` | yes | 1 |  |
| 69 | `experiment_result.q3.generations` |  | 70 | `closeness_to_outstanding` | yes | 1 |  |
