import csv
import sys
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import *
from sklearn.model_selection import train_test_split


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
    #
    # micro = [round(p_mic, num_dec_point),round(r_mic, num_dec_point), round(f1_mic, num_dec_point)]
    # macro = [round(p_mac, num_dec_point), round(r_mac, num_dec_point), round(f1_mac, num_dec_point)]
    # return a_mic,micro,macro




# read file
data_file = pd.read_csv("summaries.tsv", sep='\t', header=None, quoting=csv.QUOTE_NONE)


# split file into train and test
train, test = train_test_split(data_file, test_size=0.2, random_state=0, shuffle=False)


'''

             preprocessing
1.  replace URL to space
2.  delete invalid symbol (excepted "#@_$% ")
3.  delete one letter word ("a")

'''

def data_progressing(data):

    lis1, lis2, lis3 = [], [], []

    for j in data[1]:
        result = ' '.join(
            [" " if i.lower().startswith("www.") or i.lower().startswith("http") or i.lower().startswith('https') else i for
             i in j.split(" ")])
        lis1.append(result)

    for i in lis1:
        new_text = re.sub('[^\w#@_$% ]', '', i)
        lis2.append(new_text)

    for k in lis2:
        result2 = ' '.join(["" if len(i) <= 1 else i for i in k.split(" ")])
        lis3.append(result2)

    return lis3

train[1] = data_progressing(train)
test[1] = data_progressing(test)
test.to_csv("pretest.csv")

# X: text          y: type
X_train, X_test, y_train, y_test = train[1], test[1], train[2], test[2]

count = CountVectorizer(lowercase=False, max_features=1000)

X_train_bag_of_words = count.fit_transform(X_train)
X_test_bag_of_words = count.transform(X_test)

# with min_samples_leaf 1% = 8
clf_leaf = tree.DecisionTreeClassifier(min_samples_leaf=8, criterion='entropy', random_state=0)
dt_model_leaf = clf_leaf.fit(X_train_bag_of_words, y_train)
predict_and_test(dt_model_leaf, X_test_bag_of_words,y_test)

clf_leaf = tree.DecisionTreeClassifier(min_samples_leaf=1, criterion='entropy', random_state=0)
dt_model_leaf = clf_leaf.fit(X_train_bag_of_words, y_train)
predict_and_test(dt_model_leaf, X_test_bag_of_words,y_test)