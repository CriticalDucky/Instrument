LEDS_PER_NOTE = 13
LED_GROUPS = 12

import subprocess
import json
from color_util import *
import time
from instrument_util import *

# Processes can be added to this table, and every frame they will update.
led_processes = []

class LEDProcess:
    def __init__(self, name):
        self.name = name
        # {pixel_num: (r, g, b)}
        self.data = {}
        self.stopped = False

    def update(self):
        pass

    def report(self):
        return self.data

    def stop(self):
        self.stopped = True
        if self in led_processes:
            led_processes.remove(self)
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

class LEDProcessStatic(LEDProcess):
    def __init__(self, color, pixel_nums, duration):
        super().__init__("LedStatic")
        self.color = color
        self.duration = duration
        self.start_time = time.time()
        self.time = 0

        for pixel_num in pixel_nums:
            self.data[pixel_num] = color

    def update(self):
        if not self.duration: return

        self.time = time.time() - self.start_time

        if self.time >= self.duration:
            self.stop()

class LEDProcessHold(LEDProcess):
    def __init__(self, gradient1, middle_color, gradient2, instance, pixel_nums):
        super().__init__("LedHold")
        self.gradient1 = gradient1
        self.middle_color = middle_color
        self.gradient2 = gradient2
        self.instance = instance
        self.pixel_nums = pixel_nums
        self.still_holding = True

        self.process1 = LEDProcessFade(gradient1, 0.32*0.5, pixel_nums)
        self.current_process = 1

        for pixel_num in pixel_nums:
            self.data[pixel_num] = gradient1.get_rgb_at_position(0)

    def update(self, active_note_info):
        if self.still_holding:
            isInstanceFound = False

            for sensor_info in active_note_info.values():
                for instance in sensor_info:
                    if instance == self.instance:
                        isInstanceFound = True
                        break

            if not isInstanceFound:
                self.still_holding = False

        if self.still_holding:
            current_process = self.current_process

            if current_process == 1:
                self.process1.update()
                self.data = self.process1.report()

                if not self.process1.stopped:
                    return
                else:
                    self.current_process = 2
                    self.process2 = LEDProcessStatic(self.middle_color, self.pixel_nums)
                    self.data = self.process2.report()
        else:
            if current_process == 1:
                self.process1.update()
                self.data = self.process1.report()

                if not self.process1.stopped:
                    return
                else:
                    self.current_process = 3
                    self.process3 = LEDProcessFade(self.gradient2, 0.65*0.5, self.pixel_nums)
                    self.data = self.process3.report()

            elif current_process == 2:
                self.current_process = 3
                self.process3 = LEDProcessFade(self.gradient2, 0.65*0.5, self.pixel_nums)
                self.data = self.process3.report()

            else:
                self.process3.update()
                self.data = self.process3.report()

                if not self.process3.stopped:
                    return
                else:
                    self.stop()

# data: list of tuples (r, g, b)
def write(data):
    print(data)
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

def shift_led_data(data, shift_amount=(4*LEDS_PER_NOTE)): # The beginning of the LED strip is not at sensor 1, so we need to shift the data (binaries). The data is also reversed.
    reversed_list = list(reversed(data))
    shifted_list = reversed_list[shift_amount:] + reversed_list[:shift_amount]
    return shifted_list


def update_with_binaries(binaries): # For debug purposes
    data = []

    binaries = shift_led_data(binaries, 4)

    for note, val in enumerate(binaries):
        color_off = (0, 0, 0)

        for led in range(LEDS_PER_NOTE):
            num_led = note * LEDS_PER_NOTE + led

            if val == 1:
                data.append(rainbow.get_rgb_at_position(num_led / (LED_GROUPS * LEDS_PER_NOTE)))
            else:
                data.append(color_off)

    write(data)

def led_blink1(led_group, dimmed=False):
    process = LEDProcessFade(
        blink_gradient_1 if not dimmed else blink_gradient_1_dimmed,
        0.5,
        [(led_group - 1) * LEDS_PER_NOTE + i + 1 for i in range(LEDS_PER_NOTE)])
    
    led_processes.append(process)

    return process

def led_hold1(led_group, instance, dimmed=False):
    on = on_gradient_1 if not dimmed else on_gradient_1_dimmed
    off = off_gradient_1 if not dimmed else off_gradient_1_dimmed

    process = LEDProcessHold(
        on,
        on.get_rgb_at_position(1),
        off,
        instance,
        [(led_group - 1) * LEDS_PER_NOTE + i + 1 for i in range(LEDS_PER_NOTE)])
    
    led_processes.append(process)

    return process

def update_with_active_note_info(active_note_info: dict):
    data = [] # [{pixel_num: (r, g, b)}, ...]

    for process in led_processes:
        process: LEDProcess
        process.update(active_note_info)
        data.append(process.report())

    for sensor_info in active_note_info.values():
        for instance in sensor_info:
            notes = instance.get_notes()
            instrument = instance.instrument
            
            isInstanceChord = True if len(notes) > 1 else False
            isBurst = is_instrument_burst(instrument)

            if not instance.led_primed:
                instance.set_led_primed()
            else:
                continue

            sensor_number = note_to_sensor(notes[0])

            if isInstanceChord:
                for note in notes:
                    new_process: LEDProcess
                    dimmed = True if note == instance.original_note else False

                    if isBurst:
                        new_process = led_blink1(sensor_number, dimmed)
                    else:
                        new_process = led_hold1(sensor_number, instance, dimmed)

                    led_processes.append(new_process)
                    data.append(new_process.report())
            else:
                new_process: LEDProcess

                if isBurst:
                    new_process = led_blink1(sensor_number)
                else:
                    new_process = led_hold1(sensor_number, instance)

                led_processes.append(new_process)
                data.append(new_process.report())

    data_to_be_merged = [[] for i in range(LEDS_PER_NOTE * LED_GROUPS)]

    for pixel_data in data:
        for pixel_num, pixel_color in pixel_data.items():
            data_to_be_merged[pixel_num - 1].append(colorsys.rgb_to_hsv(*pixel_color))

    final_data = [] # [(r, g, b), ...]

    for hsv_colors in data_to_be_merged:
        if len(hsv_colors) == 0:
            final_data.append((0, 0, 0))
            continue

        # convert the hsv_colors list to a tuple
        average_color = average_hsv(tuple(tuple(row) for row in hsv_colors))
        print("But I caught you red handed:", average_color)

        final_data.append((int(i) for i in colorsys.hsv_to_rgb(*average_color)))

    print("ONE", final_data)
    final_data = shift_led_data(final_data)

    write(final_data)