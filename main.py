import flight
import pandas as pd


def main():
    data_origin = flight.Flight.load_in_data_origin('resources/flight-dataset-2/flights-small.csv',
                                                    'resources/gz_2010_us_040_00_5m.json')
    data_dest = flight.Flight.load_in_data_dest('resources/flight-dataset-2/flights-small.csv',
                                                'resources/gz_2010_us_040_00_5m.json')
    data_carrier = flight.Flight.load_in_data_carrier('resources/flight-dataset-2/flights-small.csv',
                                                      'resources/flight-dataset-2/carriers.csv')
    df_flight = pd.read_csv('resources/flight-dataset-2/flights-small.csv')
    flight.Flight.plot_data_origin(data_origin)
    flight.Flight.plot_data_dest(data_dest)
    flight.Flight.plot_data_biggest_carrier(data_carrier)
    flight.Flight.plot_data_least_carrier_delay(data_carrier)
    flight.Flight.plot_data_worst_carrier_delay(data_carrier)
    flight.Flight.plot_data_worst_carrier_cancel(data_carrier)
    flight.Flight.fit_and_predict_delay(df_flight)
    answer = int(input('Do you want to search historical delay for an air route? (1 for Yes, 0 for No)'))
    if answer == 1:
        flight.Flight.make_web(df_flight, flight.Flight.plot_data_one_route)


if __name__ == '__main__':
    main()