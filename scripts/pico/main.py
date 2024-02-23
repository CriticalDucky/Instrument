while True:
    try:
        TIMING_BUDGET = 10000  # us

        from machine import Pin, I2C, UART
        from vl53l0x import setup_tofl_device, TBOOT
        import utime

        def setup_sensors():
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

            tofl_sensors = []

            i2c_sensors = [(i2c_0, i2c_0_xshut), (i2c_1, i2c_1_xshut)]

            for i2c, xshut_pins in i2c_sensors:
                for idx, pin in enumerate(xshut_pins):
                    pin.value(1)
                    utime.sleep_us(TBOOT)
                    tofl_sensor = setup_tofl_device(i2c, TIMING_BUDGET, 12, 14)
                    tofl_sensor.set_address(0x31 + idx)
                    tofl_sensors.append(tofl_sensor)

            return tofl_sensors

        def main():
            tofl_sensors = setup_sensors()
            tofl_data = [0] * len(tofl_sensors)

            while True:
                for idx, tofl in enumerate(tofl_sensors):
                    distance_mm = tofl.ping()
                    utime.sleep_us(1200)
                    tofl_data[idx] = distance_mm
                print(' '.join(map(str, tofl_data)))

        if __name__ == "__main__":
            main()

    except Exception as e:
        print(e)
        print("Restarting script in 2 seconds...")
        utime.sleep(2)

# def thread0():
#     global tofl1
#     global tofl2
#     global tofl3
#     global tofl4
#     global tofl5
#     global tofl6

#     global tofl_data

#     current_sensor = 0

#     while True:
#         try:
#             print(' '.join(map(str, tofl_data)))

#             for idx, tofl in enumerate([tofl1, tofl2, tofl3, tofl4, tofl5, tofl6]):
#                 current_sensor = idx + 1
#                 distance_mm = tofl.ping()
#                 utime.sleep_ms(2)
#                 tofl_data[idx] = distance_mm

#         except Exception as e:
#             print(e, f"Sensor {current_sensor} failed")

    

# def thread1():
#     global tofl7
#     global tofl8
#     global tofl9
#     global tofl10
#     global tofl11
#     global tofl12

#     global tofl_data

#     current_sensor = 0

#     while True:
#         try:
#             for idx, tofl in enumerate([tofl7, tofl8, tofl9, tofl10, tofl11, tofl12]):
#                 current_sensor = idx + 7
#                 distance_mm = tofl.ping()
#                 utime.sleep_ms(2)
#                 tofl_data[idx + 6] = distance_mm
#         except Exception as e:
#             print(e, f"Sensor {current_sensor} failed")

# _thread.start_new_thread(thread0, ())

# thread1()