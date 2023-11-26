LEDS_PER_NOTE = 13
LED_GROUPS = 12

import subprocess
import json
from color_util import Gradient, rainbow
#
def write(data):
    data = json.dumps(data)

    command = ["sudo", "python3", "led_admin.py", data]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def shift_led_data(data, shift_amount=4): # The beginning of the LED strip is not at sensor 1, so we need to shift the data (binaries). The data is also reversed.
    reversed_list = list(reversed(data))
    shifted_list = reversed_list[shift_amount:] + reversed_list[:shift_amount]
    return shifted_list

def update_with_binaries(binaries): # For debug purposes
    data = []

    binaries = shift_led_data(binaries)

    for note, val in enumerate(binaries):
        color_off = (0, 0, 0)

        for led in range(LEDS_PER_NOTE):
            num_led = note * LEDS_PER_NOTE + led

            if val == 1:
                data.append(rainbow.get_color_at_position(num_led / (LED_GROUPS * LEDS_PER_NOTE)))
            else:
                data.append(color_off)

    write(data)