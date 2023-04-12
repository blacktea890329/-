from machine import Pin,PWM
from time import sleep

pwm=PWM(Pin(16))
pwm.duty_u16(1000)

# while True:
for freq in range(500,3000,50):
    print(freq)
    pwm.freq(freq)
    sleep(0.1)
pwm.freq(500)
pwm.duty_u16(65535)

