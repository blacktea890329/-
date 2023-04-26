from machine import Pin,UART,I2C,RTC,WDT,reset,PWM
import machine
import utime
from lib.dht import DHT11, InvalidChecksum


pin = Pin(28, Pin.OUT, Pin.PULL_UP)
sensor = DHT11(pin)

x=0
wifi_ready=0
uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)
led = Pin(25,Pin.OUT)

led_onboard = machine.Pin(14, machine.Pin.OUT)
pwm=PWM(Pin(15))

#=======MQTT/Line notify========
reset='RESET'
ssid = 'SSID,blacktea890329'   #
password = 'PSWD,20000329'   #
mqtt_server = 'BROKER,mqttgo.io'
topic_sub = 'TOPIC,topic/2023/0426'     
topic_pub1= 'TOPIC1,blacktea'  
ready='ready'

def sendCMD_waitResp(cmd, uart=uart, timeout=1000):
    print(cmd)
    uart.write(cmd+'\r\n')
    waitResp()
   
def waitResp(uart=uart, timeout=1000):
    global data,wifi_ready
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    if resp != b'' :
        data=resp
        resp = str(resp)
        print(resp)
        if (resp.find('connect'))>=0:
            wifi_ready=1
            
sendCMD_waitResp(reset)
utime.sleep(0.5)
sendCMD_waitResp(ssid)
utime.sleep(0.1)
sendCMD_waitResp(password)
utime.sleep(0.1)
sendCMD_waitResp(mqtt_server)
utime.sleep(0.1)
sendCMD_waitResp(topic_sub)
utime.sleep(0.1)
sendCMD_waitResp(topic_pub1)
utime.sleep(0.1)
sendCMD_waitResp(ready)

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
    waitResp()
    print(data)
    if data==b'1\r\n':
        led_onboard.value(1)
    if data==b'0\r\n':
        led_onboard.value(0)


    numbers = [int(data)for data in data.split() if data.isdigit()] #從字串中取數字
    if len(numbers)==1:
        pwm.duty_u16(numbers[0])
    print(numbers)
#     temp = (sensor.temperature)
#     hum = (sensor.humidity)
#     print(temp)
#     print(hum)
#     temp=str(temp)
#     humi=str(hum)
#     x+=1
#     y=str(x)
#     sendCMD_waitResp('PB1,'+temp)
#     sendCMD_waitResp('PB1,'+humi)
    utime.sleep(1)