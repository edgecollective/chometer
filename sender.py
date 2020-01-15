"""Sample code and test for adafruit_in219"""
import board
import busio
import digitalio
from digitalio import DigitalInOut
import gc
import time
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

SLEEPTIME = 1200

# Get Wifi and FarmOS details
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

WIFI_ESSID=secrets['ssid']
WIFI_PASS=secrets['password']
farmos_pubkey=secrets['farmos_pubkey']
farmos_privkey=secrets['farmos_privkey']

base_url= "https://edgecollective.farmos.net/farm/sensor/listener/"

JSON_POST_URL = base_url+farmos_pubkey+"?private_key="+farmos_privkey

# esp32

import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests

esp32_cs = DigitalInOut(board.D12)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D10)

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


i2c_bus = board.I2C()

ina219 = INA219(i2c_bus)

print("ina219 test")

# display some of the advanced field (just to test)
print("Config register:")
print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
print("  gain:                 0x%1X" % ina219.gain)
print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
print("  mode:                 0x%1X" % ina219.mode)
print("")

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

for i in range(1,2):
    led.value=True
    time.sleep(1)
    led.value = False
    time.sleep(1)
        
# measure and display loop
while True:

    gc.collect()

    try:

        bus_voltage = ina219.bus_voltage        # voltage on V- (load side)
        shunt_voltage = ina219.shunt_voltage    # voltage between V+ and V- across the shunt
        current = ina219.current                # current in mA

        # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
        print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
        print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
        print("Load Voltage:  {:6.3f} V".format(bus_voltage))
        print("Current:       {:9.6f} A".format(current/1000))
        print("")

        json_data={"shunt_voltage_V":shunt_voltage,"current_mA":current,"bus_voltage_V":bus_voltage}
        print("Posting to ",JSON_POST_URL)

        connect(WIFI_ESSID,WIFI_PASS)
        response = requests.post(JSON_POST_URL, json=json_data)
        print(response.content)
        response.close()

        print("Done. Sleeping ... ")
        for i in range(1,3):
            led.value=True
            time.sleep(.1)
            led.value = False
            time.sleep(.1)

    except Exception as e:

        print("error: "+str(e))

    time.sleep(90)
