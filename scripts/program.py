from tof import get_sensor_binaries
from note_controller import loop as note_controller_loop
from led_controller import update_with_binaries

while True:
    note_controller_loop()
    binaries = get_sensor_binaries()
    update_with_binaries(binaries)