# TB-MathModeling 任务与答案汇总

本文档汇总当前 18 道题：3 年 x 2 个竞赛 x A/B/C 三题。

口径说明:
- 当前 verifier 只看最后一问的数值核心；如果最后一问本身是备忘录或文字建议，就使用支撑该建议的最后可量化答案。
- `最后答案数值项` 不是全题所有数字，而是表达 final answer 所需的少量核心数字；有些最终答案天然是一个向量或几种情景结果，所以会有 2-6 个数值项。
- `Verifier/O answer` 是 verifier 使用的数值答案，来自 O 奖论文复现结果；它不是数学建模问题唯一可能的正确答案。
- `Baseline answer = N/A` 不表示没有 baseline；它表示当前 baseline 结果没有和该 final answer 同语义的逐项字段，评分仍会用该题的 baseline panel score，不强行把无关数字凑成端点。
- 方向标签来自 `score_config.json`：有真实 baseline-to-outstanding 端点时标为 `越高越好` / `越低越好`；legacy fallback 指标没有逐指标 baseline 方向，因此标为 `越接近 verifier/O奖值越好`。
- `v4-flash answer` 来自当前 `terminus2-deepseek-v4-flash-current-*` jobs，并用当前 `score_config.json` 对保存下来的 artifact 重新计分；`N/A` 表示没有找到该路径下的答案。
- 当前默认 benchmark reward 是 `B-Eval`；本文档会用当前 `score_config.json` 对已有 artifact 重新计分，并同时列出 `BO-Eval`。

## 总览

| 竞赛 | 年份 | 题号 | Task | 简洁描述 | 最后评测问题 | 子问题数 | 最后答案数值项 | v4-flash 状态 | v4 B-Eval | v4 BO-Eval |
|---|---:|---|---|---|---|---:|---:|---|---:|---:|
| CUMCM | 2023 | A | [`cumcm-2023-a-heliostat-field`](#cumcm-2023-a) | CUMCM 2023 A: heliostat field design | 在定日镜尺寸和安装高度都可以变化时，重新设计镜场，在满足约 60 MW 年平均输出功率的同时，让单位镜面面积输出尽量大。 | 3 | 5 | error: AgentTimeoutError(1) | 0 | 0 |
| CUMCM | 2023 | B | [`cumcm-2023-b-multibeam-lines`](#cumcm-2023-b) | CUMCM 2023 B: multibeam survey-line layout | 给定真实海深数据，设计测线方案，尽量减少测线总长度，同时控制漏测面积和重叠过大的测线长度。 | 4 | 4 | error: CancelledError(1) | N/A | N/A |
| CUMCM | 2023 | C | [`cumcm-2023-c-vegetable-pricing`](#cumcm-2023-c) | CUMCM 2023 C: vegetable pricing and replenishment | 最后一问本身是让商超说明还应采集哪些数据、这些数据怎样帮助补货和定价；它主要是文字建议。 | 4 | 2 | error: AgentTimeoutError(1) | 0.262879428093 | 0.262879428093 |
| CUMCM | 2024 | A | [`cumcm-2024-a-dragon-dance`](#cumcm-2024-a) | CUMCM 2024 A: dragon-dance bench kinematics | 沿着前面求出的调头路径行进时，求龙头最大能跑多快，才能保证所有把手速度都不超过 2 m/s。 | 5 | 2 | error: AgentTimeoutError(1) | 0.107142857143 | 0.107142857143 |
| CUMCM | 2024 | B | [`cumcm-2024-b-production-decision`](#cumcm-2024-b) | CUMCM 2024 B: production-process decision optimization | 把零配件和成品次品率看成抽样估出来的不确定量，然后重新求问题 2 和问题 3 的最优检测、装配、拆解决策。 | 4 | 6 | error: AgentTimeoutError(1) | 0.691799203783 | 0.691799203783 |
| CUMCM | 2024 | C | [`cumcm-2024-c-crop-planting`](#cumcm-2024-c) | CUMCM 2024 C: crop-planting strategy optimization | 在问题 2 的基础上加入作物之间的替代、互补和价格/成本/销量相关性，求 2024-2030 年的稳健种植策略。 | 3 | 2 | error: AgentTimeoutError(1) | 0.31433102394 | 0.31433102394 |
| CUMCM | 2025 | A | [`cumcm-2025-a-smoke-screen`](#cumcm-2025-a) | CUMCM 2025 A: UAV smoke-screen strategy | 5 架无人机、每架最多 3 枚烟幕弹，同时对 3 枚导弹实施遮蔽，求总体遮蔽时间尽量长的投放方案。 | 5 | 4 | error: AgentTimeoutError(1) | N/A | N/A |
| CUMCM | 2025 | B | [`cumcm-2025-b-sic-thickness`](#cumcm-2025-b) | CUMCM 2025 B: SiC epitaxial-layer thickness inversion | 把多光束反射/透射造成的干涉也考虑进去，重新确定碳化硅外延层厚度，并分析结果可靠性。 | 3 | 2 | error: AgentTimeoutError(1) | 0.143178654302 | 0.143178654302 |
| CUMCM | 2025 | C | [`cumcm-2025-c-nipt`](#cumcm-2025-c) | CUMCM 2025 C: NIPT timing and fetal abnormality modeling | 对女胎样本，用染色体 Z 值、GC 含量、读段数、BMI 等指标判断胎儿是否异常。 | 4 | 2 | scored | 0.471826516941 | 0.471826516941 |
| MCM | 2023 | A | [`mcm-2023-a-plant-community`](#mcm-2023-a) | MCM 2023 A: drought-stricken plant communities | 综合物种数、干旱、污染和栖息地压力，说明怎样保证植物群落长期可生存。 | 9 | 3 | error: AgentTimeoutError(1) | -0.248454921739 | 0 |
| MCM | 2023 | B | [`mcm-2023-b-maasai-mara`](#mcm-2023-b) | MCM 2023 B: reimagining Maasai Mara | 把土地分区和政策方案整理成给当地管理者的非技术报告，说明推荐方案的收益和用地分配。 | 3 | 5 | scored | -0.572294585853 | 0 |
| MCM | 2023 | C | [`mcm-2023-c-wordle`](#mcm-2023-c) | MCM 2023 C: predicting Wordle results | 在给纽约时报编辑的总结信之前，最后一个可量化核心是判断 EERIE 的难度，并给出难度分类模型准确率。 | 4 | 1 | scored | 0 | 0 |
| MCM | 2024 | A | [`mcm-2024-a-lamprey`](#mcm-2024-a) | MCM 2024 A: lamprey sex-ratio ecology | 判断七鳃鳗可变性别比例是否也会让生态系统中的其他生物受益，尤其是寄生者/宿主相关指标。 | 4 | 3 | scored | -0.194531681993 | 0 |
| MCM | 2024 | B | [`mcm-2024-b-submersible-search`](#mcm-2024-b) | MCM 2024 B: submersible localization and search planning | 把潜水器搜索模型迁移到加勒比海场景，并说明洋流、海底地形和多潜水器协同时需要怎样调整。 | 4 | 2 | scored | -0.402596368978 | 0 |
| MCM | 2024 | C | [`mcm-2024-c-tennis-momentum`](#mcm-2024-c) | MCM 2024 C: momentum in tennis | 把势头模型转成教练能用的赛中提示：什么时候可能发生势头转换，应重点监控哪些指标。 | 1 | 4 | scored | -0.561238131236 | 0 |
| MCM | 2025 | A | [`mcm-2025-a-stair-wear`](#mcm-2025-a) | MCM 2025 A: stair wear and historical traffic inference | 根据楼梯磨损反推典型一天大约多少人使用，以及这些人是短时间集中经过还是长时间稀疏经过。 | 8 | 3 | scored | 0 | 0 |
| MCM | 2025 | B | [`mcm-2025-b-juneau-tourism`](#mcm-2025-b) | MCM 2025 B: sustainable tourism management in Juneau | 给朱诺旅游委员会写一页备忘录，概括预测、各种限制/收费措施的效果，并推荐最优可持续旅游政策。 | 3 | 6 | scored | 0 | 0 |
| MCM | 2025 | C | [`mcm-2025-c-olympic-medals`](#mcm-2025-c) | MCM 2025 C: Olympic medal prediction | 说明模型还能发现哪些原创奖牌规律，以及这些规律怎样指导国家奥委会分配项目和教练资源。 | 1 | 5 | error: AgentTimeoutError(1) | -0.491474074565 | 0 |

# 分题表格

<a id="cumcm-2023-a"></a>

## CUMCM 2023 A: heliostat field design

- Task slug: `cumcm-2023-a-heliostat-field`
- 简洁任务描述: CUMCM 2023 A: heliostat field design
- 最后评测问题: 在定日镜尺寸和安装高度都可以变化时，重新设计镜场，在满足约 60 MW 年平均输出功率的同时，让单位镜面面积输出尽量大。
- final answer: O 奖复现给出的核心设计是年平均热功率 60.336111 MW，单位面积功率 0.506192417 kW/m2，年平均光学效率 0.496428083，镜面总面积 119196 m2，定日镜 3311 面。
- baseline模型: baseline 用几何解析和太阳运动参数方程做一个简化镜场拟合，再从几何约束中估计设计参数。
- 当前 instruction 子问题数: 3
- 最后答案数值项: 5 个计分 / 5 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2023-a-heliostat-field`; 状态: error: AgentTimeoutError(1); 当前口径 reward: 0
- v4-flash B-Eval: 0; BO-Eval: 0; raw panel score: 0
- v4-flash 对齐 verifier metric path 的答案覆盖: 0/5

子问题:
- 问题1: 若将吸收塔建于该圆形定日镜场中心，定日镜尺寸均为 6 m×6 m，安装高度均为
- 问题2: 按设计要求，定日镜场的额定年平均输出热功率（以下简称额定功率）为60 MW。
- 问题3: 如果定日镜尺寸可以不同，安装高度也可以不同，额定功率设置同问题2，请重新

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.design_summary[2].annual_optical_efficiency` | 越接近 verifier/O奖值越好 | 0.496428083 | N/A | N/A | 0 | 是 |
| 2 | `reproduced.design_summary[2].mirror_area_m2` | 越接近 verifier/O奖值越好 | 119196 | N/A | N/A | 0 | 是 |
| 3 | `reproduced.design_summary[2].mirror_count` | 越接近 verifier/O奖值越好 | 3311 | N/A | N/A | 0 | 是 |
| 4 | `reproduced.design_summary[2].unit_area_power_kw_m2` | 越接近 verifier/O奖值越好 | 0.506192417 | N/A | N/A | 0 | 是 |
| 5 | `target_comparison.q3_annual_thermal_power_mw.actual` | 越接近 verifier/O奖值越好 | 60.336111 | N/A | N/A | 0 | 是 |

<a id="cumcm-2023-b"></a>

## CUMCM 2023 B: multibeam survey-line layout

- Task slug: `cumcm-2023-b-multibeam-lines`
- 简洁任务描述: CUMCM 2023 B: multibeam survey-line layout
- 最后评测问题: 给定真实海深数据，设计测线方案，尽量减少测线总长度，同时控制漏测面积和重叠过大的测线长度。
- final answer: O 奖复现的核心方案总测线长度 622.0 海里，漏测面积 3.48%，重叠超过 20% 的测线长度 30.0 海里，平均重叠率约 10.48%。
- baseline模型: baseline 先用数据拟合近似海底地形，再用规则化/贪心测线布置估计覆盖质量。
- 当前 instruction 子问题数: 4
- 最后答案数值项: 4 个计分 / 4 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2023-b-multibeam-lines`; 状态: error: CancelledError(1); 当前口径 reward: N/A
- v4-flash B-Eval: N/A; BO-Eval: N/A; raw panel score: N/A
- v4-flash 对齐 verifier metric path 的答案覆盖: 0/4

子问题:
- 问题1: 与测线方向垂直的平面和海底坡面的交线构成一条与水平面夹角为 𝛼 的斜线（图
- 问题2: 考虑一个矩形待测海域（图8），测线方向与海底坡面的法向在水平面上投影的夹
- 问题3: 考虑一个南北长2 海里、东西宽4 海里的矩形海域内，海域中心点处的海水深度
- 问题4: 海水深度数据（附件.xlsx）是若干年前某海域（南北长5 海里、东西宽4 海里）

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles` | 越接近 verifier/O奖值越好 | 30 | N/A | N/A | N/A | 是 |
| 2 | `reproduced.problem4_summary.sa_avg_overlap_pct` | 越接近 verifier/O奖值越好 | 10.48 | N/A | N/A | N/A | 是 |
| 3 | `target_comparison.problem4_missed_area_pct.actual` | 越接近 verifier/O奖值越好 | 3.48 | N/A | N/A | N/A | 是 |
| 4 | `target_comparison.problem4_total_length_nm.actual` | 越接近 verifier/O奖值越好 | 622 | N/A | N/A | N/A | 是 |

<a id="cumcm-2023-c"></a>

## CUMCM 2023 C: vegetable pricing and replenishment

- Task slug: `cumcm-2023-c-vegetable-pricing`
- 简洁任务描述: CUMCM 2023 C: vegetable pricing and replenishment
- 最后评测问题: 最后一问本身是让商超说明还应采集哪些数据、这些数据怎样帮助补货和定价；它主要是文字建议。
- final answer: 当前数值 verifier 只看支撑这些建议的最后可量化补货定价结果：未来一周最大利润 5105.6 元，并选择 29 个单品进入补货定价方案。
- baseline模型: baseline 用规划优化和资源配置模型，把可售空间、补货量和价格决策转成利润最大化问题。
- 备注: Q4 is qualitative, so this benchmark records the last quantifiable pricing/replenishment answer that Q4 asks to improve with more data.
- 当前 instruction 子问题数: 4
- 最后答案数值项: 2 个计分 / 2 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2023-c-vegetable-pricing`; 状态: error: AgentTimeoutError(1); 当前口径 reward: 0.262879428093
- v4-flash B-Eval: 0.262879428093; BO-Eval: 0.262879428093; raw panel score: 0.262879428093
- v4-flash 对齐 verifier metric path 的答案覆盖: 2/2

子问题:
- 问题1: 蔬菜类商品不同品类或不同单品之间可能存在一定的关联关系，请分析蔬菜各
- 问题2: 考虑商超以品类为单位做补货计划，请分析各蔬菜品类的销售总量与成本加成
- 问题3: 因蔬菜类商品的销售空间有限，商超希望进一步制定单品的补货计划，要求可
- 问题4: 为了更好地制定蔬菜商品的补货和定价决策，商超还需要采集哪些相关数据，

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `target_comparison.future_week_max_profit_yuan.actual` | 越接近 verifier/O奖值越好 | 5105.6 | N/A | 14616.69 | 0.060518214474 | 是 |
| 2 | `target_comparison.problem3_selected_item_count.actual` | 越接近 verifier/O奖值越好 | 29 | N/A | 33 | 0.465240641711 | 是 |

<a id="cumcm-2024-a"></a>

## CUMCM 2024 A: dragon-dance bench kinematics

- Task slug: `cumcm-2024-a-dragon-dance`
- 简洁任务描述: CUMCM 2024 A: dragon-dance bench kinematics
- 最后评测问题: 沿着前面求出的调头路径行进时，求龙头最大能跑多快，才能保证所有把手速度都不超过 2 m/s。
- final answer: O 奖复现给出的最大龙头速度约 2.00002 m/s；当龙头速度为 1 m/s 时，全队最大速度比例约 0.99999。
- baseline模型: baseline 用几何解析和运动学参数方程，沿路径传播各把手位置，再由速度约束反推龙头速度上限。
- 当前 instruction 子问题数: 5
- 最后答案数值项: 2 个计分 / 2 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2024-a-dragon-dance`; 状态: error: AgentTimeoutError(1); 当前口径 reward: 0.107142857143
- v4-flash B-Eval: 0.107142857143; BO-Eval: 0.107142857143; raw panel score: 0.107142857143
- v4-flash 对齐 verifier metric path 的答案覆盖: 2/2

子问题:
- 问题1: 舞龙队沿螺距为 55 cm 的等距螺线顺时针盘入，各把手中心均位于螺线上。龙
- 问题2: 舞龙队沿问题 1 设定的螺线盘入， 请确定舞龙队盘入的终止时刻， 使得板凳之
- 问题3: 从盘入到盘出， 舞龙队将由顺时针盘入调头切换为逆时针盘出，这需要一定的
- 问题4: 盘入螺线的螺距为 1.7 m，盘出螺线与盘入螺线关于螺线中心呈中心对称，舞
- 问题5: 舞龙队沿问题 4 设定的路径行进，龙头行进速度保持不变， 请确定龙头的最大

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q5.max_head_speed_mps` | 越接近 verifier/O奖值越好 | 2.00002 | N/A | 0 | 0.107142857143 | 是 |
| 2 | `experiment_result.q5.max_speed_ratio_when_head_1mps` | 越接近 verifier/O奖值越好 | 0.99999 | N/A | 0 | 0.107142857143 | 是 |

<a id="cumcm-2024-b"></a>

## CUMCM 2024 B: production-process decision optimization

- Task slug: `cumcm-2024-b-production-decision`
- 简洁任务描述: CUMCM 2024 B: production-process decision optimization
- 最后评测问题: 把零配件和成品次品率看成抽样估出来的不确定量，然后重新求问题 2 和问题 3 的最优检测、装配、拆解决策。
- final answer: O 奖复现用 3 组后验缺陷率情景重算利润：Q2 case1 利润约 25.9691、25.8694、25.7715；Q3 最优策略后验利润约 86.8529、86.5588、86.2647。
- baseline模型: baseline 用二项抽样/贝叶斯后验估计次品率，再用期望利润枚举和多阶段决策搜索求最优策略。
- 当前 instruction 子问题数: 4
- 最后答案数值项: 6 个计分 / 6 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2024-b-production-decision`; 状态: error: AgentTimeoutError(1); 当前口径 reward: 0.691799203783
- v4-flash B-Eval: 0.691799203783; BO-Eval: 0.691799203783; raw panel score: 0.691799203783
- v4-flash 对齐 verifier metric path 的答案覆盖: 6/6

子问题:
- 问题1: 供应商声称一批零配件（零配件 1 或零配件 2）的次品率不会超过某个标称值。
- 问题2: 已知两种零配件和成品次品率，请为企业生产过程的各个阶段作出决策：
- 问题3: 对 𝑚 道工序、𝑛 个零配件，已知零配件、半成品和成品的次品率，重复问题
- 问题4: 假设问题 2 和问题 3 中零配件、 半成品和成品的次品率均是通过抽样检测方法

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q4.posterior_rows[0].q2_best_profit_case1` | 越接近 verifier/O奖值越好 | 25.9691 | N/A | 27.49 | 0.672021343951 | 是 |
| 2 | `experiment_result.q4.posterior_rows[0].q3_best_policy_profit_under_posterior` | 越接近 verifier/O奖值越好 | 86.8529 | N/A | 96.721 | 0.513657855164 | 是 |
| 3 | `experiment_result.q4.posterior_rows[1].q2_best_profit_case1` | 越接近 verifier/O奖值越好 | 25.8694 | N/A | 26.9595 | 0.740107590356 | 是 |
| 4 | `experiment_result.q4.posterior_rows[1].q3_best_policy_profit_under_posterior` | 越接近 verifier/O奖值越好 | 86.5588 | N/A | 91.6033 | 0.673104902707 | 是 |
| 5 | `experiment_result.q4.posterior_rows[2].q2_best_profit_case1` | 越接近 verifier/O奖值越好 | 25.7715 | N/A | 26.4072 | 0.829492420097 | 是 |
| 6 | `experiment_result.q4.posterior_rows[2].q3_best_policy_profit_under_posterior` | 越接近 verifier/O奖值越好 | 86.2647 | N/A | 90.2424 | 0.722411110423 | 是 |

<a id="cumcm-2024-c"></a>

## CUMCM 2024 C: crop-planting strategy optimization

- Task slug: `cumcm-2024-c-crop-planting`
- 简洁任务描述: CUMCM 2024 C: crop-planting strategy optimization
- 最后评测问题: 在问题 2 的基础上加入作物之间的替代、互补和价格/成本/销量相关性，求 2024-2030 年的稳健种植策略。
- final answer: O 奖复现的相关性稳健方案给出 best correlated CVaR10 利润 118550698.19 元，价格和成本的 Spearman 相关系数约 0.2551。
- baseline模型: baseline 用规划优化和资源配置模型，在随机场景下比较候选种植方案的收益和风险。
- 当前 instruction 子问题数: 3
- 最后答案数值项: 2 个计分 / 2 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2024-c-crop-planting`; 状态: error: AgentTimeoutError(1); 当前口径 reward: 0.31433102394
- v4-flash B-Eval: 0.31433102394; BO-Eval: 0.31433102394; raw panel score: 0.31433102394
- v4-flash 对齐 verifier metric path 的答案覆盖: 2/2

子问题:
- 问题1: 假定各种农作物未来的预期销售量、种植成本、亩产量和销售价格相对于 2023 年保持
- 问题2: 根据经验，小麦和玉米未来的预期销售量有增长的趋势，平均年增长率介于5%~10%
- 问题3: 在现实生活中，各种农作物之间可能存在一定的可替代性和互补性，预期销售量与销

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q2_q3.best_correlated_cvar10_profit_yuan` | 越接近 verifier/O奖值越好 | 118550698.19 | N/A | 69059695.53 | 0.223269527485 | 是 |
| 2 | `experiment_result.q2_q3.spearman_price_cost` | 越接近 verifier/O奖值越好 | 0.2551 | N/A | 0.3 | 0.405392520394 | 是 |

<a id="cumcm-2025-a"></a>

## CUMCM 2025 A: UAV smoke-screen strategy

- Task slug: `cumcm-2025-a-smoke-screen`
- 简洁任务描述: CUMCM 2025 A: UAV smoke-screen strategy
- 最后评测问题: 5 架无人机、每架最多 3 枚烟幕弹，同时对 3 枚导弹实施遮蔽，求总体遮蔽时间尽量长的投放方案。
- final answer: O 奖复现的联合遮蔽时长为 M1 10.3 s、M2 6.2 s、M3 3.4 s，总计 19.9 s。
- baseline模型: baseline 用轨迹几何和规划优化，把无人机速度、航向、投放时刻、起爆时刻一起搜索，最大化有效遮蔽时长。
- 当前 instruction 子问题数: 5
- 最后答案数值项: 4 个计分 / 4 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2025-a-smoke-screen`; 状态: error: AgentTimeoutError(1); 当前口径 reward: N/A
- v4-flash B-Eval: N/A; BO-Eval: N/A; raw panel score: N/A
- v4-flash 对齐 verifier metric path 的答案覆盖: 0/4

子问题:
- 问题1: 利用无人机FY1 投放1 枚烟幕干扰弹实施对M1 的干扰，若FY1 以120 m/s 的
- 问题2: 利用无人机FY1 投放1 枚烟幕干扰弹实施对M1 的干扰，确定FY1 的飞行方
- 问题3: 利用无人机FY1 投放3 枚烟幕干扰弹，实施对M1 的干扰。请给出烟幕干扰弹
- 问题4: 利用FY1、FY2、FY3 等3 架无人机，各投放1 枚烟幕干扰弹，实施对M1 的
- 问题5: 利用5 架无人机，每架无人机至多投放3 枚烟幕干扰弹，实施对M1、M2、M3

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.q5_union_duration_s.M1` | 越接近 verifier/O奖值越好 | 10.3 | N/A | N/A | N/A | 是 |
| 2 | `experiment_result.q5_union_duration_s.M2` | 越接近 verifier/O奖值越好 | 6.2 | N/A | N/A | N/A | 是 |
| 3 | `experiment_result.q5_union_duration_s.M3` | 越接近 verifier/O奖值越好 | 3.4 | N/A | N/A | N/A | 是 |
| 4 | `experiment_result.q5_union_duration_s.total` | 越接近 verifier/O奖值越好 | 19.9 | N/A | N/A | N/A | 是 |

<a id="cumcm-2025-b"></a>

## CUMCM 2025 B: SiC epitaxial-layer thickness inversion

- Task slug: `cumcm-2025-b-sic-thickness`
- 简洁任务描述: CUMCM 2025 B: SiC epitaxial-layer thickness inversion
- 最后评测问题: 把多光束反射/透射造成的干涉也考虑进去，重新确定碳化硅外延层厚度，并分析结果可靠性。
- final answer: O 奖复现推荐厚度为 SiC 8.9815 um、Si 10.5145 um。
- baseline模型: baseline 用数据拟合与回归分析，从光谱条纹周期和非线性拟合中反推出外延层厚度。
- 当前 instruction 子问题数: 3
- 最后答案数值项: 2 个计分 / 2 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2025-b-sic-thickness`; 状态: error: AgentTimeoutError(1); 当前口径 reward: 0.143178654302
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
- 最后评测问题: 对女胎样本，用染色体 Z 值、GC 含量、读段数、BMI 等指标判断胎儿是否异常。
- final answer: O 奖复现的女胎异常判定模型 leave-one-out accuracy 为 0.8659，F1 为 0.3721。
- baseline模型: baseline 用综合评价和权重决策，把多项检测指标合成风险分数，再给出异常判定。
- 当前 instruction 子问题数: 4
- 最后答案数值项: 2 个计分 / 2 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-cumcm-2025-c-nipt`; 状态: scored; 当前口径 reward: 0.471826516941
- v4-flash B-Eval: 0.471826516941; BO-Eval: 0.471826516941; raw panel score: 0.471826516941
- v4-flash 对齐 verifier metric path 的答案覆盖: 2/2

子问题:
- 问题1: 试分析胎儿Y 染色体浓度与孕妇的孕周数和BMI 等指标的相关特性，给出相应的关系模
- 问题2: 临床证明，男胎孕妇的BMI 是影响胎儿Y 染色体浓度的最早达标时间（即浓度达到或超
- 问题3: 男胎Y 染色体浓度达标时间受多种因素(身高、体重、年龄等)的影响，试综合考虑这些因
- 问题4: 由于孕妇和女胎都不携带Y 染色体，重要的是如何判定女胎是否异常。试以女胎孕妇的21

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.female_loo_accuracy` | 越接近 verifier/O奖值越好 | 0.8659 | N/A | 0.9174 | 0.668614228354 | 是 |
| 2 | `female_abnormality.leave_one_out_f1` | 越接近 verifier/O奖值越好 | 0.3721 | N/A | 0.489796 | 0.275038805529 | 是 |

<a id="mcm-2023-a"></a>

## MCM 2023 A: drought-stricken plant communities

- Task slug: `mcm-2023-a-plant-community`
- 简洁任务描述: MCM 2023 A: drought-stricken plant communities
- 最后评测问题: 综合物种数、干旱、污染和栖息地压力，说明怎样保证植物群落长期可生存。
- final answer: O 奖复现的核心量化结论包括最优/阈值物种数 2，beta 压力下生物量下降 32.0%，五物种均匀度 0.8826。
- baseline模型: baseline 把物种数阈值、功能性状、干旱敏感性和污染/栖息地压力合成为管理前沿。
- 当前 instruction 子问题数: 9
- 最后答案数值项: 3 个计分 / 3 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2023-a-plant-community`; 状态: error: AgentTimeoutError(1); 当前口径 reward: -0.248454921739
- v4-flash B-Eval: -0.248454921739; BO-Eval: 0; raw panel score: 0.254349744928
- v4-flash 对齐 verifier metric path 的答案覆盖: 3/3

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
| 1 | `target_comparison.beta_decline_pct.actual` | 越接近 verifier/O奖值越好 | 32 | N/A | 7.04 | 0.133333333333 | 是 |
| 2 | `target_comparison.five_species_pielou_evenness.actual` | 越接近 verifier/O奖值越好 | 0.8826 | N/A | 0.9673 | 0.555641827377 | 是 |
| 3 | `target_comparison.optimal_species_count.actual` | 越接近 verifier/O奖值越好 | 2 | N/A | 5 | 0.0740740740741 | 是 |

<a id="mcm-2023-b"></a>

## MCM 2023 B: reimagining Maasai Mara

- Task slug: `mcm-2023-b-maasai-mara`
- 简洁任务描述: MCM 2023 B: reimagining Maasai Mara
- 最后评测问题: 把土地分区和政策方案整理成给当地管理者的非技术报告，说明推荐方案的收益和用地分配。
- final answer: O 奖复现的方案 2 收益指标值约 154948.974，农业/狩猎/旅游/保护区格点数分别为 12、2、9、13。
- baseline模型: baseline 用空间土地利用优化，把农业、狩猎、旅游和野生动物保护的格点分配成收益最大化问题。
- 当前 instruction 子问题数: 3
- 最后答案数值项: 5 个计分 / 5 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2023-b-maasai-mara`; 状态: scored; 当前口径 reward: -0.572294585853
- v4-flash B-Eval: -0.572294585853; BO-Eval: 0; raw panel score: 0.0303626641468
- v4-flash 对齐 verifier metric path 的答案覆盖: 5/5

子问题:
- Q1: 考虑并建议针对不同领域的具体政策和管理策略 在当前的保护区内，将保护野生动物和其他自然资源，同时 也平衡了居住在该地区的人们的利益。这些政策和 战略应有助于减轻因失去机会而造成的影响 居住在保护...
- Q2: 制定并描述一种方法来确定哪些政策和管理 策略将带来最好的结果。你的报告应该讨论如何排名和 比较您的方法的结果。请务必包含描述和分析 用于预测动物与人之间相互作用的模型，以及 对保护区内及周边地区...
- Q3: 根据您提出的计划，提供对将导致的长期趋势的预测 从你的建议中。分析并提供确定性的估计 可能的长期结果的影响。您还应该描述您如何 该方法可应用于其他野生动物管理领域。

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `target_comparison.scenario2_agriculture_cells.actual` | 越接近 verifier/O奖值越好 | 12 | N/A | 100 | 0.0161001788909 | 是 |
| 2 | `target_comparison.scenario2_benefit_million.actual` | 越接近 verifier/O奖值越好 | 154948.974 | N/A | 104.24 | 0.107207252097 | 是 |
| 3 | `target_comparison.scenario2_hunting_cells.actual` | 越接近 verifier/O奖值越好 | 2 | N/A | 40 | 0.00627615062762 | 是 |
| 4 | `target_comparison.scenario2_tourism_cells.actual` | 越接近 verifier/O奖值越好 | 9 | N/A | 100 | 0.011728931364 | 是 |
| 5 | `target_comparison.scenario2_wildlife_cells.actual` | 越接近 verifier/O奖值越好 | 13 | N/A | 160 | 0.0105008077544 | 是 |

<a id="mcm-2023-c"></a>

## MCM 2023 C: predicting Wordle results

- Task slug: `mcm-2023-c-wordle`
- 简洁任务描述: MCM 2023 C: predicting Wordle results
- 最后评测问题: 在给纽约时报编辑的总结信之前，最后一个可量化核心是判断 EERIE 的难度，并给出难度分类模型准确率。
- final answer: O 奖复现把 EERIE 判为中等难度组 2，难度分类模型 holdout accuracy 为 0.7。
- baseline模型: baseline 用报告量时间序列、单词属性特征和分类模型来预测 Wordle 分布及难度等级。
- 当前 instruction 子问题数: 4
- 最后答案数值项: 1 个计分 / 2 个总项
- 评分版本: `tb-mathmodeling-v5-final-question-endpoint-target-minmax`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2023-c-wordle`; 状态: scored; 当前口径 reward: 0
- v4-flash B-Eval: 0; BO-Eval: 0; raw panel score: 0
- v4-flash 对齐 verifier metric path 的答案覆盖: 2/2

子问题:
- Q1: 报告结果的数量每天都有所不同。开发一个模型来解释这种变化并 使用您的模型为 3 月份报告的结果数量创建预测区间 2023 年 1 月 1 日。该词的任何属性是否会影响报告的分数百分比 玩困难模式...
- Q2: 对于未来日期的给定未来解决方案词，开发一个模型，使您能够 预测报告结果的分布。换句话说，预测相关的 未来日期 (1, 2, 3, 4, 5, 6, X) 的百分比。与哪些不确定性相关 你的模型和...
- Q3: 开发并总结一个模型，按难度对解决方案单词进行分类。识别 与每个分类相关联的给定单词的属性。使用你的模型， EERIE 这个词有多难？讨论您的分类模型的准确性。
- Q4: 列出并描述该数据集的一些其他有趣的特征。

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `target_comparison.eerie_group.actual` | 精确值；不计分 | 2 | 2 | 3 | 0 | 否 |
| 2 | `target_comparison.lightgbm_like_accuracy.actual` | 越高越好 | 0.7 | 0.422222 | 0.3211 | 0 | 是 |

<a id="mcm-2024-a"></a>

## MCM 2024 A: lamprey sex-ratio ecology

- Task slug: `mcm-2024-a-lamprey`
- 简洁任务描述: MCM 2024 A: lamprey sex-ratio ecology
- 最后评测问题: 判断七鳃鳗可变性别比例是否也会让生态系统中的其他生物受益，尤其是寄生者/宿主相关指标。
- final answer: O 奖复现的共存情景资源水平为 0.55，寄生者指数 8.562，宿主鱼指数 1080.356。
- baseline模型: baseline 用生态动力系统仿真，把资源水平、性别比例、七鳃鳗、宿主鱼和寄生者一起演化。
- 当前 instruction 子问题数: 4
- 最后答案数值项: 3 个计分 / 3 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2024-a-lamprey`; 状态: scored; 当前口径 reward: -0.194531681993
- v4-flash B-Eval: -0.194531681993; BO-Eval: 0; raw panel score: 0.262304068007
- v4-flash 对齐 verifier metric path 的答案覆盖: 3/3

子问题:
- Q1: 当七鳃鳗数量减少时，会对更大的生态系统产生什么影响？ 改变性别比例？
- Q2: 七鳃鳗种群的优点和缺点是什么？
- Q3: 考虑到性别比例的变化，对生态系统稳定性有何影响？
- Q4: 七鳃鳗种群中性别比例可变的生态系统能否为七鳃鳗种群提供优势？ 生态系统中的其他生物，例如寄生虫？

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.parasite_coexistence_case.final_parasite_index` | 越接近 verifier/O奖值越好 | 8.562 | N/A | 0.3124 | 0.110750842941 | 是 |
| 2 | `experiment_result.parasite_coexistence_case.host_fish_index` | 越接近 verifier/O奖值越好 | 1080.356 | N/A | 0.5981 | 0.107195843839 | 是 |
| 3 | `experiment_result.parasite_coexistence_case.resource_level` | 越接近 verifier/O奖值越好 | 0.55 | N/A | 0.5 | 0.568965517241 | 是 |

<a id="mcm-2024-b"></a>

## MCM 2024 B: submersible localization and search planning

- Task slug: `mcm-2024-b-submersible-search`
- 简洁任务描述: MCM 2024 B: submersible localization and search planning
- 最后评测问题: 把潜水器搜索模型迁移到加勒比海场景，并说明洋流、海底地形和多潜水器协同时需要怎样调整。
- final answer: O 奖复现给出的加勒比海调整为洋流不确定性乘数 1.35、地形不确定性乘数 1.2。
- baseline模型: baseline 用贝叶斯搜索规划，先估计位置后验，再按海流和地形不确定性调整搜索区域。
- 当前 instruction 子问题数: 4
- 最后答案数值项: 2 个计分 / 2 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2024-b-submersible-search`; 状态: scored; 当前口径 reward: -0.402596368978
- v4-flash B-Eval: -0.402596368978; BO-Eval: 0; raw panel score: 0.176024881022
- v4-flash 对齐 verifier metric path 的答案覆盖: 2/2

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

<a id="mcm-2024-c"></a>

## MCM 2024 C: momentum in tennis

- Task slug: `mcm-2024-c-tennis-momentum`
- 简洁任务描述: MCM 2024 C: momentum in tennis
- 最后评测问题: 把势头模型转成教练能用的赛中提示：什么时候可能发生势头转换，应重点监控哪些指标。
- final answer: O 奖复现的最终比赛预警率为 0.006；前三个势头预警特征相关系数约为 0.0302、-0.0223、0.0154。
- baseline模型: baseline 用势头时间序列、随机性检验和贝叶斯/分类预警模型，把比赛数据转成教练提示。
- 当前 instruction 子问题数: 1
- 最后答案数值项: 4 个计分 / 4 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2024-c-tennis-momentum`; 状态: scored; 当前口径 reward: -0.561238131236
- v4-flash B-Eval: -0.561238131236; BO-Eval: 0; raw panel score: 0.0300532687642
- v4-flash 对齐 verifier metric path 的答案覆盖: 4/4

子问题:
- Q1: Develop a model that captures the flow of play as points occur and apply it to one or more of the...

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.dual_temporal_bayes.final_match_warning_rate` | 越接近 verifier/O奖值越好 | 0.006 | N/A | 0.9632 | 0.000751628528478 | 是 |
| 2 | `experiment_result.top_swing_features[0].warning_correlation` | 越接近 verifier/O奖值越好 | 0.0302 | N/A | 0.1074 | 0.0448381668811 | 是 |
| 3 | `experiment_result.top_swing_features[1].warning_correlation` | 越接近 verifier/O奖值越好 | -0.0223 | N/A | 0.0809 | 0.0252748498243 | 是 |
| 4 | `experiment_result.top_swing_features[2].warning_correlation` | 越接近 verifier/O奖值越好 | 0.0154 | N/A | 0.051 | 0.0493484298227 | 是 |

<a id="mcm-2025-a"></a>

## MCM 2025 A: stair wear and historical traffic inference

- Task slug: `mcm-2025-a-stair-wear`
- 简洁任务描述: MCM 2025 A: stair wear and historical traffic inference
- 最后评测问题: 根据楼梯磨损反推典型一天大约多少人使用，以及这些人是短时间集中经过还是长时间稀疏经过。
- final answer: O 奖复现估计日均使用人数 73.52，短时峰值约 27.6 人，若分散到 10 小时则每小时约 4.6 人。
- baseline模型: baseline 用物理磨损反演，把磨损深度、材料假设和年龄区间换算成通行次数与典型日使用模式。
- 当前 instruction 子问题数: 8
- 最后答案数值项: 3 个计分 / 3 个总项
- 评分版本: `tb-mathmodeling-v5-final-question-endpoint-target-minmax`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2025-a-stair-wear`; 状态: scored; 当前口径 reward: 0
- v4-flash B-Eval: 0; BO-Eval: 0; raw panel score: 0
- v4-flash 对齐 verifier metric path 的答案覆盖: 3/3

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
| 1 | `daily_use_pattern.peak_period_users` | 越高越好 | 27.6 | 27.3 | 23.6 | 0 | 是 |
| 2 | `daily_use_pattern.regular_hour_users_if_spread_over_10_hours` | 越高越好 | 4.6 | 4.5 | 7.1 | 0 | 是 |
| 3 | `experiment_result.estimated_daily_users` | 越高越好 | 73.52 | 72.67 | 117.9 | 0 | 是 |

<a id="mcm-2025-b"></a>

## MCM 2025 B: sustainable tourism management in Juneau

- Task slug: `mcm-2025-b-juneau-tourism`
- 简洁任务描述: MCM 2025 B: sustainable tourism management in Juneau
- 最后评测问题: 给朱诺旅游委员会写一页备忘录，概括预测、各种限制/收费措施的效果，并推荐最优可持续旅游政策。
- final answer: O 奖复现推荐终端政策：日容量 11000 人，游客费 55 USD，年游客 1491526，总收入 431610327.83 USD，居民接受度 1.0，可持续得分 1.007。
- baseline模型: baseline 用可持续旅游政策优化，把游客量、收费、保护投入、居民接受度和冰川压力一起做动态规划。
- 当前 instruction 子问题数: 3
- 最后答案数值项: 6 个计分 / 6 个总项
- 评分版本: `tb-mathmodeling-v5-final-question-endpoint-target-minmax`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2025-b-juneau-tourism`; 状态: scored; 当前口径 reward: 0
- v4-flash B-Eval: 0; BO-Eval: 0; raw panel score: 0
- v4-flash 对齐 verifier metric path 的答案覆盖: 6/6

子问题:
- Q1: 在阿拉斯加朱诺建立可持续旅游业模型。你可能想要 考虑游客数量、总收入以及采取的措施等因素 稳定旅游业。清楚地说明您正在优化哪些因素以及哪些因素起作用 作为约束。包括任何额外收入的支出计划并说明如...
- Q2: 展示您的模型如何适应受以下因素影响的另一个旅游目的地： 过度旅游。位置的选择如何影响最有效的措施 重要吗？您如何使用您的模型来宣传以下景点和/或地点： 有更少的游客来发展更好的平衡吗？
- Q3: 向朱诺旅游委员会写一份一页备忘录，概述您的预测、 各种措施的效果，以及您对如何优化结果的建议。

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `experiment_result.annual_visitors` | 越高越好 | 1491526 | 1408000 | 1111429 | 0 | 是 |
| 2 | `experiment_result.optimal_daily_cap` | 越高越好 | 11000 | 10000 | 4000 | 0 | 是 |
| 3 | `experiment_result.optimal_visitor_fee_usd` | 越高越好 | 55 | 50 | 15 | 0 | 是 |
| 4 | `experiment_result.resident_acceptance_index` | 越高越好 | 1 | 0.78 | 0.764 | 0 | 是 |
| 5 | `experiment_result.sustainability_score` | 越高越好 | 1.007 | 0.908447 | 0.5827 | 0 | 是 |
| 6 | `experiment_result.total_revenue_usd` | 越高越好 | 431610327.83 | 400400000 | 277162606 | 0 | 是 |

<a id="mcm-2025-c"></a>

## MCM 2025 C: Olympic medal prediction

- Task slug: `mcm-2025-c-olympic-medals`
- 简洁任务描述: MCM 2025 C: Olympic medal prediction
- 最后评测问题: 说明模型还能发现哪些原创奖牌规律，以及这些规律怎样指导国家奥委会分配项目和教练资源。
- final answer: O 奖复现的教练效应建议中，四个候选投资的预计奖牌增益为 1.666667、2.0、3.0、1.777778，全局强教练效应 75 分位跳升为 6.0。
- baseline模型: baseline 用奥运奖牌预测、项目重要性分析和滚动三届历史成绩跳升来筛选可能的强教练效应。
- 当前 instruction 子问题数: 1
- 最后答案数值项: 5 个计分 / 5 个总项
- 评分版本: `tb-mathmodeling-v3-final-question-legacy-baseline-panel`
- v4-flash job: `terminus2-deepseek-v4-flash-current-mcm-2025-c-olympic-medals`; 状态: error: AgentTimeoutError(1); 当前口径 reward: -0.491474074565
- v4-flash B-Eval: -0.491474074565; BO-Eval: 0; raw panel score: 0.092540092102
- v4-flash 对齐 verifier metric path 的答案覆盖: 4/5

子问题:
- Q1: What other original insight(s) about Olympic medal counts does your model reveal? Explain how the...

Verifier/O 答案与 v4-flash 答案:

| # | Metric path | 方向 | Verifier/O answer | Baseline answer | v4-flash answer | Metric score | 是否计分 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `great_coach_model.global_top_jump_75pct` | 越接近 verifier/O奖值越好 | 6 | N/A | 17.7 | 0.0579710144928 | 是 |
| 2 | `great_coach_model.recommendations[0].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 1.666667 | N/A | 0.4 | 0.136363628926 | 是 |
| 3 | `great_coach_model.recommendations[1].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 2 | N/A | 3.5 | 0.137931034483 | 是 |
| 4 | `great_coach_model.recommendations[2].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 3 | N/A | 0.6 | 0.130434782609 | 是 |
| 5 | `great_coach_model.recommendations[3].estimated_medal_count_gain` | 越接近 verifier/O奖值越好 | 1.777778 | N/A | N/A | 0 | 是 |
