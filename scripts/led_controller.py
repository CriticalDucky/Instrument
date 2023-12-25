LEDS_PER_NOTE = 13
LED_GROUPS = 12

import subprocess
import json
from color_util import Gradient, rainbow, blink_gradient_1
import time

# Processes can be added to this table, and every frame they will update.
led_processes = []

class LEDProcess:
    def __init__(self, name):
        self.name = name
        # {pixel_num: (r, g, b)}
        self.data = {}

    def update(self):
        pass

    def report(self):
        pass

    def stop(self):
        pass

class LEDProcessFade(LEDProcess):
    def __init__(self, gradient: Gradient, duration, pixel_nums):
        super().__init__("LedFade")
        self.duration = duration
        self.start_time = time.time()
        self.gradient = gradient
        self.time = 0

        for pixel_num in pixel_nums:
            self.data[pixel_num] = gradient.get_rgb_at_position(0)

    def update(self):
        self.time = time.time() - self.start_time

        for pixel_num in self.data:
            self.data[pixel_num] = self.gradient.get_rgb_at_position(self.time / self.duration)

        if self.time >= self.duration:
            self.stop()

    def stop(self):
        if self in led_processes:
            led_processes.remove(self)

# data: list of tuples (r, g, b)
def write(data):
    data = json.dumps(data)

    command = ["sudo", "python3", "scripts/led_admin.py", data]
    command2 = ["sudo", "python3", "led_admin.py", data]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        try:
            subprocess.run(command2, check=True)
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
                data.append(rainbow.get_rgb_at_position(num_led / (LED_GROUPS * LEDS_PER_NOTE)))
            else:
                data.append(color_off)

    write(data)

def led_blink1(led_group):
    process = LEDProcessFade(
        blink_gradient_1,
        0.5,
        [(led_group - 1) * LEDS_PER_NOTE + i + 1 for i in range(LEDS_PER_NOTE)])
    
    led_processes.append(process)