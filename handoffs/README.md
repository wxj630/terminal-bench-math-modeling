# 写一篇 benchmark 论文需要哪些正文/附录材料

这份清单是给 `TB-MathModeling`（多模态数学建模 agent benchmark）写论文用的**交付说明 + 素材索引**。

一条重要前提：**benchmark 论文和"做方法/刷点"的论文需求不同**。
- 不需要 **消融实验**（没有"我们提出的模块"，score 全部来自被测模型）。
- 不需要 **train/test 划分**（整个 18 题就是统一的评测集，没有训练）。
- 需要的是三条别的：**任务构造可复现**、**计分口径可审计**、**参考值可验证**。前两条是 method，第三条正是本项目 Lean + 程序化 gate 两层的工作。

真正的 LaTeX 材料在 `paper/`。本文件是"要什么 + 我们已经有什么 + 还缺什么"。

---

## 一、正文（Main text）需要哪些

| # | 章节 | 内容要求 | 我们的状态 | 素材位置 |
|---|---|---|---|---|
| 1 | Abstract | 一句话讲清任务/规模/关键发现 | ✅ 可写 | `paper/sections/00-abstract.tex` |
| 2 | Introduction | 动机、缺口、贡献点列表 | ✅ 可写（4 条贡献） | `01-intro.tex` |
| 3 | Related Work | LLM agent benchmark / 数学&运筹 benchmark / 形式化验证用于评测 / 多模态 agent | ⚠️ 骨架已写，**需补引用** | `02-related.tex` |
| 4 | **Benchmark 构建（Method 主体）** | 题源、构造管线、artifact 契约、oracle 复现 | ✅ 事实齐全 | `03-benchmark.tex` |
| 5 | **计分方法** | 方向感知面板、O-Eval / B-Eval / Robust BO-Eval、单边计分、退化带、不可比指标排除 | ✅ 公式与代码都在 | `04-scoring.tex` |
| 6 | **可行性验证（本文特色）** | 程序化 gate（6 种可判定形式）+ Lean 证书（624 义务、内核校验、信任审计、判别力测试）+ 能力边界 A/B/C | ✅ 事实齐全 | `05-verification.tex` |
| 7 | Experiments: setup | 16 个模型条目、harness、prompt、软硬件、网络隔离 | ✅ 齐全（注意 prompt 版本 caveat） | `06-setup.tex` |
| 8 | **Results（主实验）** | 全 16 条榜单 + 多模态子榜 + 成本/token + hard gate 影响 | ✅ 数字齐全 | `07-results.tex` + `tables/` |
| 9 | Analysis | 逐题失分、参考值/尺度审计、pass@k 一致性 | ✅ 齐全 | `08-analysis.tex` |
| 10 | **Case Studies** | gpt-5.5 / oracle / deepseek-v4.1 的典型题建模求解 | ✅ 三题素材齐全 | `09-case-studies.tex` |
| 11 | Limitations & Ethics | 参考值依赖论文、尺度口径、许可证 | ✅ 可写 | `10-limitations.tex` |
| 12 | Conclusion | — | ✅ | `11-conclusion.tex` |

**主实验怎么汇报（按你的模板）**：你说"主实验需汇报多种子 mean 和 std，没有就汇报单次，注意汇报我们效果最好的那次"。
本项目事实是：
- **每题每模型默认 1 次**（`n_attempts=1`，`retry.max_retries=0`），所以主实验是**单次**。
- 唯一有多次的是板凳龙（`cumcm-2024-a-dragon-dance`）的 **pass@4**：Astra 与 Fable 各 4 次，**4 次答案完全一致**（`mean=1.246266`，`std≈4.6e-16`）。这可以作为"高一致性"的证据写进正文，而不是当成多 seed 统计。
- 我们在正文里**不做任何"取最好那次"的挑选**——单次就是单次，如实写。这一点建议在 Limitations 里明说，避免审稿人误读。

---

## 二、附录（Appendix）需要哪些

| # | 附录 | 内容 | 我们的状态 | 文件 |
|---|---|---|---|---|
| A | **数据集详情与划分** | 逐题表（来源/末问/指标数/oracle）、图片数、附件；**划分：明确写"无 train/test 划分，统一评测集"** | ✅ | `appendix/A-dataset.tex` |
| B | **软硬件环境** | 宿主、harbor 0.14.0、Docker 镜像与依赖版本、容器资源、网络隔离 | ✅ | `appendix/B-environment.tex` |
| C | **实验设置** | 16 个条目的模型/harness/档位、agent 命令模板、超时、重试、并发 | ✅ | `appendix/C-settings.tex` |
| D | **Baseline 信息** | 这里的 "baseline" 是 flash 基线面板（非 prompt baseline）；oracle 复现的来源与 paper id | ✅ | `appendix/D-baselines.tex` |
| E | **Prompt 设计** | `instruction.md` 模板全文、harbor 包装层、三种 harness 的实际命令行 | ✅（含版本 caveat） | `appendix/E-prompts.tex` |
| F | **Case study（完整版）** | 三题的完整数值对照与建模差异 | ✅ | `appendix/F-case-studies.tex` |
| G | **计分细节** | 逐题指标面板、公式、排除项、7 条 hard gate、退化带 | ✅ | `appendix/G-scoring-details.tex` |
| H | **Lean 义务目录** | 逐题义务数、示例义务、信任审计输出 | ✅ | `appendix/H-lean-catalog.tex` |

**不存在（不要写）**：消融实验、训练/测试划分、超参搜索。若审稿人问，用"benchmark 论文范式"回答。

---

## 三、还缺什么（写作时要补的）

| 缺口 | 说明 | 建议 |
|---|---|---|
| **引用** | `02-related.tex` 里全是 `\cite{TODO-...}` | 需要人工填 15–25 篇：agent benchmark（SWE-bench、GAIA、Terminal-Bench、τ-bench、MLE-bench）、数学/OR（FrontierMath、AIME 类、NL4OPT、Mamo）、形式化（Lean 4、Mathlib、AlphaProof、miniF2F）、多模态 agent |
| **图片资产** | `paper/figures/` 为空 | 建议放：① 榜单柱状图（现成 `mm-o-eval-bar.png`）② 计分管线示意 ③ Lean 工作流示意 ④ 三题 case study 图（现成 `dragon_spiral_snapshots.png` 等） |
| **作者/机构/致谢** | 占位 | 由你填 |
| **题面许可证** | 使用了 CUMCM/MCM 官方题面与附件 | 需在 Limitations/Ethics 说明来源与用途；确认可再分发 |
| **prompt 版本一致性** | `instruction.md` 在 trial 录制后被改过（`9d06a07`、`4c6f207`） | 论文引用**trial 实际收到的文本**（在 `trial.log`/`trajectory.json` 里），不要引用今天的文件 |

---

## 四、关键数字速查（写论文直接抄）

- 任务：**18**（CUMCM 9 + MCM 9），2023–2025，各年 A/B/C。
- 交付插图：**21 张**（从官方 PDF 裁出，6 题有图）；`instruction.md` 内联引用。
- oracle：**18/18** 有 O 奖复现；`docs/EVALUATION_RESULTS.md` 记 oracle 平均 reward ≈ **0.7893**。
- 被测模型条目：**16**（其中多模态 5 条）；每题每模型 **1 次**。
- 计分：末问数值核心；`O-Eval = clamp(model raw / O raw, 0, 1)`；`B-Eval = model raw − flash raw`；`Robust = clip(gain/gap, ±100%)`，`gap≥0.10` 才用比值，否则 `clip(gain, ±10pp)`，不可评分记 **−100%**。
- 硬门：程序化 gate **18/18** 覆盖、6 种可判定形式；`MANUAL_HARD_GATES` **4** 条；触发后 O-Eval raw → **0**、Robust → **−100%**。
- Lean 层：**624** 条义务、**18** 题、`decide`/`omega`、**无 Mathlib**、信任审计仅 `[propext, Quot.sound]`、判别力测试 **10** 类变异全被拒。
- 当前榜首：codex + gpt-5.5 xhigh **O-Eval 68.07% / Robust 23.62%**；最便宜且接近：opencode + deepseek-flash **65.76% / 18.36%，$2.54**。

生成时间：2026-10-10。数字来自 `jobs/terminus2-direction-aware-flash-baseline-bbo-2023-2025.md`（如榜单重跑请同步）。
