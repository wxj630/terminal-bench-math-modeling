# Evaluation Results

This report is generated from local Harbor jobs and task `score_config.json` files.

- Total tasks: 18
- Default eval method for regenerated tasks: `B-Eval`
- final-question endpoint target-minmax tasks: 3
- legacy fallback tasks: 15
- Oracle jobs found: 18
- Oracle mean reward: 0.789326225894
- DeepSeek/Terminus-2 jobs found: 18
- DeepSeek/Terminus-2 mean job reward: -0.0266351155646
- DeepSeek/Terminus-2 mean B-Eval: -0.0299645050101
- DeepSeek/Terminus-2 mean BO-Eval: 0.124447355263

`B-Eval` is the default baseline-only score: `raw_panel_score - baseline_panel_score`, so negative means worse than the baseline. `BO-Eval` is the optional baseline-to-outstanding normalized score. The current scoring scope is the numeric core of the final contest question. The numeric fields in the table are not all numbers in the report; they are just the small set needed to represent the final answer. `final-question endpoint target-minmax` means the task has real per-metric `baseline_value` and `outstanding_value` endpoints. `final-question legacy fallback` means no semantically comparable per-metric question-result endpoint has been mapped yet, so the task still uses the older baseline-panel normalization.

| Contest | Year | Problem | Task | Scoring status | Default eval | Final fields | Scored fields | Exact-value | Missing baseline | Baseline kind | Oracle reward | Oracle status | DeepSeek job reward | DeepSeek B-Eval | DeepSeek BO-Eval | DeepSeek status |
|---|---:|---|---|---|---|---:|---:|---:|---:|---|---:|---|---:|---:|---:|---|
| CUMCM | 2023 | A | `cumcm-2023-a-heliostat-field` | final-question legacy fallback | B-Eval | 5 | 5 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0 | 0 | 0 | error: AgentTimeoutError(1) |
| CUMCM | 2023 | B | `cumcm-2023-b-multibeam-lines` | final-question legacy fallback | B-Eval | 4 | 4 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0 |  |  | error: CancelledError(1) |
| CUMCM | 2023 | C | `cumcm-2023-c-vegetable-pricing` | final-question legacy fallback | B-Eval | 2 | 2 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.262879428093 | 0.262879428093 | 0.262879428093 | error: AgentTimeoutError(1) |
| CUMCM | 2024 | A | `cumcm-2024-a-dragon-dance` | final-question legacy fallback | B-Eval | 2 | 2 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.107142857143 | 0.107142857143 | 0.107142857143 | error: AgentTimeoutError(1) |
| CUMCM | 2024 | B | `cumcm-2024-b-production-decision` | final-question legacy fallback | B-Eval | 6 | 6 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.691799203783 | 0.691799203783 | 0.691799203783 | error: AgentTimeoutError(1) |
| CUMCM | 2024 | C | `cumcm-2024-c-crop-planting` | final-question legacy fallback | B-Eval | 2 | 2 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.31433102394 | 0.31433102394 | 0.31433102394 | error: AgentTimeoutError(1) |
| CUMCM | 2025 | A | `cumcm-2025-a-smoke-screen` | final-question legacy fallback | B-Eval | 4 | 4 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0 |  |  | error: AgentTimeoutError(1) |
| CUMCM | 2025 | B | `cumcm-2025-b-sic-thickness` | final-question legacy fallback | B-Eval | 2 | 2 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 1 | scored | 0.143178654302 | 0.143178654302 | 0.143178654302 | error: AgentTimeoutError(1) |
| CUMCM | 2025 | C | `cumcm-2025-c-nipt` | final-question legacy fallback | B-Eval | 2 | 2 |  |  | `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match` | 0.52409654943 | scored | 0.471826516941 | 0.471826516941 | 0.471826516941 | scored |
| MCM | 2023 | A | `mcm-2023-a-plant-community` | final-question legacy fallback | B-Eval | 3 | 3 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 0.497195333333 | scored | -0.248454921739 | -0.248454921739 | 0 | error: AgentTimeoutError(1) |
| MCM | 2023 | B | `mcm-2023-b-maasai-mara` | final-question legacy fallback | B-Eval | 5 | 5 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 0.39734275 | scored | -0.572294585853 | -0.572294585853 | 0 | scored |
| MCM | 2023 | C | `mcm-2023-c-wordle` | final-question endpoint target-minmax | B-Eval | 2 | 1 | 1 | 0 | `question_result_minmax_endpoint` | 1 | scored | 0 | 0 | 0 | scored |
| MCM | 2024 | A | `mcm-2024-a-lamprey` | final-question legacy fallback | B-Eval | 3 | 3 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 0.54316425 | scored | -0.194531681993 | -0.194531681993 | 0 | scored |
| MCM | 2024 | B | `mcm-2024-b-submersible-search` | final-question legacy fallback | B-Eval | 2 | 2 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 0.42137875 | scored | -0.402596368978 | -0.402596368978 | 0 | scored |
| MCM | 2024 | C | `mcm-2024-c-tennis-momentum` | final-question legacy fallback | B-Eval | 4 | 4 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 0.4087086 | scored | -0.561238131236 | -0.561238131236 | 0 | scored |
| MCM | 2025 | A | `mcm-2025-a-stair-wear` | final-question endpoint target-minmax | B-Eval | 3 | 3 | 0 | 0 | `question_result_minmax_endpoint` | 1 | scored | 0 | 0 | 0 | scored |
| MCM | 2025 | B | `mcm-2025-b-juneau-tourism` | final-question endpoint target-minmax | B-Eval | 6 | 6 | 0 | 0 | `question_result_minmax_endpoint` | 1 | scored | 0 | 0 | 0 | scored |
| MCM | 2025 | C | `mcm-2025-c-olympic-medals` | final-question legacy fallback | B-Eval | 5 | 5 |  |  | `legacy_explicit_generic_baseline_score_mean_no_question_metric_match` | 0.415985833333 | scored | -0.491474074565 | -0.491474074565 | 0 | error: AgentTimeoutError(1) |

# Per-Task Tables

## CUMCM 2023 A: `cumcm-2023-a-heliostat-field`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 在定日镜尺寸和安装高度都可以变化时，重新设计镜场，在满足约 60 MW 年平均输出功率的同时，让单位镜面面积输出尽量大。
- Final answer: O 奖复现给出的核心设计是年平均热功率 60.336111 MW，单位面积功率 0.506192417 kW/m2，年平均光学效率 0.496428083，镜面总面积 119196 m2，定日镜 3311 面。
- Baseline model: baseline 用几何解析和太阳运动参数方程做一个简化镜场拟合，再从几何约束中估计设计参数。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 5 total, 5 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.design_summary[2].annual_optical_efficiency` |  | 0.496428083 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 2 | `reproduced.design_summary[2].mirror_area_m2` |  | 119196 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 3 | `reproduced.design_summary[2].mirror_count` |  | 3311 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 4 | `reproduced.design_summary[2].unit_area_power_kw_m2` |  | 0.506192417 | `closeness_to_outstanding` |  | 0 |  | yes |  |
| 5 | `target_comparison.q3_annual_thermal_power_mw.actual` |  | 60.336111 | `closeness_to_outstanding` |  | 0 |  | yes |  |
## CUMCM 2023 B: `cumcm-2023-b-multibeam-lines`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 给定真实海深数据，设计测线方案，尽量减少测线总长度，同时控制漏测面积和重叠过大的测线长度。
- Final answer: O 奖复现的核心方案总测线长度 622.0 海里，漏测面积 3.48%，重叠超过 20% 的测线长度 30.0 海里，平均重叠率约 10.48%。
- Baseline model: baseline 先用数据拟合近似海底地形，再用规则化/贪心测线布置估计覆盖质量。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 4 total, 4 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: CancelledError(1))
- DeepSeek/Terminus-2 B-Eval: N/A
- DeepSeek/Terminus-2 BO-Eval: N/A

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles` |  | 30 | `closeness_to_outstanding` |  |  |  | yes |  |
| 2 | `reproduced.problem4_summary.sa_avg_overlap_pct` |  | 10.48 | `closeness_to_outstanding` |  |  |  | yes |  |
| 3 | `target_comparison.problem4_missed_area_pct.actual` |  | 3.48 | `closeness_to_outstanding` |  |  |  | yes |  |
| 4 | `target_comparison.problem4_total_length_nm.actual` |  | 622 | `closeness_to_outstanding` |  |  |  | yes |  |
## CUMCM 2023 C: `cumcm-2023-c-vegetable-pricing`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 最后一问本身是让商超说明还应采集哪些数据、这些数据怎样帮助补货和定价；它主要是文字建议。
- Final answer: 当前数值 verifier 只看支撑这些建议的最后可量化补货定价结果：未来一周最大利润 5105.6 元，并选择 29 个单品进入补货定价方案。
- Baseline model: baseline 用规划优化和资源配置模型，把可售空间、补货量和价格决策转成利润最大化问题。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 2 total, 2 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.262879428093 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.262879428093
- DeepSeek/Terminus-2 BO-Eval: 0.262879428093

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `target_comparison.future_week_max_profit_yuan.actual` |  | 5105.6 | `closeness_to_outstanding` | 14616.69 | 0.060518214474 |  | yes |  |
| 2 | `target_comparison.problem3_selected_item_count.actual` |  | 29 | `closeness_to_outstanding` | 33 | 0.465240641711 |  | yes |  |
## CUMCM 2024 A: `cumcm-2024-a-dragon-dance`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 沿着前面求出的调头路径行进时，求龙头最大能跑多快，才能保证所有把手速度都不超过 2 m/s。
- Final answer: O 奖复现给出的最大龙头速度约 2.00002 m/s；当龙头速度为 1 m/s 时，全队最大速度比例约 0.99999。
- Baseline model: baseline 用几何解析和运动学参数方程，沿路径传播各把手位置，再由速度约束反推龙头速度上限。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 2 total, 2 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.107142857143 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.107142857143
- DeepSeek/Terminus-2 BO-Eval: 0.107142857143

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q5.max_head_speed_mps` |  | 2.00002 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
| 2 | `experiment_result.q5.max_speed_ratio_when_head_1mps` |  | 0.99999 | `closeness_to_outstanding` | 0 | 0.107142857143 |  | yes |  |
## CUMCM 2024 B: `cumcm-2024-b-production-decision`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 把零配件和成品次品率看成抽样估出来的不确定量，然后重新求问题 2 和问题 3 的最优检测、装配、拆解决策。
- Final answer: O 奖复现用 3 组后验缺陷率情景重算利润：Q2 case1 利润约 25.9691、25.8694、25.7715；Q3 最优策略后验利润约 86.8529、86.5588、86.2647。
- Baseline model: baseline 用二项抽样/贝叶斯后验估计次品率，再用期望利润枚举和多阶段决策搜索求最优策略。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 6 total, 6 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.691799203783 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.691799203783
- DeepSeek/Terminus-2 BO-Eval: 0.691799203783

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q4.posterior_rows[0].q2_best_profit_case1` |  | 25.9691 | `closeness_to_outstanding` | 27.49 | 0.672021343951 |  | yes |  |
| 2 | `experiment_result.q4.posterior_rows[0].q3_best_policy_profit_under_posterior` |  | 86.8529 | `closeness_to_outstanding` | 96.721 | 0.513657855164 |  | yes |  |
| 3 | `experiment_result.q4.posterior_rows[1].q2_best_profit_case1` |  | 25.8694 | `closeness_to_outstanding` | 26.9595 | 0.740107590356 |  | yes |  |
| 4 | `experiment_result.q4.posterior_rows[1].q3_best_policy_profit_under_posterior` |  | 86.5588 | `closeness_to_outstanding` | 91.6033 | 0.673104902707 |  | yes |  |
| 5 | `experiment_result.q4.posterior_rows[2].q2_best_profit_case1` |  | 25.7715 | `closeness_to_outstanding` | 26.4072 | 0.829492420097 |  | yes |  |
| 6 | `experiment_result.q4.posterior_rows[2].q3_best_policy_profit_under_posterior` |  | 86.2647 | `closeness_to_outstanding` | 90.2424 | 0.722411110423 |  | yes |  |
## CUMCM 2024 C: `cumcm-2024-c-crop-planting`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 在问题 2 的基础上加入作物之间的替代、互补和价格/成本/销量相关性，求 2024-2030 年的稳健种植策略。
- Final answer: O 奖复现的相关性稳健方案给出 best correlated CVaR10 利润 118550698.19 元，价格和成本的 Spearman 相关系数约 0.2551。
- Baseline model: baseline 用规划优化和资源配置模型，在随机场景下比较候选种植方案的收益和风险。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 2 total, 2 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.31433102394 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.31433102394
- DeepSeek/Terminus-2 BO-Eval: 0.31433102394

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q2_q3.best_correlated_cvar10_profit_yuan` |  | 118550698.19 | `closeness_to_outstanding` | 69059695.53 | 0.223269527485 |  | yes |  |
| 2 | `experiment_result.q2_q3.spearman_price_cost` |  | 0.2551 | `closeness_to_outstanding` | 0.3 | 0.405392520394 |  | yes |  |
## CUMCM 2025 A: `cumcm-2025-a-smoke-screen`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 5 架无人机、每架最多 3 枚烟幕弹，同时对 3 枚导弹实施遮蔽，求总体遮蔽时间尽量长的投放方案。
- Final answer: O 奖复现的联合遮蔽时长为 M1 10.3 s、M2 6.2 s、M3 3.4 s，总计 19.9 s。
- Baseline model: baseline 用轨迹几何和规划优化，把无人机速度、航向、投放时刻、起爆时刻一起搜索，最大化有效遮蔽时长。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 4 total, 4 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: N/A
- DeepSeek/Terminus-2 BO-Eval: N/A

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.q5_union_duration_s.M1` |  | 10.3 | `closeness_to_outstanding` |  |  |  | yes |  |
| 2 | `experiment_result.q5_union_duration_s.M2` |  | 6.2 | `closeness_to_outstanding` |  |  |  | yes |  |
| 3 | `experiment_result.q5_union_duration_s.M3` |  | 3.4 | `closeness_to_outstanding` |  |  |  | yes |  |
| 4 | `experiment_result.q5_union_duration_s.total` |  | 19.9 | `closeness_to_outstanding` |  |  |  | yes |  |
## CUMCM 2025 B: `cumcm-2025-b-sic-thickness`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 把多光束反射/透射造成的干涉也考虑进去，重新确定碳化硅外延层厚度，并分析结果可靠性。
- Final answer: O 奖复现推荐厚度为 SiC 8.9815 um、Si 10.5145 um。
- Baseline model: baseline 用数据拟合与回归分析，从光谱条纹周期和非线性拟合中反推出外延层厚度。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 2 total, 2 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0.143178654302 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: 0.143178654302
- DeepSeek/Terminus-2 BO-Eval: 0.143178654302

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.si_recommended_thickness_um` |  | 10.5145 | `closeness_to_outstanding` | 4.82505875455 | 0.181514472929 |  | yes |  |
| 2 | `experiment_result.sic_recommended_thickness_um` |  | 8.9815 | `closeness_to_outstanding` | 18.1836785023 | 0.104842835674 |  | yes |  |
## CUMCM 2025 C: `cumcm-2025-c-nipt`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 对女胎样本，用染色体 Z 值、GC 含量、读段数、BMI 等指标判断胎儿是否异常。
- Final answer: O 奖复现的女胎异常判定模型 leave-one-out accuracy 为 0.8659，F1 为 0.3721。
- Baseline model: baseline 用综合评价和权重决策，把多项检测指标合成风险分数，再给出异常判定。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 2 total, 2 scored
- Baseline endpoint: `legacy_matched_metric_panel_from_generic_baselines_no_question_metric_match`
- Oracle reward: 0.52409654943 (scored)
- DeepSeek/Terminus-2 job reward: 0.471826516941 (scored)
- DeepSeek/Terminus-2 B-Eval: 0.471826516941
- DeepSeek/Terminus-2 BO-Eval: 0.471826516941

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.female_loo_accuracy` |  | 0.8659 | `closeness_to_outstanding` | 0.9174 | 0.668614228354 |  | yes |  |
| 2 | `female_abnormality.leave_one_out_f1` |  | 0.3721 | `closeness_to_outstanding` | 0.489796 | 0.275038805529 |  | yes |  |
## MCM 2023 A: `mcm-2023-a-plant-community`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 综合物种数、干旱、污染和栖息地压力，说明怎样保证植物群落长期可生存。
- Final answer: O 奖复现的核心量化结论包括最优/阈值物种数 2，beta 压力下生物量下降 32.0%，五物种均匀度 0.8826。
- Baseline model: baseline 把物种数阈值、功能性状、干旱敏感性和污染/栖息地压力合成为管理前沿。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 3 total, 3 scored
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 0.497195333333 (scored)
- DeepSeek/Terminus-2 job reward: -0.248454921739 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: -0.248454921739
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `target_comparison.beta_decline_pct.actual` |  | 32 | `closeness_to_outstanding` | 7.04 | 0.133333333333 |  | yes |  |
| 2 | `target_comparison.five_species_pielou_evenness.actual` |  | 0.8826 | `closeness_to_outstanding` | 0.9673 | 0.555641827377 |  | yes |  |
| 3 | `target_comparison.optimal_species_count.actual` |  | 2 | `closeness_to_outstanding` | 5 | 0.0740740740741 |  | yes |  |
## MCM 2023 B: `mcm-2023-b-maasai-mara`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 把土地分区和政策方案整理成给当地管理者的非技术报告，说明推荐方案的收益和用地分配。
- Final answer: O 奖复现的方案 2 收益指标值约 154948.974，农业/狩猎/旅游/保护区格点数分别为 12、2、9、13。
- Baseline model: baseline 用空间土地利用优化，把农业、狩猎、旅游和野生动物保护的格点分配成收益最大化问题。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 5 total, 5 scored
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 0.39734275 (scored)
- DeepSeek/Terminus-2 job reward: -0.572294585853 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.572294585853
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `target_comparison.scenario2_agriculture_cells.actual` |  | 12 | `closeness_to_outstanding` | 100 | 0.0161001788909 |  | yes |  |
| 2 | `target_comparison.scenario2_benefit_million.actual` |  | 154948.974 | `closeness_to_outstanding` | 104.24 | 0.107207252097 |  | yes |  |
| 3 | `target_comparison.scenario2_hunting_cells.actual` |  | 2 | `closeness_to_outstanding` | 40 | 0.00627615062762 |  | yes |  |
| 4 | `target_comparison.scenario2_tourism_cells.actual` |  | 9 | `closeness_to_outstanding` | 100 | 0.011728931364 |  | yes |  |
| 5 | `target_comparison.scenario2_wildlife_cells.actual` |  | 13 | `closeness_to_outstanding` | 160 | 0.0105008077544 |  | yes |  |
## MCM 2023 C: `mcm-2023-c-wordle`

- Scoring status: final-question endpoint target-minmax
- Scoring scope: `final_question_only`
- Final question: 在给纽约时报编辑的总结信之前，最后一个可量化核心是判断 EERIE 的难度，并给出难度分类模型准确率。
- Final answer: O 奖复现把 EERIE 判为中等难度组 2，难度分类模型 holdout accuracy 为 0.7。
- Baseline model: baseline 用报告量时间序列、单词属性特征和分类模型来预测 Wordle 分布及难度等级。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 2 total, 1 scored
- Baseline endpoint: `question_result_minmax_endpoint`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: 0
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `target_comparison.eerie_group.actual` | 2 | 2 | `exact_value` | 3 | 0 |  | no | difficulty_model.eerie_classifier_class |
| 2 | `target_comparison.lightgbm_like_accuracy.actual` | 0.422222 | 0.7 | `higher_is_better` | 0.3211 | 0 | -0.101122 | yes | difficulty_model.holdout_accuracy |
## MCM 2024 A: `mcm-2024-a-lamprey`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 判断七鳃鳗可变性别比例是否也会让生态系统中的其他生物受益，尤其是寄生者/宿主相关指标。
- Final answer: O 奖复现的共存情景资源水平为 0.55，寄生者指数 8.562，宿主鱼指数 1080.356。
- Baseline model: baseline 用生态动力系统仿真，把资源水平、性别比例、七鳃鳗、宿主鱼和寄生者一起演化。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 3 total, 3 scored
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 0.54316425 (scored)
- DeepSeek/Terminus-2 job reward: -0.194531681993 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.194531681993
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.parasite_coexistence_case.final_parasite_index` |  | 8.562 | `closeness_to_outstanding` | 0.3124 | 0.110750842941 |  | yes |  |
| 2 | `experiment_result.parasite_coexistence_case.host_fish_index` |  | 1080.356 | `closeness_to_outstanding` | 0.5981 | 0.107195843839 |  | yes |  |
| 3 | `experiment_result.parasite_coexistence_case.resource_level` |  | 0.55 | `closeness_to_outstanding` | 0.5 | 0.568965517241 |  | yes |  |
## MCM 2024 B: `mcm-2024-b-submersible-search`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 把潜水器搜索模型迁移到加勒比海场景，并说明洋流、海底地形和多潜水器协同时需要怎样调整。
- Final answer: O 奖复现给出的加勒比海调整为洋流不确定性乘数 1.35、地形不确定性乘数 1.2。
- Baseline model: baseline 用贝叶斯搜索规划，先估计位置后验，再按海流和地形不确定性调整搜索区域。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 2 total, 2 scored
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 0.42137875 (scored)
- DeepSeek/Terminus-2 job reward: -0.402596368978 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.402596368978
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.caribbean_adaptation.current_multiplier` |  | 1.35 | `closeness_to_outstanding` | 2 | 0.199507389163 |  | yes |  |
| 2 | `experiment_result.caribbean_adaptation.terrain_uncertainty_multiplier` |  | 1.2 | `closeness_to_outstanding` | 2 | 0.152542372881 |  | yes |  |
## MCM 2024 C: `mcm-2024-c-tennis-momentum`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 把势头模型转成教练能用的赛中提示：什么时候可能发生势头转换，应重点监控哪些指标。
- Final answer: O 奖复现的最终比赛预警率为 0.006；前三个势头预警特征相关系数约为 0.0302、-0.0223、0.0154。
- Baseline model: baseline 用势头时间序列、随机性检验和贝叶斯/分类预警模型，把比赛数据转成教练提示。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 4 total, 4 scored
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 0.4087086 (scored)
- DeepSeek/Terminus-2 job reward: -0.561238131236 (scored)
- DeepSeek/Terminus-2 B-Eval: -0.561238131236
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.dual_temporal_bayes.final_match_warning_rate` |  | 0.006 | `closeness_to_outstanding` | 0.9632 | 0.000751628528478 |  | yes |  |
| 2 | `experiment_result.top_swing_features[0].warning_correlation` |  | 0.0302 | `closeness_to_outstanding` | 0.1074 | 0.0448381668811 |  | yes |  |
| 3 | `experiment_result.top_swing_features[1].warning_correlation` |  | -0.0223 | `closeness_to_outstanding` | 0.0809 | 0.0252748498243 |  | yes |  |
| 4 | `experiment_result.top_swing_features[2].warning_correlation` |  | 0.0154 | `closeness_to_outstanding` | 0.051 | 0.0493484298227 |  | yes |  |
## MCM 2025 A: `mcm-2025-a-stair-wear`

- Scoring status: final-question endpoint target-minmax
- Scoring scope: `final_question_only`
- Final question: 根据楼梯磨损反推典型一天大约多少人使用，以及这些人是短时间集中经过还是长时间稀疏经过。
- Final answer: O 奖复现估计日均使用人数 73.52，短时峰值约 27.6 人，若分散到 10 小时则每小时约 4.6 人。
- Baseline model: baseline 用物理磨损反演，把磨损深度、材料假设和年龄区间换算成通行次数与典型日使用模式。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 3 total, 3 scored
- Baseline endpoint: `question_result_minmax_endpoint`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: 0
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `daily_use_pattern.peak_period_users` | 27.3 | 27.6 | `higher_is_better` | 23.6 | 0 | -3.7 | yes | daily_use_pattern.peak_period_users |
| 2 | `daily_use_pattern.regular_hour_users_if_spread_over_10_hours` | 4.5 | 4.6 | `higher_is_better` | 7.1 | 0 | 2.6 | yes | daily_use_pattern.regular_hour_users_if_spread_over_10_hours |
| 3 | `experiment_result.estimated_daily_users` | 72.67 | 73.52 | `higher_is_better` | 117.9 | 0 | 45.23 | yes | inverse_wear_model.usage_frequency.estimated_daily_users |
## MCM 2025 B: `mcm-2025-b-juneau-tourism`

- Scoring status: final-question endpoint target-minmax
- Scoring scope: `final_question_only`
- Final question: 给朱诺旅游委员会写一页备忘录，概括预测、各种限制/收费措施的效果，并推荐最优可持续旅游政策。
- Final answer: O 奖复现推荐终端政策：日容量 11000 人，游客费 55 USD，年游客 1491526，总收入 431610327.83 USD，居民接受度 1.0，可持续得分 1.007。
- Baseline model: baseline 用可持续旅游政策优化，把游客量、收费、保护投入、居民接受度和冰川压力一起做动态规划。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 6 total, 6 scored
- Baseline endpoint: `question_result_minmax_endpoint`
- Oracle reward: 1 (scored)
- DeepSeek/Terminus-2 job reward: 0 (scored)
- DeepSeek/Terminus-2 B-Eval: 0
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `experiment_result.annual_visitors` | 1408000 | 1491526 | `higher_is_better` | 1111429 | 0 | -296571 | yes | sustainability_model.optimal_policy.annual_visitors |
| 2 | `experiment_result.optimal_daily_cap` | 10000 | 11000 | `higher_is_better` | 4000 | 0 | -6000 | yes | sustainability_model.optimal_policy.daily_cap |
| 3 | `experiment_result.optimal_visitor_fee_usd` | 50 | 55 | `higher_is_better` | 15 | 0 | -35 | yes | sustainability_model.optimal_policy.visitor_fee_usd |
| 4 | `experiment_result.resident_acceptance_index` | 0.78 | 1 | `higher_is_better` | 0.764 | 0 | -0.016 | yes | sustainability_model.optimal_policy.resident_acceptance_index |
| 5 | `experiment_result.sustainability_score` | 0.908447 | 1.007 | `higher_is_better` | 0.5827 | 0 | -0.325747 | yes | sustainability_model.optimal_policy.sustainability_score |
| 6 | `experiment_result.total_revenue_usd` | 400400000 | 431610327.83 | `higher_is_better` | 277162606 | 0 | -123237394 | yes | sustainability_model.optimal_policy.total_revenue_usd |
## MCM 2025 C: `mcm-2025-c-olympic-medals`

- Scoring status: final-question legacy fallback
- Scoring scope: `final_question_only`
- Final question: 说明模型还能发现哪些原创奖牌规律，以及这些规律怎样指导国家奥委会分配项目和教练资源。
- Final answer: O 奖复现的教练效应建议中，四个候选投资的预计奖牌增益为 1.666667、2.0、3.0、1.777778，全局强教练效应 75 分位跳升为 6.0。
- Baseline model: baseline 用奥运奖牌预测、项目重要性分析和滚动三届历史成绩跳升来筛选可能的强教练效应。
- Default eval method: `B-Eval`
- Final-answer numeric fields: 5 total, 5 scored
- Baseline endpoint: `legacy_explicit_generic_baseline_score_mean_no_question_metric_match`
- Oracle reward: 0.415985833333 (scored)
- DeepSeek/Terminus-2 job reward: -0.491474074565 (error: AgentTimeoutError(1))
- DeepSeek/Terminus-2 B-Eval: -0.491474074565
- DeepSeek/Terminus-2 BO-Eval: 0

| # | Metric path | Baseline value | Outstanding value | Direction | DeepSeek actual | BO metric score | B-Eval gain | Scored | Baseline source |
|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | `great_coach_model.global_top_jump_75pct` |  | 6 | `closeness_to_outstanding` | 17.7 | 0.0579710144928 |  | yes |  |
| 2 | `great_coach_model.recommendations[0].estimated_medal_count_gain` |  | 1.666667 | `closeness_to_outstanding` | 0.4 | 0.136363628926 |  | yes |  |
| 3 | `great_coach_model.recommendations[1].estimated_medal_count_gain` |  | 2 | `closeness_to_outstanding` | 3.5 | 0.137931034483 |  | yes |  |
| 4 | `great_coach_model.recommendations[2].estimated_medal_count_gain` |  | 3 | `closeness_to_outstanding` | 0.6 | 0.130434782609 |  | yes |  |
| 5 | `great_coach_model.recommendations[3].estimated_medal_count_gain` |  | 1.777778 | `closeness_to_outstanding` |  | 0 |  | yes |  |
