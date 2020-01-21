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

WIFI_ESSID=secrets['ssid']
WIFI_PASS=secrets['password']
PRIVATE_KEY=secrets['privkey']

print("PK=",PRIVATE_KEY)

#JSON_POST_URL = 'http://64.227.0.108:8001/api/user'
#JSON_POST_URL = 'http://localhost:8001/api/user'

#JSON_POST_URL = "http://localhost:8001/api/user"
#JSON_POST_URL = "http://localhost:8001/api/reading"
#JSON_POST_URL = "http://192.168.1.254:8001/api/reading"
#JSON_POST_URL = "http://64.227.0.108:8002/api/reading"

JSON_POST_URL = "http://157.245.241.239:8002/api/reading"

# esp32

import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
#import adafruit_requests as requests
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

esp32_cs = DigitalInOut(board.D11)
esp32_ready = DigitalInOut(board.D12)
esp32_reset = DigitalInOut(board.D9)

esp_spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(esp_spi, esp32_cs, esp32_ready, esp32_reset)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# status_light = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
# Uncomment below for an externally defined RGB LED

import adafruit_rgbled
from adafruit_esp32spi import PWMOut
RED_LED = PWMOut.PWMOut(esp, 26)
GREEN_LED = PWMOut.PWMOut(esp, 27)
BLUE_LED = PWMOut.PWMOut(esp, 25)
status_light = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

def blink(num_times):
    for i in range(0,num_times):
        led.value=True
        time.sleep(.1)
        led.value = False
        time.sleep(.1)

while True:

    try:

        time.sleep(.2)
        distance = sonar.distance
        blink(1)

        json_data = {'private_key':PRIVATE_KEY, 
        'sensor':SENSOR_ID, 
        'value':distance
        }

        print(json_data)

        response = wifi.post(JSON_POST_URL,json=json_data)
        print(response.json())
        #print(response)
        #response.close()

        print('hello')
        time.sleep(LAG_PERIOD)

    except (ValueError, RuntimeError) as e:

        print("Failed to get data, retrying\n", e)
        wifi.reset()
        time.sleep(1)
        continue

        #print("error: "+str(e))
        #time.sleep(2)
