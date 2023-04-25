import time,math
from machine import Pin, PWM
from time import sleep


pin_led = Pin(25, Pin.OUT)
trig = Pin(10, Pin.OUT)
echo = Pin(4, Pin.IN,Pin.PULL_DOWN)
pwm = PWM(Pin(16))
pwm.freq(2500)
pwm.duty_u16(0)

def ping():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    count=0
    timeout=False
    start=time.ticks_us()
    while echo.value() == 0: #wait for HIGH
        start=time.ticks_us()
    while echo.value() : #wait for HIGH
        stop=time.ticks_us()
    duration = stop - start
    dist = ( duration *0.0343) /2
    return dist  
def bi(T):
        pwm.duty_u16(32768)
        time.sleep(0.2)
        pwm.duty_u16(0)
        time.sleep(T)
while True:
    distance = round(ping())
    print("%s cm" %distance)
    if distance >= 30 :
        pwm.duty_u16(0)
        time.sleep(0.5)
    if (distance <= 35) and (distance > 25) :
        bi(0.6)       
    if (distance <= 25) and (distance > 15) :
        bi(0.4)
    if (distance <= 15) and (distance > 8) :
        bi(0.2)
    if (distance <= 8)  :
        pwm.duty_u16(32768)
