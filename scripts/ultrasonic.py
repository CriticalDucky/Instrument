from gpiozero import Device, DistanceSensor
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

Device.pin_factory = factory

sensors = [
    DistanceSensor(echo=24, trigger=23)
]

def get_distance(sensor_number):
    return sensors[sensor_number - 1].distance * 100