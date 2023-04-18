from machine import I2C, Pin,RTC,WDT,reset
from ssd1306 import SSD1306_I2C
from font import Font
import time

sda=machine.Pin(12)
scl=machine.Pin(13)
i2c = I2C(0, scl=scl, sda=sda, freq=400000)
display= SSD1306_I2C(128, 64, i2c)

f=Font(display)

f.text("8",0,0,8)   #8 pix
f.text("16",8,0,16) #16 pix
f.text("24",24,0,24) #24 pix
f.text("32",48,0,32) #32 pix
oled.pixel(100,60,1)
f.show()