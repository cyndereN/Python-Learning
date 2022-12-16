# 导入相关的库
import pandas as pd
import csv
# fifa_ch.csv为最初的把多余属性去掉，然后把国家名翻译成了中文的kaggle下载的文件
df = pd.read_csv('InputFiles/fifa.csv', encoding="utf_8_sig")
date = df["date"]
home_team = df["home_team"]
away_team = df["away_team"]
home_score = df["home_score"]
away_score = df["away_score"]
result_n = df["result_n"]

# 创建个数据字典
# 各个国家
country = home_team.append(away_team)
allcountry = {}
for i in country:
    if i not in allcountry:
        allcountry[i] = 0

# 各个国家参加比赛的次数
times = allcountry.copy()
for i in range(900):
    times[home_team[i]] +=1
    times[away_team[i]] +=1

# 各个国家胜利的次数
win=allcountry.copy()
for i in range(900):
    if result_n[i] == 0:
        win[away_team[i]] += 1
    if result_n[i] == 1:
        win[home_team[i]] += 1

# 总进球数
goals = allcountry.copy()
for i in range(900):
    goals[home_team[i]] += home_score[i]
    goals[away_team[i]] += away_score[i]

# 各个球队胜率，并新建文档data.csv存放数据
# 新建属性为 国家名称、世界杯参赛次数、胜利次数、进球数、胜率、场均进球数
csvFile = open('ProcessedFiles/data.csv','w', newline='')
writer = csv.writer(csvFile)
writer.writerow(["country","times","win","goals","rate of winning","Average goal"])
for key in allcountry:
    writer.writerow([key,times[key],win[key],goals[key],win[key]/times[key],goals[key]/times[key]])
csvFile.close()

df = pd.read_csv('ProcessedFiles/data.csv', encoding="utf_8_sig")
country = df["country"]
data_times = df["times"]
data_win = df["win"]
data_goals = df["goals"]
r_of_winning = df["rate of winning"]
Average_goal = df["Average goal"]

csvFile2 = open('ProcessedFiles/tr_data_after.csv','w', newline='',encoding="utf_8_sig")
writer2 = csv.writer(csvFile2)
writer2.writerow(["home_team","away_team","home_times","away_times","home_win","away_win","home_goals","away_goals","home_r_win","away_r_win","home_Ave_goal","away_Ave_goal","result"])

for i in range(900):
    for j in range(81):
        if(home_team[i]==country[j]):
            for k in range(81):
                if (away_team[i] == country[k]):
                    writer2.writerow([home_team[i],away_team[i],data_times[j],data_times[k],data_win[j],data_win[k],data_goals[j],data_goals[k],r_of_winning[j],r_of_winning[k],Average_goal[j],Average_goal[k],result_n[i]])
csvFile2.close()

# 合并后生成的tr_data_after.csv中内容为：主队、客队、主队参赛次数、客队参赛次数、主队胜利次数、客队胜利次数、主队进球数、客队进球数、主队胜率、客队胜率、主队场均进球、客队场均进球、比赛结果。