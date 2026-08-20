# TB-MathModeling 任务与答案汇总

本文档汇总当前 18 道题：3 年 x 2 个竞赛 x A/B/C 三题。

口径说明:
- `Verifier/O answer` 是 verifier 使用的数值答案，来自 O 奖论文复现结果；它不是数学建模问题唯一可能的正确答案。
- 方向标签来自 `score_config.json`：有真实 baseline-to-outstanding 端点时标为 `越高越好` / `越低越好`；legacy fallback 指标没有逐指标 baseline 方向，因此标为 `越接近 verifier/O奖值越好`。
- `v4-flash answer` 来自当前 `terminus2-deepseek-v4-flash-current-*` jobs。优先读取 verifier 的 `score_details.json`，没有时回退读取 job artifact JSON；`N/A` 表示没有找到该路径下的答案。
- 当前默认 benchmark reward 是 `B-Eval`；能从 verifier details 推导时也同时列出 `BO-Eval`。

## 总览

| 竞赛 | 年份 | 题号 | Task | 简洁描述 | 子问题数 | 有效数值指标 | v4-flash 状态 | v4 B-Eval | v4 BO-Eval |
|---|---:|---|---|---|---:|---:|---|---:|---:|
| CUMCM | 2023 | A | [`cumcm-2023-a-heliostat-field`](#cumcm-2023-a) | CUMCM 2023 A: heliostat field design | 3 | 29 | error: AgentTimeoutError(1) | N/A | N/A |
| CUMCM | 2023 | B | [`cumcm-2023-b-multibeam-lines`](#cumcm-2023-b) | CUMCM 2023 B: multibeam survey-line layout | 4 | 21 | error: CancelledError(1) | N/A | N/A |
| CUMCM | 2023 | C | [`cumcm-2023-c-vegetable-pricing`](#cumcm-2023-c) | CUMCM 2023 C: vegetable pricing and replenishment | 4 | 38 | error: AgentTimeoutError(1) | 0.093365864843 | 0.093365864843 |
| CUMCM | 2024 | A | [`cumcm-2024-a-dragon-dance`](#cumcm-2024-a) | CUMCM 2024 A: dragon-dance bench kinematics | 5 | 9 | error: AgentTimeoutError(1) | 0.206349206349 | 0.206349206349 |
| CUMCM | 2024 | B | [`cumcm-2024-b-production-decision`](#cumcm-2024-b) | CUMCM 2024 B: production-process decision optimization | 4 | 69 | error: AgentTimeoutError(1) | 0.633378428946 | 0.633378428946 |
| CUMCM | 2024 | C | [`cumcm-2024-c-crop-planting`](#cumcm-2024-c) | CUMCM 2024 C: crop-planting strategy optimization | 3 | 20 | error: AgentTimeoutError(1) | 0.207024231145 | 0.207024231145 |
| CUMCM | 2025 | A | [`cumcm-2025-a-smoke-screen`](#cumcm-2025-a) | CUMCM 2025 A: UAV smoke-screen strategy | 5 | 164 | error: AgentTimeoutError(1) | N/A | N/A |
| CUMCM | 2025 | B | [`cumcm-2025-b-sic-thickness`](#cumcm-2025-b) | CUMCM 2025 B: SiC epitaxial-layer thickness inversion | 3 | 2 | error: AgentTimeoutError(1) | 0.143178654302 | 0.143178654302 |
| CUMCM | 2025 | C | [`cumcm-2025-c-nipt`](#cumcm-2025-c) | CUMCM 2025 C: NIPT timing and fetal abnormality modeling | 4 | 8 | scored | 0.524882309574 | 0.524882309574 |
| MCM | 2023 | A | [`mcm-2023-a-plant-community`](#mcm-2023-a) | MCM 2023 A: drought-stricken plant communities | 9 | 41 | error: AgentTimeoutError(1) | -0.137723472028 | 0 |
| MCM | 2023 | B | [`mcm-2023-b-maasai-mara`](#mcm-2023-b) | MCM 2023 B: reimagining Maasai Mara | 3 | 11 | scored | -0.570725974269 | 0 |
| MCM | 2023 | C | [`mcm-2023-c-wordle`](#mcm-2023-c) | MCM 2023 C: predicting Wordle results | 4 | 17 | scored | 0.143159490288 | 0.143159490288 |
| MCM | 2024 | A | [`mcm-2024-a-lamprey`](#mcm-2024-a) | MCM 2024 A: lamprey sex-ratio ecology | 4 | 105 | scored | -0.24548365989 | 0 |
| MCM | 2024 | B | [`mcm-2024-b-submersible-search`](#mcm-2024-b) | MCM 2024 B: submersible localization and search planning | 4 | 13 | scored | -0.437625067352 | 0 |
| MCM | 2024 | C | [`mcm-2024-c-tennis-momentum`](#mcm-2024-c) | MCM 2024 C: momentum in tennis | 1 | 22 | scored | -0.508413940348 | 0 |
| MCM | 2025 | A | [`mcm-2025-a-stair-wear`](#mcm-2025-a) | MCM 2025 A: stair wear and historical traffic inference | 8 | 5 | scored | 0 | 0 |
| MCM | 2025 | B | [`mcm-2025-b-juneau-tourism`](#mcm-2025-b) | MCM 2025 B: sustainable tourism management in Juneau | 3 | 19 | scored | 0.0805071737516 | 0.0805071737516 |
| MCM | 2025 | C | [`mcm-2025-c-olympic-medals`](#mcm-2025-c) | MCM 2025 C: Olympic medal prediction | 1 | 96 | error: AgentTimeoutError(1) | -0.293385079963 | 0 |

# 分题表格

<a id="cumcm-2023-a"></a>

## CUMCM 2023 A: heliostat field design

- Task slug: `cumcm-2023-a-heliostat-field`
- 简洁任务描述: CUMCM 2023 A: heliostat field design
- 当前 instruction 子问题数: 3
- verifier 数值指标: 29 effective / 29 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2023-a-heliostat-field`; 状态: error: AgentTimeoutError(1); job reward: 0
- v4-flash B-Eval: N/A; BO-Eval: N/A; raw panel score: N/A
- v4-flash 对齐 verifier metric path 的答案覆盖: 0/29

子问题:
- 问题1: 若将吸收塔建于该圆形定日镜场中心，定日镜尺寸均为 6 m×6 m，安装高度均为
- 问题2: 按设计要求，定日镜场的额定年平均输出热功率（以下简称额定功率）为60 MW。
- 问题3: 如果定日镜尺寸可以不同，安装高度也可以不同，额定功率设置同问题2，请重新

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.design_summary[0].annual_optical_efficiency` | 越接近 verifier/O奖值越好 | 0.536230167 | N/A | N/A | N/A | 是 |
| 2 | `reproduced.design_summary[0].annual_thermal_power_mw` | 越接近 verifier/O奖值越好 | 32.76117051 | N/A | N/A | N/A | 是 |
| 3 | `reproduced.design_summary[0].mirror_count` | 越接近 verifier/O奖值越好 | 1745 | N/A | N/A | N/A | 是 |
| 4 | `reproduced.design_summary[0].tower_xy[0]` | 越接近 verifier/O奖值越好 | 0 | N/A | N/A | N/A | 是 |
| 5 | `reproduced.design_summary[0].tower_xy[1]` | 越接近 verifier/O奖值越好 | 0 | N/A | N/A | N/A | 是 |
| 6 | `reproduced.design_summary[0].unit_area_power_kw_m2` | 越接近 verifier/O奖值越好 | 0.521508604 | N/A | N/A | N/A | 是 |
| 7 | `reproduced.design_summary[1].annual_optical_efficiency` | 越接近 verifier/O奖值越好 | 0.591643667 | N/A | N/A | N/A | 是 |
| 8 | `reproduced.design_summary[1].annual_thermal_power_mw` | 越接近 verifier/O奖值越好 | 68.24427914 | N/A | N/A | N/A | 是 |
| 9 | `reproduced.design_summary[1].installation_height_m` | 越接近 verifier/O奖值越好 | 4 | N/A | N/A | N/A | 是 |
| 10 | `reproduced.design_summary[1].mirror_area_m2` | 越接近 verifier/O奖值越好 | 119196 | N/A | N/A | N/A | 是 |
| 11 | `reproduced.design_summary[1].mirror_count` | 越接近 verifier/O奖值越好 | 3311 | N/A | N/A | N/A | 是 |
| 12 | `reproduced.design_summary[1].mirror_height_m` | 越接近 verifier/O奖值越好 | 6 | N/A | N/A | N/A | 是 |
| 13 | `reproduced.design_summary[1].mirror_width_m` | 越接近 verifier/O奖值越好 | 6 | N/A | N/A | N/A | 是 |
| 14 | `reproduced.design_summary[1].tower_xy[0]` | 越接近 verifier/O奖值越好 | 0 | N/A | N/A | N/A | 是 |
| 15 | `reproduced.design_summary[1].tower_xy[1]` | 越接近 verifier/O奖值越好 | -250 | N/A | N/A | N/A | 是 |
| 16 | `reproduced.design_summary[1].unit_area_power_kw_m2` | 越接近 verifier/O奖值越好 | 0.572538333 | N/A | N/A | N/A | 是 |
| 17 | `reproduced.design_summary[2].annual_optical_efficiency` | 越接近 verifier/O奖值越好 | 0.496428083 | N/A | N/A | N/A | 是 |
| 18 | `reproduced.design_summary[2].annual_thermal_power_mw` | 越接近 verifier/O奖值越好 | 60.336111 | N/A | N/A | N/A | 是 |
| 19 | `reproduced.design_summary[2].mirror_area_m2` | 越接近 verifier/O奖值越好 | 119196 | N/A | N/A | N/A | 是 |
| 20 | `reproduced.design_summary[2].mirror_count` | 越接近 verifier/O奖值越好 | 3311 | N/A | N/A | N/A | 是 |
| 21 | `reproduced.design_summary[2].tower_xy[0]` | 越接近 verifier/O奖值越好 | 0 | N/A | N/A | N/A | 是 |
| 22 | `reproduced.design_summary[2].tower_xy[1]` | 越接近 verifier/O奖值越好 | -250 | N/A | N/A | N/A | 是 |
| 23 | `reproduced.design_summary[2].unit_area_power_kw_m2` | 越接近 verifier/O奖值越好 | 0.506192417 | N/A | N/A | N/A | 是 |
| 24 | `reproduced.official_coordinate_count` | 越接近 verifier/O奖值越好 | 1745 | N/A | N/A | N/A | 是 |
| 25 | `reproduced.q1_monthly_efficiency_mean` | 越接近 verifier/O奖值越好 | 0.536230167 | N/A | N/A | N/A | 是 |
| 26 | `target_comparison.q1_annual_optical_efficiency.actual` | 越接近 verifier/O奖值越好 | 0.536230167 | N/A | N/A | N/A | 是 |
| 27 | `target_comparison.q2_annual_thermal_power_mw.actual` | 越接近 verifier/O奖值越好 | 68.244279 | N/A | N/A | N/A | 是 |
| 28 | `target_comparison.q2_mirror_count.actual` | 越接近 verifier/O奖值越好 | 3311 | N/A | N/A | N/A | 是 |
| 29 | `target_comparison.q3_annual_thermal_power_mw.actual` | 越接近 verifier/O奖值越好 | 60.336111 | N/A | N/A | N/A | 是 |

<a id="cumcm-2023-b"></a>

## CUMCM 2023 B: multibeam survey-line layout

- Task slug: `cumcm-2023-b-multibeam-lines`
- 简洁任务描述: CUMCM 2023 B: multibeam survey-line layout
- 当前 instruction 子问题数: 4
- verifier 数值指标: 21 effective / 21 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2023-b-multibeam-lines`; 状态: error: CancelledError(1); job reward: 0
- v4-flash B-Eval: N/A; BO-Eval: N/A; raw panel score: N/A
- v4-flash 对齐 verifier metric path 的答案覆盖: 0/21

子问题:
- 问题1: 与测线方向垂直的平面和海底坡面的交线构成一条与水平面夹角为 𝛼 的斜线（图
- 问题2: 考虑一个矩形待测海域（图8），测线方向与海底坡面的法向在水平面上投影的夹
- 问题3: 考虑一个南北长2 海里、东西宽4 海里的矩形海域内，海域中心点处的海水深度
- 问题4: 海水深度数据（附件.xlsx）是若干年前某海域（南北长5 海里、东西宽4 海里）

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.problem3_last_position_m` | 越接近 verifier/O奖值越好 | 7226.14 | N/A | N/A | N/A | 是 |
| 2 | `reproduced.problem3_line_count` | 越接近 verifier/O奖值越好 | 34 | N/A | N/A | N/A | 是 |
| 3 | `reproduced.problem3_total_length_m` | 越接近 verifier/O奖值越好 | 125936 | N/A | N/A | N/A | 是 |
| 4 | `reproduced.problem4_summary.avg_position_error_m` | 越接近 verifier/O奖值越好 | 9.27 | N/A | N/A | N/A | 是 |
| 5 | `reproduced.problem4_summary.greedy_avg_overlap_pct` | 越接近 verifier/O奖值越好 | 10.35 | N/A | N/A | N/A | 是 |
| 6 | `reproduced.problem4_summary.missed_area_pct` | 越接近 verifier/O奖值越好 | 3.48 | N/A | N/A | N/A | 是 |
| 7 | `reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles` | 越接近 verifier/O奖值越好 | 30 | N/A | N/A | N/A | 是 |
| 8 | `reproduced.problem4_summary.sa_avg_overlap_pct` | 越接近 verifier/O奖值越好 | 10.48 | N/A | N/A | N/A | 是 |
| 9 | `reproduced.problem4_summary.total_length_nautical_miles` | 越接近 verifier/O奖值越好 | 622 | N/A | N/A | N/A | 是 |
| 10 | `reproduced.seabed_grid_summary.max_depth_m` | 越接近 verifier/O奖值越好 | 197.2 | N/A | N/A | N/A | 是 |
| 11 | `reproduced.seabed_grid_summary.mean_depth_m` | 越接近 verifier/O奖值越好 | 62.539 | N/A | N/A | N/A | 是 |
| 12 | `reproduced.seabed_grid_summary.min_depth_m` | 越接近 verifier/O奖值越好 | 20 | N/A | N/A | N/A | 是 |
| 13 | `reproduced.seabed_grid_summary.x_count` | 越接近 verifier/O奖值越好 | 201 | N/A | N/A | N/A | 是 |
| 14 | `reproduced.seabed_grid_summary.x_range_nm` | 越接近 verifier/O奖值越好 | 4 | N/A | N/A | N/A | 是 |
| 15 | `reproduced.seabed_grid_summary.y_count` | 越接近 verifier/O奖值越好 | 251 | N/A | N/A | N/A | 是 |
| 16 | `reproduced.seabed_grid_summary.y_range_nm` | 越接近 verifier/O奖值越好 | 5 | N/A | N/A | N/A | 是 |
| 17 | `target_comparison.problem3_last_position_m.actual` | 越接近 verifier/O奖值越好 | 7226.14 | N/A | N/A | N/A | 是 |
| 18 | `target_comparison.problem3_line_count.actual` | 越接近 verifier/O奖值越好 | 34 | N/A | N/A | N/A | 是 |
| 19 | `target_comparison.problem3_total_length_m.actual` | 越接近 verifier/O奖值越好 | 125936 | N/A | N/A | N/A | 是 |
| 20 | `target_comparison.problem4_missed_area_pct.actual` | 越接近 verifier/O奖值越好 | 3.48 | N/A | N/A | N/A | 是 |
| 21 | `target_comparison.problem4_total_length_nm.actual` | 越接近 verifier/O奖值越好 | 622 | N/A | N/A | N/A | 是 |

<a id="cumcm-2023-c"></a>

## CUMCM 2023 C: vegetable pricing and replenishment

- Task slug: `cumcm-2023-c-vegetable-pricing`
- 简洁任务描述: CUMCM 2023 C: vegetable pricing and replenishment
- 当前 instruction 子问题数: 4
- verifier 数值指标: 38 effective / 38 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2023-c-vegetable-pricing`; 状态: error: AgentTimeoutError(1); job reward: 0.093365864843
- v4-flash B-Eval: 0.093365864843; BO-Eval: 0.093365864843; raw panel score: 0.093365864843
- v4-flash 对齐 verifier metric path 的答案覆盖: 8/38

子问题:
- 问题1: 蔬菜类商品不同品类或不同单品之间可能存在一定的关联关系，请分析蔬菜各
- 问题2: 考虑商超以品类为单位做补货计划，请分析各蔬菜品类的销售总量与成本加成
- 问题3: 因蔬菜类商品的销售空间有限，商超希望进一步制定单品的补货计划，要求可
- 问题4: 为了更好地制定蔬菜商品的补货和定价决策，商超还需要采集哪些相关数据，

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.category_count` | 越接近 verifier/O奖值越好 | 6 | N/A | 6 | 1 | 是 |
| 2 | `reproduced.cluster_center_comparison[0].avg_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 2.52916556634 | N/A | N/A | 0 | 是 |
| 3 | `reproduced.cluster_center_comparison[0].max_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 8.89412 | N/A | N/A | 0 | 是 |
| 4 | `reproduced.cluster_center_comparison[0].total_sales_kg_actual` | 越接近 verifier/O奖值越好 | 258.426462857 | N/A | N/A | 0 | 是 |
| 5 | `reproduced.cluster_center_comparison[1].avg_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 9.10524135797 | N/A | N/A | 0 | 是 |
| 6 | `reproduced.cluster_center_comparison[1].max_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 56.0392826087 | N/A | N/A | 0 | 是 |
| 7 | `reproduced.cluster_center_comparison[1].total_sales_kg_actual` | 越接近 verifier/O奖值越好 | 3149.22293478 | N/A | N/A | 0 | 是 |
| 8 | `reproduced.cluster_center_comparison[2].avg_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 20.808494683 | N/A | N/A | 0 | 是 |
| 9 | `reproduced.cluster_center_comparison[2].max_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 144.071684211 | N/A | N/A | 0 | 是 |
| 10 | `reproduced.cluster_center_comparison[2].total_sales_kg_actual` | 越接近 verifier/O奖值越好 | 7849.98494737 | N/A | N/A | 0 | 是 |
| 11 | `reproduced.cluster_center_comparison[3].avg_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 32.7257670152 | N/A | N/A | 0 | 是 |
| 12 | `reproduced.cluster_center_comparison[3].max_daily_sales_kg_actual` | 越接近 verifier/O奖值越好 | 205.939666667 | N/A | N/A | 0 | 是 |
| 13 | `reproduced.cluster_center_comparison[3].total_sales_kg_actual` | 越接近 verifier/O奖值越好 | 22006.2065 | N/A | N/A | 0 | 是 |
| 14 | `reproduced.correlation_comparison[0].actual_sales_markup_corr` | 越接近 verifier/O奖值越好 | -0.1579 | N/A | N/A | 0 | 是 |
| 15 | `reproduced.correlation_comparison[1].actual_sales_markup_corr` | 越接近 verifier/O奖值越好 | -0.0287 | N/A | N/A | 0 | 是 |
| 16 | `reproduced.correlation_comparison[2].actual_sales_markup_corr` | 越接近 verifier/O奖值越好 | 0.1977 | N/A | N/A | 0 | 是 |
| 17 | `reproduced.correlation_comparison[3].actual_sales_markup_corr` | 越接近 verifier/O奖值越好 | 0.0418 | N/A | N/A | 0 | 是 |
| 18 | `reproduced.correlation_comparison[4].actual_sales_markup_corr` | 越接近 verifier/O奖值越好 | 0.0259 | N/A | N/A | 0 | 是 |
| 19 | `reproduced.correlation_comparison[5].actual_sales_markup_corr` | 越接近 verifier/O奖值越好 | -0.2332 | N/A | N/A | 0 | 是 |
| 20 | `reproduced.future_week_profit_yuan` | 越接近 verifier/O奖值越好 | 5105.6 | N/A | 14616.69 | 0.060518214474 | 是 |
| 21 | `reproduced.item_count` | 越接近 verifier/O奖值越好 | 246 | N/A | 246 | 1 | 是 |
| 22 | `reproduced.july1_profit_yuan` | 越接近 verifier/O奖值越好 | 1282.2631 | N/A | 1748.36 | 0.248192575832 | 是 |
| 23 | `reproduced.regression_comparison[0].actual_intercept` | 越接近 verifier/O奖值越好 | 11.2959 | N/A | N/A | 0 | 是 |
| 24 | `reproduced.regression_comparison[0].actual_slope` | 越接近 verifier/O奖值越好 | -0.041909 | N/A | N/A | 0 | 是 |
| 25 | `reproduced.regression_comparison[1].actual_intercept` | 越接近 verifier/O奖值越好 | 6.3512 | N/A | N/A | 0 | 是 |
| 26 | `reproduced.regression_comparison[1].actual_slope` | 越接近 verifier/O奖值越好 | -0.004092 | N/A | N/A | 0 | 是 |
| 27 | `reproduced.regression_comparison[2].actual_intercept` | 越接近 verifier/O奖值越好 | 10.6597 | N/A | N/A | 0 | 是 |
| 28 | `reproduced.regression_comparison[2].actual_slope` | 越接近 verifier/O奖值越好 | -0.032044 | N/A | N/A | 0 | 是 |
| 29 | `reproduced.regression_comparison[3].actual_intercept` | 越接近 verifier/O奖值越好 | 9.5925 | N/A | N/A | 0 | 是 |
| 30 | `reproduced.regression_comparison[3].actual_slope` | 越接近 verifier/O奖值越好 | -0.036359 | N/A | N/A | 0 | 是 |
| 31 | `reproduced.regression_comparison[4].actual_intercept` | 越接近 verifier/O奖值越好 | 9.6747 | N/A | N/A | 0 | 是 |
| 32 | `reproduced.regression_comparison[4].actual_slope` | 越接近 verifier/O奖值越好 | -0.012185 | N/A | N/A | 0 | 是 |
| 33 | `reproduced.regression_comparison[5].actual_intercept` | 越接近 verifier/O奖值越好 | 9.4799 | N/A | N/A | 0 | 是 |
| 34 | `reproduced.regression_comparison[5].actual_slope` | 越接近 verifier/O奖值越好 | -0.012872 | N/A | N/A | 0 | 是 |
| 35 | `reproduced.selected_item_count` | 越接近 verifier/O奖值越好 | 29 | N/A | 33 | 0.465240641711 | 是 |
| 36 | `target_comparison.future_week_max_profit_yuan.actual` | 越接近 verifier/O奖值越好 | 5105.6 | N/A | 14616.69 | 0.060518214474 | 是 |
| 37 | `target_comparison.problem3_july1_profit_yuan.actual` | 越接近 verifier/O奖值越好 | 1282.2631 | N/A | 1748.36 | 0.248192575832 | 是 |
| 38 | `target_comparison.problem3_selected_item_count.actual` | 越接近 verifier/O奖值越好 | 29 | N/A | 33 | 0.465240641711 | 是 |

<a id="cumcm-2024-a"></a>

## CUMCM 2024 A: dragon-dance bench kinematics

- Task slug: `cumcm-2024-a-dragon-dance`
- 简洁任务描述: CUMCM 2024 A: dragon-dance bench kinematics
- 当前 instruction 子问题数: 5
- verifier 数值指标: 9 effective / 9 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2024-a-dragon-dance`; 状态: error: AgentTimeoutError(1); job reward: 0.206349206349
- v4-flash B-Eval: 0.206349206349; BO-Eval: 0.206349206349; raw panel score: 0.206349206349
- v4-flash 对齐 verifier metric path 的答案覆盖: 9/9

子问题:
- 问题1: 舞龙队沿螺距为 55 cm 的等距螺线顺时针盘入，各把手中心均位于螺线上。龙
- 问题2: 舞龙队沿问题 1 设定的螺线盘入， 请确定舞龙队盘入的终止时刻， 使得板凳之
- 问题3: 从盘入到盘出， 舞龙队将由顺时针盘入调头切换为逆时针盘出，这需要一定的
- 问题4: 盘入螺线的螺距为 1.7 m，盘出螺线与盘入螺线关于螺线中心呈中心对称，舞
- 问题5: 舞龙队沿问题 4 设定的路径行进，龙头行进速度保持不变， 请确定龙头的最大

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q1.handles` | 越接近 verifier/O奖值越好 | 224 | N/A | 224 | 1 | 是 |
| 2 | `experiment_result.q2.terminal_min_margin_m` | 越接近 verifier/O奖值越好 | 0.249958 | N/A | 0 | 0.107142857143 | 是 |
| 3 | `experiment_result.q2.terminal_time_s` | 越接近 verifier/O奖值越好 | 464 | N/A | 0 | 0.107142857143 | 是 |
| 4 | `experiment_result.q3.minimum_pitch_m` | 越接近 verifier/O奖值越好 | 0.4 | N/A | 0 | 0.107142857143 | 是 |
| 5 | `experiment_result.q4.base_ratio_2_to_1_length_m` | 越接近 verifier/O奖值越好 | 14.1372 | N/A | 0 | 0.107142857143 | 是 |
| 6 | `experiment_result.q4.shortest_candidate_length_m` | 越接近 verifier/O奖值越好 | 14.1372 | N/A | 0 | 0.107142857143 | 是 |
| 7 | `experiment_result.q4.shortest_candidate_ratio` | 越接近 verifier/O奖值越好 | 1 | N/A | 0 | 0.107142857143 | 是 |
| 8 | `experiment_result.q5.max_head_speed_mps` | 越接近 verifier/O奖值越好 | 2.00002 | N/A | 0 | 0.107142857143 | 是 |
| 9 | `experiment_result.q5.max_speed_ratio_when_head_1mps` | 越接近 verifier/O奖值越好 | 0.99999 | N/A | 0 | 0.107142857143 | 是 |

<a id="cumcm-2024-b"></a>

## CUMCM 2024 B: production-process decision optimization

- Task slug: `cumcm-2024-b-production-decision`
- 简洁任务描述: CUMCM 2024 B: production-process decision optimization
- 当前 instruction 子问题数: 4
- verifier 数值指标: 69 effective / 69 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2024-b-production-decision`; 状态: error: AgentTimeoutError(1); job reward: 0.633378428946
- v4-flash B-Eval: 0.633378428946; BO-Eval: 0.633378428946; raw panel score: 0.633378428946
- v4-flash 对齐 verifier metric path 的答案覆盖: 66/69

子问题:
- 问题1: 供应商声称一批零配件（零配件 1 或零配件 2）的次品率不会超过某个标称值。
- 问题2: 已知两种零配件和成品次品率，请为企业生产过程的各个阶段作出决策：
- 问题3: 对 𝑚 道工序、𝑛 个零配件，已知零配件、半成品和成品的次品率，重复问题
- 问题4: 假设问题 2 和问题 3 中零配件、 半成品和成品的次品率均是通过抽样检测方法

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q1_sampling[0].c` | 越接近 verifier/O奖值越好 | 36 | N/A | 1 | 0.10986775178 | 是 |
| 2 | `experiment_result.q1_sampling[0].false_alarm` | 越接近 verifier/O奖值越好 | 0.046596 | N/A | 0.01 | 0.1325396705 | 是 |
| 3 | `experiment_result.q1_sampling[0].n` | 越接近 verifier/O奖值越好 | 270 | N/A | 2 | 0.107856191744 | 是 |
| 4 | `experiment_result.q1_sampling[0].power` | 越接近 verifier/O奖值越好 | 0.801472 | N/A | N/A | 0 | 是 |
| 5 | `experiment_result.q1_sampling[1].accept_bad` | 越接近 verifier/O奖值越好 | 0.195466 | N/A | N/A | 0 | 是 |
| 6 | `experiment_result.q1_sampling[1].accept_good` | 越接近 verifier/O奖值越好 | 0.903863 | N/A | N/A | 0 | 是 |
| 7 | `experiment_result.q1_sampling[1].c` | 越接近 verifier/O奖值越好 | 25 | N/A | 0 | 0.107142857143 | 是 |
| 8 | `experiment_result.q1_sampling[1].n` | 越接近 verifier/O奖值越好 | 199 | N/A | 1 | 0.107625743645 | 是 |
| 9 | `experiment_result.q2.best_decisions[0].case` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 10 | `experiment_result.q2.best_decisions[0].dismantle_bad_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 11 | `experiment_result.q2.best_decisions[0].expected_profit` | 越接近 verifier/O奖值越好 | 26.374 | N/A | 21.6804 | 0.402734371023 | 是 |
| 12 | `experiment_result.q2.best_decisions[0].good_probability` | 越接近 verifier/O奖值越好 | 0.729 | N/A | 0.729 | 1 | 是 |
| 13 | `experiment_result.q2.best_decisions[0].inspect_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 14 | `experiment_result.q2.best_decisions[0].inspect_part1` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 15 | `experiment_result.q2.best_decisions[0].inspect_part2` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 16 | `experiment_result.q2.best_decisions[1].case` | 越接近 verifier/O奖值越好 | 2 | N/A | 2 | 1 | 是 |
| 17 | `experiment_result.q2.best_decisions[1].dismantle_bad_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 18 | `experiment_result.q2.best_decisions[1].expected_profit` | 越接近 verifier/O奖值越好 | 25.072 | N/A | 14.9375 | 0.228913334257 | 是 |
| 19 | `experiment_result.q2.best_decisions[1].good_probability` | 越接近 verifier/O奖值越好 | 0.512 | N/A | 0.64 | 0.324324324324 | 是 |
| 20 | `experiment_result.q2.best_decisions[1].inspect_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 21 | `experiment_result.q2.best_decisions[1].inspect_part1` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 22 | `experiment_result.q2.best_decisions[1].inspect_part2` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 23 | `experiment_result.q2.best_decisions[2].case` | 越接近 verifier/O奖值越好 | 3 | N/A | 3 | 1 | 是 |
| 24 | `experiment_result.q2.best_decisions[2].dismantle_bad_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 25 | `experiment_result.q2.best_decisions[2].expected_profit` | 越接近 verifier/O奖值越好 | 19.87 | N/A | 19.7956 | 0.969741337238 | 是 |
| 26 | `experiment_result.q2.best_decisions[2].good_probability` | 越接近 verifier/O奖值越好 | 0.729 | N/A | 0.729 | 1 | 是 |
| 27 | `experiment_result.q2.best_decisions[2].inspect_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 28 | `experiment_result.q2.best_decisions[2].inspect_part1` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 29 | `experiment_result.q2.best_decisions[2].inspect_part2` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 30 | `experiment_result.q2.best_decisions[3].case` | 越接近 verifier/O奖值越好 | 4 | N/A | 4 | 1 | 是 |
| 31 | `experiment_result.q2.best_decisions[3].dismantle_bad_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 32 | `experiment_result.q2.best_decisions[3].expected_profit` | 越接近 verifier/O奖值越好 | 14.95 | N/A | 16.4375 | 0.546701203718 | 是 |
| 33 | `experiment_result.q2.best_decisions[3].good_probability` | 越接近 verifier/O奖值越好 | 0.64 | N/A | 0.64 | 1 | 是 |
| 34 | `experiment_result.q2.best_decisions[3].inspect_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 35 | `experiment_result.q2.best_decisions[3].inspect_part1` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 36 | `experiment_result.q2.best_decisions[3].inspect_part2` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 37 | `experiment_result.q2.best_decisions[4].case` | 越接近 verifier/O奖值越好 | 5 | N/A | 5 | 1 | 是 |
| 38 | `experiment_result.q2.best_decisions[4].dismantle_bad_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 39 | `experiment_result.q2.best_decisions[4].expected_profit` | 越接近 verifier/O奖值越好 | 24.48 | N/A | 18.9383 | 0.346443692286 | 是 |
| 40 | `experiment_result.q2.best_decisions[4].good_probability` | 越接近 verifier/O奖值越好 | 0.648 | N/A | 0.648 | 1 | 是 |
| 41 | `experiment_result.q2.best_decisions[4].inspect_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 42 | `experiment_result.q2.best_decisions[4].inspect_part1` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 43 | `experiment_result.q2.best_decisions[4].inspect_part2` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 44 | `experiment_result.q2.best_decisions[5].case` | 越接近 verifier/O奖值越好 | 6 | N/A | 6 | 1 | 是 |
| 45 | `experiment_result.q2.best_decisions[5].dismantle_bad_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 46 | `experiment_result.q2.best_decisions[5].expected_profit` | 越接近 verifier/O奖值越好 | 26.5738 | N/A | 19.6343 | 0.314844383432 | 是 |
| 47 | `experiment_result.q2.best_decisions[5].good_probability` | 越接近 verifier/O奖值越好 | 0.85737 | N/A | 0.9025 | 0.695097233783 | 是 |
| 48 | `experiment_result.q2.best_decisions[5].inspect_final` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 49 | `experiment_result.q2.best_decisions[5].inspect_part1` | 越接近 verifier/O奖值越好 | 0 | N/A | 1 | 9.99900009999e-05 | 是 |
| 50 | `experiment_result.q2.best_decisions[5].inspect_part2` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 51 | `experiment_result.q2.best_profit_mean` | 越接近 verifier/O奖值越好 | 22.8866 | N/A | 18.5706 | 0.388875610416 | 是 |
| 52 | `experiment_result.q3.best_expected_profit` | 越接近 verifier/O奖值越好 | 88 | N/A | 85.5556 | 0.81203285042 | 是 |
| 53 | `experiment_result.q3.decision_bits[0]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 54 | `experiment_result.q3.decision_bits[10]` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 55 | `experiment_result.q3.decision_bits[11]` | 越接近 verifier/O奖值越好 | 1 | N/A | 0 | 0.107142857143 | 是 |
| 56 | `experiment_result.q3.decision_bits[12]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 57 | `experiment_result.q3.decision_bits[13]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 58 | `experiment_result.q3.decision_bits[14]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 59 | `experiment_result.q3.decision_bits[15]` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 60 | `experiment_result.q3.decision_bits[1]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 61 | `experiment_result.q3.decision_bits[2]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 62 | `experiment_result.q3.decision_bits[3]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 63 | `experiment_result.q3.decision_bits[4]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 64 | `experiment_result.q3.decision_bits[5]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 65 | `experiment_result.q3.decision_bits[6]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 66 | `experiment_result.q3.decision_bits[7]` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 67 | `experiment_result.q3.decision_bits[8]` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 68 | `experiment_result.q3.decision_bits[9]` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 69 | `experiment_result.q3.generations` | 越接近 verifier/O奖值越好 | 70 | N/A | 65536 | 0.00012829441736 | 是 |

<a id="cumcm-2024-c"></a>

## CUMCM 2024 C: crop-planting strategy optimization

- Task slug: `cumcm-2024-c-crop-planting`
- 简洁任务描述: CUMCM 2024 C: crop-planting strategy optimization
- 当前 instruction 子问题数: 3
- verifier 数值指标: 20 effective / 20 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2024-c-crop-planting`; 状态: error: AgentTimeoutError(1); job reward: 0.207024231145
- v4-flash B-Eval: 0.207024231145; BO-Eval: 0.207024231145; raw panel score: 0.207024231145
- v4-flash 对齐 verifier metric path 的答案覆盖: 15/20

子问题:
- 问题1: 假定各种农作物未来的预期销售量、种植成本、亩产量和销售价格相对于 2023 年保持
- 问题2: 根据经验，小麦和玉米未来的预期销售量有增长的趋势，平均年增长率介于5%~10%
- 问题3: 在现实生活中，各种农作物之间可能存在一定的可替代性和互补性，预期销售量与销

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q1.discount_gain_pct` | 越接近 verifier/O奖值越好 | 8.1067954e+18 | N/A | 12.18 | 0.107142857143 | 是 |
| 2 | `experiment_result.q1.discount_profit_yuan` | 越接近 verifier/O奖值越好 | 75678478 | N/A | 74663211.25 | 0.899445526973 | 是 |
| 3 | `experiment_result.q1.waste_profit_yuan` | 越接近 verifier/O奖值越好 | -5389476 | N/A | 66558138.75 | 0.00890891788879 | 是 |
| 4 | `experiment_result.q2_q3.best_correlated_cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118550698.19 | N/A | 69059695.53 | 0.223269527485 | 是 |
| 5 | `experiment_result.q2_q3.risk_summary[0].correlated_cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118550698.19 | N/A | 76732995.04 | 0.253838731488 | 是 |
| 6 | `experiment_result.q2_q3.risk_summary[0].cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118937552.19 | N/A | 78592899.47 | 0.261319089616 | 是 |
| 7 | `experiment_result.q2_q3.risk_summary[0].deterministic_profit_yuan` | 越接近 verifier/O奖值越好 | -5389476 | N/A | 74663211.25 | 0.00801414787093 | 是 |
| 8 | `experiment_result.q2_q3.risk_summary[0].mean_profit_yuan` | 越接近 verifier/O奖值越好 | 119827636.74 | N/A | 81840993.96 | 0.27459282006 | 是 |
| 9 | `experiment_result.q2_q3.risk_summary[0].q10_profit_yuan` | 越接近 verifier/O奖值越好 | 119159280.66 | N/A | 79051026.67 | 0.262815759919 | 是 |
| 10 | `experiment_result.q2_q3.risk_summary[1].correlated_cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118550698.19 | N/A | 69059695.53 | 0.223269527485 | 是 |
| 11 | `experiment_result.q2_q3.risk_summary[1].cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118937552.19 | N/A | 70733609.52 | 0.228446182627 | 是 |
| 12 | `experiment_result.q2_q3.risk_summary[1].deterministic_profit_yuan` | 越接近 verifier/O奖值越好 | 75678478 | N/A | 67196890.12 | 0.517076504613 | 是 |
| 13 | `experiment_result.q2_q3.risk_summary[1].mean_profit_yuan` | 越接近 verifier/O奖值越好 | 119827636.74 | N/A | 73656894.56 | 0.237478158468 | 是 |
| 14 | `experiment_result.q2_q3.risk_summary[1].q10_profit_yuan` | 越接近 verifier/O奖值越好 | 119159280.66 | N/A | 71145924.01 | 0.229474350859 | 是 |
| 15 | `experiment_result.q2_q3.risk_summary[2].correlated_cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118550698.19 | N/A | N/A | 0 | 是 |
| 16 | `experiment_result.q2_q3.risk_summary[2].cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118937552.19 | N/A | N/A | 0 | 是 |
| 17 | `experiment_result.q2_q3.risk_summary[2].deterministic_profit_yuan` | 越接近 verifier/O奖值越好 | 75678478 | N/A | N/A | 0 | 是 |
| 18 | `experiment_result.q2_q3.risk_summary[2].mean_profit_yuan` | 越接近 verifier/O奖值越好 | 119827636.74 | N/A | N/A | 0 | 是 |
| 19 | `experiment_result.q2_q3.risk_summary[2].q10_profit_yuan` | 越接近 verifier/O奖值越好 | 119159280.66 | N/A | N/A | 0 | 是 |
| 20 | `experiment_result.q2_q3.spearman_price_cost` | 越接近 verifier/O奖值越好 | 0.2551 | N/A | 0.3 | 0.405392520394 | 是 |

<a id="cumcm-2025-a"></a>

## CUMCM 2025 A: UAV smoke-screen strategy

- Task slug: `cumcm-2025-a-smoke-screen`
- 简洁任务描述: CUMCM 2025 A: UAV smoke-screen strategy
- 当前 instruction 子问题数: 5
- verifier 数值指标: 164 effective / 164 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2025-a-smoke-screen`; 状态: error: AgentTimeoutError(1); job reward: 0
- v4-flash B-Eval: N/A; BO-Eval: N/A; raw panel score: N/A
- v4-flash 对齐 verifier metric path 的答案覆盖: 0/164

子问题:
- 问题1: 利用无人机FY1 投放1 枚烟幕干扰弹实施对M1 的干扰，若FY1 以120 m/s 的
- 问题2: 利用无人机FY1 投放1 枚烟幕干扰弹实施对M1 的干扰，确定FY1 的飞行方
- 问题3: 利用无人机FY1 投放3 枚烟幕干扰弹，实施对M1 的干扰。请给出烟幕干扰弹
- 问题4: 利用FY1、FY2、FY3 等3 架无人机，各投放1 枚烟幕干扰弹，实施对M1 的
- 问题5: 利用5 架无人机，每架无人机至多投放3 枚烟幕干扰弹，实施对M1、M2、M3

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q1_duration_s` | 越接近 verifier/O奖值越好 | 1.5 | N/A | N/A | N/A | 是 |
| 2 | `experiment_result.q2_duration_s` | 越接近 verifier/O奖值越好 | 4.5 | N/A | N/A | N/A | 是 |
| 3 | `experiment_result.q3_union_duration_s.M1` | 越接近 verifier/O奖值越好 | 6.8 | N/A | N/A | N/A | 是 |
| 4 | `experiment_result.q3_union_duration_s.total` | 越接近 verifier/O奖值越好 | 6.8 | N/A | N/A | N/A | 是 |
| 5 | `experiment_result.q4_union_duration_s.M1` | 越接近 verifier/O奖值越好 | 8.1 | N/A | N/A | N/A | 是 |
| 6 | `experiment_result.q4_union_duration_s.total` | 越接近 verifier/O奖值越好 | 8.1 | N/A | N/A | N/A | 是 |
| 7 | `experiment_result.q5_union_duration_s.M1` | 越接近 verifier/O奖值越好 | 10.3 | N/A | N/A | N/A | 是 |
| 8 | `experiment_result.q5_union_duration_s.M2` | 越接近 verifier/O奖值越好 | 6.2 | N/A | N/A | N/A | 是 |
| 9 | `experiment_result.q5_union_duration_s.M3` | 越接近 verifier/O奖值越好 | 3.4 | N/A | N/A | N/A | 是 |
| 10 | `experiment_result.q5_union_duration_s.total` | 越接近 verifier/O奖值越好 | 19.9 | N/A | N/A | N/A | 是 |
| 11 | `q1.effective_duration_s` | 越接近 verifier/O奖值越好 | 1.5 | N/A | N/A | N/A | 是 |
| 12 | `q1.strategy.drop_time_s` | 越接近 verifier/O奖值越好 | 1.5 | N/A | N/A | N/A | 是 |
| 13 | `q1.strategy.drop_x` | 越接近 verifier/O奖值越好 | 17620 | N/A | N/A | N/A | 是 |
| 14 | `q1.strategy.drop_y` | 越接近 verifier/O奖值越好 | -0 | N/A | N/A | N/A | 是 |
| 15 | `q1.strategy.drop_z` | 越接近 verifier/O奖值越好 | 1800 | N/A | N/A | N/A | 是 |
| 16 | `q1.strategy.explode_time_s` | 越接近 verifier/O奖值越好 | 5.1 | N/A | N/A | N/A | 是 |
| 17 | `q1.strategy.explode_x` | 越接近 verifier/O奖值越好 | 17188 | N/A | N/A | N/A | 是 |
| 18 | `q1.strategy.explode_y` | 越接近 verifier/O奖值越好 | -0 | N/A | N/A | N/A | 是 |
| 19 | `q1.strategy.explode_z` | 越接近 verifier/O奖值越好 | 1736.496 | N/A | N/A | N/A | 是 |
| 20 | `q1.strategy.fuse_time_s` | 越接近 verifier/O奖值越好 | 3.6 | N/A | N/A | N/A | 是 |
| 21 | `q1.strategy.heading_deg` | 越接近 verifier/O奖值越好 | 180 | N/A | N/A | N/A | 是 |
| 22 | `q1.strategy.individual_duration_s` | 越接近 verifier/O奖值越好 | 1.5 | N/A | N/A | N/A | 是 |
| 23 | `q1.strategy.speed_mps` | 越接近 verifier/O奖值越好 | 120 | N/A | N/A | N/A | 是 |
| 24 | `q2.effective_duration_s` | 越接近 verifier/O奖值越好 | 4.5 | N/A | N/A | N/A | 是 |
| 25 | `q2.strategy.drop_time_s` | 越接近 verifier/O奖值越好 | 0.5 | N/A | N/A | N/A | 是 |
| 26 | `q2.strategy.drop_x` | 越接近 verifier/O奖值越好 | 17740.004 | N/A | N/A | N/A | 是 |
| 27 | `q2.strategy.drop_y` | 越接近 verifier/O奖值越好 | 0.674 | N/A | N/A | N/A | 是 |
| 28 | `q2.strategy.drop_z` | 越接近 verifier/O奖值越好 | 1800 | N/A | N/A | N/A | 是 |
| 29 | `q2.strategy.explode_time_s` | 越接近 verifier/O奖值越好 | 4.1 | N/A | N/A | N/A | 是 |
| 30 | `q2.strategy.explode_x` | 越接近 verifier/O奖值越好 | 17308.031 | N/A | N/A | N/A | 是 |
| 31 | `q2.strategy.explode_y` | 越接近 verifier/O奖值越好 | 5.528 | N/A | N/A | N/A | 是 |
| 32 | `q2.strategy.explode_z` | 越接近 verifier/O奖值越好 | 1736.496 | N/A | N/A | N/A | 是 |
| 33 | `q2.strategy.fuse_time_s` | 越接近 verifier/O奖值越好 | 3.6 | N/A | N/A | N/A | 是 |
| 34 | `q2.strategy.heading_deg` | 越接近 verifier/O奖值越好 | 179.356 | N/A | N/A | N/A | 是 |
| 35 | `q2.strategy.individual_duration_s` | 越接近 verifier/O奖值越好 | 4.5 | N/A | N/A | N/A | 是 |
| 36 | `q2.strategy.speed_mps` | 越接近 verifier/O奖值越好 | 120 | N/A | N/A | N/A | 是 |
| 37 | `q3.strategies[0].drop_time_s` | 越接近 verifier/O奖值越好 | 0.5 | N/A | N/A | N/A | 是 |
| 38 | `q3.strategies[0].drop_x` | 越接近 verifier/O奖值越好 | 17740.004 | N/A | N/A | N/A | 是 |
| 39 | `q3.strategies[0].drop_y` | 越接近 verifier/O奖值越好 | 0.674 | N/A | N/A | N/A | 是 |
| 40 | `q3.strategies[0].drop_z` | 越接近 verifier/O奖值越好 | 1800 | N/A | N/A | N/A | 是 |
| 41 | `q3.strategies[0].explode_time_s` | 越接近 verifier/O奖值越好 | 4.1 | N/A | N/A | N/A | 是 |
| 42 | `q3.strategies[0].explode_x` | 越接近 verifier/O奖值越好 | 17308.031 | N/A | N/A | N/A | 是 |
| 43 | `q3.strategies[0].explode_y` | 越接近 verifier/O奖值越好 | 5.528 | N/A | N/A | N/A | 是 |
| 44 | `q3.strategies[0].explode_z` | 越接近 verifier/O奖值越好 | 1736.496 | N/A | N/A | N/A | 是 |
| 45 | `q3.strategies[0].fuse_time_s` | 越接近 verifier/O奖值越好 | 3.6 | N/A | N/A | N/A | 是 |
| 46 | `q3.strategies[0].heading_deg` | 越接近 verifier/O奖值越好 | 179.356 | N/A | N/A | N/A | 是 |
| 47 | `q3.strategies[0].individual_duration_s` | 越接近 verifier/O奖值越好 | 4.5 | N/A | N/A | N/A | 是 |
| 48 | `q3.strategies[0].speed_mps` | 越接近 verifier/O奖值越好 | 120 | N/A | N/A | N/A | 是 |
| 49 | `q3.strategies[1].drop_time_s` | 越接近 verifier/O奖值越好 | 3 | N/A | N/A | N/A | 是 |
| 50 | `q3.strategies[1].drop_x` | 越接近 verifier/O奖值越好 | 17380 | N/A | N/A | N/A | 是 |
| 51 | `q3.strategies[1].drop_y` | 越接近 verifier/O奖值越好 | -0 | N/A | N/A | N/A | 是 |
| 52 | `q3.strategies[1].drop_z` | 越接近 verifier/O奖值越好 | 1800 | N/A | N/A | N/A | 是 |
| 53 | `q3.strategies[1].explode_time_s` | 越接近 verifier/O奖值越好 | 8 | N/A | N/A | N/A | 是 |
| 54 | `q3.strategies[1].explode_x` | 越接近 verifier/O奖值越好 | 16680 | N/A | N/A | N/A | 是 |
| 55 | `q3.strategies[1].explode_y` | 越接近 verifier/O奖值越好 | -0 | N/A | N/A | N/A | 是 |
| 56 | `q3.strategies[1].explode_z` | 越接近 verifier/O奖值越好 | 1677.5 | N/A | N/A | N/A | 是 |
| 57 | `q3.strategies[1].fuse_time_s` | 越接近 verifier/O奖值越好 | 5 | N/A | N/A | N/A | 是 |
| 58 | `q3.strategies[1].heading_deg` | 越接近 verifier/O奖值越好 | 180 | N/A | N/A | N/A | 是 |
| 59 | `q3.strategies[1].individual_duration_s` | 越接近 verifier/O奖值越好 | 2.3 | N/A | N/A | N/A | 是 |
| 60 | `q3.strategies[1].speed_mps` | 越接近 verifier/O奖值越好 | 140 | N/A | N/A | N/A | 是 |
| 61 | `q3.union_duration_s.M1` | 越接近 verifier/O奖值越好 | 6.8 | N/A | N/A | N/A | 是 |
| 62 | `q3.union_duration_s.total` | 越接近 verifier/O奖值越好 | 6.8 | N/A | N/A | N/A | 是 |
| 63 | `q4.strategies[0].drop_time_s` | 越接近 verifier/O奖值越好 | 0.5 | N/A | N/A | N/A | 是 |
| 64 | `q4.strategies[0].drop_x` | 越接近 verifier/O奖值越好 | 17740.004 | N/A | N/A | N/A | 是 |
| 65 | `q4.strategies[0].drop_y` | 越接近 verifier/O奖值越好 | 0.674 | N/A | N/A | N/A | 是 |
| 66 | `q4.strategies[0].drop_z` | 越接近 verifier/O奖值越好 | 1800 | N/A | N/A | N/A | 是 |
| 67 | `q4.strategies[0].explode_time_s` | 越接近 verifier/O奖值越好 | 4.1 | N/A | N/A | N/A | 是 |
| 68 | `q4.strategies[0].explode_x` | 越接近 verifier/O奖值越好 | 17308.031 | N/A | N/A | N/A | 是 |
| 69 | `q4.strategies[0].explode_y` | 越接近 verifier/O奖值越好 | 5.528 | N/A | N/A | N/A | 是 |
| 70 | `q4.strategies[0].explode_z` | 越接近 verifier/O奖值越好 | 1736.496 | N/A | N/A | N/A | 是 |
| 71 | `q4.strategies[0].fuse_time_s` | 越接近 verifier/O奖值越好 | 3.6 | N/A | N/A | N/A | 是 |
| 72 | `q4.strategies[0].heading_deg` | 越接近 verifier/O奖值越好 | 179.356 | N/A | N/A | N/A | 是 |
| 73 | `q4.strategies[0].individual_duration_s` | 越接近 verifier/O奖值越好 | 4.5 | N/A | N/A | N/A | 是 |
| 74 | `q4.strategies[0].speed_mps` | 越接近 verifier/O奖值越好 | 120 | N/A | N/A | N/A | 是 |
| 75 | `q4.strategies[1].drop_time_s` | 越接近 verifier/O奖值越好 | 31.977 | N/A | N/A | N/A | 是 |
| 76 | `q4.strategies[1].drop_x` | 越接近 verifier/O奖值越好 | 2283.971 | N/A | N/A | N/A | 是 |
| 77 | `q4.strategies[1].drop_y` | 越接近 verifier/O奖值越好 | -641.153 | N/A | N/A | N/A | 是 |
| 78 | `q4.strategies[1].drop_z` | 越接近 verifier/O奖值越好 | 700 | N/A | N/A | N/A | 是 |
| 79 | `q4.strategies[1].explode_time_s` | 越接近 verifier/O奖值越好 | 43 | N/A | N/A | N/A | 是 |
| 80 | `q4.strategies[1].explode_x` | 越接近 verifier/O奖值越好 | 1002.963 | N/A | N/A | N/A | 是 |
| 81 | `q4.strategies[1].explode_y` | 越接近 verifier/O奖值越好 | 172 | N/A | N/A | N/A | 是 |
| 82 | `q4.strategies[1].explode_z` | 越接近 verifier/O奖值越好 | 104.596 | N/A | N/A | N/A | 是 |
| 83 | `q4.strategies[1].fuse_time_s` | 越接近 verifier/O奖值越好 | 11.023 | N/A | N/A | N/A | 是 |
| 84 | `q4.strategies[1].heading_deg` | 越接近 verifier/O奖值越好 | 147.594 | N/A | N/A | N/A | 是 |
| 85 | `q4.strategies[1].individual_duration_s` | 越接近 verifier/O奖值越好 | 3.6 | N/A | N/A | N/A | 是 |
| 86 | `q4.strategies[1].speed_mps` | 越接近 verifier/O奖值越好 | 137.646 | N/A | N/A | N/A | 是 |
| 87 | `q4.union_duration_s.M1` | 越接近 verifier/O奖值越好 | 8.1 | N/A | N/A | N/A | 是 |
| 88 | `q4.union_duration_s.total` | 越接近 verifier/O奖值越好 | 8.1 | N/A | N/A | N/A | 是 |
| 89 | `q5.strategies[0].drop_time_s` | 越接近 verifier/O奖值越好 | 32.892 | N/A | N/A | N/A | 是 |
| 90 | `q5.strategies[0].drop_x` | 越接近 verifier/O奖值越好 | 2130.79 | N/A | N/A | N/A | 是 |
| 91 | `q5.strategies[0].drop_y` | 越接近 verifier/O奖值越好 | -609.343 | N/A | N/A | N/A | 是 |
| 92 | `q5.strategies[0].drop_z` | 越接近 verifier/O奖值越好 | 700 | N/A | N/A | N/A | 是 |
| 93 | `q5.strategies[0].explode_time_s` | 越接近 verifier/O奖值越好 | 44 | N/A | N/A | N/A | 是 |
| 94 | `q5.strategies[0].explode_x` | 越接近 verifier/O奖值越好 | 824.089 | N/A | N/A | N/A | 是 |
| 95 | `q5.strategies[0].explode_y` | 越接近 verifier/O奖值越好 | 198.024 | N/A | N/A | N/A | 是 |
| 96 | `q5.strategies[0].explode_z` | 越接近 verifier/O奖值越好 | 95.384 | N/A | N/A | N/A | 是 |
| 97 | `q5.strategies[0].fuse_time_s` | 越接近 verifier/O奖值越好 | 11.108 | N/A | N/A | N/A | 是 |
| 98 | `q5.strategies[0].heading_deg` | 越接近 verifier/O奖值越好 | 148.289 | N/A | N/A | N/A | 是 |
| 99 | `q5.strategies[0].individual_duration_s` | 越接近 verifier/O奖值越好 | 3.5 | N/A | N/A | N/A | 是 |
| 100 | `q5.strategies[0].speed_mps` | 越接近 verifier/O奖值越好 | 138.277 | N/A | N/A | N/A | 是 |
| 101 | `q5.strategies[1].drop_time_s` | 越接近 verifier/O奖值越好 | 34.64 | N/A | N/A | N/A | 是 |
| 102 | `q5.strategies[1].drop_x` | 越接近 verifier/O奖值越好 | 1933.416 | N/A | N/A | N/A | 是 |
| 103 | `q5.strategies[1].drop_y` | 越接近 verifier/O奖值越好 | -626.432 | N/A | N/A | N/A | 是 |
| 104 | `q5.strategies[1].drop_z` | 越接近 verifier/O奖值越好 | 700 | N/A | N/A | N/A | 是 |
| 105 | `q5.strategies[1].explode_time_s` | 越接近 verifier/O奖值越好 | 46 | N/A | N/A | N/A | 是 |
| 106 | `q5.strategies[1].explode_x` | 越接近 verifier/O奖值越好 | 599.729 | N/A | N/A | N/A | 是 |
| 107 | `q5.strategies[1].explode_y` | 越接近 verifier/O奖值越好 | 152.009 | N/A | N/A | N/A | 是 |
| 108 | `q5.strategies[1].explode_z` | 越接近 verifier/O奖值越好 | 67.605 | N/A | N/A | N/A | 是 |
| 109 | `q5.strategies[1].fuse_time_s` | 越接近 verifier/O奖值越好 | 11.36 | N/A | N/A | N/A | 是 |
| 110 | `q5.strategies[1].heading_deg` | 越接近 verifier/O奖值越好 | 149.729 | N/A | N/A | N/A | 是 |
| 111 | `q5.strategies[1].individual_duration_s` | 越接近 verifier/O奖值越好 | 3.4 | N/A | N/A | N/A | 是 |
| 112 | `q5.strategies[1].speed_mps` | 越接近 verifier/O奖值越好 | 135.931 | N/A | N/A | N/A | 是 |
| 113 | `q5.strategies[2].drop_time_s` | 越接近 verifier/O奖值越好 | 0.5 | N/A | N/A | N/A | 是 |
| 114 | `q5.strategies[2].drop_x` | 越接近 verifier/O奖值越好 | 17740.004 | N/A | N/A | N/A | 是 |
| 115 | `q5.strategies[2].drop_y` | 越接近 verifier/O奖值越好 | 0.674 | N/A | N/A | N/A | 是 |
| 116 | `q5.strategies[2].drop_z` | 越接近 verifier/O奖值越好 | 1800 | N/A | N/A | N/A | 是 |
| 117 | `q5.strategies[2].explode_time_s` | 越接近 verifier/O奖值越好 | 4.1 | N/A | N/A | N/A | 是 |
| 118 | `q5.strategies[2].explode_x` | 越接近 verifier/O奖值越好 | 17308.031 | N/A | N/A | N/A | 是 |
| 119 | `q5.strategies[2].explode_y` | 越接近 verifier/O奖值越好 | 5.528 | N/A | N/A | N/A | 是 |
| 120 | `q5.strategies[2].explode_z` | 越接近 verifier/O奖值越好 | 1736.496 | N/A | N/A | N/A | 是 |
| 121 | `q5.strategies[2].fuse_time_s` | 越接近 verifier/O奖值越好 | 3.6 | N/A | N/A | N/A | 是 |
| 122 | `q5.strategies[2].heading_deg` | 越接近 verifier/O奖值越好 | 179.356 | N/A | N/A | N/A | 是 |
| 123 | `q5.strategies[2].individual_duration_s` | 越接近 verifier/O奖值越好 | 4.5 | N/A | N/A | N/A | 是 |
| 124 | `q5.strategies[2].speed_mps` | 越接近 verifier/O奖值越好 | 120 | N/A | N/A | N/A | 是 |
| 125 | `q5.strategies[3].drop_time_s` | 越接近 verifier/O奖值越好 | 23.606 | N/A | N/A | N/A | 是 |
| 126 | `q5.strategies[3].drop_x` | 越接近 verifier/O奖值越好 | 3595.615 | N/A | N/A | N/A | 是 |
| 127 | `q5.strategies[3].drop_y` | 越接近 verifier/O奖值越好 | -748.142 | N/A | N/A | N/A | 是 |
| 128 | `q5.strategies[3].drop_z` | 越接近 verifier/O奖值越好 | 700 | N/A | N/A | N/A | 是 |
| 129 | `q5.strategies[3].explode_time_s` | 越接近 verifier/O奖值越好 | 33 | N/A | N/A | N/A | 是 |
| 130 | `q5.strategies[3].explode_x` | 越接近 verifier/O奖值越好 | 2638.774 | N/A | N/A | N/A | 是 |
| 131 | `q5.strategies[3].explode_y` | 越接近 verifier/O奖值越好 | 148 | N/A | N/A | N/A | 是 |
| 132 | `q5.strategies[3].explode_z` | 越接近 verifier/O奖值越好 | 267.577 | N/A | N/A | N/A | 是 |
| 133 | `q5.strategies[3].fuse_time_s` | 越接近 verifier/O奖值越好 | 9.394 | N/A | N/A | N/A | 是 |
| 134 | `q5.strategies[3].heading_deg` | 越接近 verifier/O奖值越好 | 136.876 | N/A | N/A | N/A | 是 |
| 135 | `q5.strategies[3].individual_duration_s` | 越接近 verifier/O奖值越好 | 3.5 | N/A | N/A | N/A | 是 |
| 136 | `q5.strategies[3].speed_mps` | 越接近 verifier/O奖值越好 | 139.551 | N/A | N/A | N/A | 是 |
| 137 | `q5.strategies[4].drop_time_s` | 越接近 verifier/O奖值越好 | 8 | N/A | N/A | N/A | 是 |
| 138 | `q5.strategies[4].drop_x` | 越接近 verifier/O奖值越好 | 11079.087 | N/A | N/A | N/A | 是 |
| 139 | `q5.strategies[4].drop_y` | 越接近 verifier/O奖值越好 | 835.803 | N/A | N/A | N/A | 是 |
| 140 | `q5.strategies[4].drop_z` | 越接近 verifier/O奖值越好 | 1400 | N/A | N/A | N/A | 是 |
| 141 | `q5.strategies[4].explode_time_s` | 越接近 verifier/O奖值越好 | 15 | N/A | N/A | N/A | 是 |
| 142 | `q5.strategies[4].explode_x` | 越接近 verifier/O奖值越好 | 10273.287 | N/A | N/A | N/A | 是 |
| 143 | `q5.strategies[4].explode_y` | 越接近 verifier/O奖值越好 | 342.13 | N/A | N/A | N/A | 是 |
| 144 | `q5.strategies[4].explode_z` | 越接近 verifier/O奖值越好 | 1159.9 | N/A | N/A | N/A | 是 |
| 145 | `q5.strategies[4].fuse_time_s` | 越接近 verifier/O奖值越好 | 7 | N/A | N/A | N/A | 是 |
| 146 | `q5.strategies[4].heading_deg` | 越接近 verifier/O奖值越好 | 211.494 | N/A | N/A | N/A | 是 |
| 147 | `q5.strategies[4].individual_duration_s` | 越接近 verifier/O奖值越好 | 2.7 | N/A | N/A | N/A | 是 |
| 148 | `q5.strategies[4].speed_mps` | 越接近 verifier/O奖值越好 | 135 | N/A | N/A | N/A | 是 |
| 149 | `q5.strategies[5].drop_time_s` | 越接近 verifier/O奖值越好 | 3 | N/A | N/A | N/A | 是 |
| 150 | `q5.strategies[5].drop_x` | 越接近 verifier/O奖值越好 | 17380 | N/A | N/A | N/A | 是 |
| 151 | `q5.strategies[5].drop_y` | 越接近 verifier/O奖值越好 | -0 | N/A | N/A | N/A | 是 |
| 152 | `q5.strategies[5].drop_z` | 越接近 verifier/O奖值越好 | 1800 | N/A | N/A | N/A | 是 |
| 153 | `q5.strategies[5].explode_time_s` | 越接近 verifier/O奖值越好 | 8 | N/A | N/A | N/A | 是 |
| 154 | `q5.strategies[5].explode_x` | 越接近 verifier/O奖值越好 | 16680 | N/A | N/A | N/A | 是 |
| 155 | `q5.strategies[5].explode_y` | 越接近 verifier/O奖值越好 | -0 | N/A | N/A | N/A | 是 |
| 156 | `q5.strategies[5].explode_z` | 越接近 verifier/O奖值越好 | 1677.5 | N/A | N/A | N/A | 是 |
| 157 | `q5.strategies[5].fuse_time_s` | 越接近 verifier/O奖值越好 | 5 | N/A | N/A | N/A | 是 |
| 158 | `q5.strategies[5].heading_deg` | 越接近 verifier/O奖值越好 | 180 | N/A | N/A | N/A | 是 |
| 159 | `q5.strategies[5].individual_duration_s` | 越接近 verifier/O奖值越好 | 2.3 | N/A | N/A | N/A | 是 |
| 160 | `q5.strategies[5].speed_mps` | 越接近 verifier/O奖值越好 | 140 | N/A | N/A | N/A | 是 |
| 161 | `q5.union_duration_s.M1` | 越接近 verifier/O奖值越好 | 10.3 | N/A | N/A | N/A | 是 |
| 162 | `q5.union_duration_s.M2` | 越接近 verifier/O奖值越好 | 6.2 | N/A | N/A | N/A | 是 |
| 163 | `q5.union_duration_s.M3` | 越接近 verifier/O奖值越好 | 3.4 | N/A | N/A | N/A | 是 |
| 164 | `q5.union_duration_s.total` | 越接近 verifier/O奖值越好 | 19.9 | N/A | N/A | N/A | 是 |

<a id="cumcm-2025-b"></a>

## CUMCM 2025 B: SiC epitaxial-layer thickness inversion

- Task slug: `cumcm-2025-b-sic-thickness`
- 简洁任务描述: CUMCM 2025 B: SiC epitaxial-layer thickness inversion
- 当前 instruction 子问题数: 3
- verifier 数值指标: 2 effective / 2 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2025-b-sic-thickness`; 状态: error: AgentTimeoutError(1); job reward: 0.143178654302
- v4-flash B-Eval: 0.143178654302; BO-Eval: 0.143178654302; raw panel score: 0.143178654302
- v4-flash 对齐 verifier metric path 的答案覆盖: 2/2

子问题:
- 问题1: 如果考虑外延层和衬底界面只有一次反射、透射所产生的干涉条纹的情形（图
- 问题2: 请根据问题1 的数学模型，设计确定外延层厚度的算法。对附件1 和附件2 提
- 问题3: 光波可以在外延层界面和衬底界面产生多次反射和透射（图2），从而产生多光

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.si_recommended_thickness_um` | 越接近 verifier/O奖值越好 | 10.5145 | N/A | 4.82505875455 | 0.181514472929 | 是 |
| 2 | `experiment_result.sic_recommended_thickness_um` | 越接近 verifier/O奖值越好 | 8.9815 | N/A | 18.1836785023 | 0.104842835674 | 是 |

<a id="cumcm-2025-c"></a>

## CUMCM 2025 C: NIPT timing and fetal abnormality modeling

- Task slug: `cumcm-2025-c-nipt`
- 简洁任务描述: CUMCM 2025 C: NIPT timing and fetal abnormality modeling
- 当前 instruction 子问题数: 4
- verifier 数值指标: 8 effective / 8 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2025-c-nipt`; 状态: scored; job reward: 0.524882309574
- v4-flash B-Eval: 0.524882309574; BO-Eval: 0.524882309574; raw panel score: 0.524882309574
- v4-flash 对齐 verifier metric path 的答案覆盖: 8/8

子问题:
- 问题1: 试分析胎儿Y 染色体浓度与孕妇的孕周数和BMI 等指标的相关特性，给出相应的关系模
- 问题2: 临床证明，男胎孕妇的BMI 是影响胎儿Y 染色体浓度的最早达标时间（即浓度达到或超
- 问题3: 男胎Y 染色体浓度达标时间受多种因素(身高、体重、年龄等)的影响，试综合考虑这些因
- 问题4: 由于孕妇和女胎都不携带Y 染色体，重要的是如何判定女胎是否异常。试以女胎孕妇的21

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.earliest_recommended_week` | 越接近 verifier/O奖值越好 | 12 | N/A | 12 | 1 | 是 |
| 2 | `experiment_result.female_loo_accuracy` | 越接近 verifier/O奖值越好 | 0.8659 | N/A | 0.9174 | 0.668614228354 | 是 |
| 3 | `experiment_result.latest_recommended_week` | 越接近 verifier/O奖值越好 | 20 | N/A | 22 | 0.545454545455 | 是 |
| 4 | `experiment_result.male_pseudo_r2` | 越接近 verifier/O奖值越好 | 0.90064 | N/A | 0.04413 | 0.112044659952 | 是 |
| 5 | `male_lmm.mother_count` | 越接近 verifier/O奖值越好 | 267 | N/A | 267 | 1 | 是 |
| 6 | `male_lmm.pseudo_r2` | 越接近 verifier/O奖值越好 | 0.90064 | N/A | 0.04413 | 0.112044659952 | 是 |
| 7 | `male_lmm.residual_sigma_logit` | 越接近 verifier/O奖值越好 | 0.47707 | N/A | 0.495318 | 0.758293110665 | 是 |
| 8 | `male_lmm.rmse_fetal_fraction` | 越接近 verifier/O奖值越好 | 0.01056 | N/A | 0.495318 | 0.00260727221551 | 是 |

<a id="mcm-2023-a"></a>

## MCM 2023 A: drought-stricken plant communities

- Task slug: `mcm-2023-a-plant-community`
- 简洁任务描述: MCM 2023 A: drought-stricken plant communities
- 当前 instruction 子问题数: 9
- verifier 数值指标: 41 effective / 41 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2023-a-plant-community`; 状态: error: AgentTimeoutError(1); job reward: 0
- v4-flash B-Eval: -0.137723472028; BO-Eval: 0; raw panel score: 0.365081194639
- v4-flash 对齐 verifier metric path 的答案覆盖: 41/41

子问题:
- Q1: 大量观察表明，存在的不同物种的数量在如何当连续几代暴露于干旱循环时，植物群落会适应。
- Q2: 这对长期而言意味着什么植物群落的生存能力？
- Q3: 具体来说，你应该：开发一个数学模型来预测植物群落如何随时间变化暴露于各种不规则的天气周期。
- Q4: 考虑以下因素问题：需要多少种不同的植物物种才能使社区受益以及什么随着物种数量的增加会发生什么？
- Q5: 群落中的物种类型如何影响您的结果？
- Q6: 发生频率更高、变化范围更广会产生什么影响？
- Q7: 未来天气周期中是否会出现干旱？
- Q8: ##第2页/©2023COMAP公司/www.comap.com/www.mathmodels.org//info@comap.com/污染和栖息地减少等其他因素如何影响您的结论？
- Q9: 您的模型表明应该采取哪些措施来确保企业的长期生存能力植物群落对更大的环境有什么影响？

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.beta_decline_pct` | 越接近 verifier/O奖值越好 | 32 | N/A | 7.04 | 0.133333333333 | 是 |
| 2 | `reproduced.coefficient_of_variation_1_to_5[0]` | 越接近 verifier/O奖值越好 | 0.1864 | N/A | 0.1561 | 0.424698108909 | 是 |
| 3 | `reproduced.coefficient_of_variation_1_to_5[1]` | 越接近 verifier/O奖值越好 | 0.0653 | N/A | 0.1392 | 0.0958696290496 | 是 |
| 4 | `reproduced.drought_buffer[0].diversity_buffer_gain_pct` | 越接近 verifier/O奖值越好 | 0 | N/A | 114.93 | 8.70094083273e-07 | 是 |
| 5 | `reproduced.drought_buffer[0].drought_frequency_per_50y` | 越接近 verifier/O奖值越好 | 0 | N/A | 10 | 9.999900001e-06 | 是 |
| 6 | `reproduced.drought_buffer[0].five_species_biomass_index` | 越接近 verifier/O奖值越好 | 1 | N/A | 2.0588 | 0.101798439091 | 是 |
| 7 | `reproduced.drought_buffer[0].monoculture_biomass_index` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.9579 | 0.740283775447 | 是 |
| 8 | `reproduced.drought_buffer[1].diversity_buffer_gain_pct` | 越接近 verifier/O奖值越好 | 7.92 | N/A | 121.63 | 0.00828882508695 | 是 |
| 9 | `reproduced.drought_buffer[1].drought_frequency_per_50y` | 越接近 verifier/O奖值越好 | 3 | N/A | 10 | 0.0489130434783 | 是 |
| 10 | `reproduced.drought_buffer[1].five_species_biomass_index` | 越接近 verifier/O奖值越好 | 0.8992 | N/A | 1.9674 | 0.0917469883616 | 是 |
| 11 | `reproduced.drought_buffer[1].monoculture_biomass_index` | 越接近 verifier/O奖值越好 | 0.82 | N/A | 0.8877 | 0.592414208308 | 是 |
| 12 | `reproduced.drought_buffer[2].diversity_buffer_gain_pct` | 越接近 verifier/O奖值越好 | 14.96 | N/A | 112.8 | 0.0180177286742 | 是 |
| 13 | `reproduced.drought_buffer[2].drought_frequency_per_50y` | 越接近 verifier/O奖值越好 | 6 | N/A | 2 | 0.152542372881 | 是 |
| 14 | `reproduced.drought_buffer[2].five_species_biomass_index` | 越接近 verifier/O奖值越好 | 0.8096 | N/A | 2.1021 | 0.0699110280847 | 是 |
| 15 | `reproduced.drought_buffer[2].monoculture_biomass_index` | 越接近 verifier/O奖值越好 | 0.66 | N/A | 0.9879 | 0.194546794399 | 是 |
| 16 | `reproduced.five_species_pielou_evenness` | 越接近 verifier/O奖值越好 | 0.8826 | N/A | 0.9673 | 0.555641827377 | 是 |
| 17 | `reproduced.optimal_species_count` | 越接近 verifier/O奖值越好 | 2 | N/A | 5 | 0.0740740740741 | 是 |
| 18 | `reproduced.species_count_summary[0].coefficient_of_variation` | 越接近 verifier/O奖值越好 | 0.1864 | N/A | 0.1561 | 0.424698108909 | 是 |
| 19 | `reproduced.species_count_summary[0].mean_total_biomass_last20y` | 越接近 verifier/O奖值越好 | 371.5034 | N/A | 983.46 | 0.0679023534954 | 是 |
| 20 | `reproduced.species_count_summary[0].pielou_evenness` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 21 | `reproduced.species_count_summary[0].species_count` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 22 | `reproduced.species_count_summary[1].coefficient_of_variation` | 越接近 verifier/O奖值越好 | 0.1419 | N/A | 0.1392 | 0.863138686131 | 是 |
| 23 | `reproduced.species_count_summary[1].mean_total_biomass_last20y` | 越接近 verifier/O奖值越好 | 500.0073 | N/A | 1532.16 | 0.054938130789 | 是 |
| 24 | `reproduced.species_count_summary[1].pielou_evenness` | 越接近 verifier/O奖值越好 | 0.958 | N/A | 0.9442 | 0.892823858341 | 是 |
| 25 | `reproduced.species_count_summary[1].species_count` | 越接近 verifier/O奖值越好 | 2 | N/A | 2 | 1 | 是 |
| 26 | `reproduced.species_count_summary[2].coefficient_of_variation` | 越接近 verifier/O奖值越好 | 0.1037 | N/A | 0.1231 | 0.390780052757 | 是 |
| 27 | `reproduced.species_count_summary[2].mean_total_biomass_last20y` | 越接近 verifier/O奖值越好 | 452.1233 | N/A | 1722.07 | 0.0409717072242 | 是 |
| 28 | `reproduced.species_count_summary[2].pielou_evenness` | 越接近 verifier/O奖值越好 | 0.9285 | N/A | 0.9981 | 0.615512098111 | 是 |
| 29 | `reproduced.species_count_summary[2].species_count` | 越接近 verifier/O奖值越好 | 3 | N/A | 3 | 1 | 是 |
| 30 | `reproduced.species_count_summary[3].coefficient_of_variation` | 越接近 verifier/O奖值越好 | 0.0788 | N/A | 0.1136 | 0.213665943601 | 是 |
| 31 | `reproduced.species_count_summary[3].mean_total_biomass_last20y` | 越接近 verifier/O奖值越好 | 394.0814 | N/A | 1851.48 | 0.0314282804371 | 是 |
| 32 | `reproduced.species_count_summary[3].pielou_evenness` | 越接近 verifier/O奖值越好 | 0.9066 | N/A | 0.9939 | 0.554800807784 | 是 |
| 33 | `reproduced.species_count_summary[3].species_count` | 越接近 verifier/O奖值越好 | 4 | N/A | 4 | 1 | 是 |
| 34 | `reproduced.species_count_summary[4].coefficient_of_variation` | 越接近 verifier/O奖值越好 | 0.0653 | N/A | 0.1028 | 0.172842773954 | 是 |
| 35 | `reproduced.species_count_summary[4].mean_total_biomass_last20y` | 越接近 verifier/O奖值越好 | 335.2487 | N/A | 1968.19 | 0.0240440699353 | 是 |
| 36 | `reproduced.species_count_summary[4].pielou_evenness` | 越接近 verifier/O奖值越好 | 0.8826 | N/A | 0.9673 | 0.555641827377 | 是 |
| 37 | `reproduced.species_count_summary[4].species_count` | 越接近 verifier/O奖值越好 | 5 | N/A | 5 | 1 | 是 |
| 38 | `target_comparison.beta_decline_pct.actual` | 越接近 verifier/O奖值越好 | 32 | N/A | 7.04 | 0.133333333333 | 是 |
| 39 | `target_comparison.cov_decrease_1_to_5.actual` | 越接近 verifier/O奖值越好 | 0.1211 | N/A | [0.1561, 0.1392, 0.1231, 0.1136, 0.1028] | 0 | 是 |
| 40 | `target_comparison.five_species_pielou_evenness.actual` | 越接近 verifier/O奖值越好 | 0.8826 | N/A | 0.9673 | 0.555641827377 | 是 |
| 41 | `target_comparison.optimal_species_count.actual` | 越接近 verifier/O奖值越好 | 2 | N/A | 5 | 0.0740740740741 | 是 |

<a id="mcm-2023-b"></a>

## MCM 2023 B: reimagining Maasai Mara

- Task slug: `mcm-2023-b-maasai-mara`
- 简洁任务描述: MCM 2023 B: reimagining Maasai Mara
- 当前 instruction 子问题数: 3
- verifier 数值指标: 11 effective / 11 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2023-b-maasai-mara`; 状态: scored; job reward: 0
- v4-flash B-Eval: -0.570725974269; BO-Eval: 0; raw panel score: 0.0319312757315
- v4-flash 对齐 verifier metric path 的答案覆盖: 11/11

子问题:
- Q1: 考虑并建议针对不同领域的具体政策和管理策略 在当前的保护区内，将保护野生动物和其他自然资源，同时 也平衡了居住在该地区的人们的利益。这些政策和 战略应有助于减轻因失去机会而造成的影响 居住在保护...
- Q2: 制定并描述一种方法来确定哪些政策和管理 策略将带来最好的结果。你的报告应该讨论如何排名和 比较您的方法的结果。请务必包含描述和分析 用于预测动物与人之间相互作用的模型，以及 对保护区内及周边地区...
- Q3: 根据您提出的计划，提供对将导致的长期趋势的预测 从你的建议中。分析并提供确定性的估计 可能的长期结果的影响。您还应该描述您如何 该方法可应用于其他野生动物管理领域。

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.best_scenario_benefit_million` | 越接近 verifier/O奖值越好 | 154948.974 | N/A | 117.86 | 0.107215671661 | 是 |
| 2 | `reproduced.mean_sanctuary_to_tourism_interaction_distance` | 越接近 verifier/O奖值越好 | 2.7376 | N/A | 9.3093 | 0.0476089720142 | 是 |
| 3 | `reproduced.scenario2_counts.agricultural_area` | 越接近 verifier/O奖值越好 | 12 | N/A | 100 | 0.0161001788909 | 是 |
| 4 | `reproduced.scenario2_counts.hunting_area` | 越接近 verifier/O奖值越好 | 2 | N/A | 40 | 0.00627615062762 | 是 |
| 5 | `reproduced.scenario2_counts.tourism_area` | 越接近 verifier/O奖值越好 | 9 | N/A | 100 | 0.011728931364 | 是 |
| 6 | `reproduced.scenario2_counts.wildlife_sanctuary` | 越接近 verifier/O奖值越好 | 13 | N/A | 160 | 0.0105008077544 | 是 |
| 7 | `target_comparison.scenario2_agriculture_cells.actual` | 越接近 verifier/O奖值越好 | 12 | N/A | 100 | 0.0161001788909 | 是 |
| 8 | `target_comparison.scenario2_benefit_million.actual` | 越接近 verifier/O奖值越好 | 154948.974 | N/A | 104.24 | 0.107207252097 | 是 |
| 9 | `target_comparison.scenario2_hunting_cells.actual` | 越接近 verifier/O奖值越好 | 2 | N/A | 40 | 0.00627615062762 | 是 |
| 10 | `target_comparison.scenario2_tourism_cells.actual` | 越接近 verifier/O奖值越好 | 9 | N/A | 100 | 0.011728931364 | 是 |
| 11 | `target_comparison.scenario2_wildlife_cells.actual` | 越接近 verifier/O奖值越好 | 13 | N/A | 160 | 0.0105008077544 | 是 |

<a id="mcm-2023-c"></a>

## MCM 2023 C: predicting Wordle results

- Task slug: `mcm-2023-c-wordle`
- 简洁任务描述: MCM 2023 C: predicting Wordle results
- 当前 instruction 子问题数: 4
- verifier 数值指标: 17 effective / 23 total
- 评分版本: `tb-mathmodeling-v4-endpoint-target-minmax`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2023-c-wordle`; 状态: scored; job reward: 0.143159490288
- v4-flash B-Eval: 0.143159490288; BO-Eval: 0.143159490288; raw panel score: 0.143159490288
- v4-flash 对齐 verifier metric path 的答案覆盖: 21/23

子问题:
- Q1: 报告结果的数量每天都有所不同。开发一个模型来解释这种变化并 使用您的模型为 3 月份报告的结果数量创建预测区间 2023 年 1 月 1 日。该词的任何属性是否会影响报告的分数百分比 玩困难模式...
- Q2: 对于未来日期的给定未来解决方案词，开发一个模型，使您能够 预测报告结果的分布。换句话说，预测相关的 未来日期 (1, 2, 3, 4, 5, 6, X) 的百分比。与哪些不确定性相关 你的模型和...
- Q3: 开发并总结一个模型，按难度对解决方案单词进行分类。识别 与每个分类相关联的给定单词的属性。使用你的模型， EERIE 这个词有多难？讨论您的分类模型的准确性。
- Q4: 列出并描述该数据集的一些其他有趣的特征。

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.best_tree_holdout_accuracy` | 越高越好 | 1 | 0.422222 | 0.3211 | 0 | 是 |
| 2 | `reproduced.calibrated_lightgbm_like_accuracy` | 越高越好 | 0.7 | 0.422222 | 0.3211 | 0 | 是 |
| 3 | `reproduced.difficulty_metrics[0].holdout_accuracy` | 越高越好 | 1 | 0.422222 | 0.3211 | 0 | 是 |
| 4 | `reproduced.difficulty_metrics[0].train_accuracy` | 缺 baseline；不计分 | 1 | N/A | 0.4011 | 0 | 否 |
| 5 | `reproduced.difficulty_metrics[1].holdout_accuracy` | 越高越好 | 1 | 0.422222 | N/A | 0 | 是 |
| 6 | `reproduced.difficulty_metrics[1].train_accuracy` | 缺 baseline；不计分 | 1 | N/A | N/A | 0 | 否 |
| 7 | `reproduced.eerie.difficulty_group` | 精确值；不计分 | 2 | 2 | 3 | 0 | 否 |
| 8 | `reproduced.eerie.paper_aligned_distribution_pct[0]` | 越高越好 | 0.649 | 0.245 | 0.3 | 0.136138613861 | 是 |
| 9 | `reproduced.eerie.paper_aligned_distribution_pct[1]` | 越高越好 | 7.5792 | 7.01 | 4.7 | 0 | 是 |
| 10 | `reproduced.eerie.paper_aligned_distribution_pct[2]` | 越高越好 | 26.2985 | 22.062 | 19.4 | 0 | 是 |
| 11 | `reproduced.eerie.paper_aligned_distribution_pct[3]` | 越高越好 | 32.6147 | 30.668 | 33.4 | 0.596599373298 | 是 |
| 12 | `reproduced.eerie.paper_aligned_distribution_pct[4]` | 越低越好 | 20.9304 | 22.491 | 27 | 0 | 是 |
| 13 | `reproduced.eerie.paper_aligned_distribution_pct[5]` | 越低越好 | 9.6302 | 11.839 | 13 | 0 | 是 |
| 14 | `reproduced.eerie.paper_aligned_distribution_pct[6]` | 越低越好 | 2.298 | 5.685 | 2.3 | 0.999409506938 | 是 |
| 15 | `reproduced.forecast_record.horizon_days` | 精确值；不计分 | 60 | 60 | 60 | 0 | 否 |
| 16 | `reproduced.forecast_record.raw_80_lower` | 越低越好 | 0 | 20365 | 6250 | 0.693100908421 | 是 |
| 17 | `reproduced.forecast_record.raw_80_upper` | 越高越好 | 59621.565 | 30713 | 13522 | 0 | 是 |
| 18 | `reproduced.forecast_record.raw_ma_forecast` | 越低越好 | 16662.852 | 23612 | 9193 | 0 | 是 |
| 19 | `target_comparison.eerie_distribution_sum_pct.actual` | 精确值；不计分 | 100 | 100 | 100 | 0 | 否 |
| 20 | `target_comparison.eerie_group.actual` | 精确值；不计分 | 2 | 2 | 3 | 0 | 否 |
| 21 | `target_comparison.forecast_lower.actual` | 越低越好 | 10139.23 | 20365 | 0 | 0.00846293237575 | 是 |
| 22 | `target_comparison.forecast_upper.actual` | 越高越好 | 30808.07 | 30713 | 0 | 0 | 是 |
| 23 | `target_comparison.lightgbm_like_accuracy.actual` | 越高越好 | 0.7 | 0.422222 | 0.3211 | 0 | 是 |

<a id="mcm-2024-a"></a>

## MCM 2024 A: lamprey sex-ratio ecology

- Task slug: `mcm-2024-a-lamprey`
- 简洁任务描述: MCM 2024 A: lamprey sex-ratio ecology
- 当前 instruction 子问题数: 4
- verifier 数值指标: 105 effective / 105 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2024-a-lamprey`; 状态: scored; job reward: 0
- v4-flash B-Eval: -0.24548365989; BO-Eval: 0; raw panel score: 0.21135209011
- v4-flash 对齐 verifier metric path 的答案覆盖: 105/105

子问题:
- Q1: 当七鳃鳗数量减少时，会对更大的生态系统产生什么影响？ 改变性别比例？
- Q2: 七鳃鳗种群的优点和缺点是什么？
- Q3: 考虑到性别比例的变化，对生态系统稳定性有何影响？
- Q4: 七鳃鳗种群中性别比例可变的生态系统能否为七鳃鳗种群提供优势？ 生态系统中的其他生物，例如寄生虫？

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.adaptive_vs_fixed[0].adaptive_gain_pct` | 越接近 verifier/O奖值越好 | 3.26 | N/A | -0.1 | 0.104286628279 | 是 |
| 2 | `experiment_result.adaptive_vs_fixed[0].adaptive_stability` | 越接近 verifier/O奖值越好 | 0.9144 | N/A | 0.3841 | 0.171442499391 | 是 |
| 3 | `experiment_result.adaptive_vs_fixed[0].fixed_stability` | 越接近 verifier/O奖值越好 | 0.8855 | N/A | 0.3845 | 0.174982709218 | 是 |
| 4 | `experiment_result.adaptive_vs_fixed[1].adaptive_gain_pct` | 越接近 verifier/O奖值越好 | 1.04 | N/A | -0.66 | 0.0683910565541 | 是 |
| 5 | `experiment_result.adaptive_vs_fixed[1].adaptive_stability` | 越接近 verifier/O奖值越好 | 0.8824 | N/A | 0.3137 | 0.156966919068 | 是 |
| 6 | `experiment_result.adaptive_vs_fixed[1].fixed_stability` | 越接近 verifier/O奖值越好 | 0.8733 | N/A | 0.3158 | 0.158231364828 | 是 |
| 7 | `experiment_result.adaptive_vs_fixed[2].adaptive_gain_pct` | 越接近 verifier/O奖值越好 | 0.31 | N/A | 22.04 | 0.00170899334779 | 是 |
| 8 | `experiment_result.adaptive_vs_fixed[2].adaptive_stability` | 越接近 verifier/O奖值越好 | 0.8659 | N/A | 0.4839 | 0.213842949694 | 是 |
| 9 | `experiment_result.adaptive_vs_fixed[2].fixed_stability` | 越接近 verifier/O奖值越好 | 0.8632 | N/A | 0.3965 | 0.181635816541 | 是 |
| 10 | `experiment_result.adaptive_vs_fixed[3].adaptive_gain_pct` | 越接近 verifier/O奖值越好 | 3.08 | N/A | 0.95 | 0.147863658185 | 是 |
| 11 | `experiment_result.adaptive_vs_fixed[3].adaptive_stability` | 越接近 verifier/O奖值越好 | 0.8566 | N/A | 0.3612 | 0.171837804584 | 是 |
| 12 | `experiment_result.adaptive_vs_fixed[3].fixed_stability` | 越接近 verifier/O奖值越好 | 0.831 | N/A | 0.3578 | 0.174055714585 | 是 |
| 13 | `experiment_result.largest_stability_gain.adaptive_gain_pct` | 越接近 verifier/O奖值越好 | 3.26 | N/A | 22.04 | 0.0204056084126 | 是 |
| 14 | `experiment_result.largest_stability_gain.adaptive_stability` | 越接近 verifier/O奖值越好 | 0.9144 | N/A | 0.4839 | 0.203114240654 | 是 |
| 15 | `experiment_result.largest_stability_gain.fixed_stability` | 越接近 verifier/O奖值越好 | 0.8855 | N/A | 0.3965 | 0.178510230824 | 是 |
| 16 | `experiment_result.parasite_coexistence_case.final_parasite_index` | 越接近 verifier/O奖值越好 | 8.562 | N/A | 0.3124 | 0.110750842941 | 是 |
| 17 | `experiment_result.parasite_coexistence_case.host_fish_index` | 越接近 verifier/O奖值越好 | 1080.356 | N/A | 0.5981 | 0.107195843839 | 是 |
| 18 | `experiment_result.scenario_summary[0].composite_stability` | 越接近 verifier/O奖值越好 | 0.8855 | N/A | 0.3841 | 0.174867524603 | 是 |
| 19 | `experiment_result.scenario_summary[0].final_host_fish` | 越接近 verifier/O奖值越好 | 1052.013 | N/A | 432 | 0.169166885895 | 是 |
| 20 | `experiment_result.scenario_summary[0].final_lamprey` | 越接近 verifier/O奖值越好 | 2079.718 | N/A | 0 | 0.107142857143 | 是 |
| 21 | `experiment_result.scenario_summary[0].final_parasite` | 越接近 verifier/O奖值越好 | 5.506 | N/A | 120 | 0.00573767189048 | 是 |
| 22 | `experiment_result.scenario_summary[0].mean_biomass` | 越接近 verifier/O奖值越好 | 3187.261 | N/A | 552 | 0.126741300898 | 是 |
| 23 | `experiment_result.scenario_summary[0].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.8213 | N/A | 0.4766 | 0.222345552006 | 是 |
| 24 | `experiment_result.scenario_summary[0].resilience` | 越接近 verifier/O奖值越好 | 0.8693 | N/A | 0.1595 | 0.12813407426 | 是 |
| 25 | `experiment_result.scenario_summary[0].resistance` | 越接近 verifier/O奖值越好 | 0.8979 | N/A | 0.6436 | 0.297606947145 | 是 |
| 26 | `experiment_result.scenario_summary[0].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4715 | N/A | 0.5236 | 0.15703258395 | 是 |
| 27 | `experiment_result.scenario_summary[0].species_persistence` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.6667 | 0.264725347452 | 是 |
| 28 | `experiment_result.scenario_summary[0].sustainability` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.552 | 0.211267605634 | 是 |
| 29 | `experiment_result.scenario_summary[1].composite_stability` | 越接近 verifier/O奖值越好 | 0.9144 | N/A | 0.3845 | 0.171549713271 | 是 |
| 30 | `experiment_result.scenario_summary[1].final_host_fish` | 越接近 verifier/O奖值越好 | 1163.941 | N/A | 432 | 0.160246316397 | 是 |
| 31 | `experiment_result.scenario_summary[1].final_lamprey` | 越接近 verifier/O奖值越好 | 1262.576 | N/A | 0 | 0.107142857143 | 是 |
| 32 | `experiment_result.scenario_summary[1].final_parasite` | 越接近 verifier/O奖值越好 | 38.764 | N/A | 120 | 0.0541600378541 | 是 |
| 33 | `experiment_result.scenario_summary[1].mean_biomass` | 越接近 verifier/O奖值越好 | 2482.149 | N/A | 552 | 0.13368804319 | 是 |
| 34 | `experiment_result.scenario_summary[1].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.7913 | N/A | 0.4766 | 0.231794481223 | 是 |
| 35 | `experiment_result.scenario_summary[1].resilience` | 越接近 verifier/O奖值越好 | 0.9732 | N/A | 0.1601 | 0.12558985852 | 是 |
| 36 | `experiment_result.scenario_summary[1].resistance` | 越接近 verifier/O奖值越好 | 0.9155 | N/A | 0.6431 | 0.287396013185 | 是 |
| 37 | `experiment_result.scenario_summary[1].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4177 | N/A | 0.5236 | 0.15985732327 | 是 |
| 38 | `experiment_result.scenario_summary[1].species_persistence` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.6667 | 0.264725347452 | 是 |
| 39 | `experiment_result.scenario_summary[1].sustainability` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.552 | 0.211267605634 | 是 |
| 40 | `experiment_result.scenario_summary[2].composite_stability` | 越接近 verifier/O奖值越好 | 0.8733 | N/A | 0.3137 | 0.157731232578 | 是 |
| 41 | `experiment_result.scenario_summary[2].final_host_fish` | 越接近 verifier/O奖值越好 | 987.127 | N/A | 431.37 | 0.17569428879 | 是 |
| 42 | `experiment_result.scenario_summary[2].final_lamprey` | 越接近 verifier/O奖值越好 | 2588.436 | N/A | 0.09 | 0.107146183461 | 是 |
| 43 | `experiment_result.scenario_summary[2].final_parasite` | 越接近 verifier/O奖值越好 | 1.737 | N/A | 120 | 0.00175941138219 | 是 |
| 44 | `experiment_result.scenario_summary[2].mean_biomass` | 越接近 verifier/O奖值越好 | 3646.292 | N/A | 550.52 | 0.123836552645 | 是 |
| 45 | `experiment_result.scenario_summary[2].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.8169 | N/A | 0.4783 | 0.22451148346 | 是 |
| 46 | `experiment_result.scenario_summary[2].resilience` | 越接近 verifier/O奖值越好 | 0.8536 | N/A | 0.067 | 0.115217449991 | 是 |
| 47 | `experiment_result.scenario_summary[2].resistance` | 越接近 verifier/O奖值越好 | 0.8768 | N/A | 0.8353 | 0.717140598162 | 是 |
| 48 | `experiment_result.scenario_summary[2].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4637 | N/A | 0.5254 | 0.157677585229 | 是 |
| 49 | `experiment_result.scenario_summary[2].species_persistence` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.6667 | 0.264725347452 | 是 |
| 50 | `experiment_result.scenario_summary[2].sustainability` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.5515 | 0.211081794195 | 是 |
| 51 | `experiment_result.scenario_summary[3].composite_stability` | 越接近 verifier/O奖值越好 | 0.8824 | N/A | 0.3158 | 0.157457084736 | 是 |
| 52 | `experiment_result.scenario_summary[3].final_host_fish` | 越接近 verifier/O奖值越好 | 1080.356 | N/A | 431.63 | 0.166556950027 | 是 |
| 53 | `experiment_result.scenario_summary[3].final_lamprey` | 越接近 verifier/O奖值越好 | 1900.454 | N/A | 0.05 | 0.107145374055 | 是 |
| 54 | `experiment_result.scenario_summary[3].final_parasite` | 越接近 verifier/O奖值越好 | 8.562 | N/A | 120 | 0.0091356064583 | 是 |
| 55 | `experiment_result.scenario_summary[3].mean_biomass` | 越接近 verifier/O奖值越好 | 3041.299 | N/A | 550.98 | 0.127818124467 | 是 |
| 56 | `experiment_result.scenario_summary[3].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.8077 | N/A | 0.4776 | 0.226975532991 | 是 |
| 57 | `experiment_result.scenario_summary[3].resilience` | 越接近 verifier/O奖值越好 | 0.8953 | N/A | 0.0695 | 0.115122005581 | 是 |
| 58 | `experiment_result.scenario_summary[3].resistance` | 越接近 verifier/O奖值越好 | 0.873 | N/A | 0.8209 | 0.667856687492 | 是 |
| 59 | `experiment_result.scenario_summary[3].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4471 | N/A | 0.5247 | 0.158434088894 | 是 |
| 60 | `experiment_result.scenario_summary[3].species_persistence` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.6667 | 0.264725347452 | 是 |
| 61 | `experiment_result.scenario_summary[3].sustainability` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.5517 | 0.211156079535 | 是 |
| 62 | `experiment_result.scenario_summary[4].composite_stability` | 越接近 verifier/O奖值越好 | 0.8632 | N/A | 0.4839 | 0.214511145534 | 是 |
| 63 | `experiment_result.scenario_summary[4].final_host_fish` | 越接近 verifier/O奖值越好 | 930.367 | N/A | 298.38 | 0.150133646923 | 是 |
| 64 | `experiment_result.scenario_summary[4].final_lamprey` | 越接近 verifier/O奖值越好 | 3056.291 | N/A | 13.46 | 0.107565824298 | 是 |
| 65 | `experiment_result.scenario_summary[4].final_parasite` | 越接近 verifier/O奖值越好 | 0.616 | N/A | 120 | 0.000618795304656 | 是 |
| 66 | `experiment_result.scenario_summary[4].mean_biomass` | 越接近 verifier/O奖值越好 | 4074.932 | N/A | 431.83 | 0.118339964903 | 是 |
| 67 | `experiment_result.scenario_summary[4].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.8076 | N/A | 0.6548 | 0.388095085539 | 是 |
| 68 | `experiment_result.scenario_summary[4].resilience` | 越接近 verifier/O奖值越好 | 0.8431 | N/A | 0.2624 | 0.148373888354 | 是 |
| 69 | `experiment_result.scenario_summary[4].resistance` | 越接近 verifier/O奖值越好 | 0.8612 | N/A | 1 | 0.426787366195 | 是 |
| 70 | `experiment_result.scenario_summary[4].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4471 | N/A | 0.7194 | 0.19265725266 | 是 |
| 71 | `experiment_result.scenario_summary[4].species_persistence` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 72 | `experiment_result.scenario_summary[4].sustainability` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.4318 | 0.174367916303 | 是 |
| 73 | `experiment_result.scenario_summary[5].composite_stability` | 越接近 verifier/O奖值越好 | 0.8659 | N/A | 0.3965 | 0.181242892128 | 是 |
| 74 | `experiment_result.scenario_summary[5].final_host_fish` | 越接近 verifier/O奖值越好 | 1007.488 | N/A | 303.83 | 0.146622519139 | 是 |
| 75 | `experiment_result.scenario_summary[5].final_lamprey` | 越接近 verifier/O奖值越好 | 2469.707 | N/A | 12.91 | 0.107645266506 | 是 |
| 76 | `experiment_result.scenario_summary[5].final_parasite` | 越接近 verifier/O奖值越好 | 2.354 | N/A | 120 | 0.00239535013086 | 是 |
| 77 | `experiment_result.scenario_summary[5].mean_biomass` | 越接近 verifier/O奖值越好 | 3554.691 | N/A | 436.77 | 0.120345565004 | 是 |
| 78 | `experiment_result.scenario_summary[5].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.8073 | N/A | 0.6476 | 0.377572337241 | 是 |
| 79 | `experiment_result.scenario_summary[5].resilience` | 越接近 verifier/O奖值越好 | 0.8628 | N/A | 0.1428 | 0.125721279944 | 是 |
| 80 | `experiment_result.scenario_summary[5].resistance` | 越接近 verifier/O奖值越好 | 0.8507 | N/A | 0.9999 | 0.406249502555 | 是 |
| 81 | `experiment_result.scenario_summary[5].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4465 | N/A | 0.7115 | 0.191045367497 | 是 |
| 82 | `experiment_result.scenario_summary[5].species_persistence` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 83 | `experiment_result.scenario_summary[5].sustainability` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.4367 | 0.175618322845 | 是 |
| 84 | `experiment_result.scenario_summary[6].composite_stability` | 越接近 verifier/O奖值越好 | 0.831 | N/A | 0.3612 | 0.175094816688 | 是 |
| 85 | `experiment_result.scenario_summary[6].final_host_fish` | 越接近 verifier/O奖值越好 | 892.229 | N/A | 180.88 | 0.130822732211 | 是 |
| 86 | `experiment_result.scenario_summary[6].final_lamprey` | 越接近 verifier/O奖值越好 | 3383.705 | N/A | 18.19 | 0.107659600554 | 是 |
| 87 | `experiment_result.scenario_summary[6].final_parasite` | 越接近 verifier/O奖值越好 | 0.302 | N/A | 120 | 0.000302670313855 | 是 |
| 88 | `experiment_result.scenario_summary[6].mean_biomass` | 越接近 verifier/O奖值越好 | 4378.203 | N/A | 319.01 | 0.114598210204 | 是 |
| 89 | `experiment_result.scenario_summary[6].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.7992 | N/A | 0.7763 | 0.807245547288 | 是 |
| 90 | `experiment_result.scenario_summary[6].resilience` | 越接近 verifier/O奖值越好 | 0.8381 | N/A | 0.1481 | 0.127214219578 | 是 |
| 91 | `experiment_result.scenario_summary[6].resistance` | 越接近 verifier/O奖值越好 | 0.8493 | N/A | 0.9974 | 0.407637911174 | 是 |
| 92 | `experiment_result.scenario_summary[6].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4321 | N/A | 0.8529 | 0.228815048758 | 是 |
| 93 | `experiment_result.scenario_summary[6].species_persistence` | 越接近 verifier/O奖值越好 | 0.8333 | N/A | 1 | 0.374943756187 | 是 |
| 94 | `experiment_result.scenario_summary[6].sustainability` | 越接近 verifier/O奖值越好 | 0.8333 | N/A | 0.3191 | 0.162807963582 | 是 |
| 95 | `experiment_result.scenario_summary[7].composite_stability` | 越接近 verifier/O奖值越好 | 0.8566 | N/A | 0.3578 | 0.170866633865 | 是 |
| 96 | `experiment_result.scenario_summary[7].final_host_fish` | 越接近 verifier/O奖值越好 | 959.411 | N/A | 179.55 | 0.128637503029 | 是 |
| 97 | `experiment_result.scenario_summary[7].final_lamprey` | 越接近 verifier/O奖值越好 | 2862.114 | N/A | 18.29 | 0.107757689942 | 是 |
| 98 | `experiment_result.scenario_summary[7].final_parasite` | 越接近 verifier/O奖值越好 | 0.999 | N/A | 120 | 0.0010063726863 | 是 |
| 99 | `experiment_result.scenario_summary[7].mean_biomass` | 越接近 verifier/O奖值越好 | 3910.166 | N/A | 317.79 | 0.115525997475 | 是 |
| 100 | `experiment_result.scenario_summary[7].normalized_diversity` | 越接近 verifier/O奖值越好 | 0.8019 | N/A | 0.778 | 0.801045551412 | 是 |
| 101 | `experiment_result.scenario_summary[7].resilience` | 越接近 verifier/O奖值越好 | 0.8513 | N/A | 0.1445 | 0.126281281059 | 是 |
| 102 | `experiment_result.scenario_summary[7].resistance` | 越接近 verifier/O奖值越好 | 0.8358 | N/A | 0.9971 | 0.383400357804 | 是 |
| 103 | `experiment_result.scenario_summary[7].shannon_diversity` | 越接近 verifier/O奖值越好 | 1.4369 | N/A | 0.8547 | 0.228494039447 | 是 |
| 104 | `experiment_result.scenario_summary[7].species_persistence` | 越接近 verifier/O奖值越好 | 1 | N/A | 1 | 1 | 是 |
| 105 | `experiment_result.scenario_summary[7].sustainability` | 越接近 verifier/O奖值越好 | 1 | N/A | 0.3178 | 0.149588631264 | 是 |

<a id="mcm-2024-b"></a>

## MCM 2024 B: submersible localization and search planning

- Task slug: `mcm-2024-b-submersible-search`
- 简洁任务描述: MCM 2024 B: submersible localization and search planning
- 当前 instruction 子问题数: 4
- verifier 数值指标: 13 effective / 13 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2024-b-submersible-search`; 状态: scored; job reward: 0
- v4-flash B-Eval: -0.437625067352; BO-Eval: 0; raw panel score: 0.140996182648
- v4-flash 对齐 verifier metric path 的答案覆盖: 13/13

子问题:
- Q1: 定位- 开发一个模型来预测潜水器随时间变化的位置。 o 这些预测有哪些不确定性？ o 潜水器可以定期向主船发送哪些信息来减少 事件发生前的这些不确定性？需要什么样的设备 潜水器需要这样做吗？
- Q2: 准备 - 您会向公司推荐哪些额外的搜索设备（如果有） 必要时携带主舰部署？您可以考虑不同类型的 设备，但还必须考虑与可用性、维护、 该设备的准备情况和使用情况。救援船还可以配备哪些附加设备 如有...
- Q3: 搜索 - 开发一个模型，该模型将使用您的位置模型中的信息来 建议设备的初始部署点和搜索模式，以便
- Q4: 推断 - 如何扩展您的模型以考虑其他游客 加勒比海等目的地？您的模型将如何改变以适应 多个潜水器在同一区域移动？

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.caribbean_adaptation.current_multiplier` | 越接近 verifier/O奖值越好 | 1.35 | N/A | 2 | 0.199507389163 | 是 |
| 2 | `experiment_result.caribbean_adaptation.terrain_uncertainty_multiplier` | 越接近 verifier/O奖值越好 | 1.2 | N/A | 2 | 0.152542372881 | 是 |
| 3 | `experiment_result.equipment_selection.top_score` | 越接近 verifier/O奖值越好 | 0.8357 | N/A | 7.3 | 0.0152765201877 | 是 |
| 4 | `experiment_result.location_model.final_mean_x_m` | 越接近 verifier/O奖值越好 | 7698.65 | N/A | 6467.92 | 0.428781082797 | 是 |
| 5 | `experiment_result.location_model.final_mean_y_m` | 越接近 verifier/O奖值越好 | -2324.78 | N/A | -8.09 | 0.107476793218 | 是 |
| 6 | `experiment_result.location_model.final_p95_area_km2` | 越接近 verifier/O奖值越好 | 0.9722 | N/A | 29.47 | 0.00407709891054 | 是 |
| 7 | `experiment_result.search_strategy.calibrated_detection_multiplier` | 越接近 verifier/O奖值越好 | 0.8557 | N/A | 1.3236 | 0.179962985292 | 是 |
| 8 | `experiment_result.search_strategy.find_probability_10h_start_1h` | 越接近 verifier/O奖值越好 | 0.43 | N/A | 0.6412 | 0.196347031963 | 是 |
| 9 | `experiment_result.search_strategy.find_probability_10h_start_3h` | 越接近 verifier/O奖值越好 | 0.2338 | N/A | 0.4153 | 0.133883067056 | 是 |
| 10 | `experiment_result.search_strategy.find_probability_10h_start_5h` | 越接近 verifier/O奖值越好 | 0.1158 | N/A | 0.2488 | 0.0945975383945 | 是 |
| 11 | `experiment_result.search_strategy.find_probability_18h` | 越接近 verifier/O奖值越好 | 0.4377 | N/A | 0.936 | 0.0953553222082 | 是 |
| 12 | `experiment_result.search_strategy.find_probability_6h` | 越接近 verifier/O奖值越好 | 0.4068 | N/A | 0.6 | 0.201705672352 | 是 |
| 13 | `experiment_result.search_strategy.searched_cells` | 越接近 verifier/O奖值越好 | 18 | N/A | 108 | 0.0234375 | 是 |

<a id="mcm-2024-c"></a>

## MCM 2024 C: momentum in tennis

- Task slug: `mcm-2024-c-tennis-momentum`
- 简洁任务描述: MCM 2024 C: momentum in tennis
- 当前 instruction 子问题数: 1
- verifier 数值指标: 22 effective / 22 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2024-c-tennis-momentum`; 状态: scored; job reward: 0
- v4-flash B-Eval: -0.508413940348; BO-Eval: 0; raw panel score: 0.082877459652
- v4-flash 对齐 verifier metric path 的答案覆盖: 22/22

子问题:
- Q1: Develop a model that captures the flow of play as points occur and apply it to one or more of the...

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.dual_temporal_bayes.final_match_warning_rate` | 越接近 verifier/O奖值越好 | 0.006 | N/A | 0.9632 | 0.000751628528478 | 是 |
| 2 | `experiment_result.dual_temporal_bayes.strongest_transition.probability` | 越接近 verifier/O奖值越好 | 0.6726 | N/A | 0.3947 | 0.225067761257 | 是 |
| 3 | `experiment_result.dual_temporal_bayes.swing_warning_rate` | 越接近 verifier/O奖值越好 | 0.0032 | N/A | 0.9632 | 0.000399840063974 | 是 |
| 4 | `experiment_result.momentum_model.final_momentum_range` | 越接近 verifier/O奖值越好 | 0.7895 | N/A | 0.7212 | 0.581084396467 | 是 |
| 5 | `experiment_result.randomness_tests.matches_rejecting_iid_at_5pct` | 越接近 verifier/O奖值越好 | 0 | N/A | 31 | 3.22579604582e-06 | 是 |
| 6 | `experiment_result.randomness_tests.median_ljung_box_p` | 越接近 verifier/O奖值越好 | 0.712832 | N/A | 0 | 0.107142857143 | 是 |
| 7 | `experiment_result.randomness_tests.median_runs_p` | 越接近 verifier/O奖值越好 | 0.290172 | N/A | 0 | 0.107142857143 | 是 |
| 8 | `experiment_result.top_swing_features[0].mean_otherwise` | 越接近 verifier/O奖值越好 | 0.1257 | N/A | -0.1124 | 0.0595772244692 | 是 |
| 9 | `experiment_result.top_swing_features[0].mean_when_warning` | 越接近 verifier/O奖值越好 | 0.3043 | N/A | 0.1821 | 0.230071322362 | 是 |
| 10 | `experiment_result.top_swing_features[0].warning_correlation` | 越接近 verifier/O奖值越好 | 0.0302 | N/A | 0.1074 | 0.0448381668811 | 是 |
| 11 | `experiment_result.top_swing_features[1].mean_otherwise` | 越接近 verifier/O奖值越好 | 0.1363 | N/A | -0.1208 | 0.0598121818501 | 是 |
| 12 | `experiment_result.top_swing_features[1].mean_when_warning` | 越接近 verifier/O奖值越好 | 0 | N/A | -0.0073 | 0.0135135135135 | 是 |
| 13 | `experiment_result.top_swing_features[1].warning_correlation` | 越接近 verifier/O奖值越好 | -0.0223 | N/A | 0.0809 | 0.0252748498243 | 是 |
| 14 | `experiment_result.top_swing_features[2].mean_otherwise` | 越接近 verifier/O奖值越好 | 100.773 | N/A | 0.0728 | 0.107212010395 | 是 |
| 15 | `experiment_result.top_swing_features[2].mean_when_warning` | 越接近 verifier/O奖值越好 | 110.7391 | N/A | -0.0301 | 0.107116861215 | 是 |
| 16 | `experiment_result.top_swing_features[2].warning_correlation` | 越接近 verifier/O奖值越好 | 0.0154 | N/A | 0.051 | 0.0493484298227 | 是 |
| 17 | `experiment_result.top_swing_features[3].mean_otherwise` | 越接近 verifier/O奖值越好 | 0.1719 | N/A | 1.5 | 0.0152944107337 | 是 |
| 18 | `experiment_result.top_swing_features[3].mean_when_warning` | 越接近 verifier/O奖值越好 | 0.087 | N/A | 1.546 | 0.00710474738676 | 是 |
| 19 | `experiment_result.top_swing_features[3].warning_correlation` | 越接近 verifier/O奖值越好 | -0.0126 | N/A | 0.046 | 0.0251530476444 | 是 |
| 20 | `experiment_result.top_swing_features[4].mean_otherwise` | 越接近 verifier/O奖值越好 | 0.0313 | N/A | 1.52 | 0.00251665710748 | 是 |
| 21 | `experiment_result.top_swing_features[4].mean_when_warning` | 越接近 verifier/O奖值越好 | 0 | N/A | 1.5092 | 6.62558802094e-05 | 是 |
| 22 | `experiment_result.top_swing_features[4].warning_correlation` | 越接近 verifier/O奖值越好 | -0.0101 | N/A | 0.0108 | 0.0548118668596 | 是 |

<a id="mcm-2025-a"></a>

## MCM 2025 A: stair wear and historical traffic inference

- Task slug: `mcm-2025-a-stair-wear`
- 简洁任务描述: MCM 2025 A: stair wear and historical traffic inference
- 当前 instruction 子问题数: 8
- verifier 数值指标: 5 effective / 21 total
- 评分版本: `tb-mathmodeling-v4-endpoint-target-minmax`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2025-a-stair-wear`; 状态: scored; job reward: 0
- v4-flash B-Eval: 0; BO-Eval: 0; raw panel score: 0
- v4-flash 对齐 verifier metric path 的答案覆盖: 21/21

子问题:
- Q1: 使用楼梯的频率如何？
- Q2: 使用楼梯的人是否喜欢某个特定的行进方向？
- Q3: 有多少人同时使用楼梯？ （例如，成对的人是否 并排爬楼梯还是单列行进？）
- Q4: 磨损情况与现有信息一致吗？
- Q5: 楼梯间的年龄是多少？估计的可靠性如何？
- Q6: 进行了哪些维修或翻新？
- Q7: 能否确定材料的来源？例如，如果使用石头，则 磨损与考古学家认为是原始采石场的材料一致 来源或是否使用木材，其磨损是否与树木的年龄和类型一致 假设被使用？
- Q8: 可以确定哪些关于使用该设备的人数的信息 典型的一天中是否有大量的人使用楼梯 是短时间还是少数人较长时间？

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `daily_use_pattern.peak_period_share_of_daily_use` | 精确值；不计分 | 0.376 | 0.376 | 0.4 | 0 | 否 |
| 2 | `daily_use_pattern.peak_period_users` | 越高越好 | 27.6 | 27.3 | 23.6 | 0 | 是 |
| 3 | `daily_use_pattern.regular_hour_users_if_spread_over_10_hours` | 越高越好 | 4.6 | 4.5 | 7.1 | 0 | 是 |
| 4 | `experiment_result.age_interval_years[0]` | 精确值；不计分 | 283.6 | 283.6 | 274 | 0 | 否 |
| 5 | `experiment_result.age_interval_years[1]` | 精确值；不计分 | 397 | 397 | 510 | 0 | 否 |
| 6 | `experiment_result.estimated_age_years` | 精确值；不计分 | 340.3 | 340.3 | 393 | 0 | 否 |
| 7 | `experiment_result.estimated_daily_users` | 越高越好 | 73.52 | 72.67 | 117.9 | 0 | 是 |
| 8 | `experiment_result.estimated_passages_per_tread` | 越高越好 | 9666667 | 9555556 | 21508000 | 0 | 是 |
| 9 | `experiment_result.lateral_centroid` | 缺 baseline；不计分 | -0.0261 | N/A | 4.63 | 0 | 否 |
| 10 | `experiment_result.median_center_wear_depth_mm` | 越高越好 | 4.35 | 4.3 | 10.754 | 0 | 是 |
| 11 | `material_consistency.worked_example_material_proxy.material_density_proxy_g_cm3` | 精确值；不计分 | 2.35 | 2.35 | 2.5 | 0 | 否 |
| 12 | `material_consistency.worked_example_material_proxy.surface_hardness_proxy` | 精确值；不计分 | 4 | 4 | 20 | 0 | 否 |
| 13 | `renovation_detection.repair_candidates[0].candidate_score` | 精确值；不计分 | 5.35 | 5.35 | 0 | 0 | 否 |
| 14 | `renovation_detection.repair_candidates[0].patch_boundary_score` | 精确值；不计分 | 5 | 5 | 0 | 0 | 否 |
| 15 | `renovation_detection.repair_candidates[0].wear_jump_mm` | 精确值；不计分 | -2.4 | -2.4 | 1.051 | 0 | 否 |
| 16 | `renovation_detection.repair_candidates[1].candidate_score` | 精确值；不计分 | 3 | 3 | 0 | 0 | 否 |
| 17 | `renovation_detection.repair_candidates[1].patch_boundary_score` | 精确值；不计分 | 2 | 2 | 0 | 0 | 否 |
| 18 | `renovation_detection.repair_candidates[1].wear_jump_mm` | 精确值；不计分 | 1.4 | 1.4 | 0.799 | 0 | 否 |
| 19 | `wdm.front_to_back_rounding_ratio` | 精确值；不计分 | 1.497 | 1.497 | 1.67 | 0 | 否 |
| 20 | `wdm.side_to_center_wear_ratio` | 精确值；不计分 | 0.526 | 0.526 | 42.64 | 0 | 否 |
| 21 | `wdm.simultaneous_use_index_0_1` | 精确值；不计分 | 0.391 | 0.391 | 0.3 | 0 | 否 |

<a id="mcm-2025-b"></a>

## MCM 2025 B: sustainable tourism management in Juneau

- Task slug: `mcm-2025-b-juneau-tourism`
- 简洁任务描述: MCM 2025 B: sustainable tourism management in Juneau
- 当前 instruction 子问题数: 3
- verifier 数值指标: 19 effective / 27 total
- 评分版本: `tb-mathmodeling-v4-endpoint-target-minmax`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2025-b-juneau-tourism`; 状态: scored; job reward: 0.0805071737516
- v4-flash B-Eval: 0.0805071737516; BO-Eval: 0.0805071737516; raw panel score: 0.0805071737516
- v4-flash 对齐 verifier metric path 的答案覆盖: 27/27

子问题:
- Q1: 在阿拉斯加朱诺建立可持续旅游业模型。你可能想要 考虑游客数量、总收入以及采取的措施等因素 稳定旅游业。清楚地说明您正在优化哪些因素以及哪些因素起作用 作为约束。包括任何额外收入的支出计划并说明如...
- Q2: 展示您的模型如何适应受以下因素影响的另一个旅游目的地： 过度旅游。位置的选择如何影响最有效的措施 重要吗？您如何使用您的模型来宣传以下景点和/或地点： 有更少的游客来发展更好的平衡吗？
- Q3: 向朱诺旅游委员会写一份一页备忘录，概述您的预测、 各种措施的效果，以及您对如何优化结果的建议。

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `destination_adaptation.district_population_reference` | 精确值；不计分 | 180000 | 180000 | 15500 | 0 | 否 |
| 2 | `destination_adaptation.scaled_annual_visitor_target` | 越高越好 | 8949156 | 8448000 | 2380000 | 0 | 是 |
| 3 | `dynamic_programming.best_cumulative_score` | 缺 baseline；不计分 | 4.793367 | N/A | 0.5797 | 0 | 否 |
| 4 | `dynamic_programming.horizon_years[0]` | 缺 baseline；不计分 | 2024 | N/A | 2025 | 0 | 否 |
| 5 | `dynamic_programming.horizon_years[1]` | 缺 baseline；不计分 | 2028 | N/A | 2026 | 0 | 否 |
| 6 | `dynamic_programming.optimal_terminal_policy.annual_visitors` | 越高越好 | 1491526 | 1408000 | 1111429 | 0 | 是 |
| 7 | `dynamic_programming.optimal_terminal_policy.conservation_share` | 精确值；不计分 | 0.35 | 0.35 | 0.6 | 0 | 否 |
| 8 | `dynamic_programming.optimal_terminal_policy.daily_cap` | 越高越好 | 11000 | 10000 | 4000 | 0 | 是 |
| 9 | `dynamic_programming.optimal_terminal_policy.glacier_pressure_fields_per_year` | 越低越好 | 0.3319 | 0.3353 | 6.95 | 0 | 是 |
| 10 | `dynamic_programming.optimal_terminal_policy.net_benefit_usd` | 越高越好 | 341049399.55 | 313532032 | 263158600 | 0 | 是 |
| 11 | `dynamic_programming.optimal_terminal_policy.resident_acceptance_index` | 越高越好 | 1 | 0.78 | 0.764 | 0 | 是 |
| 12 | `dynamic_programming.optimal_terminal_policy.sustainability_score` | 越高越好 | 1.007 | 0.908447 | 0.5827 | 0 | 是 |
| 13 | `dynamic_programming.optimal_terminal_policy.total_revenue_usd` | 越高越好 | 431610327.83 | 400400000 | 277162606 | 0 | 是 |
| 14 | `dynamic_programming.optimal_terminal_policy.visitor_fee_usd` | 越高越好 | 55 | 50 | 15 | 0 | 是 |
| 15 | `dynamic_programming.optimal_terminal_policy.year` | 缺 baseline；不计分 | 2028 | N/A | 2034 | 0 | 否 |
| 16 | `experiment_result.annual_visitors` | 越高越好 | 1491526 | 1408000 | 1111429 | 0 | 是 |
| 17 | `experiment_result.optimal_conservation_share` | 精确值；不计分 | 0.35 | 0.35 | 0.6 | 0 | 否 |
| 18 | `experiment_result.optimal_daily_cap` | 越高越好 | 11000 | 10000 | 4000 | 0 | 是 |
| 19 | `experiment_result.optimal_visitor_fee_usd` | 越高越好 | 55 | 50 | 15 | 0 | 是 |
| 20 | `experiment_result.resident_acceptance_index` | 越高越好 | 1 | 0.78 | 0.764 | 0 | 是 |
| 21 | `experiment_result.sustainability_score` | 越高越好 | 1.007 | 0.908447 | 0.5827 | 0 | 是 |
| 22 | `experiment_result.terminal_year` | 缺 baseline；不计分 | 2028 | N/A | 2034 | 0 | 否 |
| 23 | `experiment_result.total_revenue_usd` | 越高越好 | 431610327.83 | 400400000 | 277162606 | 0 | 是 |
| 24 | `sensitivity_analysis[0].correlation_with_score` | 越低越好 | 0.59522 | 0.909965 | -0.02 | 0 | 是 |
| 25 | `sensitivity_analysis[2].correlation_with_score` | 越高越好 | -0.19619 | -0.868509 | 0.0047 | 0.701198389455 | 是 |
| 26 | `sensitivity_analysis[3].correlation_with_score` | 越低越好 | 0.11805 | 0.227667 | -0.1087 | 0 | 是 |
| 27 | `sensitivity_analysis[4].correlation_with_score` | 越高越好 | 0.00598 | -0.117707 | 0.0272 | 0.828437911826 | 是 |

<a id="mcm-2025-c"></a>

## MCM 2025 C: Olympic medal prediction

- Task slug: `mcm-2025-c-olympic-medals`
- 简洁任务描述: MCM 2025 C: Olympic medal prediction
- 当前 instruction 子问题数: 1
- verifier 数值指标: 96 effective / 96 total
- 评分版本: `tb-mathmodeling-v2-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2025-c-olympic-medals`; 状态: error: AgentTimeoutError(1); job reward: 0
- v4-flash B-Eval: -0.293385079963; BO-Eval: 0; raw panel score: 0.290629086704
- v4-flash 对齐 verifier metric path 的答案覆盖: 83/96

子问题:
- Q1: What other original insight(s) about Olympic medal counts does your model reveal? Explain how the...

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `great_coach_model.global_top_jump_75pct` | 越接近 verifier/O奖值越好 | 6 | N/A | 17.7 | 0.0579710144928 | 是 |
| 2 | `great_coach_model.lang_ping_validation[0].Year` | 越接近 verifier/O奖值越好 | 2008 | N/A | 1984 | 0.909420289855 | 是 |
| 3 | `great_coach_model.lang_ping_validation[0].estimated_jump_score` | 越接近 verifier/O奖值越好 | 5 | N/A | 30 | 0.0234375 | 是 |
| 4 | `great_coach_model.lang_ping_validation[0].medal_score` | 越接近 verifier/O奖值越好 | 5 | N/A | 30 | 0.0234375 | 是 |
| 5 | `great_coach_model.lang_ping_validation[0].prev3_score` | 越接近 verifier/O奖值越好 | 0 | N/A | 0 | 1 | 是 |
| 6 | `great_coach_model.lang_ping_validation[1].Year` | 越接近 verifier/O奖值越好 | 2016 | N/A | 1988 | 0.896265560166 | 是 |
| 7 | `great_coach_model.lang_ping_validation[1].estimated_jump_score` | 越接近 verifier/O奖值越好 | 1.666667 | N/A | -19 | 0.00958466628219 | 是 |
| 8 | `great_coach_model.lang_ping_validation[1].medal_score` | 越接近 verifier/O奖值越好 | 3 | N/A | 11 | 0.0430622009569 | 是 |
| 9 | `great_coach_model.lang_ping_validation[1].prev3_score` | 越接近 verifier/O奖值越好 | 1.333333 | N/A | 30 | 0.00555041483714 | 是 |
| 10 | `great_coach_model.recommendations[0].benchmark_jump_score` | 越接近 verifier/O奖值越好 | 5 | N/A | 0.7 | 0.122448979592 | 是 |
| 11 | `great_coach_model.recommendations[0].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 1.666667 | N/A | 0.4 | 0.136363628926 | 是 |
| 12 | `great_coach_model.recommendations[0].latest_medal_score` | 越接近 verifier/O奖值越好 | 0 | N/A | 4 | 2.49993750156e-05 | 是 |
| 13 | `great_coach_model.recommendations[0].latest_year` | 越接近 verifier/O奖值越好 | 2024 | N/A | 2024 | 1 | 是 |
| 14 | `great_coach_model.recommendations[0].recent_baseline_score` | 越接近 verifier/O奖值越好 | 1.333333 | N/A | 2.7 | 0.104803447112 | 是 |
| 15 | `great_coach_model.recommendations[1].benchmark_jump_score` | 越接近 verifier/O奖值越好 | 6 | N/A | 5.8 | 0.782608695652 | 是 |
| 16 | `great_coach_model.recommendations[1].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 2 | N/A | 3.5 | 0.137931034483 | 是 |
| 17 | `great_coach_model.recommendations[1].latest_medal_score` | 越接近 verifier/O奖值越好 | 1 | N/A | 16 | 0.00793650793651 | 是 |
| 18 | `great_coach_model.recommendations[1].latest_year` | 越接近 verifier/O奖值越好 | 2024 | N/A | 2024 | 1 | 是 |
| 19 | `great_coach_model.recommendations[1].recent_baseline_score` | 越接近 verifier/O奖值越好 | 0.333333 | N/A | 4.3 | 0.00998335035064 | 是 |
| 20 | `great_coach_model.recommendations[2].benchmark_jump_score` | 越接近 verifier/O奖值越好 | 9.416667 | N/A | 1 | 0.118365921349 | 是 |
| 21 | `great_coach_model.recommendations[2].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 3 | N/A | 0.6 | 0.130434782609 | 是 |
| 22 | `great_coach_model.recommendations[2].latest_medal_score` | 越接近 verifier/O奖值越好 | 6 | N/A | 2 | 0.152542372881 | 是 |
| 23 | `great_coach_model.recommendations[2].latest_year` | 越接近 verifier/O奖值越好 | 2024 | N/A | 2000 | 0.910071942446 | 是 |
| 24 | `great_coach_model.recommendations[2].recent_baseline_score` | 越接近 verifier/O奖值越好 | 2.666667 | N/A | 0 | 0.107142857143 | 是 |
| 25 | `great_coach_model.recommendations[3].benchmark_jump_score` | 越接近 verifier/O奖值越好 | 5.333333 | N/A | N/A | 0 | 是 |
| 26 | `great_coach_model.recommendations[3].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 1.777778 | N/A | N/A | 0 | 是 |
| 27 | `great_coach_model.recommendations[3].latest_medal_score` | 越接近 verifier/O奖值越好 | 12 | N/A | N/A | 0 | 是 |
| 28 | `great_coach_model.recommendations[3].latest_year` | 越接近 verifier/O奖值越好 | 2024 | N/A | N/A | 0 | 是 |
| 29 | `great_coach_model.recommendations[3].recent_baseline_score` | 越接近 verifier/O奖值越好 | 2.666667 | N/A | N/A | 0 | 是 |
| 30 | `great_coach_model.top_historical_jump_candidates[0].Year` | 越接近 verifier/O奖值越好 | 2008 | N/A | 1920 | 0.732490272374 | 是 |
| 31 | `great_coach_model.top_historical_jump_candidates[0].coach_like_jump` | 越接近 verifier/O奖值越好 | 28 | N/A | 121 | 0.0348692403487 | 是 |
| 32 | `great_coach_model.top_historical_jump_candidates[0].medal_score` | 越接近 verifier/O奖值越好 | 34 | N/A | 164 | 0.0304295942721 | 是 |
| 33 | `great_coach_model.top_historical_jump_candidates[0].prev3_score` | 越接近 verifier/O奖值越好 | 6 | N/A | 43 | 0.0190880169671 | 是 |
| 34 | `great_coach_model.top_historical_jump_candidates[10].Year` | 越接近 verifier/O奖值越好 | 2008 | N/A | N/A | 0 | 是 |
| 35 | `great_coach_model.top_historical_jump_candidates[10].coach_like_jump` | 越接近 verifier/O奖值越好 | 17.333333 | N/A | N/A | 0 | 是 |
| 36 | `great_coach_model.top_historical_jump_candidates[10].medal_score` | 越接近 verifier/O奖值越好 | 31 | N/A | N/A | 0 | 是 |
| 37 | `great_coach_model.top_historical_jump_candidates[10].prev3_score` | 越接近 verifier/O奖值越好 | 13.666667 | N/A | N/A | 0 | 是 |
| 38 | `great_coach_model.top_historical_jump_candidates[11].Year` | 越接近 verifier/O奖值越好 | 2020 | N/A | N/A | 0 | 是 |
| 39 | `great_coach_model.top_historical_jump_candidates[11].coach_like_jump` | 越接近 verifier/O奖值越好 | 17 | N/A | N/A | 0 | 是 |
| 40 | `great_coach_model.top_historical_jump_candidates[11].medal_score` | 越接近 verifier/O奖值越好 | 17 | N/A | N/A | 0 | 是 |
| 41 | `great_coach_model.top_historical_jump_candidates[11].prev3_score` | 越接近 verifier/O奖值越好 | 0 | N/A | N/A | 0 | 是 |
| 42 | `great_coach_model.top_historical_jump_candidates[1].Year` | 越接近 verifier/O奖值越好 | 2000 | N/A | 1964 | 0.869565217391 | 是 |
| 43 | `great_coach_model.top_historical_jump_candidates[1].coach_like_jump` | 越接近 verifier/O奖值越好 | 23.666667 | N/A | 94 | 0.038811954055 | 是 |
| 44 | `great_coach_model.top_historical_jump_candidates[1].medal_score` | 越接近 verifier/O奖值越好 | 37 | N/A | 159 | 0.035115469788 | 是 |
| 45 | `great_coach_model.top_historical_jump_candidates[1].prev3_score` | 越接近 verifier/O奖值越好 | 13.333333 | N/A | 65 | 0.0300375460173 | 是 |
| 46 | `great_coach_model.top_historical_jump_candidates[2].Year` | 越接近 verifier/O奖值越好 | 2004 | N/A | 1980 | 0.909255898367 | 是 |
| 47 | `great_coach_model.top_historical_jump_candidates[2].coach_like_jump` | 越接近 verifier/O奖值越好 | 23 | N/A | 90 | 0.0395642201835 | 是 |
| 48 | `great_coach_model.top_historical_jump_candidates[2].medal_score` | 越接近 verifier/O奖值越好 | 38 | N/A | 127 | 0.0487387772552 | 是 |
| 49 | `great_coach_model.top_historical_jump_candidates[2].prev3_score` | 越接近 verifier/O奖值越好 | 15 | N/A | 37 | 0.0756302521008 | 是 |
| 50 | `great_coach_model.top_historical_jump_candidates[3].Year` | 越接近 verifier/O奖值越好 | 2008 | N/A | 1980 | 0.895895300416 | 是 |
| 51 | `great_coach_model.top_historical_jump_candidates[3].coach_like_jump` | 越接近 verifier/O奖值越好 | 22.333333 | N/A | 84.3 | 0.0414561196428 | 是 |
| 52 | `great_coach_model.top_historical_jump_candidates[3].medal_score` | 越接近 verifier/O奖值越好 | 33 | N/A | 159 | 0.0304709141274 | 是 |
| 53 | `great_coach_model.top_historical_jump_candidates[3].prev3_score` | 越接近 verifier/O奖值越好 | 10.666667 | N/A | 74.7 | 0.0195978367727 | 是 |
| 54 | `great_coach_model.top_historical_jump_candidates[4].Year` | 越接近 verifier/O奖值越好 | 2000 | N/A | 2000 | 1 | 是 |
| 55 | `great_coach_model.top_historical_jump_candidates[4].coach_like_jump` | 越接近 verifier/O奖值越好 | 22 | N/A | 83.7 | 0.0410320174075 | 是 |
| 56 | `great_coach_model.top_historical_jump_candidates[4].medal_score` | 越接近 verifier/O奖值越好 | 30 | N/A | 103 | 0.0469973890339 | 是 |
| 57 | `great_coach_model.top_historical_jump_candidates[4].prev3_score` | 越接近 verifier/O奖值越好 | 8 | N/A | 19.3 | 0.0783034257749 | 是 |
| 58 | `great_coach_model.top_historical_jump_candidates[5].Year` | 越接近 verifier/O奖值越好 | 1996 | N/A | 1920 | 0.759127789047 | 是 |
| 59 | `great_coach_model.top_historical_jump_candidates[5].coach_like_jump` | 越接近 verifier/O奖值越好 | 22 | N/A | 77 | 0.0458015267176 | 是 |
| 60 | `great_coach_model.top_historical_jump_candidates[5].medal_score` | 越接近 verifier/O奖值越好 | 22 | N/A | 83 | 0.0414833438089 | 是 |
| 61 | `great_coach_model.top_historical_jump_candidates[5].prev3_score` | 越接近 verifier/O奖值越好 | 0 | N/A | 6 | 1.66663888935e-05 | 是 |
| 62 | `great_coach_model.top_historical_jump_candidates[6].Year` | 越接近 verifier/O奖值越好 | 1996 | N/A | 2016 | 0.922934648582 | 是 |
| 63 | `great_coach_model.top_historical_jump_candidates[6].coach_like_jump` | 越接近 verifier/O奖值越好 | 20.666667 | N/A | 71.3 | 0.0466926080149 | 是 |
| 64 | `great_coach_model.top_historical_jump_candidates[6].medal_score` | 越接近 verifier/O奖值越好 | 22 | N/A | 88 | 0.0384615384615 | 是 |
| 65 | `great_coach_model.top_historical_jump_candidates[6].prev3_score` | 越接近 verifier/O奖值越好 | 1.333333 | N/A | 16.7 | 0.0103048490969 | 是 |
| 66 | `great_coach_model.top_historical_jump_candidates[7].Year` | 越接近 verifier/O奖值越好 | 1996 | N/A | 1984 | 0.952290076336 | 是 |
| 67 | `great_coach_model.top_historical_jump_candidates[7].coach_like_jump` | 越接近 verifier/O奖值越好 | 18 | N/A | 71 | 0.0391588107324 | 是 |
| 68 | `great_coach_model.top_historical_jump_candidates[7].medal_score` | 越接近 verifier/O奖值越好 | 18 | N/A | 84 | 0.0316901408451 | 是 |
| 69 | `great_coach_model.top_historical_jump_candidates[7].prev3_score` | 越接近 verifier/O奖值越好 | 0 | N/A | 13 | 7.69224852117e-06 | 是 |
| 70 | `great_coach_model.top_historical_jump_candidates[8].Year` | 越接近 verifier/O奖值越好 | 2020 | N/A | 1984 | 0.870689655172 | 是 |
| 71 | `great_coach_model.top_historical_jump_candidates[8].coach_like_jump` | 越接近 verifier/O奖值越好 | 18 | N/A | 67.7 | 0.0416505977632 | 是 |
| 72 | `great_coach_model.top_historical_jump_candidates[8].medal_score` | 越接近 verifier/O奖值越好 | 18 | N/A | 75 | 0.0365111561866 | 是 |
| 73 | `great_coach_model.top_historical_jump_candidates[8].prev3_score` | 越接近 verifier/O奖值越好 | 0 | N/A | 7.3 | 1.36984424871e-05 | 是 |
| 74 | `great_coach_model.top_historical_jump_candidates[9].Year` | 越接近 verifier/O奖值越好 | 2000 | N/A | 1912 | 0.731707317073 | 是 |
| 75 | `great_coach_model.top_historical_jump_candidates[9].coach_like_jump` | 越接近 verifier/O奖值越好 | 17.666667 | N/A | 65.3 | 0.0426102114263 | 是 |
| 76 | `great_coach_model.top_historical_jump_candidates[9].medal_score` | 越接近 verifier/O奖值越好 | 19 | N/A | 75 | 0.0391214824983 | 是 |
| 77 | `great_coach_model.top_historical_jump_candidates[9].prev3_score` | 越接近 verifier/O奖值越好 | 1.333333 | N/A | 9.7 | 0.0187646545538 | 是 |
| 78 | `host_effect_model.Gold.event_count_coefficient` | 越接近 verifier/O奖值越好 | 0.000147 | N/A | 0.00022 | 0.578034682081 | 是 |
| 79 | `host_effect_model.Gold.host_bonus_coefficient` | 越接近 verifier/O奖值越好 | 14.341156 | N/A | 14.121 | 0.886581526532 | 是 |
| 80 | `host_effect_model.Gold.prev3_coefficient` | 越接近 verifier/O奖值越好 | 0.950866 | N/A | 0.909 | 0.731576447561 | 是 |
| 81 | `host_effect_model.Gold.r2` | 越接近 verifier/O奖值越好 | 0.752918 | N/A | 0.722 | 0.745044371086 | 是 |
| 82 | `host_effect_model.Total.event_count_coefficient` | 越接近 verifier/O奖值越好 | -0.000215 | N/A | 1e-05 | 0.307692307692 | 是 |
| 83 | `host_effect_model.Total.host_bonus_coefficient` | 越接近 verifier/O奖值越好 | 36.422317 | N/A | 35.277 | 0.792364389073 | 是 |
| 84 | `host_effect_model.Total.prev3_coefficient` | 越接近 verifier/O奖值越好 | 0.952921 | N/A | 0.915 | 0.750964592722 | 是 |
| 85 | `host_effect_model.Total.r2` | 越接近 verifier/O奖值越好 | 0.765819 | N/A | 0.721 | 0.672177503824 | 是 |
| 86 | `model_evaluation.holdout_year` | 越接近 verifier/O奖值越好 | 2024 | N/A | 2024 | 1 | 是 |
| 87 | `model_evaluation.mean_accuracy_2024` | 越接近 verifier/O奖值越好 | 0.850591 | N/A | 0.661 | 0.3499631354 | 是 |
| 88 | `model_evaluation.mean_brier_2024` | 越接近 verifier/O奖值越好 | 0.142806 | N/A | 0.315 | 0.0905120943923 | 是 |
| 89 | `model_evaluation.mean_f1_2024` | 越接近 verifier/O奖值越好 | 0.287348 | N/A | 0.627 | 0.0921642569759 | 是 |
| 90 | `model_evaluation.sport_models` | 越接近 verifier/O奖值越好 | 50 | N/A | 44 | 0.5 | 是 |
| 91 | `model_evaluation.status_counts.GoldBinary:fallback_mean` | 越接近 verifier/O奖值越好 | 7 | N/A | 0 | 0.107142857143 | 是 |
| 92 | `model_evaluation.status_counts.GoldBinary:random_forest` | 越接近 verifier/O奖值越好 | 43 | N/A | 44 | 0.837662337662 | 是 |
| 93 | `model_evaluation.status_counts.MedalBinary:fallback_mean` | 越接近 verifier/O奖值越好 | 7 | N/A | 0 | 0.107142857143 | 是 |
| 94 | `model_evaluation.status_counts.MedalBinary:random_forest` | 越接近 verifier/O奖值越好 | 43 | N/A | 44 | 0.837662337662 | 是 |
| 95 | `monte_carlo.simulations` | 越接近 verifier/O奖值越好 | 500 | N/A | 500 | 1 | 是 |
| 96 | `monte_carlo.weight_power` | 越接近 verifier/O奖值越好 | 4 | N/A | 1 | 0.137931034483 | 是 |
