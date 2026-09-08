# 2023-2025 全模型答案可行性复核

生成日期：2026-09-04

## 结论

这份复核不把 JSON 字段齐全、轨迹里写过代码或分数高，直接当成数学方案已经可行。可行性分成三层：题面硬约束明确违反时 hard-invalid；能用共同几何/运动学重放时报告 replay-feasible；开放题或缺少布局/代码时只能写 artifact-only，不能据此宣称方案已被独立验证。

本轮共检查 180 个模型-题目单元。状态计数：artifact-only/calibrated-model=10, artifact-only/no-layout-replay=6, hard-invalid=6, missing-artifact=7, needs-review/decision-structure-pass=8, needs-review/lamprey-state-range-pass=10, needs-review/maasai-partition-pass=10, needs-review/model-layout-missing=5, needs-review/model-scale-mismatch=1, needs-review/nipt-group-coverage=1, needs-review/nipt-range-pass=9, needs-review/no-replenishment-schedule=5, needs-review/olympic-structure-pass=8, needs-review/overlap-quality-warning=2, needs-review/replay-gaps=2, needs-review/schedule-basic-check-pass=4, needs-review/schedule-fields-missing=1, needs-review/tourism-scale-mismatch=9, range-clean/artifact-only=68, replay-feasible-under-O-geometry=8。

新增确定性处罚：GLM-5.3 的 `cumcm-2023-a-heliostat-field` Q3 文字明确给出一面尾镜 `z=1.9024 m`，低于题面安装高度下限 2 m；v4 flash baseline 的 Q3 年平均热功率为 53.7955 MW，Gemini 3.7 Flash 的 Q2/Q3 年平均热功率为 55.460/54.966 MW，均未达到约 60 MW。这些是题面硬约束违反，进入 whole-task hard gate。此前对 Hy4 的 `cumcm-2024-b-production-decision`（SPRT 的 `c=-1` 哨兵）和 Juneau 中间年份 `sustainability_score>100` 的判断是审计误报，已撤销；它们现在分别标为结构通过和量纲需复核。
多波束题补充了独立重放：GLM、ox-alpha、Kimi 和 Qwen 的 artifact 都保存了可读取的实际 Q4 测线坐标。GLM/ox-alpha 为 60 条线，在官方海深网格上覆盖率约 99.945%，存在少量漏测；Kimi 为 81 条线、覆盖率 100%，但约 79.6% 的相邻局部重叠超过 20%；Qwen 为 60 条线、覆盖率 100%，但只有约 14.8% 的局部重叠落在 10%–20%，约 36.2% 低于 10%，约 51.0% 高于 20%。这些结果说明覆盖几何可执行，但质量约束仍需复核，不能直接写成完全满足题面。Qwen 的 Q3 末条测线中心超出 4 海里边界约 4.17 m，仅作为边界约定警告。

## 烟幕题独立重放

统一采用题面导弹/无人机坐标、300 m/s 导弹、重力抛体、10 m 烟幕半径、20 s 有效期，以及 Outstanding 复现使用的 27 个目标采样点和 25% 覆盖阈值。重放不读取模型自报的遮蔽时长，只读取投放参数重新计算。

| 模型 | 自报 Q5 总时长(s) | 独立重放总时长(s) | 状态 |
|---|---:|---:|---|
| v4 flash baseline | 22.23 | 24.04 | replay-feasible-under-O-geometry |
| v4 pro | 19.5486 | 20.44 | replay-feasible-under-O-geometry |
| GLM-5.3 | 15.5443 | 20.3 | replay-feasible-under-O-geometry |
| GPT-5.6 SOL high | 42.3921 | 54.46 | replay-feasible-under-O-geometry |
| Kimi K3 | 34.37 | 39.64 | replay-feasible-under-O-geometry |
| Gemini 3.7 Flash high primary+retry | 17.4209 | 21.04 | replay-feasible-under-O-geometry |
| Qwen3.8-27B-FP8 thinking | 31.6525 | 32.62 | replay-feasible-under-O-geometry |
| GLM-5.3-Flash (ox-alpha) | N/A | N/A | hard-invalid |
| Qwen3.8 Flash (Bailian) | N/A | N/A | missing-artifact |
| Tencent Hy4 Preview | 62.8845 | 56.42 | replay-feasible-under-O-geometry |

Qwen3.8-27B 的自报 31.65 s 在共同重放下约为 32.62 s，15 枚弹、每架不超过 3 枚、同一无人机投放间隔至少 1 s、速度和爆炸高度约束均通过。因此这个离群高分目前不能因“高于 Outstanding”而处罚；它的风险是目标模型较简化，而不是已发现的运动学不可能。

ox-alpha 的 Q5 在共同重放下为 0 s，保留既有 hard gate。其余模型的重放结果也会和自报值有差异，这是采样阈值/时间步不同造成的，不自动按数值差异处罚。

## 明确硬错误

| 模型 | 题目 | 处理 | 证据 |
|---|---|---|---|
| v4 flash baseline | `cumcm-2023-a-heliostat-field` | hard-invalid | hard-invalid/heliostat-constraint: Q2 rated-power constraint violation: 53.795541 MW is below the required approximately 60 MW; Q3 rated-power constraint violation: 53.795541 MW is below the required approximately 60 MW; Q3 does not expose numeric mirror dimensions |
| GLM-5.3 | `cumcm-2023-a-heliostat-field` | hard-invalid | explicit Q3 design note violates heliostat installation-height bound: one tail mirror uses z=1.9024 m, below the required 2 m minimum |
| Gemini 3.7 Flash high primary+retry | `cumcm-2023-a-heliostat-field` | hard-invalid | hard-invalid/heliostat-constraint: Question 2 rated-power constraint violation: 55.460000 MW is below the required approximately 60 MW; Question 3 rated-power constraint violation: 54.966000 MW is below the required approximately 60 MW |
| Kimi K3 | `mcm-2025-b-juneau-tourism` | hard-invalid | unit/scale invalid: resident_acceptance_index=1.5 and sustainability_score=232.2 on a unit-scale score |
| Kimi K3 | `mcm-2025-c-olympic-medals` | hard-invalid | invalid high coach-effect result: only three scored recommendations and endpoint verifier reward is negative/BO 0 |

其中 `mcm-2024-a-lamprey` 的 score-config invalid 是所有当前模型共用的字段量纲问题：O 奖端点给的是种群规模，若模型返回归一化指数，不能把它当成“生态边界违反”，但也不能当成同量纲精确复现；因此只保留逐指标警告，不整题 hard gate。Kimi 的 Juneau 仍因最终接受度 1.5 和可持续分数 232.2 与 unit-scale 端点不可比较而保留人工 hard gate；Kimi 的 Olympic 结构也有独立硬证据。ox-alpha 烟幕题仍以统一几何重放为准。

## 高分单元复核

下表列出 direction-aware raw ≥ 1.15 或已被 hard gate 的单元。`range-clean/artifact-only` 只表示基础数值范围和结构没有直接越界，不表示论文级数学模型已经被重跑。

| 模型 | 题目 | raw | O-Eval | 状态 | 复核结论 |
|---|---|---:|---:|---|---|
| GLM-5.3 | `cumcm-2023-a-heliostat-field` | 1.3935 | 100.00% | hard-invalid | explicit Q3 design note violates heliostat installation-height bound: one tail mirror uses z=1.9024 m, below the required 2 m minimum |
| Gemini 3.7 Flash high primary+retry | `cumcm-2023-a-heliostat-field` | 0.969 | 96.90% | hard-invalid | hard-invalid/heliostat-constraint: Question 2 rated-power constraint violation: 55.460000 MW is below the required approximately 60 MW; Question 3 rated-power constraint violation: 54.966000 MW is below the required approximately 60 MW |
| Qwen3.8 Flash (Bailian) | `cumcm-2023-a-heliostat-field` | 1.4559 | 100.00% | needs-review/model-layout-missing | summary JSON reports Q3 design values, but no per-mirror coordinates, dimensions, heights, spacing, shadow, or optical replay files are present in the artifact |
| Qwen3.8-27B-FP8 thinking | `cumcm-2023-a-heliostat-field` | 1.2445 | 100.00% | needs-review/model-scale-mismatch | Q1 fixed-field optical scale is about 14.9% above O; Q3 power is not independently replayable from saved coordinates |
| Tencent Hy4 Preview | `cumcm-2023-a-heliostat-field` | 1.464 | 100.00% | needs-review/model-layout-missing | summary JSON reports Q3 design values, but no per-mirror coordinates, dimensions, heights, spacing, shadow, or optical replay files are present in the artifact |
| v4 pro | `cumcm-2023-a-heliostat-field` | 1.3129 | 100.00% | needs-review/model-layout-missing | summary JSON reports Q3 design values, but no per-mirror coordinates, dimensions, heights, spacing, shadow, or optical replay files are present in the artifact |
| GLM-5.3 | `cumcm-2023-b-multibeam-lines` | 1.5007 | 100.00% | needs-review/replay-gaps | Q4 replay on official 201x251 grid: 60 N-S lines in [0.0217,3.9917] NM, coverage=99.945%, missed=0.0555%, >20% overlap=151.24 NM, mean overlap=27.12%; overlap below10/within10-20/above20=36.1/12.8/51.1% |
| GLM-5.3-Flash (ox-alpha) | `cumcm-2023-b-multibeam-lines` | 1.5006 | 100.00% | needs-review/replay-gaps | Q4 replay on official 201x251 grid: 60 N-S lines in [0.0217,3.9937] NM, coverage=99.945%, missed=0.0555%, >20% overlap=151.16 NM, mean overlap=27.1%; overlap below10/within10-20/above20=36.2/12.8/51% |
| GPT-5.6 SOL high | `cumcm-2023-b-multibeam-lines` | 2.4257 | 100.00% | artifact-only/no-layout-replay | final JSON has summary metrics but the claimed line schedule/coverage files are not in the collected artifact |
| Gemini 3.7 Flash high primary+retry | `cumcm-2023-b-multibeam-lines` | 1.4964 | 100.00% | artifact-only/no-layout-replay | final JSON has summary metrics but the claimed line schedule/coverage files are not in the collected artifact |
| Kimi K3 | `cumcm-2023-b-multibeam-lines` | 1.4104 | 100.00% | needs-review/overlap-quality-warning | Q4 replay on official 201x251 grid: 81 N-S lines in [0.02,4] NM, coverage=100%, missed=0%, >20% overlap=319.7 NM, mean overlap=46.16%; overlap below10/within10-20/above20=8.4/12/79.6% |
| Qwen3.8 Flash (Bailian) | `cumcm-2023-b-multibeam-lines` | 1.5427 | 100.00% | artifact-only/no-layout-replay | final JSON has summary metrics but the claimed line schedule/coverage files are not in the collected artifact |
| Qwen3.8-27B-FP8 thinking | `cumcm-2023-b-multibeam-lines` | 1.5018 | 100.00% | needs-review/overlap-quality-warning | Q4 replay on official 201x251 grid: 60 N-S lines in [0.0214,3.9962] NM, coverage=100%, missed=0%, >20% overlap=151.1 NM, mean overlap=27.08%; overlap below10/within10-20/above20=36.2/12.7/51%; warning: Q3 last line center is 4.17 m beyond the 4 NM east boundary |
| Tencent Hy4 Preview | `cumcm-2023-b-multibeam-lines` | 2.3499 | 100.00% | artifact-only/no-layout-replay | final JSON has summary metrics but the claimed line schedule/coverage files are not in the collected artifact |
| v4 pro | `cumcm-2023-b-multibeam-lines` | 1.4961 | 100.00% | artifact-only/no-layout-replay | final JSON has summary metrics but the claimed line schedule/coverage files are not in the collected artifact |
| GLM-5.3-Flash (ox-alpha) | `cumcm-2023-c-vegetable-pricing` | 1.7076 | 100.00% | needs-review/schedule-basic-check-pass | saved 33-SKU plan passes candidate/minimum-quantity checks; 6/6 categories recovered; optimization and demand-coverage claims still need replay |
| GPT-5.6 SOL high | `cumcm-2023-c-vegetable-pricing` | 1.5899 | 100.00% | needs-review/schedule-basic-check-pass | saved 33-SKU plan passes candidate/minimum-quantity checks; 6/6 categories recovered; optimization and demand-coverage claims still need replay |
| Gemini 3.7 Flash high primary+retry | `cumcm-2023-c-vegetable-pricing` | 2.5234 | 100.00% | needs-review/no-replenishment-schedule | artifact has aggregate demand/profit numbers but no concrete July 1 SKU replenishment and pricing table |
| Qwen3.8 Flash (Bailian) | `cumcm-2023-c-vegetable-pricing` | 1.755 | 100.00% | needs-review/schedule-basic-check-pass | saved 33-SKU plan passes candidate/minimum-quantity checks; 6/6 categories recovered; optimization and demand-coverage claims still need replay |
| Qwen3.8-27B-FP8 thinking | `cumcm-2023-c-vegetable-pricing` | 1.2929 | 100.00% | needs-review/no-replenishment-schedule | artifact has aggregate demand/profit numbers but no concrete July 1 SKU replenishment and pricing table |
| Qwen3.8-27B-FP8 thinking | `cumcm-2024-b-production-decision` | 1.4457 | 100.00% | needs-review/decision-structure-pass | binary decisions and probability ranges pass basic checks |
| GLM-5.3-Flash (ox-alpha) | `cumcm-2025-a-smoke-screen` | 2.5527 | 100.00% | hard-invalid | independent smoke-screen replay gives 0.00s coverage under O-reference line-of-sight geometry |
| GPT-5.6 SOL high | `cumcm-2025-a-smoke-screen` | 3.4164 | 100.00% | replay-feasible-under-O-geometry | reported total=42.3921 s; independent total=54.46 s |
| Gemini 3.7 Flash high primary+retry | `cumcm-2025-a-smoke-screen` | 1.2393 | 100.00% | replay-feasible-under-O-geometry | reported total=17.4209 s; independent total=21.04 s |
| Kimi K3 | `cumcm-2025-a-smoke-screen` | 2.894 | 100.00% | replay-feasible-under-O-geometry | reported total=34.37 s; independent total=39.64 s |
| Qwen3.8-27B-FP8 thinking | `cumcm-2025-a-smoke-screen` | 2.5918 | 100.00% | replay-feasible-under-O-geometry | reported total=31.6525 s; independent total=32.62 s |
| Tencent Hy4 Preview | `cumcm-2025-a-smoke-screen` | 4.004 | 100.00% | replay-feasible-under-O-geometry | reported total=62.8845 s; independent total=56.42 s |
| v4 pro | `cumcm-2025-a-smoke-screen` | 1.5324 | 100.00% | replay-feasible-under-O-geometry | reported total=19.5486 s; independent total=20.44 s |
| GPT-5.6 SOL high | `cumcm-2025-c-nipt` | 1.4524 | 100.00% | needs-review/nipt-range-pass | timing, probability, and classification ranges pass basic checks |
| Gemini 3.7 Flash high primary+retry | `cumcm-2025-c-nipt` | 1.2341 | 100.00% | needs-review/nipt-range-pass | timing, probability, and classification ranges pass basic checks |
| Kimi K3 | `cumcm-2025-c-nipt` | 1.2898 | 100.00% | needs-review/nipt-range-pass | timing, probability, and classification ranges pass basic checks |
| Qwen3.8 Flash (Bailian) | `cumcm-2025-c-nipt` | 1.2877 | 100.00% | needs-review/nipt-group-coverage | observed BMI ranges have an uncovered gap (33.21, 33.28); observed BMI ranges have an uncovered gap (34.06, 34.14); observed BMI ranges have an uncovered gap (35, 35.06); observed BMI ranges have an uncovered gap (36.36, 36.51) |
| Qwen3.8-27B-FP8 thinking | `cumcm-2025-c-nipt` | 1.5215 | 100.00% | needs-review/nipt-range-pass | timing, probability, and classification ranges pass basic checks |
| Tencent Hy4 Preview | `cumcm-2025-c-nipt` | 1.1846 | 100.00% | needs-review/nipt-range-pass | timing, probability, and classification ranges pass basic checks |
| v4 pro | `cumcm-2025-c-nipt` | 1.3609 | 100.00% | needs-review/nipt-range-pass | timing, probability, and classification ranges pass basic checks |
| GLM-5.3 | `mcm-2023-a-plant-community` | 1.5388 | 100.00% | artifact-only/calibrated-model | the problem supplies no numerical ecology time series; reported trajectories are model assumptions, not independently verifiable observations |
| GLM-5.3-Flash (ox-alpha) | `mcm-2023-a-plant-community` | 1.1634 | 100.00% | artifact-only/calibrated-model | the problem supplies no numerical ecology time series; reported trajectories are model assumptions, not independently verifiable observations |
| GPT-5.6 SOL high | `mcm-2023-a-plant-community` | 1.3644 | 100.00% | artifact-only/calibrated-model | the problem supplies no numerical ecology time series; reported trajectories are model assumptions, not independently verifiable observations |
| Tencent Hy4 Preview | `mcm-2023-a-plant-community` | 1.2964 | 100.00% | artifact-only/calibrated-model | the problem supplies no numerical ecology time series; reported trajectories are model assumptions, not independently verifiable observations |
| v4 pro | `mcm-2023-a-plant-community` | 1.1794 | 100.00% | artifact-only/calibrated-model | the problem supplies no numerical ecology time series; reported trajectories are model assumptions, not independently verifiable observations |
| Kimi K3 | `mcm-2025-b-juneau-tourism` | 1.4601 | 100.00% | hard-invalid | unit/scale invalid: resident_acceptance_index=1.5 and sustainability_score=232.2 on a unit-scale score |
| Kimi K3 | `mcm-2025-c-olympic-medals` | 2.9955 | 100.00% | hard-invalid | invalid high coach-effect result: only three scored recommendations and endpoint verifier reward is negative/BO 0 |

## 多波束独立重放细节

Qwen 的 Q4 方案使用 60 条南北测线，位置范围约 0.02141–3.99624 NM；官方附件为 201×251 网格，深度范围 20–197.2 m。按 120° 开角、局部东西向坡度和多波束覆盖宽度逐网格重算，覆盖率为 100%，漏测率为 0%，相邻条带重叠超过 20% 的长度约 151.10 NM，平均重叠约 27.08%，与自报 147.98 NM 和 26.28% 接近。但逐网格的相邻重叠只有约 14.8% 落在题面建议的 10%–20% 区间，约 36.2% 低于 10%，约 51.0% 高于 20%，所以这是一份“覆盖可执行、质量约束需复核”的方案，不应写成完全满足题面质量要求。

Q3 的 33 条测线间距对应约 10% 的设计重叠，但最后一个中心位置为 7412.17 m，而 4 NM 横向边界为 7408 m。差值只有 4.17 m，可能来自端点/坐标定义或四舍五入；在没有原始测线文件和坐标约定说明前，标记为需要人工复核，不把它升级成 whole-task hard gate。

## 重点开放题限制

- `cumcm-2023-b-multibeam-lines`：GLM、ox-alpha、Kimi 和 Qwen 保存了可重放的 Q4 测线坐标；GLM/ox-alpha 有约 0.055% 的网格漏测，Kimi 和 Qwen 虽然覆盖率为 100%，但相邻重叠分别明显偏高或分布很散。其他模型仍只有摘要，不能仅凭自报覆盖率称为已独立验证的可行布线。
- `mcm-2023-b-maasai-mara`：Qwen 的农业/旅游网格数相对 Outstanding 约大 73/120 倍，但题面允许自行建模，且最终 JSON 的 2500 格分配内部相加一致；当前标记为尺度需复核，不把 O 论文的 36 格复现直接当成题面硬约束。
- `mcm-2023-a-plant-community`：这是没有数值观测数据的开放生态建模题。不同模型用不同校准参数得到 5 或 8 个物种、不同生物量和干旱缓冲，并不自动意味着不可行；必须保存并重跑模型代码、参数、随机种子后才能升级为 verified feasible。
- `cumcm-2023-a-heliostat-field`：除 GLM 的高度硬错误、v4 flash/Gemini 的额定功率硬错误外，其余模型的 Q3 仍只有汇总数字，没有逐镜面坐标和光学重放包。Qwen 的 Q1 固定场光学效率比 Outstanding 约高 14.9%，Q3 的 60.08 MW 不能从已采集的镜面坐标独立复算，因此保持 needs-review，不把它当成确定的超 O 方案。
- `cumcm-2023-c-vegetable-pricing`：GPT、Kimi、Qwen Flash、Hy4 保存了 33 行单品计划；这些计划的单品均来自官方 6 月 24–30 日可售集合、数量均达到 2.5 kg 且覆盖 6 个品类，但仍没有独立重跑需求预测、价格弹性和“尽量满足各品类需求”的优化约束。其他模型没有具体单品表，不能仅凭利润和单品数 claim 可执行。

## 对榜单的影响

本轮只有证据充分的 whole-task 错误进入 hard-gated 榜：GLM 2023 A 定日镜高度、v4 flash 2023 A 额定功率、Gemini 2023 A 额定功率、Kimi 2025 B 的 unit/scale 错误、Kimi 2025 C 的推荐结构错误，以及既有的 ox-alpha 烟幕错误。Qwen 2023 A 因布局缺失保持 needs-review 不处罚；Qwen 2023 B 因覆盖几何通过但重叠质量超标改为 needs-review/overlap-quality-warning，不直接 hard gate；Qwen 2025 A 烟幕重放通过，不处罚；Hy4 的生产决策和 Juneau 不再处罚。原始 O-Eval 仍是主榜，hard-gated O-Eval 是可行性更保守的辅助榜，Robust BO-Eval 继续使用 hard-invalid=-100% 的失败惩罚。

## 复核边界

模型作答时生成的 `/root/results` 代码、Excel、CSV 和中间验证文件没有完整进入当前 Harbor artifact；因此本报告不会把轨迹中自报的“运行了仿真”当成独立证据。后续若要把某个开放题标成 verified feasible，应在 artifact 中保存最小可重放包：输入数据哈希、代码、参数、随机种子、约束检查结果和最终数值。
