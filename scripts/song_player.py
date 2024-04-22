import pygame
import os
import time
from led_scheduler import LEDScheduler

current_dir = os.path.dirname(__file__)
audio_file = os.path.join(current_dir, "song.mp3")
# led_scheduler = led_scheduler
start_time = None
current_time = 0
playing = False

def start():
    global start_time, playing
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    start_time = time.time()  # Track the start time
    playing = True
    print("Playing audio...")

def stop():
    global start_time, playing, current_time
    pygame.mixer.music.stop()
    playing = False
    start_time = None  # Reset start time
    current_time = 0
    print("Audio stopped.")

def update_current_time():
    global current_time
    if start_time is not None:
        elapsed_time = time.time() - start_time
        current_time = elapsed_time
    else:
        current_time = 0

# def get_led_data():
#     update_current_time()  # Update current time before getting LED data
#     led_data = led_scheduler.ping(current_time)
#     return led_data
