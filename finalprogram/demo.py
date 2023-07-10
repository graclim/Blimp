import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED = [1, 12, 7]
for l in LED:
    GPIO.setup(l,GPIO.OUT)

pwm_led= [ GPIO.PWM(l,10000) for l in LED ]
for pwm in pwm_led:
    pwm.start(1)

motor = [ 24, 14, 21 ]
for m in motor:
    GPIO.setup(m, GPIO.OUT)

pwm_motor = [ GPIO.PWM(m, 50) for m in motor ]
for pwm in pwm_motor:
    pwm.start(50)


try:
    while True:
        print("ok")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
