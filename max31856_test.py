import board
import time
import datetime
import sys
import busio
import digitalio
import adafruit_max31856

# create a spi object
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# allocate a CS pin and set the direction
cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT

# Create header row in new CSV file
filename = "temp_log.csv"
csv = open(filename, 'w')
csv.write("Timestamp,Temperature\n")
csv.close

# Create a loop to check for the temp value every second and log it into the spreadsheet
while True:
    try:
        # create a thermocouple object with the above
        thermocouple = adafruit_max31856.MAX31856(spi, cs)
        temp_C = thermocouple.temperature
        temp_c = str(temp_C)
        entry = str(datetime.datetime.now())
        entry = entry + ", " + temp_c + " C" + "\n"
        csv = open(filename, 'a')
        csv.write(entry)
        # print the temperature!
        print("Temperature: {} C".format(temp_C))
        time.sleep(1.0)
    except KeyboardInterrupt:
        print("Exciting and saving file")
        csv.close()
        break

sys.exit()
