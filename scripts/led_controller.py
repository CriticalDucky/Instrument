import subprocess
import json
from color import *
from notation import *
from led_util import *
from LEDFade import LEDFade
from LEDHold import LEDHold
from LEDProcess import LEDProcess
import time
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

client_socket.connect((host, 50001))

# Processes can be added to this table, and every frame they will update.
led_processes = []

test = 0
# data: list of tuples (r, g, b)
def write(data):
    # data = [1,1,1]
    data = json.dumps(data)

    # command = ["sudo", "python3", "scripts/led_admin_command.py", data]
    # command2 = ["sudo", "python3", "led_admin_command.py", data]

    # try:
    #     subprocess.run(command, check=True)
    # except subprocess.CalledProcessError as e:
    #     try:
    #         subprocess.run(command2, check=True)
    #     except subprocess.CalledProcessError as e:
    #         print("Error:", e)
    # Ping the system's time before and after the sendall() function to measure the time it takes to send the data
    start = time.time()
    client_socket.sendall(data.encode())
    end = time.time()

    global test

    test += 1

    if end - start > 0.1:
        print(data)
        print(f"Time taken to send data: {end - start} seconds; Num times sent: {test}")

        test = 0
    

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
    process = LEDFade(
        blink_gradient_1 if not dimmed else blink_gradient_1_dimmed,
        0.5,
        [(led_group - 1) * LEDS_PER_NOTE + i + 1 for i in range(LEDS_PER_NOTE)])
    
    led_processes.append(process)

    return process

def led_hold1(led_group, instance, dimmed=False):
    on = on_gradient_1 if not dimmed else on_gradient_1_dimmed
    off = off_gradient_1 if not dimmed else off_gradient_1_dimmed

    process = LEDHold(
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

        if process.stopped:
            led_processes.remove(process)

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

            if isInstanceChord:
                for note in notes:
                    new_process: LEDProcess
                    dimmed = True if note != instance.original_note else False

                    led_group = OCTAVE_NOTES.index(note[:-1]) + 1

                    if isBurst:
                        new_process = led_blink1(led_group, dimmed)
                    else:
                        new_process = led_hold1(led_group, instance, dimmed)

                    led_processes.append(new_process)
                    data.append(new_process.report())
            else:
                sensor_number = note_to_sensor(notes[0])
                new_process: LEDProcess

                if isBurst:
                    new_process = led_blink1(sensor_number)
                else:
                    new_process = led_hold1(sensor_number, instance)

                led_processes.append(new_process)
                data.append(new_process.report())

    data_to_be_merged = [[] for _ in range(LEDS_PER_NOTE * LED_GROUPS)]

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

        final_data.append(tuple(int(i) for i in colorsys.hsv_to_rgb(*average_color)))

    final_data = shift_led_data(final_data)

    write(final_data)