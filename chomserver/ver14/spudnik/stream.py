"""Sample code and test for adafruit_in219"""
import board
import busio
import digitalio
from digitalio import DigitalInOut
import gc
import time
import adafruit_hcsr04
import neopixel


SENSOR_ID = 'sensorA'
APPROACH_THRESHOLD = 50. # cm
RETREAT_THRESHOLD = 100. # cm
LAG_PERIOD = 1  # seconds
SENSOR_MINIMUM = 20.

CUSTOMER = 0.  # False
start_time = 0.
end_time = 0.

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D10, echo_pin=board.D7)

SLEEPTIME = 1200

# Get Wifi and FarmOS details
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# status_light = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
# Uncomment below for an externally defined RGB LED

def blink(num_times):
    for i in range(0,num_times):
        led.value=True
        time.sleep(.1)
        led.value = False
        time.sleep(.1)

while True:

    try:

        #time.sleep(.2)
        distance = sonar.distance
        print("d:"+str(distance))

        blink(.05)

    except (ValueError, RuntimeError) as e:

        print("Failed to get data, retrying\n", e)
        #wifi.reset()
        #time.sleep(1)
        continue

        #print("error: "+str(e))
        #time.sleep(2)
