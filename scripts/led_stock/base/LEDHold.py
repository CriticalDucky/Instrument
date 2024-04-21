from LEDProcess import LEDProcess
from scripts.utilities.color import *
from led_stock.base.LEDFade import LEDFade
from led_stock.base.LEDStatic import LEDStatic
import time

class LEDHold(LEDProcess):
    def __init__(self, gradient1, middle_color, gradient2, instance, pixel_nums):
        super().__init__("LedHold")
        self.gradient1 = gradient1
        self.middle_color = middle_color
        self.gradient2 = gradient2
        self.instance = instance
        self.pixel_nums = pixel_nums
        self.still_holding = True

        self.process1 = LEDFade(gradient1, 0.32*0.5, pixel_nums)
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