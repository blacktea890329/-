from machine import I2C, Pin, PWM
from ds3231_i2c import DS3231_I2C #RTC讀的是16進制
import utime
from GET_TIME import get_time #取得時間的函數
from servo import rotate #馬達旋轉的函數
# Set DS I2C ID, SDA, SCL respective pins and uses default frequency (freq=400000)
ds_i2c = I2C(0,sda=Pin(12), scl=Pin(13))
print("RTC I2C Address : " + hex(ds_i2c.scan()[0]).upper()) # Print the I2C device address in the command line
print("RTC I2C Configuration: " + str(ds_i2c))              # Display the basic parameters of I2C device in the command line
ds = DS3231_I2C(ds_i2c)
btn = Pin(17, Pin.IN, Pin.PULL_UP)
speaker = PWM(Pin(18))
flag2=0
#設定時間
# current_time = b'\x00\x14\x08\x03\x17\x05\x23' # sec min hour week day mon year 
# ds.set_time(current_time)

# Define the name of week days list
w  = ["Sunday","Monday","Tuesday","Wednesday","Thurday","Friday","Saturday"];

# def take(pin):
#     global flag1
#     btn.irq(handler=None)
#     if flag2!=0:
#         speaker.duty_u16(65535)
#         print("btn pushed")
#         rotate()
#         flag2=flag2+1
#         return flag2
#     else:
#         print("btn pushed")
#         rotate()
#     btn.irq(handler=take)
# 
# btn.irq(trigger=Pin.IRQ_FALLING, handler=take)

def delay():#設定延遲30分鐘
    global goal
    t = ds.read_time()
    print(t[1])
    print(hex(t[1]))#把16進位的數轉為10進位
    d=str(hex(t[1]))
    d=d.split("x")
    d=int(d[1])
    goal=d#延遲多久 改+後面的數字
    print(goal)

delay()
while 1:
    t = ds.read_time()
    s=str(hex(t[1]))
    se=s.split("x")
    print(se)
    print(goal)
    sec=int(se[1])#取得現在時間
#     print("Date: %02x/%02x/20%x" %(t[4],t[5],t[6])) #顯示日期 日/月/年
    print(" Time: %02x:%02x:%02x" %(t[2],t[1],t[0])) #顯示時間 時/分/秒
    print(t[0],t[1],t[2],t[3],t[4],t[5],t[6])
    if (sec==goal):#把16進位的數轉為10進位 設定30秒後跳出
       for i in range(0,30):
            #音響
            print("i")
#             speaker.duty_u16(5000)
#             speaker.freq(2093)
            utime.sleep(1)
#             speaker.duty_u16(65535)
            if btn.value()==0: 
                rotate()
                break
    utime.sleep(1)
