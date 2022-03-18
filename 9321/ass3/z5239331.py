import json
import sys

import pandas as pd
from scipy.stats import pearsonr
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.metrics import mean_squared_error, precision_score, recall_score, accuracy_score


def runtime_(data):
    if data <= 70:
        return 1
    elif data >= 71 and data <= 100:
        return 2
    elif data >= 101 and data <= 140:
        return 3
    elif data >= 141 and data <= 180:
        return 4
    elif data >= 181:
        return 5


def columns_name(data):
    json_test = json.loads(data)
    res = []
    for i in range(len(json_test)):
        temp = json_test[i]
        res.append(temp['name'])
    return ','.join(res)


def pd_countries(data):
    json_ = json.loads(data)
    if json_:
        if json_[0]['name'] != 'United States of America':
            return 1
        else:
            return 2
    else:
        return 1


def spoken_languages(data):
    json_text = json.loads(data)
    language_set = set()
    for i in json_text:
        if i['name'] not in language_set:
            language_set.add(i['name'])
    return len(language_set)


def count_(data):
    return len(json.loads(data))


def keywords_(data):
    json_test = json.loads(data)
    length = len(json_test)
    if length <= 5:
        return 1
    elif length >= 6 and length <= 10:
        return 2
    elif length >= 11 and length <= 15:
        return 3
    elif length >= 16:
        return 4


def cast_companies_(data, cast_list):
    json_text = json.loads(data)
    list_ = []
    for i in json_text:
        list_.append(i['name'])
    count = 0
    for e in cast_list:
        if e in list_:
            count += 1
    return count


def crew_(data, crew_list):
    json_text = json.loads(data)
    list_ = []
    for i in json_text:
        if i['job'] == 'Director':
            list_.append(i['name'])
    count = 0
    for e in crew_list:
        if e in list_:
            count += 1
    return count


def clean(train):
    df = train.copy()
    length = df.shape[0]
    # print(df)

    #################### cast,crew,production_companies top_10 #########################
    # cast list
    cast_dict = {}
    for i in train['cast']:
        json_text = json.loads(i)
        for j in json_text:
            if j['name'] not in cast_dict.keys():
                cast_dict[j['name']] = 1
            else:
                cast_dict[j['name']] += 1
    cast_list = sorted(cast_dict.items(), key=lambda x: x[1], reverse=True)
    cast_ = [i[0] for i in cast_list[:10]]
    # print(cast_)
    for cast in cast_:
        df[cast] = 0
    for i in range(length):
        name = []
        json_text = json.loads(df.loc[i, 'cast'])
        for j in json_text:
            name.append(j['name'])
        for cast in cast_:
            if cast in name:
                df.loc[i, cast] = 1
    # crew list
    crew_dict = {}
    for i in train.crew:
        json_text = json.loads(i)
        for j in json_text:
            # print(j)
            if j['job'] == 'Director':
                if j['name'] not in crew_dict.keys():
                    crew_dict[j['name']] = 1
                else:
                    crew_dict[j['name']] += 1

    crew_list = sorted(crew_dict.items(), key=lambda x: x[1], reverse=True)
    Director_ = [i[0] for i in crew_list[:10]]

    for director in Director_:
        df[director] = 0
    for i in range(length):
        director_name = []
        json_text = json.loads(df.loc[i, 'crew'])
        for j in json_text:
            # print(j)
            if j['job'] == 'Director':
                director_name.append(j['name'])
        for director in Director_:
            if director in director_name:
                df.loc[i, director] = 1

    # production_companies
    companies_dict = {}
    for i in train.production_companies:
        json_text = json.loads(i)
        for j in json_text:
            if j['name'] not in companies_dict.keys():
                companies_dict[j['name']] = 1
            else:
                companies_dict[j['name']] += 1
    companies_list = sorted(companies_dict.items(), key=lambda x: x[1], reverse=True)
    companies_ = [i[0] for i in companies_list[:10]]

    # genres
    # genres_dict = {}
    # for i in train.genres:
    #     json_text = json.loads(i)
    #     for j in json_text:
    #         if j['name'] not in genres_dict.keys():
    #             genres_dict[j['name']] = 1
    #         else:
    #             genres_dict[j['name']] += 1
    # genres_list = sorted(genres_dict.items(), key=lambda x: x[1], reverse=True)
    # genres_ = [i[0] for i in genres_list]

    ##################################################################
    # original_language
    result = []
    for i in df.original_language:
        if i == 'en':
            result.append(2)
        else:
            result.append(1)
    df['original_language'] = result

    for i in range(length):
        month = df.loc[i, 'release_date']
        # print(i[5:7])
        if month[5:7] in ['01', '02', '03']:
            df.loc[i, 'release_date'] = 1
        elif month[5:7] in ['04', '05', '06']:
            df.loc[i, 'release_date'] = 2
        elif month[5:7] in ['07', '08', '09']:
            df.loc[i, 'release_date'] = 3
        elif month[5:7] in ['10', '11', '12']:
            df.loc[i, 'release_date'] = 4
    # print(df['release_date'])

    ########################## df  ##############################
    df['cast'] = df['cast'].apply(cast_companies_, args=(cast_,))
    df['crew'] = df['crew'].apply(crew_, args=(Director_,))
    df['production_companies'] = df['production_companies'].apply(cast_companies_, args=(companies_,))
    # df['n_genres'] = df['genres'].apply(cast_companies_,args=(genres_,))

    # production_countries
    df['production_countries'] = df['production_countries'].apply(pd_countries)
    df['spoken_languages'] = df['spoken_languages'].apply(spoken_languages)
    # df['n_cast'] = train['cast'].apply(count_)
    # df['n_crew'] = train['crew'].apply(count_)
    # df['n_genres'] = train['genres'].apply(count_)
    # homepage 主页
    df['homepage'] = df['homepage'].apply(lambda x: 1 if (x != x) else 2)
    df['tagline'] = df['tagline'].apply(lambda x: 1 if (x != x) else 2)

    df['keywords'] = df['keywords'].apply(keywords_)
    # result_run = []
    # for i in df['runtime']:
    #     result_run.append(i)
    # max_ = min(result_run)
    # print(max_)
    # max = 338 / 216
    # min = 63 / 69
    df['runtime'] = df['runtime'].apply(runtime_)
    df['genres'] = df['genres'].apply(columns_name)
    df = pd.concat([df, df['genres'].str.get_dummies(sep=",")], axis=1)
    # print(df)

    drop_col = ['revenue', 'movie_id', 'original_title', 'overview', 'status','genres']
    df = df.drop(drop_col, axis=1)
    return df


if __name__ == '__main__':
    raw_train = pd.read_csv(sys.argv[1])
    raw_test = pd.read_csv(sys.argv[2])
    # raw_train = pd.read_csv('training.csv')
    # raw_test = pd.read_csv('validation.csv')
    df_train = clean(raw_train)
    df_test = clean(raw_test)

    ########################## Regression #############################
    # df_train.to_csv('test.csv', index=False)
    # drop 'rating'
    x_train = df_train.drop('rating', axis=1).values
    # print(x_train.shape)
    y_train_r = raw_train['revenue'].values
    # print(y_train_r.shape)
    x_test = df_test.drop('rating', axis=1).values
    # print(x_test.shape)
    y_test_r = raw_test['revenue'].values

    movie_id = raw_test['movie_id'].values

    # Random Forest
    # LR_model = LinearRegression()
    RFR_model = RandomForestRegressor(n_estimators=100, random_state=3)
    RFR_model.fit(x_train, y_train_r)
    y_pred_r = RFR_model.predict(x_test)

    MSR = mean_squared_error(y_test_r, y_pred_r)
    correlation = pearsonr(y_test_r, y_pred_r)
    # print(correlation[0])

    zid = 'z5239331'

    df1 = pd.DataFrame({'movie_id': movie_id, 'predicted_revenue': y_pred_r},
                       columns=['movie_id', 'predicted_revenue'])
    df1.to_csv(zid + '.PART1.output.csv', index=False)

    df2 = pd.DataFrame([[zid, round(MSR, 2), round(correlation[0], 2)]], columns=['zid', 'MSR', 'correlation'])
    df2.to_csv(zid + '.PART1.summary.csv', index=False)

    ########################## Classification ##########################

    # revenue 不能用

    y_train_rating = df_train['rating'].values
    y_test_rating = df_test['rating'].values

    x_train = df_train.drop('rating', axis=1).values
    x_test = df_test.drop('rating', axis=1).values

    # GradientBoostingClassifier
    GB_classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=0.08)
    GB_classifier.fit(x_train, y_train_rating)
    y_pred_rating = GB_classifier.predict(x_test)
    # y_predicted_rating = np.array(y_predicted_rating, dtype=np.int_)

    average_precision = precision_score(y_true=y_test_rating, y_pred=y_pred_rating, average='macro')
    average_recall = recall_score(y_true=y_test_rating, y_pred=y_pred_rating, average='macro')
    accuracy = accuracy_score(y_true=y_test_rating, y_pred=y_pred_rating)

    df3 = pd.DataFrame({'movie_id': movie_id, 'predicted_rating': y_pred_rating},
                       columns=['movie_id', 'predicted_rating'])
    df3.to_csv(zid + '.PART2.output.csv', index=False)

    df4 = pd.DataFrame([[zid, round(average_precision, 2), round(average_recall, 2), round(accuracy, 2)]],
                       columns=['zid', 'average_precision', 'average_recall', 'accuracy'])
    df4.to_csv(zid + '.PART2.summary.csv', index=False)
