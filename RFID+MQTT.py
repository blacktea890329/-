from mfrc522 import MFRC522
from machine import Pin,UART,I2C,RTC,WDT,reset,PWM
import utime
from lib.dht import DHT11, InvalidChecksum

MusicNotes = {"B0": 31, "C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,"G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,
"C2": 65,"CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98,"GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139,
"D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,"G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,
"DS4": 311,"E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,
"E5": 659,"F5": 698,"FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1324,
"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,"A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,
"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,"AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978}

mario = ["E7", "E7", "0", "E7", "0", "C7", "E7", "0", "G7", "0", "0", "0", "G6", "0", "0", "0",
         "C7", "0", "0", "G6", "0", "0", "E6","0", "0", "A6", "0", "B6", "0", "AS6", "A6", "0",
         "G6", "E7", "0", "G7", "A7", "0", "F7", "G7", "0", "E7", "0","C7", "D7","B6", "0", "0",
         "C7", "0", "0", "G6", "0", "0", "E6", "0", "0", "A6", "0", "B6", "0", "AS6", "A6", "0",
         "G6", "E7", "0", "G7","A7", "0", "F7", "G7", "0", "E7", "0","C7", "D7", "B6", "0", "0"]

speaker = PWM(Pin(16))

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

def playnote(Note, Duration):
    if Note == "0":
        utime.sleep(Duration)
    if Note == "S":
        speaker.duty_u16(0)
        utime.sleep(Duration)
    elif Note != "0":
        speaker.duty_u16(0)
        utime.sleep(0.05)
        speaker.duty_u16(150)        
        speaker.freq(MusicNotes[Note])
        print (MusicNotes[Note])
        utime.sleep(Duration)

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
        if (resp.find('connect'))>=0: #接收去做特定的動作
            wifi_ready=1
        if (resp.find('on'))>=0: #接收去做特定的動作
            led_onboard.value(1)
        if (resp.find('off'))>=0: #接收去做特定的動作
            led_onboard.value(0)
        if (resp.find('mario'))>=0: #接收去做特定的動作
            for c in mario:
                playnote(c, 0.1)
            speaker.duty_u16(65535)
# 將卡號由 2 進位轉換為 16 進位的字串
def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=26,rst=10)
print("..... 請將卡片靠近感應器.....")
while True:
    (stat, tag_type) = reader.request(reader.REQIDL)   # 搜尋 RFID 卡片
    if stat == reader.OK:      # 找到卡片
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card_num = uidToString(uid)
            print(".....卡片號碼： %s" % card_num)
            if  card_num == '0DFD2AF8':   #'7A811D60':
                print("開始連線")
                led.value(1)   # 讀到授權的卡號後點亮綠色 LED
                utime.sleep(2)       # 亮 2 秒鐘
                led.value(0)
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
                    numbers = [int(data)for data in data.split() if data.isdigit()] #從字串中取數字 #接收去做特定的動作
                    if len(numbers)==1:
                        pwm.duty_u16(numbers[0])
                    print(numbers)
#                     temp = (sensor.temperature)
#                     hum = (sensor.humidity)
#                     print(temp)
#                     print(hum)
#                     temp=str(temp)
#                     humi=str(hum)
#                     sendCMD_waitResp('PB1,'+temp)
#                     sendCMD_waitResp('PB1,'+humi)
                    utime.sleep(1)
            else:
                print(".....卡片錯誤.....")