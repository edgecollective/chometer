import requests 
import time
from random import seed
from random import random

seed(1)

PRIVATE_KEY = 'a123'

API_ENDPOINT = "http://localhost:8001/api/user"
#API_ENDPOINT = 'http://64.227.0.108:8001/api/user'

sensorA=1.5
sensorB=1.5
sensorC=1.5

while True:

    sensorA = sensorA+2*random()-1
    sensorB = sensorB+2*random()-1
    sensorC = sensorC+2*random()-1

    print(sensorA,sensorB,sensorC)

    data = {'private_key':PRIVATE_KEY, 
            'sensorA':sensorA, 
            'sensorB':sensorB,
            'sensorC':sensorC
            } 

    r = requests.post(url = API_ENDPOINT, json = data) 

    print('posted')

    time.sleep(.1)
