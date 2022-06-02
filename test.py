import flight


def test():
    data_carrier = flight.Flight.load_in_data_carrier('resources/flight-dataset-2/flights-small.csv',
                                                      'resources/flight-dataset-2/carriers.csv')
    biggest = flight.Flight.plot_data_biggest_carrier(data_carrier)
    print('Test Biggest Airline Carrier', end='----')
    if biggest == 'Southwest Airlines Co.':
        print('Passed')
    most_delayed = flight.Flight.plot_data_worst_carrier_delay(data_carrier)
    print('Test Worst Delayed Airline Carrier', end='----')
    if most_delayed == 'AirTran Airways Corporation':
        print('Passed')
    most_canceled = flight.Flight.plot_data_worst_carrier_cancel(data_carrier)
    print('Test Worst Canceled Airline Carrier', end='----')
    if most_canceled == 'Comair Inc.':
        print('Passed')


if __name__ == '__main__':
    test()
