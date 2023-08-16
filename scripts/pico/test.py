from machine import Pin, I2C #type: ignore
from vl53l0x import setup_tofl_device, TBOOT
import utime #type: ignore

i2c_1_xshut = [
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(21, Pin.OUT),
]

i2c_0_xshut = [
    Pin(22, Pin.OUT),
    Pin(26, Pin.OUT),
    Pin(27, Pin.OUT),
    Pin(28, Pin.OUT),
    Pin(2, Pin.OUT),
    Pin(3, Pin.OUT),
]

i2c_1 = I2C(id=1, sda=Pin(14), scl=Pin(15))
i2c_0 = I2C(id=0, sda=Pin(0), scl=Pin(1))

for pin in i2c_0_xshut + i2c_1_xshut:
    pin.value(0)

i2c_1_tofls = []
i2c_0_tofls = []

for pin in i2c_1_xshut:
    pin.value(1)
    utime.sleep_us(TBOOT)
    tofl = setup_tofl_device(i2c_1, 40000, 12, 8)
    tofl.set_address(0x29 + len(i2c_1_tofls))
    i2c_1_tofls.append(tofl)

for pin in i2c_0_xshut:
    pin.value(1)
    utime.sleep_us(TBOOT)
    tofl = setup_tofl_device(i2c_0, 40000, 12, 8)
    tofl.set_address(0x29 + len(i2c_0_tofls))
    i2c_0_tofls.append(tofl)

try:
    while True:
        distances_1_cm = [tofl.ping()/10 for tofl in i2c_1_tofls]
        distances_0_cm = [tofl.ping()/10 for tofl in i2c_0_tofls]
        distances_cm = distances_1_cm + distances_0_cm

        print('   '.join([str(d) for d in distances_cm]))
finally:
    # Restore default address
    for tofl in i2c_1_tofls + i2c_0_tofls:
        tofl.set_address(0x29)
