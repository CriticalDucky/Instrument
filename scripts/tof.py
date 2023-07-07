import VL53L0X #type: ignore
import matplotlib.pyplot as plt
import numpy as np
import threading

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)

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
