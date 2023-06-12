from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo="BOARD24", trigger="BOARD23")
while True:
    print('Distance: ', sensor.distance * 100)
    sleep(1)