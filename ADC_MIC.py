from machine import Pin,PWM
from time import sleep
servoPin = PWM(Pin(16))
servoPin.freq(50)
sensor_vol=machine.ADC(1)
conversion_factor = 3.3/65535
y=180/3.3
maxDuty=8000
minDuty=1000

while True:
    vol=sensor_vol.read_u16()*conversion_factor
    vol_a=round(vol,2)
    vol_b=round(vol)
    disp=str(vol_a)
    print(disp)
    newDuty=minDuty+(maxDuty-minDuty)*((sensor_vol.read_u16()*y)/180)
    servoPin.duty_u16(int(newDuty))
    sleep(0.2)
    
    