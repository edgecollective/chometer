import requests 
import time
from random import seed
from random import random

seed(1)

MIN_VALUE=40
MAX_VALUE=70

PRIVATE_KEY = 'a123'

#API_ENDPOINT = "http://localhost:8001/api/user"
API_ENDPOINT = 'http://64.227.0.108:8003/api/reading'
#API_ENDPOINT = 'http://localhost:8001/api/reading'

testvalue = random()

testvalue = 2.

sensorValue='sensorA'

print(testvalue)

data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue} 

r = requests.post(url = API_ENDPOINT, json = data) 

print('posted')

time.sleep(.1)

SLEEPTIME=1

while True:  
        for i in range(0,10):
                sensorValue='sensorA'
                testvalue=MIN_VALUE+random()*(MAX_VALUE-MIN_VALUE)
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                sensorValue='sensorB'
                testvalue=MAX_VALUE+random()*100.
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                sensorValue='sensorC'
                testvalue=MAX_VALUE+random()*100.
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                time.sleep(SLEEPTIME)

        for i in range(0,10):
                sensorValue='sensorA'
                testvalue=MAX_VALUE+random()*100.
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                sensorValue='sensorB'
                testvalue=MIN_VALUE+random()*(MAX_VALUE-MIN_VALUE)
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                sensorValue='sensorC'
                testvalue=MAX_VALUE+random()*100.
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                time.sleep(SLEEPTIME)


        for i in range(0,10):
                sensorValue='sensorA'
                testvalue=MAX_VALUE+random()*100.
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                sensorValue='sensorB'
                testvalue=MAX_VALUE+random()*100.
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                sensorValue='sensorC'
                testvalue=MIN_VALUE+random()*(MAX_VALUE-MIN_VALUE)
                data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':testvalue}
                r = requests.post(url = API_ENDPOINT, json = data)

                time.sleep(SLEEPTIME)
