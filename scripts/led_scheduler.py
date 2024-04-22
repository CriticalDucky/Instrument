import time

class LEDScheduler:
    def __init__(self):
        self.led_processes = []

    def add_process(self, led_process):
        self.led_processes.append(led_process)

    def remove_process(self, led_process):
        if led_process in self.led_processes:
            self.led_processes.remove(led_process)

    def update_processes(self, progress_time):
        for led_process in self.led_processes:
            led_process.update(progress_time)

    def ping(self, progress_time=None):
        if progress_time is None:
            progress_time = time.time()
        results = []
        self.update_processes(progress_time)
        for led_process in self.led_processes:
            results.append((led_process.name, led_process.report()))
        return results