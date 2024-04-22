from LEDProcess import LEDProcess
from utilities.color import *
import time

class LEDFade(LEDProcess):
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