import time
from LEDProcess import LEDProcess

class LEDScheduler:
    def __init__(self):
        self.led_processes = []

    def add_process(self, led_process: LEDProcess, start_time=None):
        self.led_processes.append((led_process, start_time))

    def update_processes(self, progress_time):
        for led_process, start_time in self.led_processes:
            if start_time is None:
                led_process.update(progress_time)
            elif progress_time >= start_time:
                led_process.update(progress_time - start_time)

    def ping(self, progress_time=None):
        if progress_time is None:
            progress_time = time.time()
        results = []
        self.update_processes(progress_time)
        for led_process, _ in self.led_processes:
            results.append(led_process.report())
        return results