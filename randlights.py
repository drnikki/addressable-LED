import csv
import random
import time
from LPD8806 import LPD8806


# time in seconds.
COMPOSITION_TIME = 600.00
month_window = COMPOSITION_TIME / 12.00

# -------- --------------------------------------------------------------------------------------------------------

# Choose which 2 pins you will use for output. Can be any valid output pins.
dataPin = 20
clockPin = 21

# Set the first variable to the NUMBER of pixels. 32 = 32 pixels in a row
# The LED strips are 32 LEDs per meter but you can extend/cut the strip
strip = LPD8806(160, dataPin, clockPin)

strip.begin()
# Update the strip, to start they are all 'off'
strip.show()

def allOff():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)  # turn all pixels off
    strip.show()

def lightUp(color, location, duration):
    strip.setPixelColor(location, color)
    strip.show()
    time.sleep(duration) #how long the light is on
    strip.setPixelColor(location, 0)
    strip.show()

def allFill(c, wait):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, c)
    strip.show()
    #time.sleep(wait/8000.0)


def getLEDColor(event):
    #r = random.randint(0,127)
    #g = random.randint(0,127)
    #b = random.randint(0,127)
    r = 127
    g = 0
    b = 127
    if (event["Race"] == "White"):
        r = 127
        g = 127
        b = 127
    if (event["Race"] == "Mexican"):
        g=127
        r = 0
        b = 0
    if (event["Race"] == "Indian" or event["Race"] == "navajo"):
        b=127
        r = 1
        g = 1
        
    print "r" + str(r) + "  g" + str(g) + "  b" + str(b)
    return strip.color(r,g,b)


def getLEDLocation(event):
    return random.randint(10,160)


with open('InfluenzaCountingTheDeadUpdated.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    currentMonth = ''
    prevMonth= ''
    month = {}

    # First goal: To have all of the rows of the CSV as items in a list
    # a dictionary of lists keyed by month name.  This will let us count the number of items in the month
    # and also operate on the month's events as a unit.
    for row in reader:
        if row['MonthNum'] == '':
            row['MonthNum'] = 1 #todo, this is hackery.
        if row['MonthNum'] in month:
            month[row['MonthNum']].append(row)
        else:
            month[row['MonthNum']] = []
            month[row['MonthNum']].append(row)

#print month

##
##
##deathevents = len(month[1])
##print deathevents #the number of death events
##print month_window #the amount of time per month
##time_per_death_event = month_window/deathevents
##print "death time"
##print time_per_death_event
##time_per_death_event = .005
##allOff()

### for each death event
##for event in month['January']:
##    print event
##    color = getLEDColor(event)
##    print color
##    location = getLEDLocation(event)
##    duration = time_per_death_event
####    lightUp(color, location, duration)
##
            
allOff()
allFill(strip.color(255,0,0), 10)
allOff()

for i in range(9,12): #number of month numbers in the document
    print i
    themonth = month[str(i)]
    # how much time to we have for each event in this month?
    deathevents = len(themonth)
    time_per_death_event = month_window/deathevents

    for event in themonth:
        print event
        color = getLEDColor(event)
        print color
        location = getLEDLocation(event)
        duration = time_per_death_event
       
        lightUp(color, location, time_per_death_event)

    # at the end of the month, fill with red
    allFill(strip.color(255,0,0), 10)
    allOff()





### for each death event
##for event in month['February']:
##    print event
##    color = getLEDColor(event)
##    print color
##    location = getLEDLocation(event)
##    duration = time_per_death_event
##    lightUp(color, location, duration)



allOff()




