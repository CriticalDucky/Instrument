import os
import subprocess
from control_panel_data import data
import threading

import threading

def run_control_panel(set_data):
    current_script_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_script_path)
    os.chdir(parent_dir)
    subprocess.run(['python3', 'control_panel.py', set_data])

# Create a new thread for running the control panel
control_panel_thread = threading.Thread(target=run_control_panel, args=(data))
control_panel_thread.start()

# Set up the control panel

# Main loop
from tof import get_sensor_binaries
from note_controller import loop as note_controller_loop
from led_controller import update_with_binaries

while True:
    note_controller_loop()
    binaries = get_sensor_binaries()
    update_with_binaries(binaries)