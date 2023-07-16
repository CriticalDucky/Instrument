import VL53L0X  # type: ignore
import RPi.GPIO as GPIO  # type: ignore
from time import sleep

# shutdown_pins = [(17, 0x29), (27, 0x2B), (22, 0x2D)]  # (pin, i2c_address)
# tofs = [] # key = sensor number - 1, value = tof object

# GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BCM)

# for pin in shutdown_pins:
#     GPIO.setup(pin[0], GPIO.OUT)
#     GPIO.output(pin[0], GPIO.LOW)

# # Keep all low for 500 ms or so to make sure they reset
# sleep(0.50)

# for pin in shutdown_pins:
#     tof = VL53L0X.VL53L0X(i2c_address=pin[1])
#     tof.open()
#     tofs += [tof]
#     GPIO.output(pin[0], GPIO.HIGH)

# # Keep all high for 500 ms or so to make sure they turn on
# sleep(0.50)

tofs = [
    VL53L0X.VL53L0X(i2c_address=0x29),
]

for tof in tofs:
    tof.open()
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

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
