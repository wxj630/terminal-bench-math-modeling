# 2024-C MCM-C: Momentum in Tennis

- 来源目录：`docs/mcm-2015-2025/2024/MCM-C Momentum in Tennis`
- 数据状态：见 `mcm/data_manifest.*` 与 `mcm/question_solution_index.*`。

# 题目与问题：MCM-C: Momentum in Tennis

## 每问/小问拆解
| 编号 | 小问/任务 | 适合模型 | 说明 |
|---|---|---|---|
| Q1 | Develop a model that captures the flow of play as points occur and apply it to one or more of the matches. Your model should identify which player is performing better at a given time in the match, as well as how much better they are performing. Provide a visualization based on your model to depict the match flow. | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |

## 中文题面
## 第 1 页

| ©2024 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
2024年MCM  
问题 C：网球的势头 
 
2023年温网绅士决赛，20岁的西班牙新星卡洛斯·阿尔卡拉斯 
击败了36岁的诺瓦克·德约科维奇。这是德约科维奇自2013年以来首次在温网失利 
并结束了大满贯历史上伟大球员之一的非凡表现。 
这场比赛本身就是一场非凡的战斗。[1]德约科维奇似乎注定会轻松获胜，因为他 
以6-1统治首盘（7场比赛中赢下6场）。然而第二盘比赛气氛紧张 
最终阿尔卡雷斯在决胜局中以7-6获胜。第三盘与第一盘相反，阿尔卡拉斯 
6-1 轻松获胜。第四盘开始时，这位年轻的西班牙人似乎完全掌控了局面，但是 
不知何故，比赛再次改变了方向，德约科维奇完全掌控了比赛并赢得了第六盘 
– 3. 第五盘也是最后一盘，德约科维奇在第四盘中占据优势，但再次 
方向发生改变，阿尔卡拉斯控制了局面，以 6-4 获胜。本次比赛的数据 
比赛在提供的数据集中，“match_id”为“2023-wimbledon-1701”。你可以看到所有 
当德约科维奇使用“set_no”列等于 1 的优势时，第一盘的得分。 
令人难以置信的波动，有时是很多分甚至是比赛，发生在球员身上 
似乎拥有优势的人常常将其归因于“势头”。  
字典中对动量的定义是“通过运动或一系列运动获得的力量或力量” 
事件。”[2] 在体育运动中，团队或运动员可能会觉得他们有动力，或“力量/力量” 
在比赛/比赛期间，但很难衡量这种现象。此外，也不容易 
清楚地看到比赛期间的各种事件如何产生或改变动力（如果存在）。 
提供 2023 年温布尔登网球公开赛前 2 场比赛之后所有男子比赛的每一分数据 
回合。您可以自行决定选择包含其他玩家信息或其他数据， 
但您必须完整记录来源。使用数据来： 
• 开发一个模型，捕捉发生点时的比赛流程，并将其应用于一个或多个

更多的比赛。您的模型应该确定哪个玩家表现更好 
比赛中的特定时间，以及他们的表现有多好。提供一个 
基于您的模型的可视化来描述比赛流程。注：在网球比赛中， 
发球的球员赢得分数/比赛的概率要高得多。你可以 
希望以某种方式将其纳入您的模型中。 
• 一位网球教练对“势头”在比赛中发挥的作用表示怀疑。相反，他 
假设一名球员的比赛波动和成功率是随机的。使用你的 
评估此声明的模型/指标。

## 第 2 页

| ©2024 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
• 教练们很想知道是否有指标可以帮助确定何时 
比赛流程即将从有利于一名球员转向另一名球员。  
o 使用至少一场比赛提供的数据，开发一个模型来预测 
比赛中的这些波动。哪些因素似乎最相关（如果有的话）？ 
o 鉴于过去比赛“势头”波动的差异，您如何建议 
玩家要与另一位玩家进行新的比赛吗？ 
• 在一场或多场其他比赛中测试您开发的模型。你好吗 
预测比赛的波动？如果模型有时表现不佳，您可以吗？ 
确定未来模型中可能需要包含的任何因素？如何 
可推广的是你的模型适用于其他比赛（例如女子比赛）， 
锦标赛、球场场地和其他运动（例如乒乓球）。 
• 制作一份不超过 25 页的报告，其中包含您的发现，并包括一对一的指导 
两页的备忘录总结了你的结果，并为教练提供了关于以下角色的建议 
“势头”，以及如何让玩家做好应对影响流程的事件的准备 
在网球比赛期间打球。

## 英文原文
www.comap.org | www.mathmodels.org | info@comap.org | 
2024 MCM  
Problem C: Momentum in Tennis 
 
In the 2023 Wimbledon Gentlemen’s final, 20-year-old Spanish rising star Carlos Alcaraz 
defeated 36-year-old Novak Djokovic. The loss was Djokovic’s first at Wimbledon since 2013 
and ended a remarkable run for one of the all-time great players in Grand Slams. 
The match itself was a remarkable battle.[1] Djokovic seemed destined to win easily as he 
dominated the first set 6 – 1 (winning 6 of 7 games). The second set, however, was tense and 
finally won by Alcarez in a tie-breaker 7 – 6. The third set was the reverse of the first, Alcaraz 
winning handily 6 – 1. The young Spaniard seemed in total control as the fourth set started, but 
somehow the match again changed course with Djokovic taking complete control to win the set 6 
– 3. The fifth and final set started with Djokovic carrying the edge from the fourth set, but again 
a change of direction occurred and Alcaraz gained control and the victory 6 – 4. The data for this 
match is in the provided data set, “match_id” of “2023-wimbledon-1701”. You can see all the 
points for the first set when Djokovic had the edge using the “set_no” column equal to 1. The 
incredible swings, sometimes for many points or even games, that occurred in the player who 
seemed to have the advantage are often attributed to “momentum.”  
One dictionary definition of momentum is “strength or force gained by motion or by a series of 
events.”[2] In sports, a team or player may feel they have the momentum, or “strength/force” 
during a match/game, but it is difficult to measure such a phenomenon. Further, it is not readily 
apparent how various events during the match act to create or change momentum if it exists. 
Data is provided for every point from all Wimbledon 2023 men’s matches after the first 2 
rounds. You may choose to include additional player information or other data at your discretion, 
but you must completely document the sources. Use the data to: 
• Develop a model that captures the flow of play as points occur and apply it to one or 
more of the matches. Your model should identify which player is performing better at 
a given time in the match, as well as how much better they are performing. Provide a 
visualization based on your model to depict the match flow.
