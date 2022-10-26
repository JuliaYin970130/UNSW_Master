import pandas as pd

raw_data = pd.read_csv('./asset/data.txt', sep='\t')
raw_data.head()

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

sms = 'I am not spam'
################# Question 1 #################

def multinomial_nb(training_data, sms):# do not change the heading of the function
    #smooth = 1
    total_dict = {}
    ham_dict = {}
    spam_dict = {}
    ham_sum = 0
    spam_sum = 0
    ham_count,ham_prior = 0,0
    spam_count,spam_prior = 0,0
    #count = 0
    for dict_ in training_data:
        for word in dict_[0].keys():
            if word not in total_dict.keys():
                #count += 1
                total_dict[word] = dict_[0][word]
            else:
                total_dict[word] += dict_[0][word]

    for word_dict in training_data:
        #print(word_dict)
        #print(word_dict[0])
        #print()
        if word_dict[1] == 'ham':
            ham_count += 1
            for word in word_dict[0].keys():
                ham_sum += word_dict[0][word]
                if word not in ham_dict.keys():
                    ham_dict[word] = word_dict[0][word]
                else:
                    ham_dict[word] += word_dict[0][word]

        if word_dict[1] == 'spam':
            spam_count += 1
            for word in word_dict[0].keys():
                spam_sum += word_dict[0][word]
                if word not in spam_dict.keys():
                    spam_dict[word] = word_dict[0][word]
                else:
                    spam_dict[word] += word_dict[0][word]

    #print(ham_dict)
    #print(spam_dict)
    for key in ham_dict:
        ham_dict[key] = (ham_dict[key] + 1) / (ham_sum + len(total_dict))

    for key in spam_dict:
        spam_dict[key] = (spam_dict[key] + 1) / (spam_sum + len(total_dict))

    #print(spam_dict)
    #spam:60, ham: 50
    #print(spam_sum + len(total_dict), ham_sum + len(total_dict))
    #print(ham_dict['I'])
    #print(spam_dict['I'])
    ham_prior = ham_count / len(training_data)
    spam_prior = spam_count / len(training_data)
    #print(ham_prior)
    #print(spam_prior)


    for i in sms:
        #print(i)
        if i in total_dict.keys():
            if i in ham_dict.keys():
                #print(ham_dict[i])
                #print()
                ham_prior *= ham_dict[i]
            else:
                ham_prior *= 1/(ham_sum + len(total_dict))

            if i in spam_dict.keys():
                spam_prior *= spam_dict[i]
            else:
                spam_prior *= 1/(spam_sum + len(total_dict))

    result = spam_prior / ham_prior
    print(result)
    return result
multinomial_nb(training_data, tokenize(sms))