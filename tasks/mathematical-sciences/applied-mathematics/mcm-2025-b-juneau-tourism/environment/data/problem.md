# 2025-B MCM-B: Managing Sustainable Tourism

- 来源目录：`docs/mcm-2015-2025/2025/MCM-B Managing Sustainable Tourism`
- 数据状态：见 `mcm/data_manifest.*` 与 `mcm/question_solution_index.*`。

# 题目与问题：MCM-B: Managing Sustainable Tourism

## 每问/小问拆解
| 编号 | 小问/任务 | 适合模型 | 说明 |
|---|---|---|---|
| Q1 | 在阿拉斯加朱诺建立可持续旅游业模型。你可能想要 考虑游客数量、总收入以及采取的措施等因素 稳定旅游业。清楚地说明您正在优化哪些因素以及哪些因素起作用 作为约束。包括任何额外收入的支出计划并说明如何 这些支出会反馈到您的模型中，以促进可持续旅游业。包括一个 敏感性分析并讨论哪些因素最重要。 | 微分方程与系统动力学、优化规划模型、多指标评价模型 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q2 | 展示您的模型如何适应受以下因素影响的另一个旅游目的地： 过度旅游。位置的选择如何影响最有效的措施 重要吗？您如何使用您的模型来宣传以下景点和/或地点： 有更少的游客来发展更好的平衡吗？ | 微分方程与系统动力学、优化规划模型、多指标评价模型 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q3 | 向朱诺旅游委员会写一份一页备忘录，概述您的预测、 各种措施的效果，以及您对如何优化结果的建议。 | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |

## 中文题面
## 第 1 页

| ©2025 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
2025年MCM 
问题 B：管理可持续旅游业 
 
美国阿拉斯加朱诺市人口约 30,000 人，2023 年创下 1.6 的纪录 
百万邮轮旅客，最繁忙的时候接待多达七艘大型邮轮， 
超过约 20,000 名访客。[1]这些游客虽然为当地带来了可观的收入 
城市，大约 3.75 亿美元，[2] 他们还带来了与过度拥挤有关的问题，这些问题 
市政府正在努力限制客人数量。具有讽刺意味的是，门登霍尔冰川是最重要的冰川之一 
朱诺的景点已经在减少，部分原因是气温变暖， 
由于过度旅游。自2007年以来，冰川已经消退了相当于八个足球场的面积， 
导致许多当地人担心游客和相关收入最终会消失 
与冰川。[3]幸运的是，朱诺还有其他景点，包括观鲸和下雨 
森林，并且可以保持其作为旅游目的地的地位，只要它们能够开发和制定 
可持续旅游业计划。  
最近的报告[4]强调了旅游业的隐性成本以及日益增长的会计成本 
并管理这些成本，以保护自然和文化资源并建立可持续的 
世界各地众多社区所依赖的旅游业。这些隐性成本 
包括对当地基础设施的压力，包括饮用水供应、废物管理、 
旅游目的地的碳足迹总体增加，其中许多位于 
环境敏感地区。当地居民也面临住房压力 
供应和成本、过度拥挤和吵闹的游客。已出台多项措施 
尝试减轻负担，包括增加酒店税、游客费、限制人数 
每日访客以及对酒类销售和消费的限制。额外税收收入 
已用于支持保护、改善基础设施和开发 
社区计划。虽然许多依赖旅游业的当地人担心额外的

收费可能会赶走游客，而宁愿看到数量和他们的业务增长， 
许多其他当地人也变得不满，要么离开，要么抗议游客。  
• 在阿拉斯加朱诺建立可持续旅游业模型。你可能想要 
考虑游客数量、总收入以及采取的措施等因素 
稳定旅游业。清楚地说明您正在优化哪些因素以及哪些因素起作用 
作为约束。包括任何额外收入的支出计划并说明如何 
这些支出会反馈到您的模型中，以促进可持续旅游业。包括一个 
敏感性分析并讨论哪些因素最重要。

## 第 2 页

| ©2025 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
• 展示您的模型如何适应受以下因素影响的另一个旅游目的地： 
过度旅游。位置的选择如何影响最有效的措施 
重要吗？您如何使用您的模型来宣传以下景点和/或地点： 
有更少的游客来发展更好的平衡吗？ 
• 向朱诺旅游委员会写一份一页备忘录，概述您的预测、 
各种措施的效果，以及您对如何优化结果的建议。

## 英文原文
www.comap.org | www.mathmodels.org | info@comap.org | 
2025 MCM 
Problem B: Managing Sustainable Tourism 
 
Juneau, Alaska, USA with a population of about 30,000 residents, set a record in 2023 with 1.6 
million cruise passengers, hosting as many as seven large cruise ships on the busiest days, with 
upwards of around 20,000 visitors.[1] While these tourists bring in substantial revenue for the 
city, on the order of $375 million,[2] they also bring issues related to overcrowding that have the 
city working to limit the number of guests. Ironically, Mendenhall Glacier, one of the premier 
attractions in Juneau, has been receding, primarily due to warming temperatures caused, in part, 
by overtourism. The glacier has receded the equivalent of eight football fields since 2007, 
leading many locals to worry that the tourists and associated revenue will eventually disappear 
with the glacier.[3] Fortunately, Juneau has other attractions, including whale watching and rain 
forests, and can maintain their status as a tourist destination, provided they can develop and enact 
a plan for sustainable tourism.  
Recent reports[4] have highlighted the hidden costs of tourism and the growing need to account 
for and manage these costs to protect natural and cultural resources and build a sustainable 
tourism industry on which numerous communities around the world depend. These hidden costs 
include pressure on local infrastructure including drinking water supplies, waste management, 
and an overall increased carbon footprint in tourist destinations, many of which lie in 
environmentally sensitive regions. Local populations are also under pressure due to housing 
supplies and costs, overcrowding, and rowdy tourists. Various measures have been enacted to 
attempt to ease the burden, including increased hotel taxes, visitor fees, caps on the number of 
daily visitors, and restrictions on alcohol sales and consumption. Additional revenue from taxes 
have been used to support conservation, make improvements in infrastructure, and develop 
community programs. While many locals that depend on tourism are concerned that additional 
fees might drive tourists away and would rather see the numbers, and their businesses, grow, 
many other locals are becoming disgruntled and either leaving or protesting against tourists.  
• Build a model for a sustainable tourism industry in Juneau, Alaska. You may want to 
consider factors such as the number of visitors, overall revenue, and measures enacted to 
stabilize tourism. State clearly which factors you are optimizing, and which factors serve 
as constraints. Include a plan for expenditures from any additional revenue and show how 
these expenditures feed back into your model to promote sustainable tourism. Include a 
sensitivity analysis and discuss which factors are most important.

www.comap.org | www.mathmodels.org | info@comap.org | 
• Demonstrate how your model could be adapted to another tourist destination impacted by 
overtourism. How does the choice of location effect which measures will be most 
important? How might you use your model to promote attractions and/or locations that 
have fewer tourists to develop a better balance? 
• Write a one-page memo to the tourist council of Juneau outlining your predictions, the 
effects of various measures, and your advice on how to optimize outcomes.
