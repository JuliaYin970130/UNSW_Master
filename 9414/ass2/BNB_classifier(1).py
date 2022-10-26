# Assignment 2: Topic Classification
# Decision Tree
# Load libraries
import numpy as np
import pandas as pd
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_recall_fscore_support, accuracy_score,classification_report
import csv
import sys

def predict_and_test(model, X_test_bag_of_words, y_test):
    ''' Test and report metrics using the trained model.
    '''
    num_dec_point = 3
    predicted_y = model.predict(X_test_bag_of_words)
    a_mic = accuracy_score(y_test, predicted_y)
    p_mic, r_mic, f1_mic, _ = precision_recall_fscore_support(y_test, 
                        predicted_y,
                        average='micro',
                        warn_for=())
    p_mac, r_mac, f1_mac, _ = precision_recall_fscore_support(y_test, 
                        predicted_y,
                        average='macro',
                        warn_for=())
    print('micro acc,prec,rec,f1: ',round(a_mic,num_dec_point), round(p_mic,num_dec_point), round(r_mic,num_dec_point), round(f1_mic,num_dec_point),sep="\t")
    print('macro prec,rec,f1: ',round(p_mac,num_dec_point), round(r_mac,num_dec_point), round(f1_mac,num_dec_point),sep="\t")
    print('Classification report: ', classification_report(y_test, predicted_y, target_names=['business', 'entertainment', 'politics', 'sport', 'tech']))

def evaluate(file_name):
    ''' Train and test using the training dataset only.
        Do model evaluation.
        Args:
            file_name: The training set input file name.
    '''
    # Load data
    data = pd.read_csv(file_name, sep='\t',
                   header=None, quoting=csv.QUOTE_NONE)
    # data = pd.read_csv('../data/summaries.tsv', sep='\t',
    #                header=None, quoting=csv.QUOTE_NONE)
    X = np.array(data[1])
    y = np.array(data[2])

    # Delete junk words
    good_chars = '#@$% '
    for i in range(X.shape[0]):
        temp = ''
        for c in X[i]:
            if c.isalpha() or c.isdigit() or c in good_chars:
                temp += c
        X[i] = temp

    # 8-2 split for training and testing
    split_point = 800
    X_train = X[:split_point]
    X_test = X[split_point:]
    y_train = y[:split_point]
    y_test = y[split_point:]

    # Create a count vectorizer
    count = CountVectorizer(lowercase=False)
    X_train_bag_of_words = count.fit_transform(X_train)
    X_test_bag_of_words = count.transform(X_test)

    # Create a Naive Bayes model and train it, then test it and report results
    clf = BernoulliNB()
    model = clf.fit(X_train_bag_of_words, y_train)
    predict_and_test(model, X_test_bag_of_words, y_test)

def train_and_predict(file_train, file_test):
    ''' Train and test.
        Do model evaluation.
        Args:
            file_train: The input training set file name.
            file_test: The input testing set file name.
    '''
    # Load data
    data_train = pd.read_csv(file_train, sep='\t',
                   header=None, quoting=csv.QUOTE_NONE)
    data_test = pd.read_csv(file_test, sep='\t',
                   header=None, quoting=csv.QUOTE_NONE)
    X_train = np.array(data_train[1])
    X_test = np.array(data_test[1])
    y_train = np.array(data_train[2])
    y_test = np.array(data_test[2])

    # Delete junk words
    good_chars = '#@$% '
    for i in range(X_train.shape[0]):
        temp = ''
        for c in X_train[i]:
            if c.isalpha() or c.isdigit() or c in good_chars:
                temp += c
        X_train[i] = temp

    for i in range(X_test.shape[0]):
        temp = ''
        for c in X_test[i]:
            if c.isalpha() or c.isdigit() or c in good_chars:
                temp += c
        X_test[i] = temp

    # Create a count vectorizer
    count = CountVectorizer(lowercase=False)
    X_train_bag_of_words = count.fit_transform(X_train)
    X_test_bag_of_words = count.transform(X_test)

    # Create a decision tree model and train it, then test it and report results
    clf = BernoulliNB()
    model = clf.fit(X_train_bag_of_words, y_train)
    predicted_y = model.predict(X_test_bag_of_words)
    for i in range(len(predicted_y)):
        if i != 0:
            print()  # print a new line if not the first line
        print(data_test[0][i], ' ', predicted_y[i], end='')

    # print()
    # print(accuracy_score(y_test, predicted_y))


if __name__ == '__main__':
    evaluation_mode = False

    if evaluation_mode:
        file_name = '../data/articles.tsv'
        print("Naive Bayes model evaluation on the dataset: ", file_name)
        # file_name = '../data/summaries.tsv'
        evaluate(file_name)
    else:
        # Do normal training and prediction, using the provided files
        # check the command line arguments
        if len(sys.argv) != 3:
            print(len(sys.argv))
            print("Wrong number of arguments! Usage: python3 average_ratings.py movie_list.txt movie_ratings.csv output.csv")
            sys.exit()
        # parse the command line arguments
        trainset_filename = sys.argv[1]
        testset_filename = sys.argv[2]
        train_and_predict(trainset_filename, testset_filename)
