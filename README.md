## Intro to the files

1. Run the program using `main.py`, it calls functions from the `flight.py` module.  
2. See data processing and plotting functions in `flight.py`.  
3. Run `test.py` to test several functions from `flight.py`.
4. `flight_dev.py` is the old file we've written on, it shows traces of how we develop this program.  
5. There are a lot of `.png` files in the folder. Feel free to delete them, as running `main.py` plots them all again.
6. The `resources` folder contains the dataset needed to run this program. There's no bitcoin inside so don't change it.

## While running the program
1. We print out messages indicating accomplishment of each step, don't be scared.
2. There would be a message in the console while running `main.py` asking whether you want to search for historical delays.
It will render a webpage to enable search function. Type in number `1` to start the webpage. Type in `0` to skip.
3. In the webpage's text input box, you can type in your departure city and destination city. It's not case-sensitive, but remember
to add a comma between city name and the two-letter-long state abbreviation.
4. Pressing the enter key, the webpage will jump to a presentation of two plots about delay on that specific route. The plots
are also saved locally so you can compare them to plots of other air routes.
5. The `flight.Flight.fit_and_predict_delay()` function takes a while to run, considering it's training a Machine Learning
model on over 1 million feature-label pairs. Feel free to comment it out if you're just interested in the plots.