from bibliopixel import *
import bibliopixel.colors as colors
from bibliopixel.drivers import LPD8806 as LPD8806
from bibliopixel import log
log.setLogLevel(log.DEBUG)
import time
import csv
import random

# time in seconds.
COMPOSITION_TIME = 600.00
month_window = COMPOSITION_TIME / 12.00

PINCOUNT = 320

driver = LPD8806.DriverLPD8806(PINCOUNT)
led = LEDStrip(driver)



def lightUp(color, location, duration):
    led.set(location, color)
    led.update()
    time.sleep(duration) #how long the light is on
    led.set(location, (0,0,0))
    led.update()



def getLEDColor(event):
    # https://github.com/ManiacalLabs/BiblioPixel2/wiki/Colors-Module
    c = (0,0,255)
    
    # light purpley: ((0,255,255))
# blue: ((0,0,255))
# turquoise: (255,0,255))
# red: (0,255, 0)

        
    if (event["Race"] == "White"):
        c = (255,255,255)
    if (event["Race"] == "Mexican"):
        c = (255,0,255)
    if (event["Race"] == "Indian" or event["Race"] == "navajo"):
        c = (0,255,255)
        
    if(event["Age"] > 18):
        c = colors.color_scale(c, 50)
    else:
        c = colors.color_scale(c, 100)
        
    return c


def getLEDLocation(event):
    return random.randint(1,PINCOUNT)


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


##
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
    led.fill(colors.Indigo)
    led.update()
    time.sleep(2)
    led.all_off()
    led.update()

## FORMAT g, r, b 
# green = (127,0,0)
# yellowish green = (255,255,0)
# white: (255,255,255)
# light purpley: ((0,255,255))
# blue: ((0,0,255))
# turquoise: (255,0,255))
# red: (0,255, 0)

led.fill((0,255, 0))
c=colors.color_scale((0,255,0), 50)
led.update()
##led.all_off()
time.sleep(2)
led.fill(c)
led.update()
led.all_off()
time.sleep(2)
led.update()




