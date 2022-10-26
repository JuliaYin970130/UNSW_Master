## import modules here
from math import log, exp
################# Question 1 #################
import pandas as pd

raw_data = pd.read_csv('./asset/data.txt', sep='\t')
raw_data.head()
sms = 'I am not spam'

def tokenize(sms):
    return sms.split(' ')


def get_freq_of_tokens(sms):
    tokens = {}
    for token in tokenize(sms):
        if token not in tokens:
            tokens[token] = 1
        else:
            tokens[token] += 1
    return tokens


training_data = []
for index in range(len(raw_data)):
    training_data.append((get_freq_of_tokens(raw_data.iloc[index].text), raw_data.iloc[index].category))

################# Question 1 #################

def multinomial_nb(training_data, sms):
    All_word_set = set() #所有单词的集合
    for i in training_data:
        for j in i[0].keys():
            All_word_set.add(j)

    total_ham = 0
    total_spam = 0
    for i in training_data:
        if i[1] == 'ham':
            total_ham = total_ham + 1
        if i[1] == 'spam':
            total_spam = total_spam + 1
    Priori_Probability_ham = total_ham / len(training_data)     #先验概率
    Priori_Probability_spam = total_spam / len(training_data)

    #print(Priori_Probability_ham,Priori_Probability_spam)

    sum_ham_number = 0
    sum_spam_number = 0                  #概率的分母
    for i in training_data:
        if i[-1] == 'ham':
            for j in i[0]:
                sum_ham_number = sum_ham_number + i[0][j]
        if i[-1] == 'spam':
            for j in i[0]:
                sum_spam_number = sum_spam_number + i[0][j]

    ham_dict = {}
    spam_dict = {}
    for i in training_data:
        if i[-1] == 'ham':
            for j in All_word_set:
                if j not in i[0].keys():
                    ham_dict[j] = 0
                if j in i[0].keys():
                    if j in ham_dict.keys():
                        ham_dict[j] += i[0][j]
                    if j not in ham_dict.keys():
                        ham_dict[j] = i[0][j]
        if i[-1] == 'spam':
            for j in All_word_set:
                if j not in i[0].keys():
                    spam_dict[j] = 0
                if j in i[0].keys():
                    if j in spam_dict.keys():
                        spam_dict[j] += i[0][j]
                    if j not in spam_dict.keys():
                        spam_dict[j] = i[0][j]

    for key,value in ham_dict.items():
        ham_dict[key] = (value + 1) / (sum_ham_number + len(All_word_set))
    for key,value in spam_dict.items():
        spam_dict[key] = (value + 1) / (sum_spam_number + len(All_word_set))

    spam_result = 1
    ham_result = 1
    for i in sms:
        if i not in All_word_set:
            continue
        else:
            if i in spam_dict.keys():
                spam_result = spam_result * spam_dict[i]
            if i in ham_dict.keys():
                ham_result = ham_result * ham_dict[i]
    spam_result_1 = spam_result * Priori_Probability_spam
    ham_result_1 = ham_result * Priori_Probability_ham
    output = spam_result_1 / ham_result_1
    return output

print(multinomial_nb(training_data, tokenize(sms)))