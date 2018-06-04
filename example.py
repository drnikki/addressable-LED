import LPD8806

# Example to control LPD8806-based RGB LED Modules in a strip

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
