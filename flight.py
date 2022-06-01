import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import pywebio
import seaborn as sns
# import plotly.graph_objects as go
from pywebio.output import *
from pywebio.input import *
# from PIL import Image
from fpdf import FPDF
# from pywebio.session import run_js
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


# load in the original dataset
def load_in_data_origin(csv0_file_name, csv1_file_name, json_filename):
    df0 = gpd.read_file(json_filename)
    df1 = pd.read_csv(csv0_file_name)
    df2 = pd.read_csv(csv1_file_name)
    df1 = df1.groupby('origin_state').agg({'arrival_delay': 'mean', 'price': 'mean', 'departure_delay':'mean', 'canceled' :'mean', 'capacity': 'sum'})
    df0 = df0[(df0['NAME'] != 'Alaska') & (df0['NAME'] != 'Hawaii')]
    data = df0.merge(df1, left_on='NAME', right_on='origin_state', how='right')
    return data


# groupby destination, return gpd df
def load_in_data_dest(csv0_file_name,csv1_file_name,json_filename):
    df0 = gpd.read_file(json_filename)
    df1 = pd.read_csv(csv0_file_name)
    df2 = pd.read_csv(csv1_file_name)
    df1 = df1.groupby('dest_state').agg({'arrival_delay': 'mean', 'price': 'mean', 'departure_delay': 'mean', 'canceled': 'mean', 'capacity': 'sum'})
    df0 = df0[(df0['NAME'] != 'Alaska') & (df0['NAME'] != 'Hawaii')]
    data = df0.merge(df1, left_on='NAME', right_on='dest_state', how='right')
    return data


# groupby carrier, return gpd df
def load_in_data_carrier(csv0_file_name,csv1_file_name):
    df1 = pd.read_csv(csv0_file_name)
    df2 = pd.read_csv(csv1_file_name)
    df1 = df1.merge(df2, left_on='carrier_id', right_on='cid', how='left')
    df1 = df1.groupby('name', as_index=False).agg({'arrival_delay': 'mean', 'price': 'mean', 'departure_delay': 'mean', 'canceled': 'mean', 'capacity': 'sum'})
    return df1


# group by air routes, return gpd df
def load_in_data_route(csv0_file_name,json_filename):
    df0 = gpd.read_file(json_filename)
    df1 = pd.read_csv(csv0_file_name)
    df1 = df1.groupby(['origin_city', 'dest_city'], as_index=False).agg({'arrival_delay': 'mean', 'price': 'mean', 'origin_state': 'first', 'departure_delay': 'mean', 'canceled': 'mean', 'capacity': 'sum'})
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
    data = data.sort_values(by='canceled', ascending=False)
    data = data.head(5)
    sns.catplot(x='name', y='canceled', data=data, kind='bar')
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig('US_carrier_worst_canceled.png')


# group by carriers, plot the relationship between price and delay
# def plot_data_price_delay_carriers(data):
#     data = data.sort_values(by='price', ascending=True)
#     data['total_delay'] = data['arrival_delay'] + data['departure_delay']
#     data = data.head(100)
#     sns.relplot(x='price', y='total_delay', data=data)
#     #plt.figure(figsize=(20,10))
#     plt.savefig('US_price_delay_carriers.png')
#     sns.regplot(x='price', y='total_delay', data=data)
#     plt.savefig('US_price_delay_carriers_reg.png')


# group by origin state, plot the relationship between price and delay
# def plot_data_price_delay_origin(data):
#     data = data.sort_values(by='price', ascending=True)
#     data['total_delay'] = data['arrival_delay'] + data['departure_delay']
#     data = data.head(100)
#     sns.relplot(x='price', y='total_delay', data=data)
#     # plt.figure(figsize=(20,10))
#     plt.savefig('US_price_delay_origin.png')
#     sns.regplot(x='price', y='total_delay', data=data)
#     # plt.figure(figsize=(20,10))
#     plt.savefig('US_price_delay_origin_reg.png')
#
#
# # group by destination state, plot the relationship between price and delay
# def plot_data_price_delay_dest(data):
#     data = data.sort_values(by='price', ascending=True)
#     data['total_delay'] = data['arrival_delay'] + data['departure_delay']
#     data = data.head(100)
#     sns.relplot(x='price', y='total_delay', data=data)
#     # plt.figure(figsize=(20,10))
#     plt.savefig('US_price_delay_dest.png')
#     sns.regplot(x='price', y='total_delay', data=data)
#     # plt.figure(figsize=(20,10))
#     plt.savefig('US_price_cancel_dest_reg.png')


# group by carriers, plot the relationship between price and cancel rate
# def plot_data_price_cancel_carriers(data):
#     data = data.sort_values(by='price', ascending=True)
#     sns.relplot(x='price', y='canceled', data=data)
#     #plt.figure(figsize=(20,10))
#     plt.savefig('US_price_cancel_carriers.png')
#     sns.regplot(x='price', y='canceled', data=data)
#     plt.savefig('US_price_cancel_carriers_reg.png')
#
#
# # group by origin state, plot the relationship between price and cancel rate
# def plot_data_price_cancel_origin(data):
#     data = data.sort_values(by='price', ascending=True)
#     sns.relplot(x='price', y='canceled', data=data,)
#     plt.savefig('US_price_cancel_origin.png')
#     sns.regplot(x='price', y='canceled', data=data)
#     # plt.figure(figsize=(20,10))
#     plt.savefig('US_price_cancel_origin_reg.png')
#
#
# # group by destination state, plot the relationship between price and cancel rate
# def plot_data_price_cancel_dest(data):
#     data = data.sort_values(by='price', ascending=True)
#     sns.relplot(x='price', y='canceled', data=data)
#     # plt.figure(figsize=(20,10))
#     plt.savefig('US_price_cancel_dest.png')
#     sns.regplot(x='price', y='canceled', data=data)
#     # plt.figure(figsize=(20,10))
#     plt.savefig('US_price_cancel_dest_reg.png')


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


# plot 10 best and worst routes in the US based on delay
# def plot_data_route(data):
#     data['total_delay'] = data['arrival_delay'] + data['departure_delay']
#     data = data.sort_values(by='total_delay', ascending=True)
#     data_asc = data.head(10)
#     print(data_asc)
#     data = data.sort_values(by='total_delay', ascending=False)
#     data_des = data.head(10)
#     print(data_des)
#     fig, ax = plt.subplots(1, figsize=(25.6, 14.4))
#     data.plot(ax=ax, color='#EEEEEE', edgecolor='#AAAAAA')
#     data_asc.plot(ax=ax, column='total_delay', legend=True, vmin=-50, vmax=520)
#     data_des.plot(ax=ax, column='total_delay', vmin=-50, vmax=520)
#     plt.savefig('US_best_and_worst_delay_route.png')


def plot_distance_delay(data):
    pass
'''
def plot_data_route_worst(data):
    data['total_delay'] = data['arrival_delay'] + data['departure_delay']
    data = data.sort_values(by='total_delay',ascending=False)
    data_asc = data.head(10)
    fig, ax = plt.subplots(1,figsize = (25.6,14.4))
    data.plot(ax=ax,color='#EEEEEE',edgecolor='#AAAAAA')
    data_asc.plot(ax=ax,column='total_delay',legend=True)
    plt.savefig('US_worst_delay_route.png')


def plot_data_route_best(data):
    data['total_delay'] = data['arrival_delay'] + data['departure_delay']
    data = data.sort_values(by='total_delay', ascending=True)
    data_asc = data.head(10)
    fig, ax = plt.subplots(1, figsize=(25.6, 14.4))
    data.plot(ax=ax, color='#EEEEEE', edgecolor='#AAAAAA')
    data_asc.plot(ax=ax, column='total_delay', legend=True)
    plt.savefig('US_best_delay_route.png')
'''


def fit_and_predict_delay(data):
    data = data[['origin_state', 'origin_city', 'price', 'dest_city', 'dest_state', 'carrier_id', 'distance', 'day_of_week_id', 'arrival_delay', 'departure_delay', 'capacity']]
    data = data.dropna()
    features = data.loc[:, (data.columns != 'arrival_delay') & (data.columns != 'departure_delay')]
    features = pd.get_dummies(features)
    labels = data[['arrival_delay', 'departure_delay']]
    features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2)
    model = DecisionTreeRegressor()
    model.fit(features_train, labels_train)
    label_predictions_test = model.predict(features_test)
    result = mean_squared_error(labels_test, label_predictions_test)
    print("The mean squared error is" + result)
    return result


def make_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times', 'B', 16)
    pdf.cell(w=0, txt='This is a graph', ln=1, align='C')
    pdf.output('test.pdf')
    print('pdf has been made')


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
    # put_button('Return to input', onclick=run_js('window.location.reload()'))
    # put_file(dep + "to" + dest + "route delay.png", img, "Download PNG")
    # with Image.open("US_day_delay_one_route_delay.png") as im:
    #     put_image(im)


def main():
    print('hello world')
    data_origin = load_in_data_origin('resources/flight-dataset-2/flights-small.csv','resources/flight-dataset-2/carriers.csv','resources/gz_2010_us_040_00_5m.json')
    data_dest = load_in_data_dest('resources/flight-dataset-2/flights-small.csv','resources/flight-dataset-2/carriers.csv','resources/gz_2010_us_040_00_5m.json')
    data_carrier = load_in_data_carrier('resources/flight-dataset-2/flights-small.csv','resources/flight-dataset-2/carriers.csv')
    data_route = load_in_data_route('resources/flight-dataset-2/flights-small.csv','resources/gz_2010_us_040_00_5m.json')
    df0 = gpd.read_file('resources/gz_2010_us_040_00_5m.json')
    df1 = pd.read_csv('resources/flight-dataset-2/flights-small.csv')
    df2 = pd.read_csv('resources/flight-dataset-2/carriers.csv')
    # print(df0.columns)
    # print(df1.columns)
    # print(df2.columns)
    plot_data_origin(data_origin)
    plot_data_dest(data_dest)
    plot_data_biggest_carrier(data_carrier)
    plot_data_worst_carrier_delay(data_carrier)
    plot_data_worst_carrier_cancel(data_carrier)
    # plot_data_price_delay_carriers(data_carrier)
    # plot_data_price_delay_origin(data_origin)
    # plot_data_price_delay_dest(data_dest)
    # plot_data_price_cancel_dest(data_dest)
    # plot_data_price_cancel_origin(data_origin)
    # plot_data_price_cancel_carriers(data_carrier)
    # plot_data_one_route(df1, 'Seattle WA', 'New York NY')
    # plot_data_route(data_route)
    fit_and_predict_delay(df1)
    make_pdf(data_dest)
    make_web(df1, plot_data_one_route)
    #plot_data_route_best(data_route)
    #plot_data_route_worst(data_route)
    #temp1 = gpd.read_file('resources/gz_2010_us_040_00_5m.json')
    #temp1.plot()
    #plt.savefig('temp.png')


if __name__ == '__main__':
    main()

'''
    geo_frame = df1.merge(df2, left_on='CTIDFP00',
                          right_on='CensusTract', how='left')
    return geo_frame
'''