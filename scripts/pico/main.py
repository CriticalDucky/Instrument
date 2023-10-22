from machine import Pin, I2C, UART  # type: ignore
import utime  # type: ignore
import json
import _thread

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

tofl_data = [0] * 12

i2c_0_xshut = [
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(21, Pin.OUT),
]

i2c_1_xshut = [
    Pin(22, Pin.OUT),
    Pin(26, Pin.OUT),
    Pin(27, Pin.OUT),
    Pin(28, Pin.OUT),
    Pin(2, Pin.OUT),
    Pin(3, Pin.OUT),
]

i2c_0 = I2C(id=1, sda=Pin(14), scl=Pin(15))
i2c_1 = I2C(id=0, sda=Pin(0), scl=Pin(1))

for pin in i2c_0_xshut + i2c_1_xshut:
    pin.value(0)

def thread0():
    from vl53l0x import setup_tofl_device, TBOOT

    # i2c_0

    i2c_0_xshut[0].value(1)
    utime.sleep_us(TBOOT)
    tofl1 = setup_tofl_device(i2c_0, 40000, 18, 14)
    tofl1.set_address(0x31)

    i2c_0_xshut[1].value(1)
    utime.sleep_us(TBOOT)
    tofl2 = setup_tofl_device(i2c_0, 40000, 18, 14)
    tofl2.set_address(0x32)

    i2c_0_xshut[2].value(1)
    utime.sleep_us(TBOOT)
    tofl3 = setup_tofl_device(i2c_0, 40000, 18, 14)
    tofl3.set_address(0x33)

    i2c_0_xshut[3].value(1)
    utime.sleep_us(TBOOT)
    tofl4 = setup_tofl_device(i2c_0, 40000, 18, 14)
    tofl4.set_address(0x34)

    i2c_0_xshut[4].value(1)
    utime.sleep_us(TBOOT)
    tofl5 = setup_tofl_device(i2c_0, 40000, 18, 14)
    tofl5.set_address(0x35)

    i2c_0_xshut[5].value(1)
    utime.sleep_us(TBOOT)
    tofl6 = setup_tofl_device(i2c_0, 40000, 18, 14)
    tofl6.set_address(0x36)

    while True:
        for idx, tofl in enumerate([tofl1, tofl2, tofl3, tofl4, tofl5, tofl6]):
            distance_cm = tofl.ping()/10
            tofl_data[idx] = distance_cm

            if distance_cm < 800 and distance_cm > 10:
                print(idx + 1, distance_cm, end=' ')

        uart.write(json.dumps(tofl_data))

        print()

def thread1():
    from vl53l0x import setup_tofl_device, TBOOT

    # i2c_1

    i2c_1_xshut[0].value(1)
    utime.sleep_us(TBOOT)
    tofl7 = setup_tofl_device(i2c_1, 40000, 18, 14)
    tofl7.set_address(0x31)

    i2c_1_xshut[1].value(1)
    utime.sleep_us(TBOOT)
    tofl8 = setup_tofl_device(i2c_1, 40000, 18, 14)
    tofl8.set_address(0x32)

    i2c_1_xshut[2].value(1)
    utime.sleep_us(TBOOT)
    tofl9 = setup_tofl_device(i2c_1, 40000, 18, 14)
    tofl9.set_address(0x33)

    i2c_1_xshut[3].value(1)
    utime.sleep_us(TBOOT)
    tofl10 = setup_tofl_device(i2c_1, 40000, 18, 14)
    tofl10.set_address(0x34)

    i2c_1_xshut[4].value(1)
    utime.sleep_us(TBOOT)
    tofl11 = setup_tofl_device(i2c_1, 40000, 18, 14)
    tofl11.set_address(0x35)

    i2c_1_xshut[5].value(1)
    utime.sleep_us(TBOOT)
    tofl12 = setup_tofl_device(i2c_1, 40000, 18, 14)
    tofl12.set_address(0x36)

    while True:
        for idx, tofl in enumerate([tofl7, tofl8, tofl9, tofl10, tofl11, tofl12]):
            global tofl_data

            distance_cm = tofl.ping()/10
            tofl_data[idx + 6] = distance_cm

            if distance_cm < 800 and distance_cm > 10:
                print(idx + 7, distance_cm, end=' ')

        # uart.write(json.dumps(tofl_data))

        print()

_thread.start_new_thread(thread0, ())

thread1()

# from machine import Pin, I2C, UART  # type: ignore
# from vl53l0x import setup_tofl_device, TBOOT
# import utime  # type: ignore
# import json
# import _thread

# uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# tofl_data = [0] * 12

# i2c_0_xshut = [
#     Pin(16, Pin.OUT),
#     Pin(17, Pin.OUT),
#     Pin(18, Pin.OUT),
#     Pin(19, Pin.OUT),
#     Pin(20, Pin.OUT),
#     Pin(21, Pin.OUT),
# ]

# i2c_1_xshut = [
#     Pin(22, Pin.OUT),
#     Pin(26, Pin.OUT),
#     Pin(27, Pin.OUT),
#     Pin(28, Pin.OUT),
#     Pin(2, Pin.OUT),
#     Pin(3, Pin.OUT),
# ]

# i2c_0 = I2C(id=1, sda=Pin(14), scl=Pin(15))
# i2c_1 = I2C(id=0, sda=Pin(0), scl=Pin(1))

# for pin in i2c_0_xshut + i2c_1_xshut:
#     pin.value(0)

# # i2c_0

# i2c_0_xshut[0].value(1)
# utime.sleep_us(TBOOT)
# tofl1 = setup_tofl_device(i2c_0, 40000, 18, 14)
# tofl1.set_address(0x31)

# i2c_0_xshut[1].value(1)
# utime.sleep_us(TBOOT)
# tofl2 = setup_tofl_device(i2c_0, 40000, 18, 14)
# tofl2.set_address(0x32)

# i2c_0_xshut[2].value(1)
# utime.sleep_us(TBOOT)
# tofl3 = setup_tofl_device(i2c_0, 40000, 18, 14)
# tofl3.set_address(0x33)

# i2c_0_xshut[3].value(1)
# utime.sleep_us(TBOOT)
# tofl4 = setup_tofl_device(i2c_0, 40000, 18, 14)
# tofl4.set_address(0x34)

# i2c_0_xshut[4].value(1)
# utime.sleep_us(TBOOT)
# tofl5 = setup_tofl_device(i2c_0, 40000, 18, 14)
# tofl5.set_address(0x35)

# i2c_0_xshut[5].value(1)
# utime.sleep_us(TBOOT)
# tofl6 = setup_tofl_device(i2c_0, 40000, 18, 14)
# tofl6.set_address(0x36)

# # i2c_1

# i2c_1_xshut[0].value(1)
# utime.sleep_us(TBOOT)
# tofl7 = setup_tofl_device(i2c_1, 40000, 18, 14)
# tofl7.set_address(0x31)

# i2c_1_xshut[1].value(1)
# utime.sleep_us(TBOOT)
# tofl8 = setup_tofl_device(i2c_1, 40000, 18, 14)
# tofl8.set_address(0x32)

# i2c_1_xshut[2].value(1)
# utime.sleep_us(TBOOT)
# tofl9 = setup_tofl_device(i2c_1, 40000, 18, 14)
# tofl9.set_address(0x33)

# i2c_1_xshut[3].value(1)
# utime.sleep_us(TBOOT)
# tofl10 = setup_tofl_device(i2c_1, 40000, 18, 14)
# tofl10.set_address(0x34)

# i2c_1_xshut[4].value(1)
# utime.sleep_us(TBOOT)
# tofl11 = setup_tofl_device(i2c_1, 40000, 18, 14)
# tofl11.set_address(0x35)

# i2c_1_xshut[5].value(1)
# utime.sleep_us(TBOOT)
# tofl12 = setup_tofl_device(i2c_1, 40000, 18, 14)
# tofl12.set_address(0x36)

# while True: # only if distance cm is less than 800, then print:
#     for idx, tofl in enumerate([tofl1, tofl2, tofl3, tofl4, tofl5, tofl6, tofl7, tofl8, tofl9, tofl10, tofl11, tofl12]):
#         distance_cm = tofl.ping()/10
#         tofl_data[idx] = distance_cm

#         if distance_cm < 800:
#             print(idx + 1, distance_cm, end=' ')

#     uart.write(json.dumps(tofl_data))

#     print()

# def thread0():
#     global tofl1
#     global tofl2
#     global tofl3
#     global tofl4
#     global tofl5
#     global tofl6

#     while True:
#         for idx, tofl in enumerate([tofl1, tofl2, tofl3, tofl4, tofl5, tofl6]):
#             distance_cm = tofl.ping()/10
#             tofl_data[idx] = distance_cm

#             if distance_cm < 20 and distance_cm > 10:
#                 print(idx + 1, distance_cm, end=' ')

#         uart.write(json.dumps(tofl_data))

#         print()

# def thread1():
#     global tofl7
#     global tofl8
#     global tofl9
#     global tofl10
#     global tofl11
#     global tofl12

#     while True:
#         for idx, tofl in enumerate([tofl7, tofl8, tofl9, tofl10, tofl11, tofl12]):
#             global tofl_data

#             distance_cm = tofl.ping()/10
#             tofl_data[idx + 6] = distance_cm

#             if distance_cm < 20 and distance_cm > 10:
#                 print(idx + 7, distance_cm, end=' ')

#         # uart.write(json.dumps(tofl_data))

#         print()

# _thread.start_new_thread(thread0, ())

# thread1()