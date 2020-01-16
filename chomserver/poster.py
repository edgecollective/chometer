import requests 
import time
from random import seed
from random import random

seed(1)

PRIVATE_KEY = 'a123'

API_ENDPOINT = "http://localhost:8000/api/user"

current=1.5
voltage=1.5
resistance=1.5

while True:

    current = current+2*random()-1
    voltage = voltage+2*random()-1
    resistance = resistance+2*random()-1

    print(current,voltage,resistance)

    data = {'private_key':PRIVATE_KEY, 
            'current':current, 
            'voltage':voltage,
            'resistance':resistance
            } 

    r = requests.post(url = API_ENDPOINT, json = data) 

    print('posted')

    time.sleep(.1)
