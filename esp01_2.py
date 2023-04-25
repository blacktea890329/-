from machine import Pin, UART,I2C,RTC,WDT,reset
import os, sys
import utime
import machine
from ssd1306 import SSD1306_I2C
from font import Font
from lib.dht import DHT11, InvalidChecksum
print(os.uname())

wifi_ready=0
uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)

a=0

led = machine.Pin(25, machine.Pin.OUT)


pin = Pin(28, Pin.OUT, Pin.PULL_UP)
sensor = DHT11(pin)
lens = str(len('GET /update?api_key=SR41LE48B63EN79L&field1="+temp+"&field2="+temp+"\r\n'))
print(lens)
#functions
def sendCMD_waitResp(cmd, timeout=1000):
    print(cmd)
    uart.write(cmd+'\r\n')
    
def waitResp(timeout=10000):
    global data,wifi_ready
    prvMills = utime.ticks_ms()
    resp=b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp,uart.read(1)])
    if resp !=b'':
        resp = str(resp)
        if (resp.find('connect'))>=0:
            wifi_ready=1

sendCMD_waitResp("Reset")
utime.sleep(0.1)
sendCMD_waitResp("SSID,blacktea890329")
utime.sleep(0.1)
sendCMD_waitResp("PSWD,20000329")
utime.sleep(0.1)
sendCMD_waitResp("CHID,2112446")
utime.sleep(0.1)
sendCMD_waitResp("APIKEY,SR41LE48B63EN79L")
utime.sleep(0.1)
sendCMD_waitResp("ready")
utime.sleep(0.1)
while (not wifi_ready):
    utime.sleep(0.3)
    led.value(1)
    print('.')
    utime.sleep(0.3)
    led.value(0)
    print('.')
    waitResp()
print('start')
utime.sleep(1)
while True:
    x='20'
    y='40'
    sendCMD_waitResp('TP1,'+X)
    utime.sleep(0.1)
    sendCMD_waitResp('TP2,'+Y)
    utime.sleep(0.1)
    sendCMD_waitResp('TX_EN')
    utime.sleep(0.1)
    print("sending")
