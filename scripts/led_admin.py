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

try:
    # Bind to the port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(socket.gethostname(), 50001)
    server_socket.listen(5)

    while True:
        # Accept connections
        client_socket, addr = server_socket.accept()
        print('Got connection from', addr)

        data = client_socket.recv(1024).decode()
        data = json.loads(data)

        for idx, val in enumerate(data):
            strip.setPixelColor(idx, Color(val[0], val[1], val[2]))
            strip.show()

except KeyboardInterrupt:
    print("Ctrl+C pressed. Closing the server...")
    # Close the server socket
    server_socket.close()
    sys.exit(0)
