import csv
import random
import time
from LPD8806 import LPD8806

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
  #  for i in range(strip.numPixels()):
    #    strip.setPixelColor(i, 0)  # turn all pixels off

   # for i in range(strip.numPixels()):
    strip.setPixelColor(location, color)
       # if i == 0:
       #     strip.setPixelColor(strip.numPixels()-1, 0)
       # else:
            #strip.setPixelColor(i-1, 0)
    # need to wait the duration of the event
    time.sleep(duration)
    # then turn the location off
    strip.setPixelColor(location, 0)

    strip.show()


def getLEDColor(event):
    r = random.randint(1,256)
    g = random.randint(1,256)
    b = random.randint(1,256) 
    
    return strip.color(r,g,b)


def getLEDLocation(event):
    return random.randint(1,160)

# time in milliseconds.
COMPOSITION_TIME = 600000
month_window = COMPOSITION_TIME / 12

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

# for JANUARY
for key, value in month.iteritems():
    print key


deathevents = len(month[1])
print deathevents
print month_window
time_per_death_event = month_window/deathevents
print "death time"
print time_per_death_event
time_per_death_event = .05
allOff()

### for each death event
##for event in month['January']:
##    print event
##    color = getLEDColor(event)
##    print color
##    location = getLEDLocation(event)
##    duration = time_per_death_event
####    lightUp(color, location, duration)
##
for i in range(1,12): #number of month numbers in the document
    print i
    themonth = month[str(i)]
    for event in themonth:
        print event
        color = getLEDColor(event)
        print color
        location = getLEDLocation(event)
        duration = time_per_death_event
        lightUp(color, location, duration)







### for each death event
##for event in month['February']:
##    print event
##    color = getLEDColor(event)
##    print color
##    location = getLEDLocation(event)
##    duration = time_per_death_event
##    lightUp(color, location, duration)



allOff()




