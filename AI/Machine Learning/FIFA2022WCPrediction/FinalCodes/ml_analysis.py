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
import csv
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error
from tensorflow import keras
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.model_selection import ShuffleSplit
from sklearn.linear_model import Lasso
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from keras.layers import Embedding
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")



df = pd.read_csv('tr_data_after2.csv',encoding="utf_8_sig")
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

# Min-Max处理
play_score_temp = team_merge.iloc[:, :-1]
# play_score_normal = (play_score_temp - play_score_temp.min()) / (play_score_temp.max() - play_score_temp.min())

# 标准分数处理
play_score_normal = (play_score_temp - play_score_temp.mean()) / (play_score_temp.std())
play_score_normal = pd.concat([play_score_normal, team_merge.iloc[:, -1]], axis=1)
print(play_score_normal)

# 获取csv数据的长度（条数）
with open('tr_data_after2.csv', 'r',encoding="utf_8_sig") as f:
    line=len(f.readlines())

tr_index=sample(range(0,line-1),int(line*0.7))
te_index=[i for i in range(0,line-1) if i not in tr_index]


tr_x = play_score_normal.iloc[tr_index, :-1]   # 训练特征
tr_y = play_score_normal.iloc[tr_index, -1]  # 训练目标

te_x = play_score_normal.iloc[te_index, :-1]   # 测试特征
te_y = play_score_normal.iloc[te_index, -1]  # 测试目标

df2 = pd.read_csv('data.csv',encoding="utf_8_sig")
country = df2["country"]
times = df2["times"]
win = df2["win"]
goals = df2["goals"]
rate = df2["rate of winning"]
Average = df2["Average goal"]
frames=[country,times,win,goals,rate,Average]
country_all = pd.concat(frames, axis=1).dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

num_data = country_all.iloc[:,[1,2,3,4,5]]

# 测试对象Min-Max处理
# country_all_MM = (num_data - num_data.min()) / (num_data.max() - num_data.min())

# 标准分数标准化
country_all_MM = (num_data - num_data.mean()) / (num_data.std())


country_all_MM = pd.concat([country, country_all_MM], axis=1)
# country_all_MM.to_csv("tr_data_z.csv",encoding="utf_8_sig")
play_score_normal.reset_index(drop = True)
play_score_normal.to_csv("play_score_normal.csv",encoding="utf_8_sig")



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



# 学习曲线函数

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("game num")
    plt.ylabel("score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt



cv = ShuffleSplit(n_splits=line, test_size=0.2, random_state=0)
plot_learning_curve(logreg, "logreg", tr_x, tr_y, ylim=None, cv=cv, n_jobs=1)
plot_learning_curve(tree, "tree", tr_x, tr_y, ylim=None, cv=None, n_jobs=1)
plot_learning_curve(rf, "rf", tr_x, tr_y, ylim=None, cv=None, n_jobs=1)
plot_learning_curve(model, "model", tr_x, tr_y, ylim=None, cv=None, n_jobs=1)
plot_learning_curve(clf, "clf", tr_x, tr_y, ylim=None, cv=None, n_jobs=1)

#
#
def GRA_ONE(DataFrame,m=-1):
    gray= DataFrame
    # 读取为df格式
    gray=(gray - gray.min()) / (gray.max() - gray.min())
    # 标准化
    std = gray.iloc[:, m]  # 为标准要素
    ce = gray.iloc[:, 0:]  # 为比较要素
    n=ce.shape[0]
    m=ce.shape[1]# 计算行列

    # 与标准要素比较，相减
    a=zeros([m,n])
    for i in range(m):
        for j in range(n):
            a[i,j]=abs(ce.iloc[j,i]-std[j])

    # 取出矩阵中最大值与最小值
    c=amax(a)
    d=amin(a)

    # 计算值
    result=zeros([m,n])
    for i in range(m):
        for j in range(n):
            result[i,j]=(d+0.5*c)/(a[i,j]+0.5*c)

    # 求均值，得到灰色关联值
    result2=zeros(m)
    for i in range(m):
            result2[i]=mean(result[i,:])
    RT=pd.DataFrame(result2)
    return RT

def GRA(DataFrame):
    list_columns = [str(s) for s in range(len(DataFrame.columns)) if s not in [None]]
    df_local = pd.DataFrame(columns=['home_times','away_times','home_win','away_win','home_goals','away_goals','home_r_win','away_r_win','home_Ave_goal','away_Ave_goal'])
    for i in range(len(DataFrame.columns)):
        df_local.iloc[:,i] = GRA_ONE(DataFrame,m=i)[0]
    return df_local
play_score = GRA(team_merge.drop(columns=['result']))
#
#
#
# def ShowGRAHeatMap(DataFrame):
#     import matplotlib.pyplot as plt
#     import seaborn as sns
#     colormap = plt.cm.RdBu
#     plt.figure(figsize=(14,12))
#     plt.title('FIFA Correlation of Features', y=1.05, size=15)
#     sns.heatmap(DataFrame.astype(float),linewidths=0.1,vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)
#     plt.show()
# ShowGRAHeatMap(play_score)
#
#
#
#



# keras深度学习库
# 我们是用Sequential模型，它是多个网络层的线性堆叠，通过堆叠许多层，构建出深度神经网络。通过 .add() 函数添加新的层
# 这里我们定义了3个全连接层，第一层input_dim表示我们有10个输入，也就是各个特征，然后剩余的几层全连接，最后输出维度为2的结果
#
model_k = Sequential()
model_k.add(Dense(output_dim=500, input_dim=10, activation='relu'))
model_k.add(Dense(output_dim=500, input_dim=200, activation='relu'))
model_k.add(Dense(units=2, activation='softmax'))

# 为了保证数据一致性，将目标类转化为独热编码，同时我们想要计算交叉熵损失函数，Adam算法作为优化算法，然后把准确率当做衡量这个算法的指标

y = to_categorical(tr_y, 2)
model_k.compile(loss='categorical_crossentropy',
                optimizer='adam', metrics=['accuracy'])

# 以200个样本为一批进行迭代

model_k.fit(np.asarray(tr_x), y, epochs=200, batch_size=200)
result = model_k.evaluate(np.asarray(tr_x), y)
y_pred = model_k.predict_classes(np.asarray(te_x))
print(result[1])

#
# plt.show()

# 16强
#
# df = pd.read_csv('NO16.csv',encoding="utf_8_sig")
# country = df['country']
#
# g1_index=sample(range(0,16),8)
# group1=pd.Series(country[g1_index]).reset_index(drop = True)
#
# g2_index=[i for i in range(0,16) if i not in g1_index]
# group2=pd.Series(country[g2_index])
#
#
# csvFile = open('16res.csv', 'w', newline='',encoding="utf_8_sig")
# writer = csv.writer(csvFile)
# writer.writerow(["times","team1","team2","win"])
# print("\n16进8")
# for i in range(0,8):
#     print("组1：第",i+1,"队")
#     team1 = country_all_MM.loc[
#         country_all['country'] == group1.iloc[i]]
#
#     print(group1.iloc[i])
#     print("组2：第",i+1,"队")
#     team2 = country_all_MM.loc[
#         country_all['country'] == group2.iloc[i]]
#
#     print(group2.iloc[i])
#
    # print("比赛结果")
    # vs = pd.concat([team1.reset_index(),
    #                 team2.reset_index()],
    #                axis=1).drop(['index', 'country'], axis=1)
    #
    # result=model_k.predict_classes(np.asarray(vs))
#
#     if(result==1):
#         temp = group1.iloc[i]
#     if(result==0):
#         temp = group2.iloc[i]
#     print("获胜方：", temp)
#     writer.writerow([i,group1.iloc[i],group2.iloc[i],temp])
# csvFile.close()
#
# # 8强
# df = pd.read_csv('16res.csv',encoding="utf_8_sig")
# win = df['win']
# g1_index=[i for i in  range(0,4)]
# group1=pd.Series(win[g1_index]).reset_index(drop = True)
# g2_index=[j for j in  range(4,8)]
# group2=pd.Series(win[g2_index]).reset_index(drop = True)
#
#
#
# csvFile = open('8res.csv', 'w', newline='',encoding="utf_8_sig")
# writer = csv.writer(csvFile)
# writer.writerow(["times","team1","team2","win"])
# print("\n8进4")
# for i in range(0,4):
#     print("组1：第",i+1,"队")
#     team1 = country_all_MM.loc[country_all['country'] == group1.iloc[i]]
#     print(group1.iloc[i])
#     print("组2：第",i+1,"队")
#     team2 = country_all_MM.loc[country_all['country'] == group2.iloc[i]]
#     print(group2.iloc[i])
#     print("比赛结果")
#     vs = pd.concat([team1.reset_index(), team2.reset_index()], axis=1).drop(['index', 'country'], axis=1)
#     result=model_k.predict_classes(np.asarray(vs))
#     if (result == 1):
#         temp = group1.iloc[i]
#     if (result == 0):
#         temp = group2.iloc[i]
#     print("获胜方：", temp)
#     writer.writerow([i, group1.iloc[i], group2.iloc[i], temp])
# csvFile.close()
#
#
#
#
# # 4强
# df = pd.read_csv('8res.csv',encoding="utf_8_sig")
# win = df['win']
#
# g1_index=[i for i in  range(0,2)]
# group1=pd.Series(win[g1_index]).reset_index(drop = True)
# g2_index=[j for j in  range(2,4)]
# group2=pd.Series(win[g2_index]).reset_index(drop = True)
#
#
#
# csvFile = open('4res.csv', 'w', newline='',encoding="utf_8_sig")
# writer = csv.writer(csvFile)
# writer.writerow(["times","team1","team2","win"])
# print("\n4进2")
# for i in range(0,2):
#     print("组1：第",i+1,"队")
#     team1 = country_all_MM.loc[country_all['country'] == group1.iloc[i]]
#     print(group1.iloc[i])
#     print("组2：第",i+1,"队")
#     team2 = country_all_MM.loc[country_all['country'] == group2.iloc[i]]
#     print(group2.iloc[i])
#     print("比赛结果")
#     vs = pd.concat([team1.reset_index(), team2.reset_index()], axis=1).drop(['index', 'country'], axis=1)
#     result=model_k.predict_classes(np.asarray(vs))
#     if (result == 1):
#         temp = group1.iloc[i]
#     if (result == 0):
#         temp = group2.iloc[i]
#     print("获胜方：", temp)
#     writer.writerow([i, group1.iloc[i], group2.iloc[i], temp])
# csvFile.close()
#
# #决赛
# df = pd.read_csv('4res.csv',encoding="utf_8_sig")
# win = df['win']
#
# g1_index=[i for i in  range(0,1)]
# group1=pd.Series(win[g1_index]).reset_index(drop = True)
# g2_index=[j for j in  range(1,2)]
# group2=pd.Series(win[g2_index]).reset_index(drop = True)
#
#
#
# csvFile = open('2res.csv', 'w', newline='',encoding="utf_8_sig")
# writer = csv.writer(csvFile)
# writer.writerow(["times","team1","team2","win"])
# print("\n决赛")
# for i in range(0,1):
#     print("组1：第",i+1,"队")
#     team1 = country_all_MM.loc[country_all['country'] == group1.iloc[i]]
#     print(group1.iloc[i])
#     print("组2：第",i+1,"队")
#     team2 = country_all_MM.loc[country_all['country'] == group2.iloc[i]]
#     print(group2.iloc[i])
#     print("比赛结果")
#     vs = pd.concat([team1.reset_index(), team2.reset_index()], axis=1).drop(['index', 'country'], axis=1)
#     result=model_k.predict_classes(np.asarray(vs))
#     if (result == 1):
#         temp = group1.iloc[i]
#     if (result == 0):
#         temp = group2.iloc[i]
#     print("获胜方：", temp)
#     writer.writerow([i, group1.iloc[i], group2.iloc[i], temp])
# csvFile.close()
