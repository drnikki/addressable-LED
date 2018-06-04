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

if __name__ == "__main__":
    def rainbow(wait):
        for j in range(384):  # 3 cycles of all 384 colors in the wheel
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Wheel( (i + j) % 384))
            strip.show()   # write all the pixels out
        time.sleep(wait/8000.0)

    # Slightly different, this one makes the rainbow wheel equally distributed
    # along the chain
    def rainbowCycle(wait):
        for j in range(384 * 5):  # 5 cycles of all 384 colors in the wheel
            for i in range(strip.numPixels()):
                # tricky math! we use each pixel as a fraction of the full
                # 384-color wheel (thats the i / strip.numPixels() part)
                # Then add in j which makes the colors go around per pixel
                # the % 384 is to make the wheel cycle around
                strip.setPixelColor(i, Wheel( ((i * 384 / strip.numPixels())
                    + j) % 384) )
            strip.show()   # write all the pixels out
        time.sleep(wait/8000.0)

    # fill the dots one after the other with said color
    # good for testing purposes
    def colorWipe(c, wait):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, c)
            strip.show()
        time.sleep(wait/8000.0)

    # Chase a dot down the strip
    # good for testing purposes
    def colorChase(c, wait):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, 0)  # turn all pixels off

        for i in range(strip.numPixels()):
            strip.setPixelColor(i, c)
            if i == 0:
                strip.setPixelColor(strip.numPixels()-1, 0)
            else:
                strip.setPixelColor(i-1, 0)
            strip.show()
        time.sleep(wait/8000.0)

    # Helper functions

    #Input a value 0 to 384 to get a color value.
    #The colours are a transition r - g -b - back to r

    def Wheel(WheelPos):
        wp = int(WheelPos / 128)
        if wp == 0:
            r = 127 - WheelPos % 128   #Red down
            g = WheelPos % 128      # Green up
            b = 0                  #blue off
        elif wp == 1:
            g = 127 - WheelPos % 128  #green down
            b = WheelPos % 128      #blue up
            r = 0                  #red off
        elif wp == 2:
            b = 127 - WheelPos % 128  #blue down
            r = WheelPos % 128      #red up
            g = 0                  #green off
        return strip.color(r,g,b)
