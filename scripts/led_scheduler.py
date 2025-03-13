import time
from LEDProcess import *
from data.song_settings import *
from color import *

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

    amber_gradient = Gradient()
    amber_gradient.add_stop(0.0, (255, 81, 0))
    amber_gradient.add_stop(0.5, (255, 0, 0))
    amber_gradient.add_stop(1.0, (0, 0, 0))

    time_base1 = start_time + 1

    led_scheduler.add_process(FullIllumination(amber_gradient, 2*HTPF_SPB, time_base1))
    led_scheduler.add_process(FullIllumination(amber_gradient, 2*HTPF_SPB, time_base1 + 2*HTPF_SPB))
    led_scheduler.add_process(FullIllumination(amber_gradient, 2*HTPF_SPB, time_base1 + 4*HTPF_SPB))


    return led_scheduler