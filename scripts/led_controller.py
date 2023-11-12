LEDS_PER_NOTE = 13

import subprocess
import json
#
def write(data):
    data = json.dumps(data)

    command = ["sudo", "python3", "scripts/led_admin.py", data]

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

    for _, val in enumerate(binaries):
        color_off = [0, 0, 0]
        color_on = [255, 0, 81]

        for _ in range(LEDS_PER_NOTE):
            if val == 1:
                data.append(color_on)
            else:
                data.append(color_off)

    write(data)