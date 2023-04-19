from machine import I2C, Pin,RTC,WDT,reset
from ssd1306 import SSD1306_I2C
from font import Font
from lib.dht import DHT11,InvalidChecksum
import utime as time

sda=machine.Pin(12)
scl=machine.Pin(13)
i2c = I2C(0, scl=scl, sda=sda, freq=400000)
display= SSD1306_I2C(128, 64, i2c)
f=Font(display)

pin=Pin(28,Pin.OUT,Pin.PULL_UP)
sensor = DHT11(pin)
while True:
    time.sleep(0.5)
    t = round((sensor.temperature),1)
    h = round(sensor.humidity)
    print("Temperature: {}".format(t))
    print("Humidity: {}".format(h))
    
    T=str(t)
    H=str(h)
    
    f.text("Temperature:{}".format(T),0,0,16) #32 pix
    f.text("Humidity:{}%".format(H),0,20,16) #32 pix
    f.show()
    
    time.sleep(1)