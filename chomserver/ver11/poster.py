import requests 
import time
from random import seed
from random import random

seed(1)

PRIVATE_KEY = 'a123'

#API_ENDPOINT = "http://localhost:8001/api/user"
#API_ENDPOINT = 'http://64.227.0.108:8001/api/user'
API_ENDPOINT = 'http://localhost:8001/api/reading'

testvalue = random()

testvalue = 9.

sensorValue='sensorC'

print(testvalue)

data = {'private_key':PRIVATE_KEY, 
        'sensor':sensorValue, 
        'value':testvalue,
        } 

r = requests.post(url = API_ENDPOINT, json = data) 

print('posted')

time.sleep(.1)
