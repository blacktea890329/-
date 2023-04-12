from machine import Pin,PWM
from time import sleep
servoPin = PWM(Pin(16))
servoPin.freq(50)

def servo(degrees):
    if degrees>180:
        degress=180
    if degrees<0:
        degrees=0
    maxDuty=8000
    minDuty=1000
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servoPin.duty_u16(int(newDuty))
while True:
    for degree in range(0,180,1):
        servo(degree)
        sleep(0.01)
    for degree in range(180,0,-1):
        servo(degree)
        sleep(0.01)