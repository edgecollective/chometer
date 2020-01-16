import serial
import time
import os

port='/dev/ttyACM0'

ard = serial.Serial(port,9600,timeout=5)
time.sleep(2)

f = open("out.csv","a+")
while True:
    msg=ard.readline().strip('\r\n')
    print(msg)
    f.write(msg+"\n")
    f.flush()
    os.fsync(f)

    