from machine import Pin
from time import sleep
led1=Pin(25,Pin.OUT)
led2=Pin(15,Pin.OUT)
led3=Pin(14,Pin.OUT)
button=Pin(11,PinIN,Pin.PULL_UP)
leds=[led1,led2,led3]
while True:
    for i in range(0,3):
        print(leds[i])
        leds[i].on()
        sleep(0.5)
        leds[i].off()
        sleep(0.5)