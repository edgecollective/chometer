import serial
import requests 
import time

import sys
import glob


sensorValue='sensorA'
PRIVATE_KEY = 'a123'

JSON_POST_URL = "http://157.245.241.239:8002/api/reading"

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

print(serial_ports())


while True:

    time.sleep(.1)
    try:
        # find a serial port
        PORT=serial_ports()[0]
        if len(PORT)>0:
            print(PORT)
            s=serial.Serial(PORT,115200,timeout=1)
            time.sleep(.1)
            line=s.readline()
            p=line.split(":")
            if len(p)==2:
                print(p)
                distance=float(p[1].strip())
                if(distance>5.):
                    print(distance)
                    data = {'private_key':PRIVATE_KEY, 'sensor':sensorValue, 'value':distance}
                    print(data)
                    r = requests.post(url = JSON_POST_URL, json = data)
                    print('posted') 
            s.flushInput()
            s.close()

    except Exception as e:
        print("error: "+str(e))