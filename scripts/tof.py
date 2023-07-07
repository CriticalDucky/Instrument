import VL53L0X #type: ignore
import matplotlib.pyplot as plt
import numpy as np
import threading

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
history_length = 50  # Number of past measurements to display
history = np.zeros(history_length)  # Initialize an array to store the distance history

plt.figure()
plt.switch_backend('agg')
ax = plt.axes()
ax.set_xlim([-history_length, 0])
ax.set_ylim([0, 50])  # Adjust the y-axis limits as needed

bars = ax.bar(np.arange(-history_length, 0), history)  # Create an initial set of empty bars
plt.show(block=False)  # Set block=False to allow non-blocking plotting

# I2C Address can change before tof.open()
# tof.change_address(0x32)
tof.open()
# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

def get_distance(sensor_number):
    distance = tof.get_distance()/10
    # print(distance)
    return distance # cm

# tof.stop_ranging()
# tof.close()

def update_graph():
    while True:
        # Read the distance measurement from your VL53L0X sensor
        distance = get_distance(1)

        # Shift the distance history array to the left and append the new measurement
        distance_history = np.roll(history, -1)
        distance_history[-1] = distance

        # Update the heights of the bars to reflect the new distance measurements
        for bar, dist in zip(bars, distance_history):
            bar.set_height(dist)

        plt.pause(0.01)

# Create a separate thread for updating the graph
graph_thread = threading.Thread(target=update_graph)
graph_thread.daemon = True
graph_thread.start()
