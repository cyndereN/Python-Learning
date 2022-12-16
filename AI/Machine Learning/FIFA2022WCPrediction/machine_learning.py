# 此处所引入的包大部分为下文机器学习算法
import pandas as pd
from numpy import *
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve
from sklearn.metrics import accuracy_score,recall_score,f1_score
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn import svm
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils.np_utils import to_categorical
from random import sample
from sklearn.model_selection import ShuffleSplit
# import warnings
# warnings.filterwarnings("ignore")

### Preprocessing

# 把tr_data_after.csv读入
df = pd.read_csv('ProcessedFiles/tr_data_after.csv',encoding="utf_8_sig")
home_team = df["home_team"]
away_team = df["away_team"]
home_times = df["home_times"]
away_times = df["away_times"]
home_win = df["home_win"]
away_win = df["away_win"]
home_goals = df["home_goals"]
away_goals = df["away_goals"]
home_r_win = df["home_r_win"]
away_r_win = df["away_r_win"]

home_Ave_goal = df["home_Ave_goal"]
away_Ave_goal = df["away_Ave_goal"]
result = df["result"]

team_merge = pd.concat([home_team,away_team,home_times,away_times,home_win,away_win,home_goals,away_goals,home_r_win,away_r_win,home_Ave_goal,away_Ave_goal,result], axis=1).drop(['home_team','away_team'],axis=1)

#以下使用了两种预处理方式，任选其一即可
# Min-Max处理（除了主客队名称和结果集以外数据）
play_score_temp = team_merge.iloc[:, :-1]
# play_score_normal = (play_score_temp - play_score_temp.min()) / (play_score_temp.max() - play_score_temp.min())

# 标准分数处理（除了主客队名称和结果集以外数据）
play_score_normal = (play_score_temp - play_score_temp.mean()) / (play_score_temp.std())
play_score_normal = pd.concat([play_score_normal, team_merge.iloc[:, -1]], axis=1)
# print(play_score_normal)

# 其中标准分数（z-score）是一个分数与平均数的差再除以标准差的过程。
# 用公式表示为：z=(x-μ)/σ。
# 其中x为某一具体分数，μ为平均数，σ为标准差。

# 获取csv数据的长度（条数）
with open('ProcessedFiles/tr_data_after.csv', 'r',encoding="utf_8_sig") as f:
    line=len(f.readlines())

# 70%的数据作为训练集
tr_index=sample(range(0,line-1),int(line*0.7))
te_index=[i for i in range(0,line-1) if i not in tr_index]


tr_x = play_score_normal.iloc[tr_index, :-1]   # 训练特征
tr_y = play_score_normal.iloc[tr_index, -1]  # 训练目标

te_x = play_score_normal.iloc[te_index, :-1]   # 测试特征
te_y = play_score_normal.iloc[te_index, -1]  # 测试目标

df2 = pd.read_csv('ProcessedFiles/data.csv',encoding="utf_8_sig")
country = df2["country"]
times = df2["times"]
win = df2["win"]
goals = df2["goals"]
rate = df2["rate of winning"]
Average = df2["Average goal"]
frames=[country,times,win,goals,rate,Average]
country_all = pd.concat(frames, axis=1).dropna(axis=0, how='any', subset=None, inplace=False)

num_data = country_all.iloc[:,[1,2,3,4,5]]

# 测试集Min-Max处理
# country_all_MM = (num_data - num_data.min()) / (num_data.max() - num_data.min())

# 测试集标准分数标准化
country_all_MM = (num_data - num_data.mean()) / (num_data.std())


country_all_MM = pd.concat([country, country_all_MM], axis=1)
# country_all_MM.to_csv("tr_data_z.csv",encoding="utf_8_sig")
play_score_normal.reset_index(drop = True)
# 预处理后的数据存放至play_score_normal.csv中
play_score_normal.to_csv("OutputFiles/play_score_normal.csv",encoding="utf_8_sig")

### 机器学习
model=MLPClassifier(hidden_layer_sizes=10,max_iter=1000).fit(tr_x,tr_y)
print("神经网络:")
print("训练集准确度:{:.3f}".format(model.score(tr_x,tr_y)))
print("测试集准确度:{:.3f}".format(model.score(te_x,te_y)))
y_pred = model.predict(te_x)
print("平均绝对误差:",mean_absolute_error(te_y, y_pred))
# 准确率，召回率，F-score评价
print("ACC",accuracy_score(te_y,y_pred))
print("REC",recall_score(te_y,y_pred,average="micro"))
print("F-score",f1_score(te_y,y_pred,average="micro"))


print("逻辑回归:")
logreg = LogisticRegression(C=1,solver='liblinear',multi_class ='auto')
logreg.fit(tr_x, tr_y)
score = logreg.score(tr_x, tr_y)
score2 = logreg.score(te_x, te_y)
print("训练集准确度:{:.3f}".format(logreg.score(tr_x,tr_y)))
print("测试集准确度:{:.3f}".format(logreg.score(te_x,te_y)))
y_pred = logreg.predict(te_x)
print("平均绝对误差:",mean_absolute_error(te_y, y_pred))
print("ACC",accuracy_score(te_y,y_pred))
print("REC",recall_score(te_y,y_pred,average="micro"))
print("F-score",f1_score(te_y,y_pred,average="micro"))


print("决策树:")
tree=DecisionTreeClassifier(max_depth=50,random_state=0)
tree.fit(tr_x,tr_y)
y_pred = tree.predict(te_x)
print("训练集准确度:{:.3f}".format(tree.score(tr_x,tr_y)))
print("测试集准确度:{:.3f}".format(tree.score(te_x,te_y)))
print("平均绝对误差:",mean_absolute_error(te_y, y_pred))
print("ACC",accuracy_score(te_y,y_pred))
print("REC",recall_score(te_y,y_pred,average="micro"))
print("F-score",f1_score(te_y,y_pred,average="micro"))

print("随机森林:")
rf=RandomForestClassifier(max_depth=20,n_estimators=1000,random_state=0)
rf.fit(tr_x,tr_y)
print("训练集准确度:{:.3f}".format(rf.score(tr_x,tr_y)))
print("测试集准确度:{:.3f}".format(rf.score(te_x,te_y)))
y_pred = rf.predict(te_x)
print("平均绝对误差:",mean_absolute_error(te_y, y_pred))
print("ACC",accuracy_score(te_y,y_pred))
print("REC",recall_score(te_y,y_pred,average="micro"))
print("F-score",f1_score(te_y,y_pred,average="micro"))


print("SVM支持向量机:")
clf = svm.SVC(C=0.1, kernel='linear', decision_function_shape='ovr')
clf.fit(tr_x, tr_y.ravel())
y_pred = clf.predict(te_x)
print("训练集准确度:{:.3f}".format(clf.score(tr_x,tr_y)))
print("测试集准确度:{:.3f}".format(clf.score(te_x,te_y)))
print("平均绝对误差:",mean_absolute_error(te_y, y_pred))
print("ACC",accuracy_score(te_y,y_pred))
print("REC",recall_score(te_y,y_pred,average="micro"))
print("F-score",f1_score(te_y,y_pred,average="micro"))

# 此处使用了神经网络、逻辑回归、支持向量机、决策树、随机森林算法分别进行训练。
# 并输出其在训练集上的准确度、在测试集上的准确度以及平均绝对误差。
# 此时发现结果并不理想。准确度仅为六成左右

# 查看next_step.md