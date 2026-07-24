# 2024-A MCM-A: Resource Availability and Sex Ratios

- 来源目录：`docs/mcm-2015-2025/2024/MCM-A Resource Availability and Sex Ratios`
- 数据状态：见 `mcm/data_manifest.*` 与 `mcm/question_solution_index.*`。

# 题目与问题：MCM-A: Resource Availability and Sex Ratios

## 每问/小问拆解
| 编号 | 小问/任务 | 适合模型 | 说明 |
|---|---|---|---|
| Q1 | 当七鳃鳗数量减少时，会对更大的生态系统产生什么影响？ 改变性别比例？ | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |
| Q2 | 七鳃鳗种群的优点和缺点是什么？ | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |
| Q3 | 考虑到性别比例的变化，对生态系统稳定性有何影响？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q4 | 七鳃鳗种群中性别比例可变的生态系统能否为七鳃鳗种群提供优势？ 生态系统中的其他生物，例如寄生虫？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |

## 中文题面
## 第 1 页

| ©2024 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
2024年MCM  
问题A：资源可用性和性别比例 
 
 
虽然有些动物物种存在于通常的雄性或雌性之外，但大多数物种都是 
基本上是男性或女性。尽管许多物种在出生时性别比例为 1:1，但其他物种 
物种性别比例偏离均匀。这称为适应性性别比变异。例如， 
美洲鳄巢中孵化蛋的温度影响其性别比例 
出生。  
 
七鳃鳗的作用很复杂。在一些湖泊栖息地，它们被视为具有寄生虫 
对生态系统产生重大影响，而七鳃鳗也是某些地区的食物来源 
世界各地，例如斯堪的纳维亚半岛、波罗的海地区以及太平洋地区的一些原住民 
位于北美洲西北部。 
 
海七鳃鳗的性别比例会根据外部环境而变化。海七鳃鳗变成 
雄性或雌性取决于它们在幼虫阶段的生长速度。这些幼虫的生长 
比率受食物供应情况的影响。在食物供应不足的环境中， 
增长率会较低，男性比例可达78%左右 
人口。在食物更容易获得的环境中，男性的比例 
据观察，这一比例约为人口的 56%。  
 
我们关注性别比例问题及其对当地条件的依赖，特别是对于 
海七鳃鳗。海七鳃鳗生活在湖泊或海洋栖息地，并沿河流洄游产卵。任务 
是检查一个物种改变其性别比例的能力的优点和缺点 
取决于资源的可用性。您的团队应该开发并检查一个模型来提供 
深入了解生态系统中由此产生的相互作用。 
 
要检查的问题包括以下内容： 
 
• 当七鳃鳗数量减少时，会对更大的生态系统产生什么影响？ 
改变性别比例？ 
 
• 七鳃鳗种群的优点和缺点是什么？ 
 
• 考虑到性别比例的变化，对生态系统稳定性有何影响？

七鳃鳗？ 
 
• 七鳃鳗种群中性别比例可变的生态系统能否为七鳃鳗种群提供优势？ 
生态系统中的其他生物，例如寄生虫？

## 第 2 页

| ©2024 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org |

## 英文原文
www.comap.org | www.mathmodels.org | info@comap.org | 
2024 MCM  
Problem A: Resource Availability and Sex Ratios 
 
 
While some animal species exist outside of the usual male or female sexes, most species are 
substantially either male or female. Although many species exhibit a 1:1 sex ratio at birth, other 
species deviate from an even sex ratio. This is called adaptive sex ratio variation. For example, 
the temperature of the nest incubating eggs of the American alligator influences the sex ratios at 
birth.  
 
The role of lampreys is complex. In some lake habitats, they are seen as parasites with a 
significant impact on the ecosystem, whereas lampreys are also a food source in some regions of 
the world, such as Scandinavia, the Baltics, and for some Indigenous peoples of the Pacific 
Northwest in North America. 
 
The sex ratio of sea lampreys can vary based on external circumstances. Sea lampreys become 
male or female depending on how quickly they grow during the larval stage. These larval growth 
rates are influenced by the availability of food. In environments where food availability is low, 
growth rates will be lower, and the percentage of males can reach approximately 78% of the 
population. In environments where food is more readily available, the percentage of males has 
been observed to be approximately 56% of the population.  
 
We focus on the question of sex ratios and their dependence on local conditions, specifically for 
sea lampreys. Sea lampreys live in lake or sea habitats and migrate up rivers to spawn. The task 
is to examine the advantages and disadvantages of the ability for a species to alter its sex ratio 
depending on resource availability. Your team should develop and examine a model to provide 
insights into the resulting interactions in an ecosystem. 
 
Questions to examine include the following: 
 
• What is the impact on the larger ecological system when the population of lampreys can 
alter its sex ratio? 
 
• What are the advantages and disadvantages to the population of lampreys? 
 
• What is the impact on the stability of the ecosystem given the changes in the sex ratios of 
lampreys? 
 
• Can an ecosystem with variable sex ratios in the lamprey population offer advantages to 
others in the ecosystem, such as parasites?

www.comap.org | www.mathmodels.org | info@comap.org |
