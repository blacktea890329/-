from machine import I2C, Pin, PWM ,UART,RTC,WDT,reset
from ds3231_i2c import DS3231_I2C #RTC讀的是16進制
import utime
from GET_TIME import get_time #取得時間的函數
from servo import servo #馬達旋轉的函數 橘 紅 棕

ds_i2c = I2C(0,sda=Pin(12), scl=Pin(13))

ds = DS3231_I2C(ds_i2c)
btn = Pin(17, Pin.IN, Pin.PULL_UP)
speaker = PWM(Pin(18))

pin = Pin(28, Pin.OUT, Pin.PULL_UP)

x=0
wifi_ready=0
uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)
led = Pin(25,Pin.OUT)

led_onboard = machine.Pin(14, machine.Pin.OUT)
pwm=PWM(Pin(15))

t = ds.read_time()#紀錄現實時間
block=[]#放入每一個的角度
D=[0,0,0,0]
#=======MQTT/Line notify========
reset='RESET'
ssid = 'SSID,blacktea890329'   #
password = 'PSWD,20000329'   #
mqtt_server = 'BROKER,mqttgo.io'
linetoken="TOKEN,DD5kW806kKEEH8BMQERiouCxyjwNChRNGWcM3T2swOW"
topic_sub = 'TOPIC,black'     
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
sendCMD_waitResp(linetoken)
utime.sleep(0.1)
sendCMD_waitResp(topic_sub)
utime.sleep(0.1)
sendCMD_waitResp(mqtt_server)
utime.sleep(0.1)
sendCMD_waitResp(topic_sub)
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
for i in range(0,3):
    speaker.duty_u16(5000)
    speaker.freq(2093)
    utime.sleep(1)
    speaker.duty_u16(65535)
    utime.sleep(1)
#設定時間
# current_time = b'\x00\x14\x08\x03\x17\x05\x23' # sec min hour week day mon year 
# ds.set_time(current_time)

def take(pin):
    global flag1
    btn.irq(handler=None)
    flag1=1
    utime.sleep(1)
    btn.irq(handler=take)

btn.irq(trigger=Pin.IRQ_FALLING, handler=take)
btn.irq(handler=None) #關閉中斷功能 避免提前拿藥
# def delay():#設定延遲30分鐘
#     global goal_h
#     global goal_m
#     global goal_s
#     t = ds.read_time()
#     
#     #確定小時 把16進位的數轉為10進位
#     d=str(hex(t[2]))
#     d=d.split("x")
#     d=int(d[1])
#     goal_h=d#延遲多久 後面+數字
#     
#     #確定分鐘 把16進位的數轉為10進位
#     d=str(hex(t[1]))
#     d=d.split("x")
#     d=int(d[1])
#     goal_m=d#延遲多久 後面+數字
#     
#     #確定秒 把16進位的數轉為10進位
#     d=str(hex(t[0]))
#     d=d.split("x")
#     d=int(d[1])
#     goal_s=d#延遲多久 後面+數字

def nowtime():
    global hour
    global minu
    global secs
    t = ds.read_time()
    #小時
    hour=str(hex(t[2]))
    hour=hour.split("x")
    hour=str(hour[1])#取得現在時間
    
    #分鐘
    minu=str(hex(t[1]))
    minu=minu.split("x")
    minu=str(minu[1])#取得現在時間
    #秒
    secs=str(hex(t[0]))
    secs=secs.split("x")
    secs=str(secs[1])#取得現在時間
# delay()

while True :
    waitResp()
    data=str(data)
    if (data.find('set'))>=0:
        break
    utime.sleep(1)
T=data
Time=get_time(T)
goal_h=[Time[1],Time[3],Time[5],Time[7]]
goal_m=[Time[2],Time[4],Time[6],Time[8]]
d=str(hex(t[0]))
d=d.split("x")
d=str(d[1])
goal_s=d
for k in range(0,4):
    flag1=0
    while True:#提醒迴圈
        nowtime()
#         print(hour,minu,secs)
#         print(int(goal_h[k]),int(goal_m[k]),goal_s)
        b=0
        if(hour==int(goal_h[k]) and minu==int(goal_m[k]) and secs==goal_s and D[k]==0):
            btn.irq(handler=take) #開啟中斷功能可以拿藥
            while (D[k]==0):#把16進位的數轉為10進位 設定30秒後跳出
                for i in range(0,5):#音響
#                     print(i)
#                     print(flag1)
                    speaker.duty_u16(5000)
                    speaker.freq(2093)
                    utime.sleep(1)
                    speaker.duty_u16(65535)
                    utime.sleep(1)
                    if flag1!=0:
                        b=2
                        break
                D[k]=1
        if(b!=0 and D[k]!=0):
            print("拿藥了")
            servo(block[k])
            btn.irq(handler=None)
            sendCMD_waitResp('MESSAGE,'+"病患已完成服藥")
            break
        if(b==0 and D[k]!=0):
            print("沒有拿藥")
            servo(blodk[k+1])
            btn.irq(handler=None)
            sendCMD_waitResp('MESSAGE,'+"注意！病患尚未服藥")
            sendCMD_waitResp('MESSAGE,'+"建議主動聯絡")
            break
        utime.sleep(1)
