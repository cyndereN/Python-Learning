import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv


df = pd.read_csv('fifa_ch.csv',encoding="utf_8_sig")
date = df["date"]
home_team = df["home_team"]
away_team = df["away_team"]
home_score = df["home_score"]
away_score = df["away_score"]
result_n = df["result_n"]


# 2002-2020年16强
country = home_team.append(away_team)
allcountry = {}

for i in country:
    if i not in allcountry:
        allcountry[i]=0


# for k in range(2002,2020,4):
#     times = allcountry.copy()
#     for i in range(900):
#         if date[i]==k:
#            times[home_team[i]] +=1
#            times[away_team[i]] +=1
#
#     csvFile = open('country.csv','a', newline='',encoding='utf_8')
#     writer = csv.writer(csvFile)
#     # writer.writerow(["year","country","times"])
#
#     list_2002 = sorted(times.items(), key=lambda x: x[1], reverse=True)
#     b=pd.DataFrame(list_2002)
#     c= b[0].head(16)
#     d= b[1].head(16)
#
#
#     for i in range(16):
#         writer.writerow([k,c[i],d[i]])
#     csvFile.close()


df = pd.read_csv('country.csv',encoding="utf_8")
year = df["year"]
country = df["country"]
times = df["times"]
dic={}

for cy in country:
    if cy not in dic:
        dic[cy] = 1
    else:
        dic[cy] += 1
NO16=sorted(dic.items(), key=lambda x:x[1],reverse=True)

NO16=pd.DataFrame(NO16).reset_index(drop = True)

print(NO16.head(16))

# NO16[0].head(16).to_csv("NO16.csv",encoding="utf_8_sig")

