import csv
import re
import pandas as pd
import sys
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer



def remove_url(content):
    url_http = re.compile('^(https|http)?:\S+', re.S)
    token = url_http.sub(' ', content)
    url_www = re.compile('www.\S+', re.S)
    token = url_www.sub(' ', token)
    return token

def preprocessing(content):
    # remove url
    new_content = remove_url(content)
    result = ''
    good_chars = '#@_$% '
    for i in new_content:
        # remove junk characters
        if i.isalpha() or i.isdigit() or i in good_chars:
            result += i

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
X_train, Y_train = data_train[1], data_train[2]
X_test, Y_test = data_test[1], data_test[2]


# CountVectorizer
# word is a string of at least two letters, numbers or symbols #@_$%
DT_CountVec = CountVectorizer(max_features=1000, lowercase=False,token_pattern='[a-zA-Z0-9@#$%_]{2,}')
X_train_bag_of_words = DT_CountVec.fit_transform(X_train)
X_test_bag_of_words = DT_CountVec.transform(X_test)



# Decision Tree model
# with 1% stopping criterion
min_samples = round(len(X_train) / 100)
DT_clf = tree.DecisionTreeClassifier(min_samples_leaf=min_samples, criterion='entropy', random_state=0)
DT_model = DT_clf.fit(X_train_bag_of_words, Y_train)
y_pred = DT_model.predict(X_test_bag_of_words)

# print output
for i in range(len(y_pred)-1):
    print(data_test.iloc[i][0], y_pred[i])
print(data_test.iloc[len(y_pred)-1][0], y_pred[len(y_pred)-1], end='')

