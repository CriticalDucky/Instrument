from tof import get_sensor_binaries
from note_controller import loop as note_controller_loop
from led_controller import update_with_binaries
import os
import subprocess

# Set up the control panel

current_script_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_script_path)
os.chdir(parent_dir)
subprocess.run(['python3', 'control_panel.py'])

# Main loop

while True:
    note_controller_loop()
    binaries = get_sensor_binaries()
    update_with_binaries(binaries)