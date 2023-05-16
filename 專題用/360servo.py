from machine import Pin,PWM
from time import sleep
servoPin = PWM(Pin(16))
servoPin.freq(50)

def servo(degrees):
    maxDuty=8000
    minDuty=1000
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servoPin.duty_u16(int(newDuty))
while True:
        servo(50)
        sleep(1)
        servo(100)
        sleep(5)
