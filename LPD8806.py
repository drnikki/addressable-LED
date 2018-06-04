#!/usr/bin/env python
# vim: set ai sw=4 sta fo=croql ts=8 expandtab syntax=python
#Example to control LPD8806-based RGB LED Strips
# Copyright Adafruit industries
# Copyright Russell Nelson, ported to Python
# MIT license
# Source: http://russnelson.com/LPD8806.py

import RPi.GPIO as GPIO
import time

class LPD8806:
    def __init__(self, count, dataPin, clkPin):
        self.d = dataPin
        self.c = clkPin
        self.count = count
        self.pixels = [0] * count * 3
        GPIO.setmode(GPIO.BCM)

    def begin(self):
        GPIO.setup(self.c, GPIO.OUT)
        GPIO.setup(self.d, GPIO.OUT)


    def numPixels(self):
        return self.count

    def color(self, r, g, b):
        #Take the lowest 7 bits of each value and append them end to end
        # We have the top bit set high (its a 'parity-like' bit in the protocol
        # and must be set!)

        x = g | 0x80
        x <<= 8
        x |= r | 0x80
        x <<= 8
        x |= b | 0x80

        return x

    def write8(self, d):
        # Basic, push SPI data out
        for i in range(8):
            GPIO.output(self.d, (d & (0x80 >> i)) <> 0)
            GPIO.output(self.c, True)
            GPIO.output(self.c, False)

    # This is how data is pushed to the strip.
    # Unfortunately, the company that makes the chip didnt release the
    # protocol document or you need to sign an NDA or something stupid
    # like that, but we reverse engineered this from a strip
    # controller and it seems to work very nicely!
    def show(self):
        # get the strip's attention
        self.write8(0)
        self.write8(0)
        self.write8(0)
        self.write8(0)

        # write 24 bits per pixel
        for i in range(self.count):
            self.write8(self.pixels[i*3])
            self.write8(self.pixels[i*3+1])
            self.write8(self.pixels[i*3+2])

        # to 'latch' the data, we send just zeros
        for i in range(self.count * 2):
            self.write8(0)
            self.write8(0)
            self.write8(0)

        # we need to have a delay here, 10ms seems to do the job
        # shorter may be OK as well - need to experiment :(
        time.sleep(0.005)

    # store the rgb component in our array
    def setPixelRGB(self, n, r, g, b):
        if n >= self.count: return
        self.pixels[n*3] = g | 0x80
        self.pixels[n*3+1] = r | 0x80
        self.pixels[n*3+2] = b | 0x80

    def setPixelColor(self, n, c):
        if n >= self.count: return

        self.pixels[n*3] = (c >> 16) | 0x80
        self.pixels[n*3+1] = (c >> 8) | 0x80
        self.pixels[n*3+2] = (c) | 0x80
