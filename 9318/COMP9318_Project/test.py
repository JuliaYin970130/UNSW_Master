import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
import math
## Parameters settings
past_cases_interval = 10
past_weather_interval = 10


## Read training data
train_file = './data/COVID_train_data.csv'
train_df = pd.read_csv(train_file)
# 192 * 18
#print(train_df.shape)


## Read Training labels
train_label_file = './data/COVID_train_labels.csv'
train_labels_df = pd.read_csv(train_label_file)


## Read testing Features
# 里面是30天的数据
test_fea_file = './data/test_features.csv'
test_features = pd.read_csv(test_fea_file)
# 20*511 510 = 17 * 30 除去index那一列
#print(test_features.shape)


## Set hyper-parameters for the SVM Model
svm_model = SVR()
svm_model.set_params(**{'kernel': 'rbf', 'degree': 1, 'C': 5000,
                        'gamma': 'scale', 'coef0': 0.0, 'tol': 0.001, 'epsilon': 10})

def process_train(train_df,past_cases_interval):
    x_df = train_df.copy()
    x_df['day'] = train_df.shift(-30)['day']
    x_df.dropna(inplace=True)
    # print(x_df)
    #x_df = x_df[['max_temp', 'max_dew', 'max_humid', 'dailly_cases']]
    index_ = ['max_temp', 'max_dew', 'max_humid', 'dailly_cases']
    # n = 30
    # index_list = x_df.index.to_list()
    # print(index_list)
    # x_df = x_df.head(past_cases_interval)
    #print(train_labels_df.head(10))
    X = pd.DataFrame()
    for feature in index_:
        if feature != 'past_cases':
            for i in range(past_weather_interval):
                X['{}-{}'.format(feature, past_weather_interval - i)] = x_df[
                    '{}-{}'.format(feature, past_weather_interval - i)]
        else:
            for i in range(past_cases_interval):
                X['dailly-cases_{}'.format(past_cases_interval - i)] = x_df[
                    'dailly_cases-{}'.format(past_cases_interval - i)]

    # for col in index_:
    #     for i in range(0, past_cases_interval):
    #         new_col = col + '-' + str(i + 1)
    #         # print(new_col)
    #         x_df[new_col] = x_df[col]
    # x_df = x_df.drop(index_, axis=1)

    # x_df = x_df.iloc[30:, :]
    #print(x_df.head(1))
    #x_df = x_df.head(1)

    #y_df = train_labels_df.head(10)
    #x_df['y'] = y_df['dailly_cases']
    #x_df = x_df.T
    # print(x_df)
    return X

def process_test(df_test,past_cases_interval):
    x_test = df_test.copy()

    #print(index_list)
    index_ = ['max_temp', 'max_dew', 'max_humid', 'dailly_cases']
    #x_test_['max_temp'] = x_test[result_list]

    result_list =[]
    for i in index_:
        col_ = i
        for j in range(past_cases_interval):
            col_ = col_ + '-' + str(j+1)
            result_list.append(col_)
            col_ = i
    x_test = x_test[result_list]



    return x_test



## Project-Part1
def predict_COVID_part1(svm_model, train_df, train_labels_df, past_cases_interval, past_weather_interval, test_feature):
    x_train = process_train(train_df, past_cases_interval)
    x_train = x_train.values
    print(x_train.shape)
    y_train_label = train_labels_df.iloc[30:, 1]
    y_train_label.dropna(inplace=True)
    y_train_label = y_train_label.values
    print(y_train_label)
    # 要记得限制天数
    # print(test_feature)
    x_test = process_test(test_feature,past_cases_interval)
    x_test = np.array(x_test).reshape(1, -1)
    print(x_test.shape)

    svm_model.fit(x_train, y_train_label)
    y_predicted = svm_model.predict(x_test)


    return math.floor(y_predicted)
    #pass ## Replace this line with your implementation



## Project-Part2
def predict_COVID_part2(train_df, train_labels_df, test_feature):
    pass ## Replace this line with your implementation



## Generate Prediction Results
predicted_cases_part1 = []
# 20条
for idx in range(len(test_features)):
    # idx从193开始
    test_feature = test_features.loc[idx]
    prediction = predict_COVID_part1(svm_model, train_df, train_labels_df,past_cases_interval, past_weather_interval, test_feature)
    predicted_cases_part1.append(prediction)



print(predicted_cases_part1)

## MeanAbsoluteError Computation...!

test_label_file ='./data/COVID_test_labels.csv'
test_labels_df = pd.read_csv(test_label_file)
ground_truth = test_labels_df['dailly_cases'].to_list()


MeanAbsError = mean_absolute_error(predicted_cases_part1, ground_truth)
print('MeanAbsError = ', MeanAbsError)
