import matplotlib.pyplot as plt
import numpy as np
from time import sleep

history_length = 50  # Number of past measurements to display
distance_history = np.zeros(history_length)  # Initialize an array to store the distance history

plt.figure()
ax = plt.axes()
ax.set_xlim([-history_length, 0])
ax.set_ylim([0, 50])  # Adjust the y-axis limits as needed

bars = ax.bar(np.arange(-history_length, 0), distance_history)  # Create an initial set of empty bars
plt.ion()
plt.show()

while True:
    # Read the distance measurement from your VL53L0X sensor
    distance = np.random.randint(0, 50)

    # Shift the distance history array to the left and append the new measurement
    distance_history = np.roll(distance_history, -1)
    distance_history[-1] = distance

    # Update the heights of the bars to reflect the new distance measurements
    for bar, dist in zip(bars, distance_history):
        bar.set_height(dist)

    plt.pause(0.01)