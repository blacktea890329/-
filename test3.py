from machine import Pin
import utime
led1=Pin(25,Pin.OUT)
led2=Pin(15,Pin.OUT)
led3=Pin(14,Pin.OUT)
button=Pin(11,Pin.IN,Pin.PULL_UP)
leds=[led1,led2,led3]
x=0
def change(pin):
    global x
    print(x)
    if(x==0):
        x=x+1
    else:
        x=x-1
while True:
    if(x==0):
        for i in range(0,3):
            print(x)
            leds[i].on()
            utime.sleep(0.1)
            leds[i].off()
            utime.sleep(0.1)
            button.irq(trigger=Pin.IRQ_FALLING,handler=change)
    if(x==1):
        for i in range(2,-1,-1):
            print(x)
            leds[i].on()
            utime.sleep(0.1)
            leds[i].off()
            utime.sleep(0.1)
            button.irq(trigger=Pin.IRQ_FALLING,handler=change)
            #IRQ_FALLING/RISING/LOW_LEVEL/HIGH_LEVEL

