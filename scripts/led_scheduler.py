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
    start_time = time.time() + 0.2 #delay to account for initial delay in start of song

    led_scheduler = LEDScheduler()

    amber_gradient = Gradient()
    amber_gradient.add_stop(0.0, (255, 81, 0))
    amber_gradient.add_stop(0.5, (255, 0, 0))
    amber_gradient.add_stop(1.0, (0, 0, 0))

    time_base1 = start_time + 1

    led_scheduler.add_process(FullIllumination(amber_gradient, 1, time_base1))
    led_scheduler.add_process(FullIllumination(amber_gradient, 1, time_base1 + 2*HTPF_SPB))
    led_scheduler.add_process(FullIllumination(amber_gradient, 1, time_base1 + 4*HTPF_SPB))
    led_scheduler.add_process(FullIllumination(amber_gradient, 1, time_base1 + 6*HTPF_SPB))

    time_base2 = start_time + 6.875

    chord_sequence1_gradient = Gradient()

    stops = [
        (0, (0, 0, 0)),          # Black (Fade-in Start)
        (2, (194, 0, 255)),      # Main Color Start
        (25, (194, 0, 255)),     # Holding Purple
        (27, (57, 0, 255)),      # Transition to Deep Blue
        (50, (57, 0, 255)),      # Holding Deep Blue
        (52, (0, 166, 255)),     # Transition to Cyan
        (75, (0, 166, 255)),     # Holding Cyan
        (77, (57, 0, 255)),      # Transition Back to Deep Blue
        (98, (57, 0, 255)),      # Holding Deep Blue Before Fade
        (100, (0, 0, 0))         # Black (Fade-out End)
    ]

    for position, color in stops:
        chord_sequence1_gradient.add_stop(position / 100, color)

    chord_sequence1_gradient.set_brightness(0.5)

    led_scheduler.add_process(FullIllumination(chord_sequence1_gradient, HTPF_SPB*16, time_base2))
    #repeat
    led_scheduler.add_process(FullIllumination(chord_sequence1_gradient, HTPF_SPB*16, time_base2 + HTPF_SPB*16))
    #once more
    led_scheduler.add_process(FullIllumination(chord_sequence1_gradient, HTPF_SPB*16, time_base2 + HTPF_SPB*32))

    time_base3 = start_time + 46.875

    warm_gradient_stops = [
        (0, (0, 0, 0)),           # Black
        (6, (255, 121, 0)),       # Bright Orange
        (25, (255, 160, 0)),      # Yellow-Orange
        (50, (255, 0, 0)),        # Deep Red
        (56, (255, 121, 0)),      # Bright Orange Again
        (75, (255, 160, 0)),      # Yellow-Orange Again
        (88, (220, 53, 0)),       # Deep Orange-Red
        (100, (0, 0, 0))          # Black
    ]

    warm_gradient = Gradient()
    for position, color in warm_gradient_stops:
        warm_gradient.add_stop(position / 100, color)

    warm_gradient.set_brightness(0.5)
    led_scheduler.add_process(FullIllumination(warm_gradient, HTPF_SPB*16, time_base3))

    time_base4 = start_time + 60

    cool_gradient_stops = [
        (0, (131, 58, 180)),      # Purple
        (25, (253, 29, 29)),      # Red
        (50, (252, 176, 69)),     # Orange-Yellow
        (75, (253, 29, 29)),      # Red Again
        (100, (131, 58, 180))     # Purple Again
    ]
    cool_gradient = Gradient()
    for position, color in cool_gradient_stops:
        cool_gradient.add_stop(position / 100, color)

    cool_gradient.set_brightness(0.5)

    talk_gradient1 = Gradient()
    talk_gradient1.add_stop(0.0, (255, 121, 0))
    talk_gradient1.add_stop(0.5, (255, 0, 0))
    talk_gradient1.add_stop(1.0, (0, 0, 0))

    ghost_gradient = Gradient()
    ghost_gradient.add_stop(0.0, (255, 255, 255))
    ghost_gradient.add_stop(1, (0, 0, 0))

    led_scheduler.add_process(FullRotatingGradient(cool_gradient, HTPF_SPB*8, 2, time_base4))

    led_scheduler.add_process(FullIllumination(talk_gradient1, HTPF_SPB*2, time_base4 + HTPF_SPB*8))
    led_scheduler.add_process(FullIllumination(talk_gradient1, HTPF_SPB*2, time_base4 + HTPF_SPB*10))
    led_scheduler.add_process(FullIllumination(talk_gradient1, HTPF_SPB*2, time_base4 + HTPF_SPB*12))
    led_scheduler.add_process(FullIllumination(talk_gradient1, HTPF_SPB*2, time_base4 + HTPF_SPB*14))

    led_scheduler.add_process(FullIllumination(ghost_gradient, 2, time_base4 + HTPF_SPB*16))

    time_base5 = start_time + 60 + 14.8

    blood_gradient = Gradient()
    blood_gradient.add_stop(0.0, (255, 0, 0))
    blood_gradient.add_stop(1.0, (0, 0, 0))

    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + HTPF_SPB/4))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + 5*HTPF_SPB/4))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + 6*HTPF_SPB/4))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + 7*HTPF_SPB/4))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + 12*HTPF_SPB/4))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + 13*HTPF_SPB/4))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + 17*HTPF_SPB/4))
    led_scheduler.add_process(FullIllumination(blood_gradient, 0.2, time_base5 + 18*HTPF_SPB/4))

    return led_scheduler