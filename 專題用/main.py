from machine import I2C, Pin, PWM ,UART,RTC,WDT,reset
from ds3231_i2c import DS3231_I2C #RTC讀的是16進制
import utime
from GET_TIME import get_time #取得時間的函數
from servo import rotate #馬達旋轉的函數
# Set DS I2C ID, SDA, SCL respective pins and uses default frequency (freq=400000)
ds_i2c = I2C(0,sda=Pin(12), scl=Pin(13))
# print("RTC I2C Address : " + hex(ds_i2c.scan()[0]).upper()) # Print the I2C device address in the command line
# print("RTC I2C Configuration: " + str(ds_i2c))              # Display the basic parameters of I2C device in the command line
ds = DS3231_I2C(ds_i2c)
btn = Pin(17, Pin.IN, Pin.PULL_UP)
speaker = PWM(Pin(18))

flag1=0
D=[0,0,0,0] #早 午 晚 睡前

pin = Pin(28, Pin.OUT, Pin.PULL_UP)

x=0
wifi_ready=0
uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)
led = Pin(25,Pin.OUT)

led_onboard = machine.Pin(14, machine.Pin.OUT)
pwm=PWM(Pin(15))

# #=======MQTT/Line notify========
# reset='RESET'
# ssid = 'SSID,blacktea890329'   #
# password = 'PSWD,20000329'   #
# mqtt_server = 'BROKER,mqttgo.io'
# linetoken="TOKEN,DD5kW806kKEEH8BMQERiouCxyjwNChRNGWcM3T2swOW"
# topic_sub = 'TOPIC,black'     
# topic_pub1= 'TOPIC1,black'
# topic_pub2= ''#第二個PB 依此類推
# ready='ready'
# 
# def sendCMD_waitResp(cmd, uart=uart, timeout=1000):
#     print(cmd)
#     uart.write(cmd+'\r\n')
#     waitResp()
#    
# def waitResp(uart=uart, timeout=1000):
#     global data,wifi_ready
#     prvMills = utime.ticks_ms()
#     resp = b""
#     while (utime.ticks_ms()-prvMills)<timeout:
#         if uart.any():
#             resp = b"".join([resp, uart.read(1)])
#     if resp != b'' :
#         data=resp
#         resp = str(resp)
#         print(resp)
#         if (resp.find('connect'))>=0:
#             wifi_ready=1
#             
# sendCMD_waitResp(reset)
# utime.sleep(0.5)
# sendCMD_waitResp(ssid)
# utime.sleep(0.1)
# sendCMD_waitResp(password)
# utime.sleep(0.1)
# sendCMD_waitResp(linetoken)
# utime.sleep(0.1)
# sendCMD_waitResp(topic_sub)
# utime.sleep(0.1)
# sendCMD_waitResp(topic_pub1)
# utime.sleep(0.1)
# # sendCMD_waitResp(topic_pub2)#第二個PB 依此類推
# # utime.sleep(0.1)
# sendCMD_waitResp(ready)
# 
# while (not wifi_ready) :
#     utime.sleep(0.3)
#     led.value(1)
#     print('.')
#     utime.sleep(0.3)
#     led.value(0)
#     print('.')
#     waitResp()    
# print('start')
# utime.sleep(1)

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

def delay():#設定延遲30分鐘
    global goal_h
    global goal_m
    global goal_s
    goal_h=[0,0,0,0]
    goal_m=[0,0,0,0]
    goal_s=[0,0,0,0]
    t = ds.read_time()
    
    #確定小時 把16進位的數轉為10進位
    d=str(hex(t[2]))
    d=d.split("x")
    d=int(d[1])
    goal_h[0]=d#延遲多久 後面+數字
    
    #確定分鐘 把16進位的數轉為10進位
    d=str(hex(t[1]))
    d=d.split("x")
    d=int(d[1])
    goal_m[0]=d#延遲多久 後面+數字
    
    #確定秒 把16進位的數轉為10進位
    d=str(hex(t[0]))
    d=d.split("x")
    d=int(d[1])
    goal_s[0]=d#延遲多久 後面+數字
    
btn.irq(handler=None) #關閉中斷功能 避免提前拿藥
delay()
while True:
    b=0
    t = ds.read_time()
    
    #小時
    hour=str(hex(t[2]))
    hour=hour.split("x")
    hour=int(hour[1])#取得現在時間
    
    #分鐘
    minu=str(hex(t[1]))
    minu=minu.split("x")
    minu=int(minu[1])#取得現在時間
    
    #秒
    secs=str(hex(t[0]))
    secs=secs.split("x")
    secs=int(secs[1])#取得現在時間
    
    print(hour,minu,secs)
    print(goal_h,goal_m,goal_s)

    print(" Time: %02x:%02x:%02x" %(t[2],t[1],t[0])) #顯示時間 時/分/秒
    print(t[0],t[1],t[2],t[3],t[4],t[5],t[6])
    if(hour==goal_h[0] and minu==goal_m[0] and secs==goal_s[0] and D[0]==0):
        btn.irq(handler=take) #開啟中斷功能可以拿藥
        while (D[0]==0):#把16進位的數轉為10進位 設定30秒後跳出
            for i in range(0,10):
            #音響
                print(i)
                print(flag1)
                #speaker.duty_u16(5000)
                #speaker.freq(2093)
                utime.sleep(1)
                #speaker.duty_u16(65535)
                if flag1!=0:
                    b=2
                    break
            D[0]=1
    if(b!=0 and D[0]==1):
        print(D)
        print("拿藥了")
        rotate()
#         btn.irq(handler=None)
#         sendCMD_waitResp('MESSAGE,'+"病患已完成服藥")
        break
    if(b==0 and D[0]==1):
        print("沒有拿藥")
        rotate()
        rotate()
        btn.irq(handler=None)
#         sendCMD_waitResp('MESSAGE,'+"注意！病患尚未服藥")
#         sendCMD_waitResp('MESSAGE,'+"建議主動聯絡")
        break
    utime.sleep(1)