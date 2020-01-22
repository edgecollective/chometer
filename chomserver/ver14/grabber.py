import serial
import requests 
import time

PORT='/dev/ttyACM0'

s=serial.Serial(PORT,115200,timeout=1)

sensorValue='sensorA'
PRIVATE_KEY = 'a123'

JSON_POST_URL = "http://157.245.241.239:8002/api/reading"


while True:

    try:

        line=s.readline()
        p=line.split(":")
        if len(p)==2:
            print(p)
            distance=float(p[1].strip())
            if(distance>5.):
                print(distance)
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':distance}
                r = requests.post(url = JSON_POST_URL, json = data)
                print('posted') 
            s.flushInput() 
    except Exception as e:
        print("error: "+str(e))
