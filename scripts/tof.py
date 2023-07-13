import VL53L0X  # type: ignore
import RPi.GPIO as GPIO  # type: ignore
from time import sleep

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16

# GPIO.setwarnings(False)

# # Setup GPIO for shutdown pins on each VL53L0X
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(sensor1_shutdown, GPIO.OUT)
# GPIO.setup(sensor2_shutdown, GPIO.OUT)

# # Set all shutdown pins low to turn off each VL53L0X
# GPIO.output(sensor1_shutdown, GPIO.LOW)
# GPIO.output(sensor2_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.

# Create a VL53L0X object
tofs = [
    # VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29),
    VL53L0X.VL53L0X(tca9548a_num=1, tca9548a_addr=0x70),
    VL53L0X.VL53L0X(tca9548a_num=2, tca9548a_addr=0x70),
    # VL53L0X.VL53L0X(i2c_address=0x2B, i2c_bus=0),
    # VL53L0X.VL53L0X(i2c_address=0x2D, i2c_bus=0),
]

for tof in tofs:
    tof.open()
    sleep(0.5)
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)


def get_distance(sensor_number):
    distance = tofs[sensor_number - 1].get_distance()/10

    if sensor_number == 2:
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
