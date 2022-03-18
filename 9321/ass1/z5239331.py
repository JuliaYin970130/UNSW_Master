import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math
import datetime


studentid = os.path.basename(sys.modules[__name__].__file__)


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


def question_1(exposure, countries):
    """
    :param exposure: the path for the exposure.csv file
    :param countries: the path for the Countries.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...

    df_exposure = pd.read_csv(exposure, sep=';', encoding='ISO-8859-1')
    df_country = pd.read_csv(countries)
    #print(df_exposure['Income classification according to WB'])
    df_exposure.columns = map(str.capitalize, df_exposure.columns)

    df_exposure['Country'] = df_exposure['Country'].replace({'United States of America': 'United States',
                                                             'Korea Republic of': 'South Korea',
                                                             'Korea DPR': 'North Korea',
                                                             'Viet Nam': 'Vietnam',
                                                             'Cabo Verde': 'Cape Verde',
                                                             'Brunei Darussalam': 'Brunei',
                                                             'Lao PDR': 'Laos',
                                                             'North Macedonia': 'Macedonia',
                                                             'Moldova Republic of': 'Moldova',
                                                             'Russian Federation': 'Russia',
                                                             'Eswatini': 'Swaziland',
                                                             "Côte d'Ivoire": 'Ivory Coast',
                                                             'Congo': 'Republic of the Congo',
                                                             'Congo DR': 'Democratic Republic of the Congo',
                                                             'Palestine': 'Palestinian Territory'
                                                             })
    # df_exposure['Country'] = df_exposure['Country'].map({'Unite State of America': 'USA'})
    # print(df_exposure)
    df_result = pd.merge(df_exposure, df_country, on='Country', how='inner')
    df_result = df_result[df_result.Country.notna()]
    df_result = df_result.set_index(["Country"])
    df1 = df_result.sort_index()

    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def q_split(df):
    return df.split("|||")

def q_json_avg_latitude(df):
    count_index = 0
    count = 0
    for i in df:
        count += 1
        json_disk = json.loads(i)
        #print(json_disk)
        latitude = json_disk['Latitude']
        count_index += latitude
    return count_index / count

def q_json_avg_longitude(df):
    count_index = 0
    count = 0
    for i in df:
        count += 1
        json_disk = json.loads(i)
        #print(json_disk)
        longitude = json_disk['Longitude']
        count_index += longitude
    return count_index / count


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df_result = df1.copy()
    df_result['Cities'] = df_result['Cities'].apply(lambda x:q_split(x))
    #print(df2['Cities'])
    df2 = df1.copy()
    df2['avg_latitude'] = df_result['Cities'].apply(lambda x:q_json_avg_latitude(x))
    #print(df2['avg_latitude'])
    df2['avg_longitude'] = df_result['Cities'].apply(lambda x: q_json_avg_longitude(x))
    #print(df_result)
    #return df2
    #################################################

    log("QUESTION 2", output_df=df2[["avg_latitude", "avg_longitude"]], other=df2.shape)
    return df2

def deg2rad(deg):
    return float(deg) * math.pi / 180.0
def q3_(avg_latitude, avg_longitude):
    lon1 = 114.3055
    lat1 = 30.5928
    lon1,lat1,lon2,lat2 = map(deg2rad,[float(lon1),float(lat1),float(avg_longitude),float(avg_latitude)])
    dLat = lat2-lat1
    dLon = lon2-lon1
    C = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(lat1) * \
        np.cos(lat2) * np.sin(dLon / 2) * np.sin(dLon / 2)
    R = 6373
    d = 2 * np.arcsin(np.sqrt(C))

    return d * R

def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df3 = df2.copy()
    df3['distance_to_Wuhan'] = df3.apply(lambda x: q3_(x['avg_latitude'],x['avg_longitude']),axis=1)
    df3 = df3.sort_values(by='distance_to_Wuhan')
    #################################################

    log("QUESTION 3", output_df=df3[['distance_to_Wuhan']], other=df3.shape)
    return df3


def question_4(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df_temp = df2.copy()
    df_continents = pd.read_csv(continents)
    df_temp = df_temp.reset_index(drop=False)
    # print(df_continents[(df_continents['Country'] == 'Congo, Democratic Republic of')])
    df_continents['Country'] = df_continents['Country'].replace({'Korea, North': 'North Korea',
                                                                 'Korea, South': 'South Korea',
                                                                 'US': 'United States',
                                                                 'Russian Federation': 'Russia',
                                                                 'Congo': 'Republic of the Congo',
                                                                 'Congo, Democratic Republic of': 'Democratic Republic of the Congo'
                                                                 })
    df_result = pd.merge(df_temp, df_continents, on='Country', how='inner')

    # print(df_result)
    df_result = df_result.loc[df_result['Covid_19_economic_exposure_index'] != 'x']
    df_result = df_result.loc[df_result['Covid_19_economic_exposure_index'] != 'No data']

    df_result = df_result.set_index(['Country'])

    df_result['Covid_19_economic_exposure_index'] = df_result['Covid_19_economic_exposure_index'].str.replace(",", '.')
    df_result['Covid_19_economic_exposure_index'] = df_result['Covid_19_economic_exposure_index'].astype(float)

    grouped_df = df_result.groupby('Continent')['Covid_19_economic_exposure_index']
    mean_df = grouped_df.mean()

    df4 = mean_df.reset_index(drop=False)
    df4 = df4.rename(columns={'Covid_19_economic_exposure_index': 'average_covid_19_Economic_exposure_index'})
    df4 = df4.sort_values(by='average_covid_19_Economic_exposure_index', ascending=True)
    df4 = df4.set_index(["Continent"])

    #################################################

    log("QUESTION 4", output_df=df4, other=df4.shape)
    return df4


def question_5(df2):
    """
    :param df2: the dataframe created in question 2
    :return: cities_lst
            Data Type: list
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    # Your code goes here ...
    df5 = df2.copy()
    #print(df5['Net_oda_received_perc_of_gni'])
    #print(df5[(df5['Net_oda_received_perc_of_gni'] == 'No data')])

    df5 = df5.loc[df5['Foreign direct investment'] != 'x']
    df5 = df5.loc[df5['Net_oda_received_perc_of_gni'] != 'x']
    df5 = df5.loc[df5['Net_oda_received_perc_of_gni'] != 'No data']
    df5 = df5.loc[df5['Foreign direct investment'] != 'No data']

    #print(df5[(df5['Income classification according to wb'] == 'MIC')])

    df5['Foreign direct investment'] = df5['Foreign direct investment'].str.replace(",", '.')
    df5['Net_oda_received_perc_of_gni'] =df5['Net_oda_received_perc_of_gni'].str.replace(",",'.')

    df5['Foreign direct investment'] = df5['Foreign direct investment'].astype(float)
    df5['Net_oda_received_perc_of_gni'] = df5['Net_oda_received_perc_of_gni'].astype(float)

    grouped_df = df5.groupby('Income classification according to wb')[['Foreign direct investment', 'Net_oda_received_perc_of_gni']]
    mean_df = grouped_df.mean()

    df5 = mean_df.reset_index(drop=False)
    #print(df5)
    df5 = df5.rename(columns={'Foreign direct investment': 'Avg Foreign direct investment',
                              'Net_oda_received_perc_of_gni': 'Avg_ Net_ODA_received_perc_of_GNI ',
                              'Income classification according to wb':'Income Class'
                              })
    #df5 = df5.sort_values(by='average_covid_19_Economic_exposure_index',ascending=True)
    df5 = df5.set_index(["Income Class"])

    #################################################

    log("QUESTION 5", output_df=df5, other=df5.shape)
    return df5

def q6_city(cities,population):
    for i in cities:
        json_text = json.loads(i)
        if json_text['Population'] == population:
            return json_text['City']

def q6_population(df):
    population_dict = []
    for i in df:
        json_text = json.loads(i)
        if json_text['Population'] != None:
            population_dict.append(json_text['Population'])
    population_list = sorted(population_dict, reverse=True)
    if population_list:
        return population_list[0]
    else:
        return None

def list(df,cities_lst):
    return cities_lst.append(df)

def question_6(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    cities_lst = []
    #################################################
    # Your code goes here ...
    df6 = df2.copy()
    #print(df6['Income classification according to wb'])
    df_lic = df6.loc[df6['Income classification according to wb'] == 'LIC']
    #print(df_lic)
    df_new = df_lic.copy()
    df_new['Cities'] = df_lic['Cities'].apply(lambda x: q_split(x))
    df_new['population'] = df_new['Cities'].apply(lambda x: q6_population(x))
    df_new['city'] = df_new.apply(lambda x: q6_city(x['Cities'],x['population']),axis=1)

    df_new = df_new.sort_values(by='population', ascending=False)
    df_new = df_new[0:5]
    #print(df_new)
    df_new['city'].apply(lambda x: list(x,cities_lst))
    #print(cities_lst)
    lst = cities_lst
    #print(cities_lst)
    #################################################

    log("QUESTION 6", output_df=None, other=cities_lst)
    return lst

def q7(cities, city_dict):
    #city_dict = {}
    for i in cities:
        json_text = json.loads(i)
        if json_text['City'] not in city_dict.keys():
            city_dict[json_text['City']] = []
            city_dict[json_text['City']].append(json_text['Country'])
        elif json_text['Country'] not in city_dict[json_text['City']]:
            city_dict[json_text['City']].append(json_text['Country'])

def q7_city(result):
    re_result = {}
    for i in result.keys():
        if len(result[i]) >= 2:
            re_result[i] = result[i]
    #result = {result[i] for i in result.keys() if len(result[i]) >= 2}

    return re_result
def question_7(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df_temp = df2.copy()
    df_temp['Cities'] = df_temp['Cities'].apply(lambda x:q_split(x))
    city_dict = {}
    df_temp["Cities"].apply(lambda x: q7(x, city_dict))
    df7 = pd.DataFrame(q7_city(city_dict).items(), columns=['city', 'countries'])
    df7 = df7.set_index(['city'])
    #print(df7)
    #df7 = df7.set_index(['city'])
    #################################################

    log("QUESTION 7", output_df=df7, other=df7.shape)
    return df7

def country_population(Cities):
    country_populations = 0
    for i in Cities:
        json_text = json.loads(i)
        if json_text['Population'] != None:
            country_populations += json_text['Population']
    return country_populations

def question_8(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    df8 = df2.copy()
    df_temp1 = df8.copy()

    df_temp1['Cities'] = df_temp1['Cities'].apply(lambda x: q_split(x))
    df_temp1['country_population'] = df_temp1['Cities'].apply(lambda x: country_population(x))
    global_population = df_temp1['country_population'].sum()

    # print(global_population)

    df_continents = pd.read_csv(continents)
    df_temp = df8.reset_index(drop=False)
    df_continents = df_continents.loc[df_continents['Continent'] == 'South America']
    df_continents['Country'] = df_continents['Country'].replace({'Korea, North': 'North Korea',
                                                                 'Korea, South': 'South Korea',
                                                                 'US': 'United States',
                                                                 'Russian Federation': 'Russia',
                                                                 'Congo': 'Republic of the Congo',
                                                                 'Congo, Democratic Republic of': 'Democratic Republic of the Congo'
                                                                 })

    df_new = pd.merge(df_temp, df_continents, on='Country', how='inner')
    df_new = df_new.set_index(['Country'])

    df_new['Cities'] = df_new['Cities'].apply(lambda x: q_split(x))
    df_new['country_population'] = df_new['Cities'].apply(lambda x: country_population(x))
    df_new['percentage'] = df_new['country_population'].apply(lambda x: (x / global_population) * 100)
    # print(df_new['percentage'])
    y = df_new['percentage'].to_list()
    list_country = df_new.index.to_list()

    # print(y)
    # -------------
    # 画图
    plt.bar(list_country, y)
    index = np.arange(len(list_country))
    plt.xticks(index, list_country)
    # 设置横轴标签
    plt.xlabel('Countries')
    # 设置纵轴标签
    plt.ylabel('Percentage of world population (%)')
    # 添加标题
    plt.title("Percentage of world population in South American countries")
    plt.tick_params(axis='x', labelsize=10)
    plt.xticks(rotation=15)
    for x,y in zip(index, y):
        plt.text(x,y,'%.2f' %y,ha = 'center',va='bottom')

    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_9(df2):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    df9 = df2.copy()

    df9 = df9.loc[(df9['Foreign direct investment, net inflows percent of gdp'] != 'x') &
                  (df9['Foreign direct investment'] != 'x') &
                  (df9['Covid_19_economic_exposure_index_ex_aid_and_fdi'] != 'x') &
                  (df9['Covid_19_economic_exposure_index_ex_aid_and_fdi_and_food_import']!='x')]

    df9 = df9.loc[(df9['Foreign direct investment, net inflows percent of gdp'] != 'No data') &
                  (df9['Foreign direct investment'] != 'No data') &
                  (df9['Covid_19_economic_exposure_index_ex_aid_and_fdi']!='No data') &
                  (df9['Covid_19_economic_exposure_index_ex_aid_and_fdi_and_food_import']!='No data')]

    df9['Foreign direct investment, net inflows percent of gdp'] = df9['Foreign direct investment, net inflows percent of gdp'].str.replace(",",'.').astype(float)
    df9['Foreign direct investment'] = df9['Foreign direct investment'].str.replace(",",'.').astype(float)
    df9['Covid_19_economic_exposure_index_ex_aid_and_fdi'] = df9['Covid_19_economic_exposure_index_ex_aid_and_fdi'].str.replace(",",'.').astype(float)
    df9['Covid_19_economic_exposure_index_ex_aid_and_fdi_and_food_import'] = df9['Covid_19_economic_exposure_index_ex_aid_and_fdi_and_food_import'].str.replace(",",'.').astype(float)

    #print(df9)
    df9 = df9.rename(columns={'Income classification according to wb': 'Income Class'})
    df_grouped = df9.groupby('Income Class')[['Foreign direct investment, net inflows percent of gdp',
    'Foreign direct investment','Covid_19_economic_exposure_index_ex_aid_and_fdi','Covid_19_economic_exposure_index_ex_aid_and_fdi_and_food_import']]

    df_mean = df_grouped.mean()
    #print(df_mean)
    df_mean = df_mean.T
    plt.clf()
    df_mean[['HIC','MIC','LIC']].plot(kind = 'bar',title = "Compared with 'HIC','MIC' and 'LIC'")
    labels = ['FDI/GDP','FDI','Economic','Economic and Food']
    index = np.arange(len(labels))
    plt.xticks(index, labels = labels)
    plt.xticks(rotation=0)
    plt.xlabel('Metric')
    plt.ylabel('Values')

    #################################################

    plt.savefig("{}-Q12.png".format(studentid))

def color_continent(Continent):
    continent_color_dict = {'South America':'b','Asia':'y', 'Europe':'m',
                            'Africa': 'g','Oceania':'c','North America': 'r'}
    for i in continent_color_dict.keys():
        if Continent == i:
            return continent_color_dict[i]

def point_size(df,constant):
    return df/constant

def question_10(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    :param continents: the path for the Countries-Continents.csv file
    """

    #################################################
    # Your code goes here ...
    df10 = df2.copy()
    df_continent = pd.read_csv(continents)
    #df_continent['Country'].apply(continent_replace)
    df_continent['Country'] = df_continent['Country'].replace({'Korea, North': 'North Korea',
                                                                'Korea, South': 'South Korea',
                                                                 'US': 'United States',
                                                                 'Russian Federation': 'Russia',
                                                                 'Congo': 'Republic of the Congo',
                                                                 'Congo, Democratic Republic of': 'Democratic Republic of the Congo'
                                                                 })

    df10 = df10.reset_index(drop=False)
    df_temp = pd.merge(df10,df_continent,on="Country",how='inner')
    df_temp = df_temp.set_index(['Country'])
    df_temp['Cities'] = df_temp['Cities'].apply(lambda x: q_split(x))
    df_temp['country_population'] = df_temp['Cities'].apply(lambda x: country_population(x))
    #global_population = df_temp['country_population'].sum()
    #print(global_population)

    df_temp['color'] = df_temp['Continent'].apply(lambda x: color_continent(x))
    #print(df_temp['color'])
    df_temp['point_size'] = df_temp['country_population'].apply(lambda x:point_size(x,180000))
    #print(df_temp['point_size'])
    #grouped = df_temp.groupby['Continent'].Color


    # ---- 画图
    plt.clf()
    continent_color_dict = {'South America':'b','Asia':'y', 'Europe':'m',
                            'Africa': 'g','Oceania':'c','North America': 'r'}
    # change size
    #plt.figure(figsize=(7.5, 7.0))
    #plt.rcParams['figure.figsize'] = (8.0, 6.0)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    legend_ = []
    for y,c in zip(continent_color_dict.keys(),continent_color_dict.values()):
        legend_.append(plt.scatter([],[],c = c,alpha=0.3,s=50,label =y))
    plt.scatter(x=df_temp.avg_longitude,y=df_temp.avg_latitude, c=df_temp.color, s=df_temp['point_size'])

    plt.legend(handles= legend_, scatterpoints=1, frameon=False, labelspacing=1, title='Continent', loc='upper left', fontsize='x-small')

    plt.title("Longitude and Latitude for each Country")

    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    df1 = question_1("exposure.csv", "Countries.csv")
    df2 = question_2(df1.copy(True))
    #df3 = question_3(df2.copy(True))
    #df4 = question_4(df2.copy(True), "Countries-Continents.csv")
    #df5 = question_5(df2.copy(True))
    #lst = question_6(df2.copy(True))
    #df7 = question_7(df2.copy(True))
    #question_8(df2.copy(True), "Countries-Continents.csv")
    #question_9(df2.copy(True))
    #question_10(df2.copy(True), "Countries-Continents.csv")

    # long running
    # do something other
    endtime = datetime.datetime.now()
    print(endtime - starttime).seconds
