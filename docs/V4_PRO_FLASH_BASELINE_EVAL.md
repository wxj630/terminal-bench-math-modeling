# DeepSeek v4-pro vs v4-flash Baseline Evaluation

This report treats the saved `terminus2-deepseek-v4-flash-current-*` jobs as the model baseline. Both models are rescored with the current final-question `score_config.json` panels.

Definitions:
- `raw_panel_score(model)` is the verifier's current final-question raw panel score for that model artifact.
- `B-Eval vs flash = raw_panel_score(v4-pro) - raw_panel_score(v4-flash)`. Negative means v4-pro is worse than v4-flash on that task.
- `BO-Eval vs flash = clamp((raw_panel_score(v4-pro) - raw_panel_score(v4-flash)) / (raw_panel_score(O) - raw_panel_score(v4-flash)), 0, 1)`. It is `N/A` when the flash baseline is already at or above the O reference on the raw panel.

- Total tasks: 18
- v4-pro tasks with scoreable artifacts: 18
- Mean v4-flash raw panel score: 0.227447416838
- Mean v4-pro raw panel score: 0.266889840703
- Mean v4-pro B-Eval vs flash: 0.0394424238643
- Mean v4-pro BO-Eval vs flash: 0.0925400106564

## Summary

| Contest | Year | Problem | Task | flash raw | pro raw | pro B-Eval vs flash | pro BO-Eval vs flash | O raw | flash covered | pro covered | flash status | pro status | pro job |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| CUMCM | 2023 | A | `cumcm-2023-a-heliostat-field` | 0.765139253302 | 0.669593115947 | -0.0955461373555 | 0 | 1 | 5 | 5 | finished | finished | `terminus2-deepseek-v4-pro-current-cumcm-2023-a-heliostat-field` |
| CUMCM | 2023 | B | `cumcm-2023-b-multibeam-lines` | 0.140221367927 | 0.097688447047 | -0.0425329208802 | 0 | 1 | 4 | 4 | finished | finished | `terminus2-deepseek-v4-pro-current-cumcm-2023-b-multibeam-lines` |
| CUMCM | 2023 | C | `cumcm-2023-c-vegetable-pricing` | 0.262879428093 | 0.59791780917 | 0.335038381077 | 0.454523172797 | 1 | 2 | 2 | error: AgentTimeoutError(1) | finished | `terminus2-deepseek-v4-pro-current-cumcm-2023-c-vegetable-pricing` |
| CUMCM | 2024 | A | `cumcm-2024-a-dragon-dance` | 0.107142857143 | 0.254588547414 | 0.147445690271 | 0.165139173103 | 1 | 2 | 2 | error: AgentTimeoutError(1) | finished | `terminus2-deepseek-v4-pro-current-cumcm-2024-a-dragon-dance` |
| CUMCM | 2024 | B | `cumcm-2024-b-production-decision` | 0.691799203783 | 0.318573475248 | -0.373225728535 | 0 | 1 | 6 | 6 | error: AgentTimeoutError(1) | finished | `terminus2-deepseek-v4-pro-current-cumcm-2024-b-production-decision` |
| CUMCM | 2024 | C | `cumcm-2024-c-crop-planting` | 0.31433102394 | 0.187791731498 | -0.126539292441 | 0 | 1 | 2 | 2 | error: AgentTimeoutError(1) | finished | `terminus2-deepseek-v4-pro-current-cumcm-2024-c-crop-planting` |
| CUMCM | 2025 | A | `cumcm-2025-a-smoke-screen` | 0.351900478688 | 0.383745141873 | 0.0318446631843 | 0.0491354524069 | 1 | 4 | 4 | finished | finished | `terminus2-deepseek-v4-pro-current-cumcm-2025-a-smoke-screen` |
| CUMCM | 2025 | B | `cumcm-2025-b-sic-thickness` | 0.143178654302 | 0.24609940948 | 0.102920755178 | 0.120119270715 | 1 | 2 | 2 | error: AgentTimeoutError(1) | finished | `terminus2-deepseek-v4-pro-current-cumcm-2025-b-sic-thickness` |
| CUMCM | 2025 | C | `cumcm-2025-c-nipt` | 0.471826516941 | 0.562904211432 | 0.0910776944904 | 0.172438975851 | 1 | 2 | 2 | finished | finished | `terminus2-deepseek-v4-pro-current-cumcm-2025-c-nipt` |
| MCM | 2023 | A | `mcm-2023-a-plant-community` | 0.254349744928 | 0.288681354976 | 0.0343316100481 | 0.0460425109689 | 1 | 3 | 3 | error: AgentTimeoutError(1) | finished | `terminus2-deepseek-v4-pro-current-mcm-2023-a-plant-community` |
| MCM | 2023 | B | `mcm-2023-b-maasai-mara` | 0.0303626641468 | 0.0343714362095 | 0.00400877206271 | 0.0041343004384 | 1 | 5 | 5 | finished | finished | `terminus2-deepseek-v4-pro-current-mcm-2023-b-maasai-mara` |
| MCM | 2023 | C | `mcm-2023-c-wordle` | 0 | 0.097977521618 | 0.097977521618 | 0.097977521618 | 1 | 1 | 1 | finished | finished | `terminus2-deepseek-v4-pro-current-mcm-2023-c-wordle` |
| MCM | 2024 | A | `mcm-2024-a-lamprey` | 0.262304068007 | 0.26525648804 | 0.00295242003261 | 0.00400221812886 | 1 | 3 | 3 | finished | finished | `terminus2-deepseek-v4-pro-current-mcm-2024-a-lamprey` |
| MCM | 2024 | B | `mcm-2024-b-submersible-search` | 0.176024881022 | 0.296505161695 | 0.120480280673 | 0.146218347979 | 1 | 2 | 2 | finished | finished | `terminus2-deepseek-v4-pro-current-mcm-2024-b-submersible-search` |
| MCM | 2024 | C | `mcm-2024-c-tennis-momentum` | 0.0300532687642 | 0.0322669308083 | 0.00221366204415 | 0.00228225115139 | 1 | 4 | 4 | finished | finished | `terminus2-deepseek-v4-pro-current-mcm-2024-c-tennis-momentum` |
| MCM | 2025 | A | `mcm-2025-a-stair-wear` | 0 | 0 | 0 | 0 | 1 | 3 | 3 | finished | finished | `terminus2-deepseek-v4-pro-current-mcm-2025-a-stair-wear` |
| MCM | 2025 | B | `mcm-2025-b-juneau-tourism` | 0 | 0.120686546043 | 0.120686546043 | 0.120686546043 | 1 | 6 | 6 | finished | finished | `terminus2-deepseek-v4-pro-current-mcm-2025-b-juneau-tourism` |
| MCM | 2025 | C | `mcm-2025-c-olympic-medals` | 0.092540092102 | 0.349369804149 | 0.256829712047 | 0.283020450614 | 1 | 4 | 4 | error: AgentTimeoutError(1) | finished | `terminus2-deepseek-v4-pro-current-mcm-2025-c-olympic-medals` |

# Per-Task Details

## CUMCM 2023 A: `cumcm-2023-a-heliostat-field`

- Final question: 在定日镜尺寸和安装高度都可以变化时，重新设计镜场，在满足约 60 MW 年平均输出功率的同时，让单位镜面面积输出尽量大。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2023-a-heliostat-field`; status: finished; raw: 0.765139253302
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2023-a-heliostat-field`; status: finished; raw: 0.669593115947
- v4-pro B-Eval vs v4-flash: -0.0955461373555
- v4-pro BO-Eval vs v4-flash-to-O: 0

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `reproduced.design_summary[2].annual_optical_efficiency` | `higher_is_better` | 0.496428083 | 0.487405460719 | 0.562314595999 | 0.868463374329 | 0.47483162122 | -0.393631753109 |
| 2 | `reproduced.design_summary[2].mirror_area_m2` | `lower_is_better` | 119196 | 126248.85 | 111276 | 0.669754270037 | 0.643620812545 | -0.0261334574929 |
| 3 | `reproduced.design_summary[2].mirror_count` | `lower_is_better` | 3311 | 3083 | 3091 | 0.635386682019 | 0.643620812545 | 0.00823413052574 |
| 4 | `reproduced.design_summary[2].unit_area_power_kw_m2` | `higher_is_better` | 0.506192417 | 0.476686026513 | 0.54418534773 | 0.673057503328 | 0.615206988962 | -0.0578505143657 |
| 5 | `target_comparison.q3_annual_thermal_power_mw.actual` | `target_value` | 60.336111 | 60.1810626584 | 60.554768754 | 0.979034436797 | 0.970685344461 | -0.00834909233555 |

## CUMCM 2023 B: `cumcm-2023-b-multibeam-lines`

- Final question: 给定真实海深数据，设计测线方案，尽量减少测线总长度，同时控制漏测面积和重叠过大的测线长度。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2023-b-multibeam-lines`; status: finished; raw: 0.140221367927
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2023-b-multibeam-lines`; status: finished; raw: 0.097688447047
- v4-pro B-Eval vs v4-flash: -0.0425329208802
- v4-pro BO-Eval vs v4-flash-to-O: 0

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles` | `lower_is_better` | 30 | 120.52 | 156.13 | 0.0382490437739 | 0.0277499421876 | -0.0104991015863 |
| 2 | `reproduced.problem4_summary.sa_avg_overlap_pct` | `target_value` | 10.48 | 19.6743495712 | 28.4877550803 | 0.120322050104 | 0.0652778002148 | -0.0550442498895 |
| 3 | `target_comparison.problem4_missed_area_pct.actual` | `lower_is_better` | 3.48 | 2.044 | 4.4408920985e-17 | 0.225291324989 | 0.107142857143 | -0.118148467846 |
| 4 | `target_comparison.problem4_total_length_nm.actual` | `lower_is_better` | 622 | 275 | 305 | 0.177023052841 | 0.190583188643 | 0.0135601358013 |

## CUMCM 2023 C: `cumcm-2023-c-vegetable-pricing`

- Final question: 最后一问本身是让商超说明还应采集哪些数据、这些数据怎样帮助补货和定价；它主要是文字建议。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2023-c-vegetable-pricing`; status: error: AgentTimeoutError(1); raw: 0.262879428093
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2023-c-vegetable-pricing`; status: finished; raw: 0.59791780917
- v4-pro B-Eval vs v4-flash: 0.335038381077
- v4-pro BO-Eval vs v4-flash-to-O: 0.454523172797

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `target_comparison.future_week_max_profit_yuan.actual` | `higher_is_better` | 5105.6 | 14616.69 | 4256.22179053 | 0.060518214474 | 0.419049904054 | 0.35853168958 |
| 2 | `target_comparison.problem3_selected_item_count.actual` | `target_value` | 29 | 33 | 30 | 0.465240641711 | 0.776785714286 | 0.311545072574 |

## CUMCM 2024 A: `cumcm-2024-a-dragon-dance`

- Final question: 沿着前面求出的调头路径行进时，求龙头最大能跑多快，才能保证所有把手速度都不超过 2 m/s。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2024-a-dragon-dance`; status: error: AgentTimeoutError(1); raw: 0.107142857143
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2024-a-dragon-dance`; status: finished; raw: 0.254588547414
- v4-pro B-Eval vs v4-flash: 0.147445690271
- v4-pro BO-Eval vs v4-flash-to-O: 0.165139173103

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.q5.max_head_speed_mps` | `higher_is_better` | 2.00002 | 0 | 1.40627665732 | 0.107142857143 | 0.287860420407 | 0.180717563264 |
| 2 | `experiment_result.q5.max_speed_ratio_when_head_1mps` | `lower_is_better` | 0.99999 | 0 | 1.42219526264 | 0.107142857143 | 0.22131667442 | 0.114173817277 |

## CUMCM 2024 B: `cumcm-2024-b-production-decision`

- Final question: 把零配件和成品次品率看成抽样估出来的不确定量，然后重新求问题 2 和问题 3 的最优检测、装配、拆解决策。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2024-b-production-decision`; status: error: AgentTimeoutError(1); raw: 0.691799203783
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2024-b-production-decision`; status: finished; raw: 0.318573475248
- v4-pro B-Eval vs v4-flash: -0.373225728535
- v4-pro BO-Eval vs v4-flash-to-O: 0

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.q4.posterior_rows[0].q2_best_profit_case1` | `higher_is_better` | 25.9691 | 27.49 | 23.3696063122 | 0.672021343951 | 0.545207985427 | -0.126813358525 |
| 2 | `experiment_result.q4.posterior_rows[0].q3_best_policy_profit_under_posterior` | `higher_is_better` | 86.8529 | 96.721 | 68.983115412 | 0.513657855164 | 0.368383258758 | -0.145274596406 |
| 3 | `experiment_result.q4.posterior_rows[1].q2_best_profit_case1` | `higher_is_better` | 25.8694 | 26.9595 | 18.5078888054 | 0.740107590356 | 0.296615296899 | -0.443492293457 |
| 4 | `experiment_result.q4.posterior_rows[1].q3_best_policy_profit_under_posterior` | `higher_is_better` | 86.5588 | 91.6033 | 59 | 0.673104902707 | 0.273733606115 | -0.399371296592 |
| 5 | `experiment_result.q4.posterior_rows[2].q2_best_profit_case1` | `higher_is_better` | 25.7715 | 26.4072 | 13.860058309 | 0.829492420097 | 0.206116737479 | -0.623375682619 |
| 6 | `experiment_result.q4.posterior_rows[2].q3_best_policy_profit_under_posterior` | `higher_is_better` | 86.2647 | 90.2424 | 49.8571428571 | 0.722411110423 | 0.221383966811 | -0.501027143611 |

## CUMCM 2024 C: `cumcm-2024-c-crop-planting`

- Final question: 在问题 2 的基础上加入作物之间的替代、互补和价格/成本/销量相关性，求 2024-2030 年的稳健种植策略。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2024-c-crop-planting`; status: error: AgentTimeoutError(1); raw: 0.31433102394
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2024-c-crop-planting`; status: finished; raw: 0.187791731498
- v4-pro B-Eval vs v4-flash: -0.126539292441
- v4-pro BO-Eval vs v4-flash-to-O: 0

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.q2_q3.best_correlated_cvar10_profit_yuan` | `higher_is_better` | 118550698.19 | 69059695.53 | 24746820.26 | 0.223269527485 | 0.1316864651 | -0.0915830623854 |
| 2 | `experiment_result.q2_q3.spearman_price_cost` | `target_value` | 0.2551 | 0.3 | 0.35 | 0.405392520394 | 0.243896997897 | -0.161495522497 |

## CUMCM 2025 A: `cumcm-2025-a-smoke-screen`

- Final question: 5 架无人机、每架最多 3 枚烟幕弹，同时对 3 枚导弹实施遮蔽，求总体遮蔽时间尽量长的投放方案。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2025-a-smoke-screen`; status: finished; raw: 0.351900478688
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2025-a-smoke-screen`; status: finished; raw: 0.383745141873
- v4-pro B-Eval vs v4-flash: 0.0318446631843
- v4-pro BO-Eval vs v4-flash-to-O: 0.0491354524069

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.q5_union_duration_s.M1` | `higher_is_better` | 10.3 | 7 | 5.978246 | 0.272486772487 | 0.22239199504 | -0.050094777447 |
| 2 | `experiment_result.q5_union_duration_s.M2` | `higher_is_better` | 6.2 | 7.3 | 8.510027 | 0.403470715835 | 0.24361277749 | -0.159857938345 |
| 3 | `experiment_result.q5_union_duration_s.M3` | `higher_is_better` | 3.4 | 2.45 | 5.060286 | 0.300441826215 | 0.197264788332 | -0.103177037883 |
| 4 | `experiment_result.q5_union_duration_s.total` | `higher_is_better` | 19.9 | 16.75 | 19.54856 | 0.431202600217 | 0.871711006629 | 0.440508406412 |

## CUMCM 2025 B: `cumcm-2025-b-sic-thickness`

- Final question: 把多光束反射/透射造成的干涉也考虑进去，重新确定碳化硅外延层厚度，并分析结果可靠性。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2025-b-sic-thickness`; status: error: AgentTimeoutError(1); raw: 0.143178654302
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2025-b-sic-thickness`; status: finished; raw: 0.24609940948
- v4-pro B-Eval vs v4-flash: 0.102920755178
- v4-pro BO-Eval vs v4-flash-to-O: 0.120119270715

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.si_recommended_thickness_um` | `target_value` | 10.5145 | 4.82505875455 | 7.87019059675 | 0.181514472929 | 0.323022028075 | 0.141507555146 |
| 2 | `experiment_result.sic_recommended_thickness_um` | `target_value` | 8.9815 | 18.1836785023 | 14.2744520275 | 0.104842835674 | 0.169176790884 | 0.0643339552097 |

## CUMCM 2025 C: `cumcm-2025-c-nipt`

- Final question: 对女胎样本，用染色体 Z 值、GC 含量、读段数、BMI 等指标判断胎儿是否异常。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-cumcm-2025-c-nipt`; status: finished; raw: 0.471826516941
- v4-pro job: `terminus2-deepseek-v4-pro-current-cumcm-2025-c-nipt`; status: finished; raw: 0.562904211432
- v4-pro B-Eval vs v4-flash: 0.0910776944904
- v4-pro BO-Eval vs v4-flash-to-O: 0.172438975851

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.female_loo_accuracy` | `higher_is_better` | 0.8659 | 0.9174 | 0.912396694215 | 0.668614228354 | 0.690856096895 | 0.0222418685414 |
| 2 | `female_abnormality.leave_one_out_f1` | `higher_is_better` | 0.3721 | 0.489796 | 0.430107526882 | 0.275038805529 | 0.434952325968 | 0.159913520439 |

## MCM 2023 A: `mcm-2023-a-plant-community`

- Final question: 综合物种数、干旱、污染和栖息地压力，说明怎样保证植物群落长期可生存。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2023-a-plant-community`; status: error: AgentTimeoutError(1); raw: 0.254349744928
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2023-a-plant-community`; status: finished; raw: 0.288681354976
- v4-pro B-Eval vs v4-flash: 0.0343316100481
- v4-pro BO-Eval vs v4-flash-to-O: 0.0460425109689

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `target_comparison.beta_decline_pct.actual` | `lower_is_better` | 32 | 7.04 | 12.453032 | 0.133333333333 | 0.164194007534 | 0.0308606742011 |
| 2 | `target_comparison.five_species_pielou_evenness.actual` | `higher_is_better` | 0.8826 | 0.9673 | 0.810421 | 0.555641827377 | 0.594707200252 | 0.0390653728745 |
| 3 | `target_comparison.optimal_species_count.actual` | `target_value` | 2 | 5 | 4 | 0.0740740740741 | 0.107142857143 | 0.0330687830688 |

## MCM 2023 B: `mcm-2023-b-maasai-mara`

- Final question: 把土地分区和政策方案整理成给当地管理者的非技术报告，说明推荐方案的收益和用地分配。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2023-b-maasai-mara`; status: finished; raw: 0.0303626641468
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2023-b-maasai-mara`; status: finished; raw: 0.0343714362095
- v4-pro B-Eval vs v4-flash: 0.00400877206271
- v4-pro BO-Eval vs v4-flash-to-O: 0.0041343004384

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `target_comparison.scenario2_agriculture_cells.actual` | `target_value` | 12 | 100 | 60 | 0.0161001788909 | 0.0291262135922 | 0.0130260347014 |
| 2 | `target_comparison.scenario2_benefit_million.actual` | `higher_is_better` | 154948.974 | 104.24 | 22.16 | 0.107207252097 | 0.107156540155 | -5.0711942233e-05 |
| 3 | `target_comparison.scenario2_hunting_cells.actual` | `target_value` | 2 | 40 | 16 | 0.00627615062762 | 0.0168539325843 | 0.0105777819567 |
| 4 | `target_comparison.scenario2_tourism_cells.actual` | `target_value` | 9 | 100 | 104 | 0.011728931364 | 0.011240632806 | -0.000488298558036 |
| 5 | `target_comparison.scenario2_wildlife_cells.actual` | `target_value` | 13 | 160 | 220 | 0.0105008077544 | 0.00747986191024 | -0.0030209458442 |

## MCM 2023 C: `mcm-2023-c-wordle`

- Final question: 在给纽约时报编辑的总结信之前，最后一个可量化核心是判断 EERIE 的难度，并给出难度分类模型准确率。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2023-c-wordle`; status: finished; raw: 0
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2023-c-wordle`; status: finished; raw: 0.097977521618
- v4-pro B-Eval vs v4-flash: 0.097977521618
- v4-pro BO-Eval vs v4-flash-to-O: 0.097977521618

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `target_comparison.eerie_group.actual` | `exact_value` | 2 | 3 | 2 | 0 | 0 | 0 |
| 2 | `target_comparison.lightgbm_like_accuracy.actual` | `higher_is_better` | 0.7 | 0.3211 | 0.449438 | 0 | 0.097977521618 | 0.097977521618 |

## MCM 2024 A: `mcm-2024-a-lamprey`

- Final question: 判断七鳃鳗可变性别比例是否也会让生态系统中的其他生物受益，尤其是寄生者/宿主相关指标。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2024-a-lamprey`; status: finished; raw: 0.262304068007
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2024-a-lamprey`; status: finished; raw: 0.26525648804
- v4-pro B-Eval vs v4-flash: 0.00295242003261
- v4-pro BO-Eval vs v4-flash-to-O: 0.00400221812886

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.parasite_coexistence_case.final_parasite_index` | `target_value` | 8.562 | 0.3124 | 1 | 0.110750842941 | 0.119616645555 | 0.00886580261419 |
| 2 | `experiment_result.parasite_coexistence_case.host_fish_index` | `higher_is_better` | 1080.356 | 0.5981 | 0.501714285714 | 0.107195843839 | 0.107187301322 | -8.54251637501e-06 |
| 3 | `experiment_result.parasite_coexistence_case.resource_level` | `target_value` | 0.55 | 0.5 | 0.6 | 0.568965517241 | 0.568965517241 | 5.55111512313e-16 |

## MCM 2024 B: `mcm-2024-b-submersible-search`

- Final question: 把潜水器搜索模型迁移到加勒比海场景，并说明洋流、海底地形和多潜水器协同时需要怎样调整。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2024-b-submersible-search`; status: finished; raw: 0.176024881022
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2024-b-submersible-search`; status: finished; raw: 0.296505161695
- v4-pro B-Eval vs v4-flash: 0.120480280673
- v4-pro BO-Eval vs v4-flash-to-O: 0.146218347979

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.caribbean_adaptation.current_multiplier` | `target_value` | 1.35 | 2 | 1.9 | 0.199507389163 | 0.227528089888 | 0.0280207007251 |
| 2 | `experiment_result.caribbean_adaptation.terrain_uncertainty_multiplier` | `target_value` | 1.2 | 2 | 1.45 | 0.152542372881 | 0.365482233503 | 0.212939860621 |

## MCM 2024 C: `mcm-2024-c-tennis-momentum`

- Final question: 把势头模型转成教练能用的赛中提示：什么时候可能发生势头转换，应重点监控哪些指标。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2024-c-tennis-momentum`; status: finished; raw: 0.0300532687642
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2024-c-tennis-momentum`; status: finished; raw: 0.0322669308083
- v4-pro B-Eval vs v4-flash: 0.00221366204415
- v4-pro BO-Eval vs v4-flash-to-O: 0.00228225115139

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.dual_temporal_bayes.final_match_warning_rate` | `target_value` | 0.006 | 0.9632 | 0.253048780488 | 0.000751628528478 | 0.00290593511653 | 0.00215430658805 |
| 2 | `experiment_result.top_swing_features[0].warning_correlation` | `target_value` | 0.0302 | 0.1074 | -0.0651453098248 | 0.0448381668811 | 0.0366174120686 | -0.00822075481253 |
| 3 | `experiment_result.top_swing_features[1].warning_correlation` | `target_value` | -0.0223 | 0.0809 | -0.0605062626639 | 0.0252748498243 | 0.0654562596498 | 0.0401814098255 |
| 4 | `experiment_result.top_swing_features[2].warning_correlation` | `target_value` | 0.0154 | 0.051 | -0.0594703273879 | 0.0493484298227 | 0.0240881163983 | -0.0252603134244 |

## MCM 2025 A: `mcm-2025-a-stair-wear`

- Final question: 根据楼梯磨损反推典型一天大约多少人使用，以及这些人是短时间集中经过还是长时间稀疏经过。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2025-a-stair-wear`; status: finished; raw: 0
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2025-a-stair-wear`; status: finished; raw: 0
- v4-pro B-Eval vs v4-flash: 0
- v4-pro BO-Eval vs v4-flash-to-O: 0

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `daily_use_pattern.peak_period_users` | `target_value` | 27.6 | 23.6 | 28.72 | 0 | 0 | 0 |
| 2 | `daily_use_pattern.regular_hour_users_if_spread_over_10_hours` | `target_value` | 4.6 | 7.1 | 4.42 | 0 | 0 | 0 |
| 3 | `experiment_result.estimated_daily_users` | `target_value` | 73.52 | 117.9 | 44.18 | 0 | 0 | 0 |

## MCM 2025 B: `mcm-2025-b-juneau-tourism`

- Final question: 给朱诺旅游委员会写一页备忘录，概括预测、各种限制/收费措施的效果，并推荐最优可持续旅游政策。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2025-b-juneau-tourism`; status: finished; raw: 0
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2025-b-juneau-tourism`; status: finished; raw: 0.120686546043
- v4-pro B-Eval vs v4-flash: 0.120686546043
- v4-pro BO-Eval vs v4-flash-to-O: 0.120686546043

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `experiment_result.annual_visitors` | `higher_is_better` | 1491526 | 1111429 | 1600000 | 0 | 0 | 0 |
| 2 | `experiment_result.optimal_daily_cap` | `target_value` | 11000 | 4000 | 16000 | 0 | 0 | 0 |
| 3 | `experiment_result.optimal_visitor_fee_usd` | `target_value` | 55 | 15 | 30 | 0 | 0 | 0 |
| 4 | `experiment_result.resident_acceptance_index` | `higher_is_better` | 1 | 0.764 | 75.8 | 0 | 0 | 0 |
| 5 | `experiment_result.sustainability_score` | `higher_is_better` | 1.007 | 0.5827 | 68.5976 | 0 | 0 | 0 |
| 6 | `experiment_result.total_revenue_usd` | `higher_is_better` | 431610327.83 | 277162606 | 423000000 | 0 | 0.724119276257 | 0.724119276257 |

## MCM 2025 C: `mcm-2025-c-olympic-medals`

- Final question: 说明模型还能发现哪些原创奖牌规律，以及这些规律怎样指导国家奥委会分配项目和教练资源。
- v4-flash baseline job: `terminus2-deepseek-v4-flash-current-mcm-2025-c-olympic-medals`; status: error: AgentTimeoutError(1); raw: 0.092540092102
- v4-pro job: `terminus2-deepseek-v4-pro-current-mcm-2025-c-olympic-medals`; status: finished; raw: 0.349369804149
- v4-pro B-Eval vs v4-flash: 0.256829712047
- v4-pro BO-Eval vs v4-flash-to-O: 0.283020450614

| # | Metric path | Semantic direction | O answer | v4-flash answer | v4-pro answer | flash metric score | pro metric score | score gain |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `great_coach_model.global_top_jump_75pct` | `higher_is_better` | 6 | 17.7 | 0 | 0.0579710144928 | 0.107142857143 | 0.0491718426501 |
| 2 | `great_coach_model.recommendations[0].estimated_medal_count_gain` | `higher_is_better` | 1.666667 | 0.4 | 2 | 0.136363628926 | 0.37500028125 | 0.238636652325 |
| 3 | `great_coach_model.recommendations[1].estimated_medal_count_gain` | `higher_is_better` | 2 | 3.5 | 2 | 0.137931034483 | 1 | 0.862068965517 |
| 4 | `great_coach_model.recommendations[2].estimated_medal_count_gain` | `higher_is_better` | 3 | 0.6 | 2 | 0.130434782609 | 0.264705882353 | 0.134271099744 |
| 5 | `great_coach_model.recommendations[3].estimated_medal_count_gain` | `higher_is_better` | 1.777778 | N/A | N/A | 0 | 0 | 0 |
