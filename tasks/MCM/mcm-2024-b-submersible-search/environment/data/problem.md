# 2024-B MCM-B: Searching for Submersibles

- 来源目录：`docs/mcm-2015-2025/2024/MCM-B Searching for Submersibles`
- 数据状态：见 `mcm/data_manifest.*` 与 `mcm/question_solution_index.*`。

# 题目与问题：MCM-B: Searching for Submersibles

## 每问/小问拆解
| 编号 | 小问/任务 | 适合模型 | 说明 |
|---|---|---|---|
| Q1 | 定位- 开发一个模型来预测潜水器随时间变化的位置。 o 这些预测有哪些不确定性？ o 潜水器可以定期向主船发送哪些信息来减少 事件发生前的这些不确定性？需要什么样的设备 潜水器需要这样做吗？ | 微分方程与系统动力学、优化规划模型、多指标评价模型 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q2 | 准备 - 您会向公司推荐哪些额外的搜索设备（如果有） 必要时携带主舰部署？您可以考虑不同类型的 设备，但还必须考虑与可用性、维护、 该设备的准备情况和使用情况。救援船还可以配备哪些附加设备 如有需要需要请人协助吗？ | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |
| Q3 | 搜索 - 开发一个模型，该模型将使用您的位置模型中的信息来 建议设备的初始部署点和搜索模式，以便 | 微分方程与系统动力学、优化规划模型、多指标评价模型 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |
| Q4 | 推断 - 如何扩展您的模型以考虑其他游客 加勒比海等目的地？您的模型将如何改变以适应 多个潜水器在同一区域移动？ | 微分方程与系统动力学、优化规划模型、多指标评价模型 | 系统随时间连续演化、有反馈、传播、消耗、增长或衰退机制时，用 ODE/PDE/差分方程。 |

## 中文题面
## 第 1 页

| ©2024 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org | 
2024年MCM 
问题B：寻找潜水器 
 
 
 
Maritime Cruises Mini-Submarines (MCMS) 是一家总部位于希腊的公司，生产潜水器 
能够将人类运送到海洋最深处。一艘潜水器被移至 
位置并脱离主船进行部署。 MCMS 现在希望使用他们的潜水器 
带领游客冒险探索爱奥尼亚海海底沉船残骸。 
然而，在他们做到这一点之前，他们需要通过开发来赢得监管机构的批准 
与主船失去通讯以及可能发生机械故障时的安全程序 
缺陷包括潜水器失去推进力。他们特别希望您 
开发一个模型来预测潜水器随时间的位置。与典型的搜索不同 
在陆地或海面上进行救援时，有缺陷的潜水器可能会发现 
本身位于海底或水下某个中性浮力点。它的位置 
可能进一步受到洋流、海洋不同密度和/或地理位置的影响 
海底。你的任务是：  
 
• 定位- 开发一个模型来预测潜水器随时间变化的位置。   
o 这些预测有哪些不确定性？  
o 潜水器可以定期向主船发送哪些信息来减少 
事件发生前的这些不确定性？需要什么样的设备 
潜水器需要这样做吗？ 
 
• 准备 - 您会向公司推荐哪些额外的搜索设备（如果有） 
必要时携带主舰部署？您可以考虑不同类型的 
设备，但还必须考虑与可用性、维护、 
该设备的准备情况和使用情况。救援船还可以配备哪些附加设备 
如有需要需要请人协助吗？ 
 
• 搜索 - 开发一个模型，该模型将使用您的位置模型中的信息来 
建议设备的初始部署点和搜索模式，以便

最大限度地缩短找到丢失的潜水器的位置的时间。确定找到的概率 
潜水器作为时间和累积搜索结果的函数。 
 
• 推断 - 如何扩展您的模型以考虑其他游客 
加勒比海等目的地？您的模型将如何改变以适应 
多个潜水器在同一区域移动？  
 
准备一份不超过 25 页的报告，提供您的计划的详细信息。包括两页 
您向希腊政府提交的报告的备忘录，以帮助获得批准。

## 第 2 页

| ©2024 COMAP 公司 | www.comap.org | www.mathmodels.org | | info@comap.org |

## 英文原文
www.comap.org | www.mathmodels.org | info@comap.org | 
2024 MCM 
Problem B: Searching for Submersibles 
 
 
 
Maritime Cruises Mini-Submarines (MCMS), a company based in Greece, builds submersibles 
capable of carrying humans to the deepest parts of the ocean. A submersible is moved to the 
location and deployed untethered from a host ship. MCMS now wishes to use their submersible 
to take tourists on adventures exploring the bottom of the Ionian Sea for sunken shipwrecks. 
Before they can do this, however, they need to win approval from regulators by developing 
safety procedures in case of a loss of communication to the host ship and possible mechanical 
defects including a loss of propulsion of the submersible. In particular, they would like you to 
develop a model to predict the location of the submersible over time. Unlike in a typical search 
and rescue on land or on the surface of a sea, the defective submersible could potentially find 
itself positioned on the sea floor or at some point of neutral buoyancy underwater. Its position 
could further be affected by currents, differing densities in the sea, and/or the geography of the 
sea floor. Your tasks are to:  
 
• Locate - Develop a model(s) that predicts the location of the submersible over time.   
o What are the uncertainties associated with these predictions?  
o What information can the submersible periodically send to the host ship to decrease 
these uncertainties prior to an incident? What kinds of equipment would the 
submersible need to do so? 
 
• Prepare - What, if any, additional search equipment would you recommend the company 
carry on the host ship to deploy if necessary? You may consider different types of 
equipment but must also consider costs associated with availability, maintenance, 
readiness, and usage of this equipment. What additional equipment might a rescue vessel 
need to bring in to assist if necessary? 
 
• Search - Develop a model that will use information from your location model(s) to 
recommend initial points of deployment and search patterns for the equipment so as to 
minimize the time to location of a lost submersible. Determine the probability of finding 
the submersible as a function of time and accumulated search results. 
 
• Extrapolate - How might your model be expanded to account for other tourist 
destinations such as the Caribbean Sea? How will your model change to account for 
multiple submersibles moving in the same general vicinity?  
 
Prepare a report of no more than 25 pages providing the details of your plan. Include a two-page 
memo of your report addressed to the Greek government to help win approval.

www.comap.org | www.mathmodels.org | info@comap.org |
