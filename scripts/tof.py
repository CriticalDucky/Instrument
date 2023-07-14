import VL53L0X  # type: ignore
import RPi.GPIO as GPIO  # type: ignore
from time import sleep

# Keep all low for 500 ms or so to make sure they reset
sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.

# Create a VL53L0X object
tofs = [
    # VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29),
    VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x71),
    VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x72),
    VL53L0X.VL53L0X(tca9548a_num=2, tca9548a_addr=0x72),
    # VL53L0X.VL53L0X(i2c_address=0x2B, i2c_bus=0),
    # VL53L0X.VL53L0X(i2c_address=0x2D, i2c_bus=0),
]

for tof in tofs:
    tof.open()
    sleep(0.5)
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)


def get_distance(sensor_number):
    distance = tofs[sensor_number - 1].get_distance()/10

    if distance < 700 and distance > 0:
        print("Sensor", sensor_number, "distance", distance, "cm")

    if distance < 0:
        print("Unable to read sensor", sensor_number)

    return distance  # cm

def close_sensors():
    for tof in tofs:
        tof.stop_ranging()
        tof.close()

# tof.stop_ranging()
# tof.close()
