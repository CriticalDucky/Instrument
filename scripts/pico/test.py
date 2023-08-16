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

# i2c_1

i2c_1_xshut[0].value(1)
utime.sleep_us(TBOOT)
tofl1 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl1.set_address(0x31)

i2c_1_xshut[1].value(1)
utime.sleep_us(TBOOT)
tofl2 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl2.set_address(0x32)

i2c_1_xshut[2].value(1)
utime.sleep_us(TBOOT)
tofl3 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl3.set_address(0x33)

i2c_1_xshut[3].value(1)
utime.sleep_us(TBOOT)
tofl4 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl4.set_address(0x34)

i2c_1_xshut[4].value(1)
utime.sleep_us(TBOOT)
tofl5 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl5.set_address(0x35)

i2c_1_xshut[5].value(1)
utime.sleep_us(TBOOT)
tofl6 = setup_tofl_device(i2c_1, 40000, 12, 8)
tofl6.set_address(0x36)

# i2c_0

i2c_1_xshut[0].value(1)
utime.sleep_us(TBOOT)
tofl7 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl7.set_address(0x31)

i2c_0_xshut[1].value(1)
utime.sleep_us(TBOOT)
tofl8 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl8.set_address(0x32)

i2c_0_xshut[2].value(1)
utime.sleep_us(TBOOT)
tofl9 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl9.set_address(0x33)

i2c_0_xshut[3].value(1)
utime.sleep_us(TBOOT)
tofl10 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl10.set_address(0x34)

i2c_0_xshut[4].value(1)
utime.sleep_us(TBOOT)
tofl11 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl11.set_address(0x35)

i2c_0_xshut[5].value(1)
utime.sleep_us(TBOOT)
tofl12 = setup_tofl_device(i2c_0, 40000, 12, 8)
tofl12.set_address(0x36)

try:
    while True:
        print('   '.join([str(tofl.ping()/10) for tofl in [tofl1, tofl2, tofl3, tofl4, tofl5, tofl6, tofl7, tofl8, tofl9, tofl10, tofl11, tofl12]]))
finally:
    # Restore default address
    for tofl in [tofl1, tofl2, tofl3, tofl4, tofl5, tofl6, tofl7, tofl8, tofl9, tofl10, tofl11, tofl12]:
        tofl.set_address(0x29)

# from machine import Pin, I2C #type: ignore
# from vl53l0x import setup_tofl_device, TBOOT
# import utime #type: ignore

# i2c_1_xshut = [
#     Pin(16, Pin.OUT),
#     Pin(17, Pin.OUT),
#     Pin(18, Pin.OUT),
#     Pin(19, Pin.OUT),
#     Pin(20, Pin.OUT),
#     Pin(21, Pin.OUT),
# ]

# i2c_0_xshut = [
#     Pin(22, Pin.OUT),
#     Pin(26, Pin.OUT),
#     Pin(27, Pin.OUT),
#     Pin(28, Pin.OUT),
#     Pin(2, Pin.OUT),
#     Pin(3, Pin.OUT),
# ]

# i2c_1 = I2C(id=1, sda=Pin(14), scl=Pin(15))
# i2c_0 = I2C(id=0, sda=Pin(0), scl=Pin(1))

# for pin in i2c_0_xshut + i2c_1_xshut:
#     pin.value(0)

# i2c_1_tofls = []
# i2c_0_tofls = []

# for pin in i2c_1_xshut:
#     pin.value(1)
#     utime.sleep_us(TBOOT)
#     tofl = setup_tofl_device(i2c_1, 40000, 12, 8)
#     tofl.set_address(0x29 + len(i2c_1_tofls))
#     i2c_1_tofls.append(tofl)

# for pin in i2c_0_xshut:
#     pin.value(1)
#     utime.sleep_us(TBOOT)
#     tofl = setup_tofl_device(i2c_0, 40000, 12, 8)
#     tofl.set_address(0x29 + len(i2c_0_tofls))
#     i2c_0_tofls.append(tofl)

# try:
#     while True:
#         distances_1_cm = [tofl.ping()/10 for tofl in i2c_1_tofls]
#         distances_0_cm = [tofl.ping()/10 for tofl in i2c_0_tofls]
#         distances_cm = distances_1_cm + distances_0_cm

#         print('   '.join([str(d) for d in distances_cm]))
# finally:
#     # Restore default address
#     for tofl in i2c_1_tofls + i2c_0_tofls:
#         tofl.set_address(0x29)
