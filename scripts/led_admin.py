#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import socket
import sys
import json

# LED strip configuration:
LED_COUNT      = 156      # Number of LED pixels.
LED_PIN        = 13      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

print(1)

def use_data(data):
    for idx, val in enumerate(data):
        strip.setPixelColor(idx, Color(val[0], val[1], val[2]))
        
    strip.show()
    print("Data sent to strip")
try:
    # Bind to the port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 50001))
    server_socket.listen(1)

    print(2)

    conn, addr = server_socket.accept()
    print('Got connection from', addr)

    received_data = ''

    # Check if the data *has* a full list (this list contains lists within it, so check for [[).
    def is_there_full_list(data: str):
        if ']]' in data:
            return data[:data.index(']]')+2]
        else:
            return None

    while True:
        chunk = conn.recv(1024)  # Adjust buffer size as needed
        # if not chunk and string ends with a closing 
        if not chunk:
            break

        received_data += chunk.decode('utf-8')

        # Check if the data *has* a full list (this list contains lists within it, so check for [[).

        full_list = is_there_full_list(received_data)

        if full_list:
            data = full_list

            # Remove the full list from the received data

            received_data = received_data[len(full_list):]

            # print(data)

            data = json.loads(data)

            # print('Received', data, type(data))

            use_data(data)

except KeyboardInterrupt:
    print("Ctrl+C pressed. Closing the server...")
    # Close the server socket
    server_socket.close()
    sys.exit(0)
