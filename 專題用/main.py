from machine import I2C, Pin, PWM
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
    t = ds.read_time()
    
    #確定小時 把16進位的數轉為10進位
    d=str(hex(t[2]))
    d=d.split("x")
    d=int(d[1])
    goal_h=d#延遲多久 後面+數字
    
    #確定分鐘 把16進位的數轉為10進位
    d=str(hex(t[1]))
    d=d.split("x")
    d=int(d[1])
    goal_m=d#延遲多久 後面+數字
    
    #確定秒 把16進位的數轉為10進位
    d=str(hex(t[0]))
    d=d.split("x")
    d=int(d[1])
    goal_s=d#延遲多久 後面+數字
    
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
    if(hour==goal_h and minu==goal_m and secs==goal_s and D[0]==0):
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
        btn.irq(handler=None)
        break
    if(b==0 and D[0]==1):
        print("沒有拿藥")
        rotate()
        rotate()
        btn.irq(handler=None)
        break
    utime.sleep(1)