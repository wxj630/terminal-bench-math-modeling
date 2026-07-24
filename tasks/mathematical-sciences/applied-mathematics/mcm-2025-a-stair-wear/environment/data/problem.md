# 2025-A MCM-A: Testing Time: The Constant Wear On Stairs

- 来源目录：`docs/mcm-2015-2025/2025/MCM-A Testing Time - The Constant Wear On Stairs`
- 数据状态：见 `mcm/data_manifest.*` 与 `mcm/question_solution_index.*`。

# 题目与问题：MCM-A: Testing Time: The Constant Wear On Stairs

## 每问/小问拆解
| 编号 | 小问/任务 | 适合模型 | 说明 |
|---|---|---|---|
| Q1 | 使用楼梯的频率如何？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q2 | 使用楼梯的人是否喜欢某个特定的行进方向？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q3 | 有多少人同时使用楼梯？ （例如，成对的人是否 并排爬楼梯还是单列行进？） | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q4 | 磨损情况与现有信息一致吗？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q5 | 楼梯间的年龄是多少？估计的可靠性如何？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q6 | 进行了哪些维修或翻新？ | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |
| Q7 | 能否确定材料的来源？例如，如果使用石头，则 磨损与考古学家认为是原始采石场的材料一致 来源或是否使用木材，其磨损是否与树木的年龄和类型一致 假设被使用？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q8 | 可以确定哪些关于使用该设备的人数的信息 典型的一天中是否有大量的人使用楼梯 是短时间还是少数人较长时间？ | 微分方程与系统动力学、统计回归与拟合、几何与空间分析 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |

## 中文题面
## 第 1 页

| ©2025 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
 
2025年MCM  
问题A：测试时间：楼梯的持续磨损 
 
石头是坚定不移的象征，雕刻的岩石被用作建筑材料 
因为它具有抗磨损的能力。尽管它很耐用，但即使是石头也不能不受腐蚀 
磨损。为数不多的更有弹性的事情之一就是人们的坚持。  
 
 
图 1：长期使用后出现不均匀磨损的台阶示例。 
 
用于建造台阶的石头和其他材料会受到持续、长期的磨损，并且 
磨损可能不均匀。例如，非常古老的寺庙和教堂可能有楼梯 
台阶中心的磨损程度超过边缘，踏板也没有磨损 
不再有水平顶部，但可能看起来是弓形的。由于此类结构的性质， 
建筑物往往已经有人居住了很长一段时间，但 
特定地点的人们往往早于建筑物的建造。这个可以做到 
很难准确确定建筑物的建造日期。情况进一步 
当建筑物的施工时间很长时，装修会变得很复杂 
随着时间的推移，结构中添加了新的部件。 
 
您的团队需要就考古学家可以确定的信息提供指导 
从一组破旧的楼梯上。楼梯可以由各种材料建造，例如 
石头或木头。此外，还可以估计一组楼梯的建造时间， 
然而，可能很难获得准确的时间。从历史上可能并不清楚 
记录每个时间段内建造的结构中的哪一组楼梯。  
 
除了年龄之外，考古学家可能还对确定交通模式感兴趣 
与楼梯间的使用方式有关。例如，人们是否晋升以及 
同时下楼梯还是在任何给定时间使用主要方向？安 
考古学家可能还想确定楼梯间的使用频率。例如，做了

很多人在短时间内使用它还是少数人长期使用它 
时期？ 
 
您的团队需要开发一个模型来确定基本结论 
绘制给定的一组楼梯。鉴于以下情况，您的模型应该提供一些基本预测 
一组特定楼梯的磨损模式： 
• 使用楼梯的频率如何？ 
• 使用楼梯的人是否喜欢某个特定的行进方向？ 
• 有多少人同时使用楼梯？ （例如，成对的人是否 
并排爬楼梯还是单列行进？）

## 第 2 页

| ©2025 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
 
 
您可以假设考古学家可以访问相关结构并可以获得 
您的团队认为重要的任何衡量标准。测量必须在 
一种非破坏性的方式，成本一定相对较低，并且可以测量 
由一小群人用最少的工具拍摄。你应该明确什么 
需要进行测量。 
 
还有其他问题可能更难解决。假设估计 
年龄的存在、楼梯间的使用方式以及对日常生活模式的估计 
结构可用，确定可以为以下问题提供哪些指导： 
• 磨损情况与现有信息一致吗？ 
• 楼梯间的年龄是多少？估计的可靠性如何？ 
• 进行了哪些维修或翻新？ 
• 能否确定材料的来源？例如，如果使用石头，则 
磨损与考古学家认为是原始采石场的材料一致 
来源或是否使用木材，其磨损是否与树木的年龄和类型一致 
假设被使用？ 
• 可以确定哪些关于使用该设备的人数的信息 
典型的一天中是否有大量的人使用楼梯 
是短时间还是少数人较长时间？

## 英文原文
www.comap.org | www.mathmodels.org | info@comap.org | 
 
2025 MCM  
Problem A: Testing Time: The Constant Wear On Stairs 
 
Stone is a symbol of steadfast permanence, and carved rock is used as a building material 
because of its ability to resist wear. Despite its durability, even stone is not impervious to 
wear. One of the few things more resilient is the persistence of people.  
 
 
Figure 1: Example of steps that have uneven wear after long term use. 
 
The stone and other materials used to create steps are subject to constant, long-term wear, and 
the wear can be uneven. For example, extremely old temples and churches may have stairs in 
which the center of the steps has been worn down more than their edges, and the treads no 
longer have a level top but can appear to be bowed. Due to the nature of such structures, the 
buildings tend to have been inhabited by people over a very long period, but the presence of 
people at a particular site often predates the construction of buildings. This can make it 
difficult to accurately determine the date a structure was constructed. The situation is further 
complicated when construction on a structure occurs over a very long time, renovations have 
been made, and new parts to the structure have been added over time. 
 
Your team is asked to provide guidance on what information archaeologists can determine 
from a set of worn stairs. The stairs may be constructed from various materials, for example 
stone or wood. Also, an estimate of when a set of stairs was constructed may be available, 
however, it may be difficult to get a precise time. It may not be clear from the historical 
records which set of stairs in a structure was constructed in each time period.  
 
In addition to age, an archaeologist may also be interested in determining the traffic patterns 
associated with how a stairwell was used. For example, were people moving up as well as 
down the stairs at the same time or was a predominant direction used at any given time? An 
archaeologist may also want to determine how often the stair well was used. For example, did 
a large number of people use it over a short period or did a few people use it over a very long 
period? 
 
Your team is asked to develop a model that can determine what basic conclusions can be 
drawn given a set of stairs. Your model should provide some basic predictions given the 
patterns of wear on a particular set of stairs: 
• How often were the stairs used? 
• Was a certain direction of travel favored by the people using the stairs? 
• How many people used the stairs simultaneously? (For example, did pairs of people 
climb the stairs side-by-side or did they travel single file?)

www.comap.org | www.mathmodels.org | info@comap.org | 
 
 
You can assume that an archaeologist has access to the structure in question and can obtain 
whatever measurement your team believes is important. The measurements must be made in 
a way that is non-destructive, the cost must be relatively low, and the measurements can be 
taken by a small team of people with minimal tools. You should make clear what 
measurements are required. 
 
There are other questions that may be more difficult to address. Assuming an estimate of the 
age exists, the way the stairwell was used, and an estimate on the daily patterns of life in the 
structure are available, determine what guidance can be provided to the following questions: 
• Is the wear consistent with the information available? 
• What is the age of the stairwell and how reliable is the estimate? 
• What repairs or renovations have been conducted? 
• Can the source of the material be determined? For example, if stone is used is the 
wear consistent with materials from a quarry the archaeologist believes is the original 
source or if wood was used is the wear consistent with the age and type of trees that 
are assumed to be used? 
• What information can be determined with respect to the numbers of people using the 
stairs in a typical day and were there large numbers of people using the stairs over a 
short time or a small number of people over a longer time?
