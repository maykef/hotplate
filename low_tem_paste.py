import time
import datetime
import sys
import datetime as dt
import board
import busio
import digitalio
import adafruit_max31856
from adafruit_motorkit import MotorKit

# create a spi object
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# allocate a CS pin and set the direction
cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT
thermocouple = adafruit_max31856.MAX31856(spi, cs)
temp_C = thermocouple.temperature


def fan(throttle):
    kit = MotorKit(i2c=board.I2C())
    kit.motor1.throttle = throttle

def heatplate(throttle):
    kit = MotorKit(i2c=board.I2C())
    kit.motor3.throttle = throttle

def temp_print():
    while True:
        print("Temperature: {} C".format(temp_C))
        time.sleep(1)

def soak_time():
    print("Preheat Started")
    while True:
        try:
            thermocouple = adafruit_max31856.MAX31856(spi, cs)
            temp_C = thermocouple.temperature
            if temp_C < 60:
                print("Pre Heat")
                heatplate(1)
                time.sleep(2)
                heatplate(0)
                time.sleep(1)
            elif temp_C < 130:
                print('Soaking 1')
                heatplate(1)
                time.sleep(1)
                heatplate(0)
                time.sleep(6)
            elif temp_C < 138:
                heatplate(1)
                print('Soaking 2')
            elif temp_C < 150:
                print('Reflow')
                heatplate(1)
                time.sleep(1)
                heatplate(0)
                time.sleep(4)
            elif temp_C > 165:
                fan(0.5)
                time.sleep(6)
                fan(1)
                print('Cooling')
        except KeyboardInterrupt:
            heatplate(0)
            break
    sys.exit


soak_time()
