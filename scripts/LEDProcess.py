from color import *
from led_util import *
import time

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

class LEDFade(LEDProcess):
    def __init__(self, gradient: Gradient, duration, pixel_nums, start_time=None):
        super().__init__("LedFade")
        self.duration = duration
        self.start_time = start_time if start_time is not None else time.time()
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

# pixel_nums is a list of pixel numbers: [0, 1, 2, 3, 4]
class LEDStatic(LEDProcess):
    def __init__(self, color, pixel_nums, duration=None, start_time=None):
        super().__init__("LedStatic")
        self.color = color
        self.duration = duration
        self.start_time = start_time if start_time is not None else time.time()
        self.time = 0

        for pixel_num in pixel_nums:
            self.data[pixel_num] = color

    def update(self):
        if not self.duration: return

        self.time = time.time() - self.start_time

        if self.time >= self.duration:
            self.stop()

class LEDHold(LEDProcess):
    def __init__(self, gradient1, middle_color, gradient2, instance, pixel_nums, start_time=None):
        super().__init__("LedHold")
        self.gradient1 = gradient1
        self.middle_color = middle_color
        self.gradient2 = gradient2
        self.instance = instance
        self.pixel_nums = pixel_nums
        self.still_holding = True

        self.process1 = LEDFade(gradient1, 0.32*0.5, pixel_nums, start_time)
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
                    self.process2 = LEDStatic(self.middle_color, self.pixel_nums)
                    self.data = self.process2.report()
        else:
            current_process = self.current_process

            if current_process == 1:
                self.process1.update()
                self.data = self.process1.report()

                if not self.process1.stopped:
                    return
                else:
                    self.current_process = 3
                    self.process3 = LEDFade(self.gradient2, 0.65, self.pixel_nums)
                    self.data = self.process3.report()

            elif current_process == 2:
                self.current_process = 3
                self.process3 = LEDFade(self.gradient2, 0.65, self.pixel_nums)
                self.data = self.process3.report()

            else:
                self.process3.update()
                self.data = self.process3.report()

                if not self.process3.stopped:
                    return
                else:
                    self.stop()

class FullIllumination(LEDProcess): #
    def __init__(self, gradient: Gradient, duration, start_time=None):
        super().__init__("FullIllumination")
        self.start_time = start_time if start_time is not None else time.time()
        self.duration = duration
        self.gradient = gradient
        self.time = 0

    def update(self):
        # only update if the current time has reached the start time
        if time.time() < self.start_time:
            return
        
        self.time = time.time() - self.start_time

        for pixel_num in range(LED_GROUPS*LEDS_PER_NOTE):
            self.data[pixel_num] = self.gradient.get_rgb_at_position(self.time / self.duration)

        if self.time >= self.duration:
            self.stop()

class FullRotatingGradient(LEDProcess):
    """
    This one takes a gradient and rotates it around the LEDs. The lights fade in and out at the beginning and end of the rotation. Duration is specified.
    The gradient is cropped such that the first color is at the beginning of the rotation and the last color is at the end of the rotation (156 LEDs).
    num_loops is the number of full rotations of the gradient. For example, if num_loops is 2, the gradient will be rotated twice around the LEDs during the duration.
    Note that that LED 1 is adjacent to LED 156, so the gradient is rotated such that LED 1 is at the beginning of the gradient and LED 156 is at the end of the gradient.
    """
    def __init__(self, gradient: Gradient, duration, num_loops, start_time=None):
        super().__init__("FullRotatingGradient")
        self.start_time = start_time if start_time is not None else time.time()
        self.duration = duration
        self.gradient = gradient
        self.num_loops = num_loops
        self.time = 0

    def update(self):
        # only update if the current time has reached the start time
        if time.time() < self.start_time:
            return
        
        self.time = time.time() - self.start_time

        for pixel_num in range(LED_GROUPS*LEDS_PER_NOTE):
            # calculate the resulting color for each pixel using the gradient, duration, and num_loops parameter
            position = (self.time / self.duration * self.num_loops + pixel_num / (LED_GROUPS*LEDS_PER_NOTE)) % 1
            result_color = self.gradient.get_rgb_at_position(position)
            # now we need to fade the color in and out at the beginning and end of the rotation
            if self.time < 0.5:
                fade_in = self.time / 0.5
                result_color = tuple(int(c * fade_in) for c in result_color)
            elif self.time > self.duration - 0.5:
                fade_out = (self.duration - self.time) / 0.5
                result_color = tuple(int(c * fade_out) for c in result_color)
            
            self.data[pixel_num] = result_color

        if self.time >= self.duration:
            self.stop()
        