from machine import Pin, I2C #type: ignore
from vl53l0x import setup_tofl_device, TBOOT
import utime #type: ignore

device_1_xshut = Pin(16, Pin.OUT)
device_2_xshut = Pin(17, Pin.OUT)
device_3_xshut = Pin(18, Pin.OUT)
device_4_xshut = Pin(19, Pin.OUT)
device_5_xshut = Pin(20, Pin.OUT)
device_6_xshut = Pin(21, Pin.OUT)

i2c_1 = I2C(id=1, sda=Pin(14), scl=Pin(15))

device_2_xshut.value(0)
device_3_xshut.value(0)
device_4_xshut.value(0)
device_5_xshut.value(0)
device_6_xshut.value(0)

device_1_xshut.value(1)
utime.sleep_us(TBOOT)
tofl1 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl1.set_address(0x31)

device_2_xshut.value(1)
utime.sleep_us(TBOOT)
tofl2 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl2.set_address(0x32)

device_3_xshut.value(1)
utime.sleep_us(TBOOT)
tofl3 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl3.set_address(0x33)

device_4_xshut.value(1)
utime.sleep_us(TBOOT)
tofl4 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl4.set_address(0x34)

device_5_xshut.value(1)
utime.sleep_us(TBOOT)
tofl5 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl5.set_address(0x35)

device_6_xshut.value(1)
utime.sleep_us(TBOOT)
tofl6 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl6.set_address(0x36)

try:
    while True:
        left, right, front, back, up, down = tofl1.ping(), tofl2.ping(), tofl3.ping(), tofl4.ping(), tofl5.ping(), tofl6.ping()
        print(left, 'mm, ', right, 'mm, ', front, 'mm, ', back, 'mm, ', up, 'mm, ', down, 'mm')
finally:
    # Restore default address
    tofl1.set_address(0x29)
    tofl2.set_address(0x29)
    tofl3.set_address(0x29)
    tofl4.set_address(0x29)
    tofl5.set_address(0x29)
    tofl6.set_address(0x29)