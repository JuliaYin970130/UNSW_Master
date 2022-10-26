import csv
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
import nltk


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

    micro = [round(p_mic, num_dec_point),round(r_mic, num_dec_point), round(f1_mic, num_dec_point)]
    macro = [round(p_mac, num_dec_point), round(r_mac, num_dec_point), round(f1_mac, num_dec_point)]
    return a_mic,micro,macro




    # print(classification_report(data_Y_test, predicted_y))


def remove_url(content):
    url_http = re.compile('^(https|http)?:\S+', re.S)
    token = url_http.sub(' ', content)
    url_www = re.compile('www.\S+', re.S)
    token = url_www.sub(' ', token)
    return token

def preprocessing(content):
    # remove 'junk' characters
    new_content = remove_url(content)
    result = ''
    good_chars = '#@_$% '
    for i in new_content:
        # remove junk characters
        if i.isalpha() or i.isdigit() or i in good_chars:
            result += i
    ps = PorterStemmer()
    temp = result.split(' ')
    temp_stem = [ps.stem(w) for w in temp ]
    result = ' '.join(temp_stem)
    return result





# read file
data_file = pd.read_csv("articles.tsv", sep='\t', header=None, quoting=csv.QUOTE_NONE)



# split file into train and test
data_train, data_test = train_test_split(data_file, test_size=0.2, random_state=0, shuffle=False)

# split training data and label
data_X_train, data_Y_train = data_train[1], data_train[2]
data_X_test, data_Y_test = data_test[1], data_test[2]



## articles - CountVectorizer
DT_count_vec = CountVectorizer(preprocessor=preprocessing, max_features=1000, lowercase=False,token_pattern='[a-zA-Z0-9@#$%_]{2,}')
X_train_bag_of_words = DT_count_vec.fit_transform(data_X_train)
X_test_bag_of_words = DT_count_vec.transform(data_X_test)
min_samples = round(len(data_X_train) * 0.01)

# articles - a
DT_clf_a = tree.DecisionTreeClassifier(min_samples_leaf=min_samples, criterion='entropy', random_state=0)
DT_model_a = DT_clf_a.fit(X_train_bag_of_words, data_Y_train)
acc_a, micro_a, macro_a = predict_and_test(DT_model_a,X_test_bag_of_words,data_Y_test)


# articles - b
DT_clf_b = tree.DecisionTreeClassifier(min_samples_leaf=1, criterion='entropy', random_state=0)
DT_model_b = DT_clf_b.fit(X_train_bag_of_words, data_Y_train)
acc_b, micro_b, macro_b = predict_and_test(DT_model_b,X_test_bag_of_words,data_Y_test)
#
#
# #DT_articles_pre_b = DT_model_b.predict(X_test_bag_of_words)
# #print(classification_report(data_Y_test, DT_articles_pre_b))
#
#
# ###############plot####################
#
#
# # with/without
# models = ('model a', 'model b')
# # x
# metrics = ('accuracy','precision', 'recall', 'f1-score')  #
# # metrics = ('precision', 'recall', 'f1-score')
# # y
# mirco_a_ = np.array([acc_a, micro_a[0], micro_a[1], micro_a[2]])
# mirco_b_ = np.array([acc_b, micro_b[0], micro_b[1], micro_b[2]])
#
#
# marco_a_ = np.array([macro_a[0], macro_a[1], macro_a[2]])
# marco_b_ = np.array([macro_b[0], macro_b[1], macro_b[2]])
#
# plt.figure(figsize=(8, 6))
#
# bar_width = 0.35
# index = np.arange(4)
# rects1 = plt.bar(index, mirco_a_, bar_width, color='y', label='with stopping criterion',alpha=0.5)
# rects2 = plt.bar(index + bar_width, mirco_b_, bar_width, color='g', label='without stopping criterion', alpha=0.5)
# plt.xticks(index + (bar_width/2), metrics)
# plt.title('DT_Micro_articles')
# plt.xlabel('metrics')
# plt.ylabel('score')
# plt.ylim(ymax=1)
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
# # plt.savefig('DT_Micro_a.png')
# # plt.show()
