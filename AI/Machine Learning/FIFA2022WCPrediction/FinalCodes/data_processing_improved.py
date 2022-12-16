import pandas as pd
import csv

df = pd.read_csv('fifa_ch.csv',encoding="utf_8_sig")
date = df["date"]
home_team = df["home_team"]
away_team = df["away_team"]
home_score = df["home_score"]
away_score = df["away_score"]
result_n = df["result_n"]


# 各个国家
country = home_team.append(away_team)
allcountry = {}

for i in country:
    if i not in allcountry:
        allcountry[i]=0


# 各个国家参加比赛的次数
times = allcountry.copy()
for i in range(900):
    times[home_team[i]] +=1
    times[away_team[i]] +=1

# print(times)

# 各个国家胜利的次数

win=allcountry.copy()
for i in range(900):
    if result_n[i] == 0:
        win[away_team[i]] += 1
    if result_n[i] == 1:
        win[home_team[i]] += 1
# print(win)


# 总进球数
goals = allcountry.copy()
for i in range(900):
    goals[home_team[i]] += home_score[i]
    goals[away_team[i]] += away_score[i]
# print(goals)


# 各个球队胜率

# csvFile = open('data.csv','w', newline='')
# writer = csv.writer(csvFile)
# writer.writerow(["country","times","win","goals","rate of winning","Average goal"])
# for key in allcountry:
#     writer.writerow([key,times[key],win[key],goals[key],win[key]/times[key],goals[key]/times[key]])
# csvFile.close()





df = pd.read_csv('data.csv',encoding="utf_8_sig")
country = df["country"]
data_times = df["times"]
data_win = df["win"]
data_goals = df["goals"]
r_of_winning = df["rate of winning"]
Average_goal = df["Average goal"]

csvFile2 = open('tr_data_after.csv','w', newline='',encoding="utf_8_sig")
writer2 = csv.writer(csvFile2)
writer2.writerow(["home_team","away_team","home_times","away_times","home_win","away_win","home_goals","away_goals","home_r_win","away_r_win","home_Ave_goal","away_Ave_goal","result"])

for i in range(900):
    for j in range(82):
        if(home_team[i]==country[j]):
            for k in range(82):
                if (away_team[i] == country[k]):
                    writer2.writerow([home_team[i],away_team[i],data_times[j],data_times[k],data_win[j],data_win[k],data_goals[j],data_goals[k],r_of_winning[j],r_of_winning[k],Average_goal[j],Average_goal[k],result_n[i]])
csvFile2.close()
