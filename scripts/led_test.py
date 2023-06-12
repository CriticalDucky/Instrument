from gpiozero import LED
from time import sleep

yellow = LED(13)

while True:
    yellow.on()
    sleep(1)
    yellow.off()
    sleep(1)