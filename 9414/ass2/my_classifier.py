import csv
import re
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer, HashingVectorizer
from sklearn.metrics import *
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import sys


def remove_url(content):
    url_http = re.compile('^(https|http)?:\S+', re.S)
    token = url_http.sub(' ', content)
    url_www = re.compile('www.\S+', re.S)
    token = url_www.sub(' ', token)
    return token

# preprocessing data
def preprocessing(content):
    # remove url
    new_content = remove_url(content)
    result = ''
    good_chars = '#@_$% '
    for i in new_content:
        # remove 'junk' characters
        if i.isalpha() or i.isdigit() or i in good_chars:
            result += i
    temp = result.split(' ')
    ps = PorterStemmer()
    temp_stem = [ps.stem(w) for w in temp]
    result = ' '.join(temp_stem)
    return result


# read file
data_path = sys.argv[1]
test_path = sys.argv[2]


# training dataframe
data_train_ = pd.read_csv(data_path, sep='\t', header=None, quoting=csv.QUOTE_NONE)
# test dataframe
data_test_ = pd.read_csv(test_path, sep='\t', header=None, quoting=csv.QUOTE_NONE)

data_train = data_train_.copy()
data_test = data_test_.copy()

data_train[1] = data_train_[1].apply(lambda x:preprocessing(x))
data_test[1] = data_test_[1].apply(lambda x:preprocessing(x))

# split training data and label
data_X_train, data_Y_train = data_train[1], data_train[2]
data_X_test, data_Y_test = data_test[1], data_test[2]


## HashingVectorizer  - too slow
## TfidfVectorizer
count_vec = TfidfVectorizer(max_features=4000, token_pattern='[a-zA-Z0-9@#$%_]{2,}')
X_train_bag_of_words = count_vec.fit_transform(data_X_train)
X_test_bag_of_words = count_vec.transform(data_X_test)

# GradientBoostingClassifier - 0.905
# KNeighborsClassifier - 0.67
# clf = RandomForestClassifier(n_estimators=90,random_state=5) # 0.91 -> 0.935 -> 0.955 -> 0.96
clf = SVC() # 0.985
clf.fit(X_train_bag_of_words, data_Y_train)
y_pred = clf.predict(X_test_bag_of_words)

# print output
for i in range(len(y_pred)-1):
    print(data_test.iloc[i][0], y_pred[i])
print(data_test.iloc[len(y_pred)-1][0], y_pred[len(y_pred)-1], end='')


# score = cross_val_score(clf, X_train_bag_of_words, data_Y_train, cv=10).mean()
# print(score)
