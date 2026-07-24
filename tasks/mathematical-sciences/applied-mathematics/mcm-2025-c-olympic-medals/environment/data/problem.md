# 2025-C MCM-C: Models for Olympic Medal Tables

- 来源目录：`docs/mcm-2015-2025/2025/MCM-C Models for Olympic Medal Tables`
- 数据状态：见 `mcm/data_manifest.*` 与 `mcm/question_solution_index.*`。

# 题目与问题：MCM-C: Models for Olympic Medal Tables

## 每问/小问拆解
| 编号 | 小问/任务 | 适合模型 | 说明 |
|---|---|---|---|
| Q1 | What other original insight(s) about Olympic medal counts does your model reveal? Explain how these insight(s) can inform country Olympic committees. | 时间序列预测、统计回归与拟合、机器学习建模 | 问题核心是趋势、周期、波动或未来预测时，用移动平均、指数平滑、ARIMA/GARCH/灰色模型。 |

## 中文题面
## 第 1 页

| ©2025 科玛普 | www.comap.org | www.mathmodels.org | | info@comap.org | 
2025年MCM 
问题 C：奥运会奖牌榜模型 
 
 
除了观看最近在巴黎举行的夏季奥运会期间的个人赛事外， 
2024年，球迷们关注的是每个国家的整体“奖牌榜”。最终结果（表1） 
显示美国奖牌总数最多（126枚），中美并列 
金牌榜第一名（40枚）。主办国法国是 
在金牌数（16 枚）排行榜上排名第五，但在奖牌总数方面排名第四，而伟大 
英国以 14 枚金牌排名第七，奖牌总数排名第三。 
 
黄金 
银牌 
铜牌 
总计 
美国 
40 
44 
42 
126 
中国 
40 
27 
24 
91 
日本 
20 
12 
13 
45 
澳大利亚 
18 
19 
16 
53 
法国 
16 
26 
22 
64 
荷兰 
15 
7 
12 
34 
英国 
14 
22 
29 
65 
表1：巴黎奥运会（2024年）决赛奖牌榜——金牌前7名国家[1] 
积分榜榜首的排名总是受到密切关注，但奖牌对于其他人来说也很重要。 
国家往往也同样受到重视。例如，阿尔巴尼亚（2 枚奖牌）、佛得角、多米尼加和 
圣卢西亚（2枚奖牌）在巴黎奥运会上赢得了他们国家的第一枚奥运会奖牌。多米尼克和 
圣卢西亚也在这些比赛中各获得一枚金牌。仍有60多个国家 
赢得奥运会奖牌。  
 
人们通常会对最终奖牌数进行预测，但通常不是基于历史数据 
奖牌很重要，但在即将到来的奥运会开始时，当前的运动员 
预定的比赛是已知的（例如： 
https://www.nielsen.com/news-center/2024/virtual-medal-table-forecast/）。

## 第 2 页

| ©2025 科玛普 | www.comap.org | www.mathmodels.org | | info@comap.org | 
提供了所有夏季奥运会、主办国以及奖牌榜的数据。 
所有夏季奥运会按运动项目细分的每届奥运会比赛项目数量 
玩过。此外，所有奥运会个人参赛者的数据及其运动项目和成绩 
提供（奖牌类型，或无奖牌）。您的模型和数据分析必须仅使用

提供的数据集。您可以使用其他资源来提供背景和背景或帮助 
并解释结果（请务必记录来源）。具体来说，使用提供的数据来：  
 
• 开发每个国家奖牌数的模型（金牌数和奖牌总数） 
最小值）。包括模型预测的不确定性/精度的估计以及 
衡量模型执行情况的指标。  
o 根据您的模型，您对洛杉矶奖牌榜的预测是什么 
2028 年夏季奥运会将在美国洛杉矶举行？包括所有的预测区间 
结果。您认为哪些国家最有可能取得进步？这将 
比 2024 年更糟吗？  
o 您的模型应包括尚未获得奖牌的国家；你是什么 
预测有多少人将在下一届奥运会上获得第一枚奖牌？什么 
你对这个估计有多大的把握？ 
o 您的模型还应该考虑给定的事件（数量和类型） 
奥运会。探究项目与奖牌数之间的关系 
国家赚。对于不同国家来说，哪些运动最重要？为什么？如何 
母国选择的赛事会影响结果吗？  
• 运动员可能会代表不同的国家参赛，但对他们来说这并不是一件简单的事情 
由于公民身份要求而发生变化。然而，教练可以很容易地从一个 
国家到另一个国家，因为他们不需要成为公民才能执教。因此，有 
“伟大教练”效应的可能性。两个可能的例子包括郎平[2]， 
曾执教美国和中国排球队夺得冠军 
有时引起争议的体操教练 Béla Károlyi[3]，曾执教罗马尼亚和 
随后美国女队也取得了巨大成功。检查数据以寻找证据 
可能由于“伟大教练”效应而产生的变化。这样的你估计多少钱 
效应对奖牌数有贡献吗？选择三个国家并确定它们所在的体育项目 
应该考虑投资一位“伟大”的教练并估计其影响。 
• 您的模型还揭示了哪些关于奥运会奖牌计数的其他原创见解？ 
解释这些见解如何为国家奥委会提供信息。

## 英文原文
| ©2025 by COMAP | www.comap.org | www.mathmodels.org | info@comap.org | 
2025 MCM 
Problem C: Models for Olympic Medal Tables 
 
 
In addition to watching individual events during the latest summer Olympic Games in Paris, 
2024, fans followed the overall “medal table” for each country. The final results (Table 1) 
showed the United States with the most total medals (126), and China and the United States tied 
at the top of the standings for the first place Gold medals (40). The host country, France, was 
5th in the Gold medal count (16) standings but 4th in terms of total medal count while Great 
Britain, 7th with 14 Gold medals finished 3rd in total medals. 
 
Gold 
Silver 
Bronze 
Total 
United States 
40 
44 
42 
126 
China 
40 
27 
24 
91 
Japan 
20 
12 
13 
45 
Australia 
18 
19 
16 
53 
France 
16 
26 
22 
64 
Netherlands 
15 
7 
12 
34 
Great Britain 
14 
22 
29 
65 
Table 1: Paris Olympics (2024) Final Medal Table – Gold Medal Top 7 Countries[1] 
The standings at the top of the table are always watched closely, but the medal counts for other 
countries are often just as valued. For example, Albania (2 medals), Cabo Verde, Dominica, and 
Saint Lucia (2 medals) won their nations' first Olympic medals at the Paris games. Dominica and 
Saint Lucia also each earned a Gold medal at these games. More than 60 countries have still yet 
to win an Olympic medal.  
 
Predictions of the final medal counts are commonly made, but typically not based on historical 
medal counts but closer to the start of an upcoming Olympic games when current athletes 
scheduled to compete are known (for example: 
https://www.nielsen.com/news-center/2024/virtual-medal-table-forecast/).

| ©2025 by COMAP | www.comap.org | www.mathmodels.org | info@comap.org | 
Data is provided of medal tables for all summer Olympic games, host countries, as well as the 
number of Olympic events at each games broken down by sport for all summer Olympic games 
played. Additionally, data for all individual Olympic competitors with their sport and result 
(medal type, or no medal) is provided. Your models and data analysis must ONLY use the 
provided data sets. You may use additional resources to provide background and context or help 
with interpreting results (be sure to document the sources). Specifically, use the provided data to:  
 
• Develop a model for medal counts for each country (for Gold and total medals at a 
minimum). Include estimates of the uncertainty/precision of your model predictions and 
measures of how well model performs.  
o Based on your model, what are your projections for the medal table in the Los 
Angeles, USA summer Olympics in 2028? Include prediction intervals for all 
results. Which countries do you believe are most likely to improve? Which will 
do worse than in 2024?  
o Your model should include countries that have yet to earn medals; what is your 
projection for how many will earn their first medal in the next Olympics? What 
sort of odds do you give to this estimate? 
o Your model should also consider the events (number and types) at a given 
Olympics. Explore the relationship between the events and how many medals 
countries earn. What sports are most important for various countries? Why? How 
do the events chosen by the home country impact results?  
• Athletes may compete for different countries, but it is not a simple matter for them to 
change due to citizenship requirements. Coaches, however, can easily move from one 
country to another as they do not need to be citizens to coach. There is, therefore, the 
possibility of a “great coach” effect. Two possible examples of this include Lang Ping[2], 
who coached volleyball teams from both the U.S. and China to championships, and the 
sometimes-controversial gymnastics coach, Béla Károlyi[3], who coached Romania and 
then the U.S. women’s teams with great success. Examine the data for evidence of 
changes that might be due to a “great coach” effect. How much do you estimate such an 
effect contributes to medal counts? Choose three countries and identify sports where they 
should consider investing in a “great” coach and estimate that impact. 
• What other original insight(s) about Olympic medal counts does your model reveal? 
Explain how these insight(s) can inform country Olympic committees.
