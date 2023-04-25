import time,math
from machine import I2C, Pin,RTC,WDT,reset,PWM
from ssd1306 import SSD1306_I2C
from font import Font
op=10

pin_led = Pin(25,Pin.OUT)
trig = Pin(10,Pin.OUT)
echo = Pin(4,Pin.IN,Pin.PULL_DOWN)

pwm=PWM(Pin(16))
pwm.freq(4186)

servoPin = PWM(Pin(17))
servoPin.freq(50)

sda=machine.Pin(12)
scl=machine.Pin(13)
i2c = I2C(0, scl=scl, sda=sda, freq=400000)
display= SSD1306_I2C(128, 64, i2c)
f=Font(display)

def alert(t):
    pwm.freq(4186)
    pwm.duty_u16(1000)
    time.sleep(0.2)
    pwm.duty_u16(65535)
    time.sleep(t)

def servo(degrees):
    if degrees>180:
        degress=180
    if degrees<0:
        degrees=0
    maxDuty=8000
    minDuty=1000
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
    servoPin.duty_u16(int(newDuty))

def ping():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    count=0
    timeout=False
    start=time.ticks_us()
    while not echo.value():#wait for HIGH
        time.sleep_us(10)
        count+=1
        if count>10000:#over 1s timeout
            timeout=True
            break
    if timeout:#timeout return 0
        duration=0
    else:#got HIGH pulse:calculate duration
        count=0
        start=time.ticks_us()
        while echo.value():#what for LOW
            time.sleep_us(10)
            count+=1
            if count>2320: #over 400cm range:quit
                break
        duration=time.ticks_diff(time.ticks_us(),start)
    return duration
while True:
#     i2c = I2C(0, scl=scl, sda=sda, freq=400000)
#     display= SSD1306_I2C(128, 64, i2c)
    display.fill(0)
#     f=Font(display)
    distance=round(ping()/58)
    print("%s cm"% distance)
# OLED顯示
    D=str(distance)
    f.text("{}cm".format(D),0,0,16) #24 pix
    f.show()
# 倒車雷達  
#     if (distance<=45) and (distance>35):
#         alert(0.6)
#     if (distance<=35) and (distance>25):
#         alert(0.4)
#     if (distance<=25) and (distance>15):
#         alert(0.2)
#     if distance<15:
#         pwm.duty_u16(1000)
#     else:
#         pwm.duty_u16(65535)
# 停車場閘門
#     if distance<10:
#         if distance<15:
#             servo(90)
#     elif distance>15:
#         if distance>20:
#             servo(0)

