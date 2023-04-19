from machine import I2C, Pin,RTC,WDT,reset
from ssd1306 import SSD1306_I2C
from font import Font
import time
import math
led1=Pin(14,Pin.OUT)
led2=Pin(15,Pin.OUT)
sensor_temp=machine.ADC(4)
conversion_factor = 3.3/65535
sda=machine.Pin(12)
scl=machine.Pin(13)
i2c = I2C(0, scl=scl, sda=sda, freq=400000)
display= SSD1306_I2C(128, 64, i2c)
f=Font(display)

while True:
    reading=sensor_temp.read_u16()*conversion_factor
    temp = round(27-(reading-0.706)/0.001721,2)
    print(temp)
    T=str(temp)
    f.text(T,0,0,24) #24 pix
    f.show()
    if temp>22:
        led1.on()
        led2.off()
    elif temp<20:
        led2.on()
        led1.off()
    else:
        led1.off()
        led2.off()
    time.sleep(0.1)