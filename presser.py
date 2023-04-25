import machine
import time 
import math
sensor_vol=machine.ADC(0)
factor=5/65535
while True:
    presser=sensor_vol.read_u16()
    print(presser*factor)
    time.sleep(0.2)