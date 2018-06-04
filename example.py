import LPD8806



# Example to control LPD8806-based RGB LED Modules in a strip


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


# Choose which 2 pins you will use for output.
# Can be any valid output pins.
dataPin = 20
clockPin = 21

# Set the first variable to the NUMBER of pixels. 32 = 32 pixels in a row
# The LED strips are 32 LEDs per meter but you can extend/cut the strip
strip = LPD8806(32, dataPin, clockPin)

strip.begin()

# Update the strip, to start they are all 'off'
strip.show()

while True:
    colorChase(strip.color(127,127,127), 10)

    # Send a simple pixel chase in...
    colorChase(strip.color(127,0,0), 10)         # full brightness red
    colorChase(strip.color(127,127,0), 10)       # orange
    colorChase(strip.color(0,127,0), 10)         # green
    colorChase(strip.color(0,127,127), 10)       # teal
    colorChase(strip.color(0,0,127), 10)         # blue
    colorChase(strip.color(127,0,127), 10)       # violet

    # fill the entire strip with...
    colorWipe(strip.color(127,0,0), 10)          # red
    colorWipe(strip.color(0, 127,0), 10)         # green
    colorWipe(strip.color(0,0,127), 10)                # blue

    colorChase(strip.color(127,127,127), 0)
    rainbow(10)
    colorChase(strip.color(127,127,127), 0)
    rainbowCycle(0)  # make it go through the cycle fairly fast
