from LEDProcess import LEDProcess
from color import *
import time

class LEDStatic(LEDProcess):
    def __init__(self, color, pixel_nums, duration=None):
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