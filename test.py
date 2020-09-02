import serial

import time
serCOM3 = serial.Serial("COM3", 9600, timeout=1, write_timeout=2)


serCOM3.write(b'r')     # write a string
time.sleep(0.2)

try:
    while(True):
        time.sleep(0.4)
        a = serCOM3.read_until(b';')
        lido = int(a.decode("utf-8").split(';')[0])
        percentual = (lido - 2730)/(1366) * 100
        print(lido)
        print(percentual)
except KeyboardInterrupt:
    serCOM3.close()
# close port
