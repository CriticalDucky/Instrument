from machine import Pin, I2C #type: ignore
from vl53l0x import setup_tofl_device, TBOOT
import utime #type: ignore

# Function to set up a sensor
def setup_sensor(i2c, xshut_pin, address):
    xshut_pin.value(1)
    tof = setup_tofl_device(i2c, 40000, 12, 8)
    tof.set_address(address)
    utime.sleep_us(TBOOT)  # Give time for the sensor to boot up
    xshut_pin.value(0)
    return tof

# Number of sensors you want to use
num_sensors = 6
xshut_pins_gpio = [16, 17, 18, 19, 20, 21]
sensor_addresses = [0x29 + i for i in range(num_sensors)]

# Initialize I2C bus
i2c = I2C(id=1, sda=Pin(14), scl=Pin(15))

# Set up additional sensors
sensor_xshut_pins = [Pin(pin, Pin.OUT) for pin in xshut_pins_gpio]
# turn all off:
for pin in sensor_xshut_pins:
    pin.value(0)

sensors = [setup_sensor(i2c, xshut_pin, address) for xshut_pin, address in zip(sensor_xshut_pins, sensor_addresses)]

try:
    # Turn on all sensors
    for pin in sensor_xshut_pins:
        pin.value(1)

    utime.sleep_us(TBOOT)  # Give time for the sensor to boot up

    while True:
        distances = [sensor.ping() for sensor in sensors]
        print("Distances:", distances)
finally:
    # Restore default addresses
    for sensor in sensors:
        sensor.set_address(0x29)
