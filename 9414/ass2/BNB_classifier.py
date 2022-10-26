import csv
import re
import pandas as pd
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB


def preprocessing(content):
    tokens = content.split(' ')
    new_text = []
    for i in tokens:
        # remove 'junk' characters
        token = re.sub('[^ a-zA-Z0-9@#$%_]', '', i)
        # remove URL
        url_http = re.compile('^(https|http)?:\S+', re.S)
        token = url_http.sub(' ', token)
        url_www = re.compile('www.\S+', re.S)
        token = url_www.sub(' ', token)
        new_text.append(token)

    result = ' '.join(new_text)

    return result


# read file
data_path = sys.argv[1]
test_path = sys.argv[2]

# training dataframe
data_train = pd.read_csv(data_path, sep='\t', header=None, quoting=csv.QUOTE_NONE)
# test dataframe
data_test = pd.read_csv(test_path, sep='\t', header=None, quoting=csv.QUOTE_NONE)

# split training data and label
data_X_train, data_Y_train = data_train[1], data_train[2]
data_X_test, data_Y_test = data_test[1], data_test[2]


# CountVectorizer
# word is a string of at least two letters, numbers or symbols #@_$%
BNB_CountVec = CountVectorizer(preprocessor=preprocessing, lowercase=False,token_pattern='[a-zA-Z0-9@#$%_]{2,}')
X_train_bag_of_words = BNB_CountVec.fit_transform(data_X_train)
X_test_bag_of_words = BNB_CountVec.transform(data_X_test)


# Bernoulli Naive Bayes
BNB_clf = BernoulliNB()
BNB_clf.fit(X_train_bag_of_words, data_Y_train)
y_pred = BNB_clf.predict(X_test_bag_of_words)


# print output
for i in range(len(y_pred)-1):
    print(data_test.iloc[i][0], y_pred[i])
print(data_test.iloc[len(y_pred)-1][0], y_pred[len(y_pred)-1], end='')

