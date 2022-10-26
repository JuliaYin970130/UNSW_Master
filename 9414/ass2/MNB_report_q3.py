import csv
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import *
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import  MultinomialNB
from nltk.stem import PorterStemmer


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


def preprocessing(content):
    # remove 'junk' characters
    tokens = content.split(' ')
    new_text = []
    for i in tokens:
        token = re.sub('[^ a-zA-Z0-9@#$%_]','',i)
        # remove URL
        url_http = re.compile('^(https|http)?:\S+', re.S)
        token = url_http.sub(' ', token)
        url_www = re.compile('www.\S+', re.S)
        token = url_www.sub(' ',token)
        new_text.append(token)

    # print(new_text)
    # print()

    # result = ''
    result = ' '.join(new_text)


    return result

def preprocessing_2(content):
    # remove 'junk' characters
    tokens = content.split(' ')
    new_text = []
    for i in tokens:
        # # remove URL
        url_http = re.compile('^(http[s])?:\S+', re.S)
        token = url_http.sub(' ', i)
        url_www = re.compile('www.\S+', re.S)
        token = url_www.sub(' ',token)
        token = re.sub('[^ a-zA-Z0-9@#$%_]','',token)
        new_text.append(token)

    ps = PorterStemmer()
    token_words = [ps.stem(w) for w in new_text]

    result = ' '.join(token_words)
    # print(result)
    return result


# read file
data_file = pd.read_csv("articles.tsv", sep='\t', header=None, quoting=csv.QUOTE_NONE)


# split file into train and test
data_train, data_test = train_test_split(data_file, test_size=0.2, random_state=0, shuffle=False)


# split training data and label
data_X_train, data_Y_train = data_train[1], data_train[2]
data_X_test, data_Y_test = data_test[1], data_test[2]


## articles - a
MNB_count_vec_a = CountVectorizer(preprocessor=preprocessing, lowercase=False,token_pattern='[\w#_@$%]{2,}')
X_train_bag_of_words_a = MNB_count_vec_a.fit_transform(data_X_train)
X_test_bag_of_words_a = MNB_count_vec_a.transform(data_X_test)

MNB_clf = MultinomialNB()
MNB_model_a = MNB_clf.fit(X_train_bag_of_words_a, data_Y_train)
acc_a, micro_a, macro_a = predict_and_test(MNB_model_a,X_test_bag_of_words_a,data_Y_test)


# articles - b
MNB_count_vec_b = CountVectorizer(preprocessor=preprocessing_2, stop_words='english', lowercase=False,token_pattern='[\w#_@$%]{2,}')
X_train_bag_of_words_b = MNB_count_vec_b.fit_transform(data_X_train)
X_test_bag_of_words_b = MNB_count_vec_b.transform(data_X_test)


MNB_clf = MultinomialNB()
MNB_model_b = MNB_clf.fit(X_train_bag_of_words_b, data_Y_train)
acc_b, micro_b, macro_b = predict_and_test(MNB_model_b,X_test_bag_of_words_b,data_Y_test)

score = cross_val_score(MNB_model_b, X_train_bag_of_words_b, data_Y_train, cv=10).mean()
print(score)


###############plot####################

metrics = ('precision', 'recall', 'f1-score')
# y

marco_a_ = np.array([macro_a[0], macro_a[1], macro_a[2]])
marco_b_ = np.array([macro_b[0], macro_b[1], macro_b[2]])

bar_width = 0.35
plt.figure(figsize=(8, 6))

index = np.arange(3)
rects1 = plt.bar(index, marco_a_, bar_width, color='y', label='standard model',alpha = 0.5)
rects2 = plt.bar(index + bar_width, marco_b_, bar_width, color='g', label='additional model',alpha = 0.5)

plt.xticks(index + (bar_width/2), metrics)
plt.ylim(ymax=1.2)
#plt.title('MNB_Marco_articles')
plt.title('MNB_Macro_summaries')
plt.xlabel('metrics')
plt.ylabel('score')
plt.legend(loc='upper right', fancybox=True)

def add_data(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')

add_data(rects1)
add_data(rects2)
plt.tight_layout()
plt.savefig('MNB_Macro_s.png')
plt.show()


###############micro#############
# with/without
# models = ('model a', 'model b')
# x
metrics = ('accuracy','precision', 'recall', 'f1-score')  #
#metrics = ('precision', 'recall', 'f1-score')
# y
mirco_a_ = np.array([acc_a, micro_a[0], micro_a[1], micro_a[2]])
mirco_b_ = np.array([acc_b, micro_b[0], micro_b[1], micro_b[2]])


bar_width = 0.35
plt.figure(figsize=(8, 6))

index = np.arange(4)
rects1 = plt.bar(index, mirco_a_, bar_width, color='y', label='standard model',alpha = 0.5)
rects2 = plt.bar(index + bar_width, mirco_b_, bar_width, color='g', label='additional model',alpha = 0.5)

plt.xticks(index + (bar_width/2), metrics)
plt.ylim(ymax=1.2)
#plt.title('MNB_Mirco_articles')
plt.title('MNB_Micro_summaries')
plt.xlabel('metrics')
plt.ylabel('score')
plt.legend(loc='upper right', fancybox=True)

def add_data(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')

add_data(rects1)
add_data(rects2)
plt.tight_layout()
plt.savefig('MNB_Micro_s.png')
plt.show()