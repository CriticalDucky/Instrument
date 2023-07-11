import VL53L0X #type: ignore

# Create a VL53L0X object
tofs = [
    VL53L0X.VL53L0X(i2c_bus=0, tca9548a_num=1, tca9548a_addr=0x70),
    VL53L0X.VL53L0X(i2c_bus=0, tca9548a_num=2, tca9548a_addr=0x70),
    VL53L0X.VL53L0X(i2c_bus=1, tca9548a_num=1, tca9548a_addr=0x71),
    VL53L0X.VL53L0X(i2c_bus=1, tca9548a_num=2, tca9548a_addr=0x71),
]

for tof in tofs:
    tof.open()
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

def get_distance(sensor_number):
    distance = tofs[sensor_number - 1].get_distance()/10

    if distance < 700 and distance > 0:
        print("Sensor", sensor_number, "distance", distance, "cm")
    
    if distance < 0:
        print("Unable to read sensor", sensor_number)

    return distance # cm

# tof.stop_ranging()
# tof.close()
