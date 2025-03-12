import time
from LEDProcess import *
from data.song_settings import *

class LEDScheduler:
    def __init__(self):
        self.led_processes = []

    def add_process(self, led_process: LEDProcess):
        self.led_processes.append(led_process)

    def update_processes(self):
        for led_process, _ in self.led_processes:
            led_process.update()

    def report(self):
        results = [] # list of dicts: [{pixel_num: (r, g, b)}]
        self.update_processes()
        for led_process, _ in self.led_processes:
            results.append(led_process.report())
        return results

def begin():
    start_time = time.time()

    led_scheduler = LEDScheduler()

    return led_scheduler