import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import pywebio
import seaborn as sns
from pywebio.output import *
from pywebio.input import *
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


class Flight:
    # load in the original dataset
    def load_in_data_origin(csv0_file_name, json_filename):
        df0 = gpd.read_file(json_filename)
        df1 = pd.read_csv(csv0_file_name)
        df1 = df1.groupby('origin_state').agg({'arrival_delay': 'mean', 'price': 'mean', 'departure_delay': 'mean',
                                               'canceled': 'mean', 'capacity': 'sum'})
        df0 = df0[(df0['NAME'] != 'Alaska') & (df0['NAME'] != 'Hawaii')]
        data = df0.merge(df1, left_on='NAME', right_on='origin_state', how='right')
        return data

    # groupby destination, return gpd df
    def load_in_data_dest(csv0_file_name, json_filename):
        df0 = gpd.read_file(json_filename)
        df1 = pd.read_csv(csv0_file_name)
        df1 = df1.groupby('dest_state').agg(
            {'arrival_delay': 'mean', 'price': 'mean', 'departure_delay': 'mean', 'canceled': 'mean',
             'capacity': 'sum'})
        df0 = df0[(df0['NAME'] != 'Alaska') & (df0['NAME'] != 'Hawaii')]
        data = df0.merge(df1, left_on='NAME', right_on='dest_state', how='right')
        return data

    # groupby carrier, return gpd df
    def load_in_data_carrier(csv0_file_name, csv1_file_name):
        df1 = pd.read_csv(csv0_file_name)
        df2 = pd.read_csv(csv1_file_name)
        df1 = df1.merge(df2, left_on='carrier_id', right_on='cid', how='left')
        # df1['num_flights'] = 1
        df1 = df1.groupby('name', as_index=False).agg(
            {'arrival_delay': 'mean', 'price': 'mean', 'departure_delay': 'mean', 'canceled': 'mean',
             'capacity': 'sum'})
        # print(df1[['name', 'num_flights']])
        # df1['cancel rate'] = df1['canceled'] / df1['num_flights']
        # df1['delay rate'] = df1['arrival_delay'] / df1['num_flights']
        return df1

    # group by air routes, return gpd df
    def load_in_data_route(csv0_file_name, json_filename):
        df0 = gpd.read_file(json_filename)
        df1 = pd.read_csv(csv0_file_name)
        df1 = df1.groupby(['origin_city', 'dest_city'], as_index=False).agg(
            {'arrival_delay': 'mean', 'price': 'mean', 'origin_state': 'first', 'departure_delay': 'mean',
             'canceled': 'mean', 'capacity': 'sum'})
        df0 = df0[(df0['NAME'] != 'Alaska') & (df0['NAME'] != 'Hawaii')]
        data = df0.merge(df1, left_on='NAME', right_on='origin_state', how='right')
        return data

    # based on departure state, draw 4 figs
    def plot_data_origin(data):
        fig, [[ax1, ax4], [ax3, ax2]] = plt.subplots(2, 2, figsize=(25.6, 14.4))
        data.plot(ax=ax1, column='price', legend=True)
        data.plot(ax=ax2, column='arrival_delay', legend=True)
        data.plot(ax=ax3, column='departure_delay', legend=True)
        data.plot(ax=ax4, column='canceled', legend=True)
        ax1.set_title('prices of airlines for states as origin')
        ax2.set_title('arrival delay of airlines for states as origin')
        ax3.set_title('departure delay of airlines for states as origin')
        ax4.set_title('cancellation of airlines for states as origin')
        plt.savefig('US_origin.png')
        print('image saved')

    # based on departure state, draw 4 figs
    def plot_data_dest(data):
        fig, [[ax1, ax4], [ax3, ax2]] = plt.subplots(2, 2, figsize=(25.6, 14.4))
        data.plot(ax=ax1, column='price', legend=True)
        data.plot(ax=ax2, column='arrival_delay', legend=True)
        data.plot(ax=ax3, column='departure_delay', legend=True)
        data.plot(ax=ax4, column='canceled', legend=True)
        ax1.set_title('prices of airlines for states as destinations')
        ax2.set_title('arrival delay of airlines for states as destination')
        ax3.set_title('departure delay of airlines for states as destination')
        ax4.set_title('cancellation of airlines for states as destination')
        plt.savefig('US_dest.png')
        print('image saved')

    # plot data for the 10 big carriers
    def plot_data_biggest_carrier(data):
        data_big = data.sort_values(by='capacity', ascending=False)
        data_big = data_big.head(5)
        data_big = data_big.sort_values(by='arrival_delay', ascending=False)
        sns.catplot(x='name', y='arrival_delay', data=data_big, kind='bar')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('delay_10_biggest_carrier.png')
        print('image saved')

    # plot data for the 10 smallest carriers
    def plot_data_worst_carrier_delay(data):
        data_small = data.sort_values(by='arrival_delay', ascending=False)
        data_small = data_small.head(5)
        sns.catplot(x='name', y='arrival_delay', data=data_small, kind='bar')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('worst_delay_carrier.png')

    # plot data for 10 carriers with the highest cancel rate
    def plot_data_worst_carrier_cancel(data):
        data = data.groupby
        data = data.sort_values(by='canceled', ascending=False)
        data = data.head(5)
        sns.catplot(x='name', y='canceled', data=data, kind='bar')
        plt.xticks(rotation=-90)
        plt.tight_layout()
        plt.savefig('US_carrier_worst_canceled.png')


    # save two figs, one is relationship between price and delay for a route
    # another is relationship between day of the week and delay for a route
    def plot_data_one_route(data, origin, dest):
        data = data[(data['origin_city'] == origin) & (data['dest_city'] == dest)]
        data['total_delay'] = data['arrival_delay'] + data['departure_delay']
        print(data)
        plt.figure(figsize=(25.6, 14.4))
        sns.regplot(x='price', y='total_delay', data=data)
        name = 'Relationship between price and total delay for route ' + origin + ' to ' + dest
        plt.title(name)
        plt.savefig('US_price_delay_one_route_delay.png')
        plt.figure(figsize=(25.6, 14.4))
        sns.regplot(x='day_of_week_id', y='total_delay', data=data)
        name = 'Relationship between day and total delay for route ' + origin + ' to ' + dest
        plt.title(name)
        plt.savefig('US_day_delay_one_route_delay.png')


    def fit_and_predict_delay(data):
        data = data[['origin_state', 'origin_city', 'price', 'dest_city', 'dest_state', 'carrier_id', 'distance',
                     'day_of_week_id', 'arrival_delay', 'departure_delay', 'capacity']]
        data = data.dropna()
        features = data.loc[:, (data.columns != 'arrival_delay') & (data.columns != 'departure_delay')]
        features = pd.get_dummies(features)
        labels = data[['arrival_delay', 'departure_delay']]
        features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2)
        model = DecisionTreeRegressor()
        model.fit(features_train, labels_train)
        label_predictions_test = model.predict(features_test)
        result = mean_squared_error(labels_test, label_predictions_test)
        print('Machine Learning done. Mean squared error of the model is', end=' ')
        print(result)
        return result


    def make_web(data, plot):
        pywebio.config(css_style="#output-container{min-width: 90vw;}")
        user_input = input_group('View historical delay', [
            input(label='Departure City', type=TEXT, onchange=True, name='dep',
                  placeholder='Seattle, WA (Please use comma to separate city and state)', required=True),
            input(label='Destination City', type=TEXT, onchange=True, name='dest',
                  placeholder='New York, NY (Please use comma to separate city and state)', required=True)
        ])
        dep_sep = user_input['dep'].split(',')
        dest_sep = user_input['dest'].split(',')
        dep = dep_sep[0].title().strip() + " " + dep_sep[1].upper().strip()
        dest = dest_sep[0].title().strip() + " " + dest_sep[1].upper().strip()
        plot(data, dep, dest)
        img = open('US_day_delay_one_route_delay.png', 'rb')
        put_image(img.read())