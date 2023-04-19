from machine import Pin, UART,I2C,RTC,WDT,reset
import os, sys
import utime
import machine
from ssd1306 import SSD1306_I2C
from font import Font
from lib.dht import DHT11, InvalidChecksum
print(os.uname())

sda=machine.Pin(12)
scl=machine.Pin(13)
i2c = I2C(0, scl=scl, sda=sda, freq=400000)
display= SSD1306_I2C(128, 64, i2c)
f=Font(display)

led = machine.Pin(25, machine.Pin.OUT)
led1 = machine.Pin(14, machine.Pin.OUT)
led2 = machine.Pin(15, machine.Pin.OUT)
led1.value(0)
led2.value(0)
led.value(0)
#sensor_temp=machine.ADC(4)
#conversion_factor = 3.3 / 65535
pin = Pin(28, Pin.OUT, Pin.PULL_UP)
sensor = DHT11(pin)
lens = str(len('GET /update?api_key=SR41LE48B63EN79L&field1="+temp+"&field2="+temp+"\r\n'))
print(lens)
#functions
def sendCMD_waitResp(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd.encode('utf-8'))
    waitResp(timeout)
    print()
    
def waitResp(timeout=20000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp)

#print uart info
uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)
print(uart)
#waitResp() 
sendCMD_waitResp("AT+RST\r\n") #reset the esp8266

sendCMD_waitResp("AT+CWMODE=1\r\n")   #set wifi mode 1:client 2:AP 3: Both

sendCMD_waitResp('AT+CWJAP="VELVET_5830","20000329"\r\n', 5000) #connecting

sendCMD_waitResp("AT+CIPMUX=0\r\n")  # multi user

print("RPi-PICO with ESP-01")
while True:
    t  = (sensor.temperature)
    temp=str(round(t,1))  #
    h = (sensor.humidity)
    humi=str(round(h))   #
    sendCMD_waitResp('AT+CIPSTART="TCP","184.106.153.149",80\r\n',1000)
    sendCMD_waitResp("AT+CIPSEND="+lens+"\r\n",1000)
    sendCMD_waitResp("GET /update?api_key=SR41LE48B63EN79L&field1="+temp+"&field2="+humi+"\r\n")  
    sendCMD_waitResp("AT+CIPCLOSE\r\n")
    T=str(t)
    H=str(h)
    
    f.text("Temperature:{}".format(T),0,0,16) #32 pix
    f.text("Humidity:{}%".format(H),0,20,16) #32 pix
    f.show()
    utime.sleep(30)

sendCMD_waitResp("AT+CIPCLOSE=0\r\n")
