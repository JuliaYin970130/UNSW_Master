import csv
import re
import pandas as pd
import string
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer, HashingVectorizer
from sklearn.metrics import *
from sklearn.model_selection import train_test_split, cross_val_score,cross_validate
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
import sys
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC


def predict_and_test(model, X_test_bag_of_words,data_Y_test):
    num_dec_point = 3
    predicted_y = model.predict(X_test_bag_of_words)
    a_mic = accuracy_score(data_Y_test, predicted_y)
    p_mic, r_mic, f1_mic, _ = precision_recall_fscore_support(data_Y_test,
                                                              predicted_y,
                                                              average='micro',
                                                              warn_for=())
    p_mac, r_mac, f1_mac, _ = precision_recall_fscore_support(data_Y_test,
                                                              predicted_y,
                                                              average='macro',
                                                              warn_for=())
    print('micro acc,prec,rec,f1: ', round(a_mic, num_dec_point), round(p_mic, num_dec_point),
          round(r_mic, num_dec_point), round(f1_mic, num_dec_point), sep="\t")
    print('macro prec,rec,f1: ', round(p_mac, num_dec_point), round(r_mac, num_dec_point), round(f1_mac, num_dec_point),
          sep="\t")
    # print(classification_report(data_Y_test, predicted_y))
    micro = [round(p_mic, num_dec_point),round(r_mic, num_dec_point), round(f1_mic, num_dec_point)]
    macro = [round(p_mac, num_dec_point), round(r_mac, num_dec_point), round(f1_mac, num_dec_point)]
    return a_mic,micro,macro


def remove_url(content):
    url_http = re.compile('^(https|http)?:\S+', re.S)
    token = url_http.sub(' ', content)
    url_www = re.compile('www.\S+', re.S)
    token = url_www.sub(' ', token)
    return token

# preprocessing data
def preprocessing(content):
    # remove 'junk' characters
    new_content = remove_url(content)
    result = ''
    good_chars = '#@_$% '
    for i in new_content:
        # remove junk characters
        if i.isalpha() or i.isdigit() or i in good_chars:
            result += i
    return result


def preprocessing_2(content):
    # remove 'junk' characters
    new_content = remove_url(content)
    result = ''
    good_chars = '#@_$% '
    for i in new_content:
        # remove junk characters
        if i.isalpha() or i.isdigit() or i in good_chars:
            result += i
    temp = result.split(' ')
    # wl = WordNetLemmatizer()
    ps = PorterStemmer()
    temp_stem = [ps.stem(w) for w in temp]
    # temp_wl = [wl.lemmatize(w) for w in temp_stem]
    result = ' '.join(temp_stem)


    return result


# read file
data_file = pd.read_csv("articles.tsv", sep='\t', header=None, quoting=csv.QUOTE_NONE)
# split file into train and test

split_point = 800
data_train_ = data_file[:split_point]
data_test_ = data_file[split_point:]

data_train = data_train_.copy()
data_test = data_test_.copy()

data_train[1] = data_train_[1].apply(lambda x:preprocessing_2(x))
data_test[1] = data_test_[1].apply(lambda x:preprocessing_2(x))

# split training data and label
data_X_train, data_Y_train = data_train[1], data_train[2]
data_X_test, data_Y_test = data_test[1], data_test[2]

acc_list = []
index =[]

# model.set_params(
#     **{'kernel': 'poly', 'degree': 1, 'C': 7e6, 'gamma': 'scale', 'coef0': 0.0, 'tol': 1e-3, 'epsilon': 20})

count_vec = TfidfVectorizer(max_features=4000)
X_train_bag_of_words = count_vec.fit_transform(data_X_train)
X_test_bag_of_words = count_vec.transform(data_X_test)
# 'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]


clf = SVC(gamma=0.001,C=1000)  # 0.945
model = clf.fit(X_train_bag_of_words, data_Y_train)
predicted_y = model.predict(X_test_bag_of_words)
#predicted_y = model.predict(X_test_bag_of_words)
# a_mic = accuracy_score(data_Y_test, predicted_y)
acc_b, micro_b, macro_b = predict_and_test(model,X_test_bag_of_words,data_Y_test)


# model = SVC(kernel='rbf', probability=True)
# param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
# grid_search = GridSearchCV(model, param_grid, n_jobs=8, verbose=1)
# grid_search.fit(X_train_bag_of_words, data_Y_train)
# best_parameters = grid_search.best_estimator_.get_params()
# for para, val in list(best_parameters.items()):
#     print(para, val)
# model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
# model.fit(X_train_bag_of_words, data_Y_train)
# best_param = GS.best_params_
# best_score = GS.best_score_
# print(best_param, best_score)
# acc_list.append(a_mic)
# index.append((i, a_mic))
#
# print(max(acc_list))
# max_ = max(acc_list)
# for i in index:
#     if i[1] == max_:
#         print(i[0])


# score = cross_val_score(clf, X_train_bag_of_words, data_Y_train, cv=10).mean()

scoring = ['precision_macro', 'recall_macro']

scores = cross_validate(clf, X_train_bag_of_words, data_Y_train, scoring=scoring)
sorted(scores.keys())

print(scores['test_score'])


#
# print(max(acc_list))
# max_ = max(acc_list)
# for i in index:
#     if i[1] == max_:
#         print(i[0])

    # acc_b, micro_b, macro_b = predict_and_test(model,X_test_bag_of_words,data_Y_test)
# x = np.arange(1000,10001,500)
# plt.ylabel('score')
# plt.xlabel('max_features')
# plt.plot(x, acc_list, 'r-')
# plt.savefig('max')
# plt.show()





# rf0 = RandomForestClassifier(oob_score=True,random_state=5)
# rf0.fit(X_train_bag_of_words,data_Y_train)
# print(rf0.oob_score_)
# print("accuracy:%f"%rf0.oob_score_)
#
# # score_pre = cross_val_score(clf,X_test_bag_of_words, data_Y_train, cv=10).mean()
# # print(score_pre)
#
# param_test1 = {"n_estimators":range(1,101,10)}
# gsearch1 = GridSearchCV(estimator=RandomForestClassifier(),param_grid=param_test1,
#                         scoring='roc_auc',cv=10)
# gsearch1.fit(X_train_bag_of_words,data_Y_train)
#
# print(gsearch1.grid_scores_)
# print(gsearch1.best_params_)
# print("best accuracy:%f" % gsearch1.best_score_)


# param_test1 = {"n_estimators":range(1,101,10)}
# gsearch1 = GridSearchCV(estimator=RandomForestClassifier(),param_grid=param_test1,
#                         scoring='roc_auc',cv=10)
# gsearch1.fit(X_train_bag_of_words,data_Y_train)
#
# print(gsearch1.grid_scores_)
# print(gsearch1.best_params_)
# print("best accuracy:%f" % gsearch1.best_score_)

# # 调参，绘制学习曲线来调参n_estimators（对随机森林影响最大）
# score_lt = []
#
# #每隔10步建立一个随机森林，获得不同n_estimators的得分
# for i in range(0,110,10):
#     rfc = RandomForestClassifier(n_estimators=i+1,random_state=5)
#     score = cross_val_score(rfc, X_train_bag_of_words, data_Y_train, cv=10).mean()
#     score_lt.append(score)
# score_max = max(score_lt)
# print('最大得分：{}'.format(score_max),
#       '子树数量为：{}'.format(score_lt.index(score_max)*10+1))
#
# # 绘制学习曲线
# x = np.arange(1,111,10)
# plt.subplot(111)
# plt.ylabel('score')
# plt.xlabel('number of n_estimators')
# plt.plot(x, score_lt, 'r-')
# plt.savefig('n_estimators')
# plt.show()


# 用网格搜索调整max_depth
# param_grid = {'max_depth':np.arange(1,20)}
# rfc = RandomForestClassifier(n_estimators=90, random_state=5)
# GS = GridSearchCV(rfc, param_grid, cv=10)
# GS.fit(X_train_bag_of_words, data_Y_train)
#
# best_param = GS.best_params_
# best_score = GS.best_score_
# print(best_param, best_score)
#
# param_grid = {'max_features':np.arange(5,31)}
#
# rfc = RandomForestClassifier(n_estimators=90
#                             ,random_state=5
#                             ,max_depth=16)
# GS = GridSearchCV(rfc, param_grid, cv=10)
# GS.fit(X_train_bag_of_words, data_Y_train)
# best_param = GS.best_params_
# best_score = GS.best_score_
# print(best_param, best_score)

#############plot####################

#
# metrics = ('accuracy','precision', 'recall', 'f1-score')  #
# #metrics = ('precision', 'recall', 'f1-score')
#
# # micro = [round(p_mic, num_dec_point), round(r_mic, num_dec_point), round(f1_mic, num_dec_point)]
# # macro = [round(p_mac, num_dec_point), round(r_mac, num_dec_point), round(f1_mac, num_dec_point)]
# # y
#
#
# mirco = np.array([acc_b, micro_b[0], micro_b[1], micro_b[2]])
# marco = np.array([acc_b, macro_b[0], macro_b[1], macro_b[2]])
#
# plt.figure(figsize=(8, 6))
#
# bar_width = 0.35
# index = np.arange(4)
# rects1 = plt.bar(index, mirco, bar_width, color='y', label='micro',alpha=0.5)
# rects2 = plt.bar(index + bar_width, marco, bar_width, color='g', label='macro', alpha=0.5)
# plt.xticks(index + (bar_width/2), metrics)
# plt.ylim(ymax=1.2)
# plt.title('SVM_Micro&Macro_summaries')
# plt.xlabel('metrics')
# plt.ylabel('score')
# plt.legend(loc='upper right', fancybox=True)
#
# def add_data(rects):
#     for rect in rects:
#         height = rect.get_height()
#         plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
#
# add_data(rects1)
# add_data(rects2)
# plt.tight_layout()
# plt.savefig('SVM_Micro&Macro_s.png')
# plt.show()

