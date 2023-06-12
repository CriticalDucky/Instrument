from gpiozero import Device, DistanceSensor
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

Device.pin_factory = factory

sensor = DistanceSensor(echo=24, trigger=23)
while True:
    print('Distance: ', sensor.distance * 100)
    sleep(1)