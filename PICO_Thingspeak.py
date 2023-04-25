from machine import Pin,UART,I2C,RTC,WDT,reset
import machine
import utime
import machine
from lib.dht import DHT11, InvalidChecksum


pin = Pin(28, Pin.OUT, Pin.PULL_UP)
sensor = DHT11(pin)

a=0
wifi_ready=0
led = Pin(25,Pin.OUT)
uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)
def sendCMD_waitResp(cmd, uart=uart, timeout=1000):
    print(cmd)
    uart.write(cmd+'\r\n')
   
def waitResp(uart=uart, timeout=1000):
    global data,wifi_ready
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    if resp != b'' :      
        resp = str(resp)
        if (resp.find('connect'))>=0:
            wifi_ready=1
sendCMD_waitResp("RESET")
utime.sleep(0.5)
sendCMD_waitResp("SSID,blacktea890329")
utime.sleep(0.1)
sendCMD_waitResp("PSWD,20000329")
utime.sleep(0.1)
sendCMD_waitResp("CHID,1905251")
utime.sleep(0.1)
sendCMD_waitResp("APIKEY,SR41LE48B63EN79L")
utime.sleep(0.1)
sendCMD_waitResp("ready")
utime.sleep(0.1)

while (not wifi_ready) :
    utime.sleep(0.3)
    led.value(1)
    print('.')
    utime.sleep(0.3)
    led.value(0)
    print('.')
    waitResp()    
print('start')
utime.sleep(1)
while True :
#     print("send")
    temp = (sensor.temperature)
    hum = (sensor.humidity)
    print(temp)
    print(hum)
    temp=str(temp)
    humi=str(hum)
    sendCMD_waitResp('TP1,'+temp)
    utime.sleep(0.1)
    sendCMD_waitResp('TP2,'+humi)
    utime.sleep(0.1)
    sendCMD_waitResp('TX_EN')
    utime.sleep(20)