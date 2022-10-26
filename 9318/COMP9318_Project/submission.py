import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error

## Read training data
train_file = './data/COVID_train_data.csv'
train_df = pd.read_csv(train_file)

## Read Training labels
train_label_file = './data/COVID_train_labels.csv'
train_labels_df = pd.read_csv(train_label_file)


## Read testing Features
test_fea_file = './data/test_features.csv'
test_features = pd.read_csv(test_fea_file)

## Set hyper-parameters for the SVM Model
svm_model = SVR()
svm_model.set_params(**{'kernel': 'rbf', 'degree': 1, 'C': 5000,
                        'gamma': 'scale', 'coef0': 0.0, 'tol': 0.001, 'epsilon': 10})




## Project-Part1
def predict_COVID_part1(svm_model, train_df, train_labels_df, past_cases_interval, past_weather_interval, test_feature):
    x_train = pd.DataFrame()
    for column in train_df.columns:
        if column == 'day':
            x_train['day'] = train_df.shift(-30)['day']
            continue
        for i in range(30):
            x_train['{}-{}'.format(column, 30 - i)] = train_df.shift(-(i))[column]

    x_train.dropna(inplace=True)
    X = pd.DataFrame()
    features = ['max_temp', 'max_dew', 'max_humid', 'past_cases']
    for feature in features:
        if feature != 'past_cases':
            for i in range(past_weather_interval):
                X['{}-{}'.format(feature, past_weather_interval - i)] = x_train[
                    '{}-{}'.format(feature, past_weather_interval - i)]
        else:
            for i in range(past_cases_interval):
                X['dailly-cases_{}'.format(past_cases_interval - i)] = x_train[
                    'dailly_cases-{}'.format(past_cases_interval - i)]

    y = train_labels_df.iloc[30:, 1]

    X_test = []
    for feature in features:
        if feature != 'past_cases':
            for i in range(past_weather_interval):
                X_test.append(test_feature['{}-{}'.format(feature, past_weather_interval - i)])
        else:
            for i in range(past_cases_interval):
                X_test.append(test_feature['dailly_cases-{}'.format(past_cases_interval - i)])

    svm_model.fit(X, y)

    X_test = np.array(X_test).reshape(1, -1)
    y_pred = int(svm_model.predict(X_test)[0])
    return y_pred


## Project-Part2
def predict_COVID_part2(train_df, train_labels_df, test_feature):
    x_train = pd.DataFrame()
    for column in train_df.columns:
        if column == 'day':
            x_train['day'] = train_df.shift(-30)['day']
            continue
        for i in range(30):
            x_train['{}-{}'.format(column, 30 - i)] = train_df.shift(-(i))[column]
    x_train.dropna(inplace=True)

    # features = [feature for feature in train_df.columns]
    # # print(features)
    # features = features[1:]

    # features = features + ['dailly_cases']
    features = ['max_temp', 'max_dew', 'dailly_cases']


    X = pd.DataFrame()
    for feature in features:
        if feature != 'past_cases':
            for i in range(30):
                X['{}-{}'.format(feature, 30 - i)] = x_train['{}-{}'.format(feature, 30 - i)]
        else:
            for i in range(30):
                X['dailly-cases_{}'.format(30 - i)] = x_train['dailly_cases-{}'.format(30 - i)]
    X = X[60:]
    # print(train_labels_df)
    y = train_labels_df.iloc[89:, 1]
    # print(y)
    y = (y.shift(-1) - y).dropna()
    # print(y)

    model = SVR()
    model.set_params(
        **{'kernel': 'poly', 'degree': 1, 'C': 7e6, 'gamma': 'scale', 'coef0': 0.0, 'tol': 1e-3, 'epsilon': 20})
    model.fit(X, y)

    X_test = []
    for feature in features:
        if feature != 'past_cases':
            for i in range(30):
                X_test.append(test_feature['{}-{}'.format(feature, 30 - i)])
        else:
            for i in range(30):
                X_test.append(test_feature['dailly_cases-{}'.format(30 - i)])

    X_test = np.array(X_test).reshape(1, -1)
    y_pred = model.predict(X_test)
    y_pred = int(test_feature['dailly_cases-1'] + y_pred[0])
    return y_pred

## Generate Prediction Results
predicted_cases_part2 = []
for idx in range(len(test_features)):
    test_feature = test_features.loc[idx]
    prediction = predict_COVID_part2(train_df, train_labels_df, test_feature)
    predicted_cases_part2.append(prediction)

print(predicted_cases_part2)

test_label_file ='./data/COVID_test_labels.csv'
test_labels_df = pd.read_csv(test_label_file)
ground_truth = test_labels_df['dailly_cases'].to_list()


MeanAbsError = mean_absolute_error(predicted_cases_part2, ground_truth)
print('MeanAbsError = ', MeanAbsError)