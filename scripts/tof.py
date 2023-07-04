import time
import VL53L0X # type: ignore

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

while True:
    distance = tof.get_distance()
    print(distance)
    time.sleep(0.1)