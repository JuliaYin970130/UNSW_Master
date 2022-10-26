import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import tree
import csv
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

    # micro = [round(p_mic, num_dec_point),round(r_mic, num_dec_point), round(f1_mic, num_dec_point)]
    # macro = [round(p_mac, num_dec_point), round(r_mac, num_dec_point), round(f1_mac, num_dec_point)]
    # return a_mic,micro,macro

# train = sys.argv[1]
# test = sys.argv[2]


# read file
data_file = pd.read_csv("summaries.tsv", sep='\t', header=None, quoting=csv.QUOTE_NONE)


# split file into train and test
train_data, test_data = train_test_split(data_file, test_size=0.2, random_state=0, shuffle=False)

# train_data = pd.read_csv(train,sep='\t',header=None,quoting=csv.QUOTE_NONE)
# test_data = pd.read_csv(test, sep='\t', header=None,quoting=csv.QUOTE_NONE)
train_data_X = train_data[1]
train_data_Y = train_data[2]
test_data_X = test_data[1]
test_data_Y = test_data[2]


def preprocessing(value):
    text = value.split(' ')
    new_text = []
    for i in text:
        word = re.sub('[^ \w#@$%]','',i)
        url_http = re.compile('^(http[s]?:\S+)', re.S)
        word = url_http.sub(' ', word)
        url_www = re.compile('www.\S+', re.S)
        word = url_www.sub(' ',word)
        new_text.append(word)
    result = ' '.join(new_text)
    return result

min_samples = round(len(train_data_X) / 100)

DT_count = CountVectorizer(preprocessor=preprocessing,max_features=1000,lowercase=False)
X_train_bag_of_words = DT_count.fit_transform(train_data_X)
X_test_bag_of_words = DT_count.transform(test_data_X)

Decision_Tree = tree.DecisionTreeClassifier(min_samples_leaf=min_samples,criterion='entropy',random_state=0)
DT = Decision_Tree.fit(X_train_bag_of_words,train_data_Y)
predict_and_test(DT,X_test_bag_of_words,test_data_Y)

DT_clf_b = tree.DecisionTreeClassifier(min_samples_leaf=1, criterion='entropy', random_state=0)
DT_model_b = DT_clf_b.fit(X_train_bag_of_words, train_data_Y)
predict_and_test(DT_model_b,X_test_bag_of_words,test_data_Y)
