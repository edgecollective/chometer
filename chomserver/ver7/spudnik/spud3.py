"""Sample code and test for adafruit_in219"""
import board
import busio
import digitalio
from digitalio import DigitalInOut
import gc
import time
import adafruit_hcsr04


SENSOR_ID = 'SensorA'


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

JSON_POST_URL = "http://localhost:8001/api/user"

# esp32

import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests

esp32_cs = DigitalInOut(board.D11)
esp32_ready = DigitalInOut(board.D12)
esp32_reset = DigitalInOut(board.D9)

esp_spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(esp_spi, esp32_cs, esp32_ready, esp32_reset)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT


def connect(essid,password): # note that these are arguments are b'essid' and b'password'
    print("Connecting to AP...")
    while not esp.is_connected:
        try:
            esp.connect_AP(essid, password)
        except RuntimeError as e:
            print("could not connect to AP, retrying: ",e)
            continue
    print("Connected to", str(esp.ssid, 'utf-8'), "\tRSSI:", esp.rssi)

    # Initialize a requests object with a socket and esp32spi interface
    requests.set_socket(socket, esp)


# measure and display loop
connect(WIFI_ESSID,WIFI_PASS)

while True:

    gc.collect()

    try:
  
        distance = sonar.distance
        print((distance,))


        json_data = {'private_key':PRIVATE_KEY, 
            'sensor':SENSOR_ID, 
            'value':distance
        } 
        #json_data={"distance":distance}
        print("Posting to ",JSON_POST_URL)

        response = requests.post(JSON_POST_URL, json=json_data)
        print(response.content)
        response.close()

        print("Done. Sleeping ... ")
        time.sleep(2)


    except Exception as e:

        print("error: "+str(e))
        time.sleep(2)
