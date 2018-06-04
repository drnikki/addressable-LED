import csv

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
        if row['Month'] in month:
            month[row['Month']].append(row)
        else:
            month[row['Month']] = []
            month[row['Month']].append(row)

#print month

# for JANUARY
deathevents = len(month['January'])
print deathevents
print month_window
time_per_death_event = month_window/deathevents
print time_per_death_event



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
