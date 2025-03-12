import time
from LEDProcess import *
from data.song_settings import *

class LEDScheduler:
    def __init__(self):
        self.led_processes = []

    def add_process(self, led_process: LEDProcess):
        self.led_processes.append(led_process)

    def update_processes(self):
        for led_process in self.led_processes:
            if led_process.stopped:
                self.led_processes.remove(led_process)
                continue

            led_process.update()

            if led_process.stopped:
                self.led_processes.remove(led_process)
                continue

    def report(self):
        results = [] # list of dicts: [{pixel_num: (r, g, b)}]
        self.update_processes()
        for led_process in self.led_processes:
            results.append(led_process.report())
        return results

def begin():
    start_time = time.time()

    led_scheduler = LEDScheduler()

    led_scheduler.add_process(LEDStatic((200, 0, 0), [n for n in range(0, 155)], 10, start_time))

    return led_scheduler