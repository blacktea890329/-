from machine import I2C, Pin
# Import the DS3231_I2C class from ds3231_i2c (This is light driver with limited functionalities)
from ds3231_i2c import DS3231_I2C #RTC讀的是16進制
import utime

# Set DS I2C ID, SDA, SCL respective pins and uses default frequency (freq=400000)
ds_i2c = I2C(0,sda=Pin(12), scl=Pin(13))
print("RTC I2C Address : " + hex(ds_i2c.scan()[0]).upper()) # Print the I2C device address in the command line
print("RTC I2C Configuration: " + str(ds_i2c))              # Display the basic parameters of I2C device in the command line
ds = DS3231_I2C(ds_i2c)
# 
# current_time = b'\x00\x10\x11\x02\x16\x05\x23' # sec min hour week day mon year 
# ds.set_time(current_time)

# Define the name of week days list
w  = ["Sunday","Monday","Tuesday","Wednesday","Thurday","Friday","Saturday"];
t = ds.read_time()
print(t[0])
print(hex(t[0]))
#把16進位的數轉為10進位 設定30秒後跳出
s=str(hex(t[0]))
se=s.split("x")
print(se)
sec=int(se[1])
goal=sec+30
print(sec)
print(goal)
# 

while 1:
    t = ds.read_time()
    s=str(hex(t[0]))
    se=s.split("x")
    print(se)
    sec=int(se[1])
    print("Date: %02x/%02x/20%x" %(t[4],t[5],t[6]))
    print(" Time: %02x:%02x:%02x" %(t[2],t[1],t[0]))
    print(t[0],t[1],t[2],t[3],t[4],t[5],t[6])
    if (sec==goal):#把16進位的數轉為10進位 設定30秒後跳出
        print("time up!")
        break
    utime.sleep(1)