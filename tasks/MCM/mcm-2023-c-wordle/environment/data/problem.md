# 2023-C MCM-C: Predicting Wordle Results

- 来源目录：`docs/mcm-2015-2025/2023/MCM-C Predicting Wordle Results`
- 数据状态：见 `mcm/data_manifest.*` 与 `mcm/question_solution_index.*`。

# 题目与问题：MCM-C: Predicting Wordle Results

## 每问/小问拆解
| 编号 | 小问/任务 | 适合模型 | 说明 |
|---|---|---|---|
| Q1 | 报告结果的数量每天都有所不同。开发一个模型来解释这种变化并 使用您的模型为 3 月份报告的结果数量创建预测区间 2023 年 1 月 1 日。该词的任何属性是否会影响报告的分数百分比 玩困难模式？如果是这样，怎么办？如果没有，为什么不呢？ | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |
| Q2 | 对于未来日期的给定未来解决方案词，开发一个模型，使您能够 预测报告结果的分布。换句话说，预测相关的 未来日期 (1, 2, 3, 4, 5, 6, X) 的百分比。与哪些不确定性相关 你的模型和预测？给出你对这个词的预测的具体例子 EERIE，2023 年 3 月 1 日。您对模型的预测有多大信心？ | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |
| Q3 | 开发并总结一个模型，按难度对解决方案单词进行分类。识别 与每个分类相关联的给定单词的属性。使用你的模型， EERIE 这个词有多难？讨论您的分类模型的准确性。 | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |
| Q4 | 列出并描述该数据集的一些其他有趣的特征。 | 优化规划模型、统计回归与拟合、仿真与蒙特卡洛 | 目标明确且约束清楚时，用线性规划、非线性规划、整数规划或多目标规划求最优方案。 |

## 中文题面
## 第 1 页

| ©2023 COMAP 公司 | www.comap.com | www.mathmodels.org | | info@comap.com |

2023年MCM
问题 C：预测 Wordle 结果


图片：nytco.com[1]

背景
Wordle 是《纽约时报》目前每天提供的一个流行谜题。玩家尝试解决
通过在六次或更少的尝试中猜测五个字母的单词来解决谜题，每次猜测都会收到反馈。
对于这个版本，每个猜测都必须是一个实际的英文单词。不被认可的猜测
因为比赛中不允许使用言语。 Wordle 的受欢迎程度和版本持续增长
该游戏现已提供 60 多种语言版本。

《纽约时报》网站关于 Wordle 的说明指出，图块的颜色将会改变
当你提交你的话语后。黄色图块表示该图块中的字母在单词中，但它在
位置错误。绿色图块表示该图块中的字母在单词中并且在
正确的位置。灰色图块表示该图块中的字母根本不包含在该单词中
（见附件2）[2]。  图 1 是一个示例解决方案，其中找到了正确的结果
三次尝试。


图 1：2022 年 7 月 21 日的 Wordle Puzzle 解决方案示例[3]

## 第 2 页

| ©2023 COMAP 公司 | www.comap.com | www.mathmodels.org | | info@comap.com |

玩家可以在常规模式或“困难模式”下进行游戏。 Wordle 的困难模式让游戏更加精彩
困难在于要求玩家一旦找到单词中的正确字母（图块是黄色或
绿色），这些字母必须在后续的猜测中使用。图 1 中的示例是在
困难模式。

许多（但不是全部）用户在 Twitter 上报告他们的分数。针对这个问题，MCM 生成了一个
2022年1月7日至2022年12月31日的每日结果文件（见附件1）。这个
文件包括日期、比赛编号、当天单词、报告分数的人数
当天，困难模式的玩家人数，以及一局中猜出单词的百分比
尝试、两次尝试、三次尝试、四次尝试、五次尝试、六次尝试，或者无法解决该难题（由
X）。  例如，在图 2 中，2022 年 7 月 20 日的单词是“TRITE”，结果为

通过挖掘 Twitter 获得。尽管图 2 中的百分比总和为 100%，但在某些情况下
由于四舍五入，这可能不正确。


图2：2022年7月20日报告结果在Twitter上的分布[4]

要求
《纽约时报》要求您对此文件中的结果进行分析，以
回答几个问题。
•
报告结果的数量每天都有所不同。开发一个模型来解释这种变化并
使用您的模型为 3 月份报告的结果数量创建预测区间
2023 年 1 月 1 日。该词的任何属性是否会影响报告的分数百分比
玩困难模式？如果是这样，怎么办？如果没有，为什么不呢？

•
对于未来日期的给定未来解决方案词，开发一个模型，使您能够
预测报告结果的分布。换句话说，预测相关的
未来日期 (1, 2, 3, 4, 5, 6, X) 的百分比。与哪些不确定性相关
你的模型和预测？给出你对这个词的预测的具体例子
EERIE，2023 年 3 月 1 日。您对模型的预测有多大信心？

## 第 3 页

| ©2023 COMAP 公司 | www.comap.com | www.mathmodels.org | | info@comap.com |

•
开发并总结一个模型，按难度对解决方案单词进行分类。识别
与每个分类相关联的给定单词的属性。使用你的模型，
EERIE 这个词有多难？讨论您的分类模型的准确性。

•
列出并描述该数据集的一些其他有趣的特征。

最后，将你的结果总结在一封写给纽约拼图编辑的一到两页的信中
次。

## 英文原文
www.comap.com | www.mathmodels.org | info@comap.com |

2023 MCM
Problem C: Predicting Wordle Results


Image: nytco.com[1]

Background
Wordle is a popular puzzle currently offered daily by the New York Times. Players try to solve
the puzzle by guessing a five-letter word in six tries or less, receiving feedback with every guess.
For this version, each guess must be an actual word in English. Guesses that are not recognized
as words by the contest are not allowed. Wordle continues to grow in popularity and versions of
the game are now available in over 60 languages.

The New York Times website directions for Wordle state that the color of the tiles will change
after you submit your word. A yellow tile indicates the letter in that tile is in the word, but it is in
the wrong location. A green tile indicates that the letter in that tile is in the word and is in the
correct location. A gray tile indicates that the letter in that tile is not included in the word at all
(see Attachment 2)[2].  Figure 1 is an example solution where the correct result was found in
three tries.


Figure 1: Example Solution of Wordle Puzzle from July 21, 2022[3]

www.comap.com | www.mathmodels.org | info@comap.com |

Players can play in regular mode or “Hard Mode.” Wordle’s Hard Mode makes the game more
difficult by requiring that once a player has found a correct letter in a word (the tile is yellow or
green), those letters must be used in subsequent guesses. The example in Figure 1 was played in
Hard Mode.

Many (but not all) users report their scores on Twitter. For this problem, MCM has generated a
file of daily results for January 7, 2022 through December 31, 2022 (see Attachment 1). This
file includes the date, contest number, word of the day, the number of people reporting scores
that day, the number of players on hard mode, and the percentage that guessed the word in one
try, two tries, three tries, four tries, five tries, six tries, or could not solve the puzzle (indicated by
X).  For example, in Figure 2 the word on July 20, 2022 was “TRITE” and the results were
obtained by mining Twitter. Although the percentages in Figure 2 sum to 100%, in some cases
this may not be true due to rounding.


Figure 2: Distribution of the Reported Results for July 20, 2022 to Twitter[4]

Requirement
You have been asked by the New York Times to do an analysis of the results in this file to
answer several questions.
•
The number of reported results vary daily. Develop a model to explain this variation and
use your model to create a prediction interval for the number of reported results on March
1, 2023. Do any attributes of the word affect the percentage of scores reported that were
played in Hard Mode? If so, how? If not, why not?

•
For a given future solution word on a future date, develop a model that allows you to
predict the distribution of the reported results. In other words, to predict the associated
percentages of (1, 2, 3, 4, 5, 6, X) for a future date. What uncertainties are associated with
your model and predictions? Give a specific example of your prediction for the word
EERIE on March 1, 2023. How confident are you in your model’s prediction?

www.comap.com | www.mathmodels.org | info@comap.com |

•
Develop and summarize a model to classify solution words by difficulty. Identify the
attributes of a given word that are associated with each classification. Using your model,
how difficult is the word EERIE? Discuss the accuracy of your classification model.

•
List and describe some other interesting features of this data set.

Finally, summarize your results in a one- to two-page letter to the Puzzle Editor of the New York
Times.
