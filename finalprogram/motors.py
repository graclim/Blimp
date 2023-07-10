import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED = [1, 12, 7]
for l in LED:
    GPIO.setup(l,GPIO.OUT)

pwm_led= [ GPIO.PWM(l,10000) for l in LED ]

motor = [ 24, 14, 21 ]
for m in motor:
    GPIO.setup(m, GPIO.OUT)

pwm_motor = [ GPIO.PWM(m, 50) for m in motor ]

def right():
    pwm_motor[0].stop()
    pwm_motor[1].stop()
    pwm_motor[2].start()

def left():
    pwm_motor[0].start()
    pwm_motor[1].stop()
    pwm_motor[2].stop()

def top():
    pwm_motor[0].stop()
    pwm_motor[1].start()
    pwm_motor[2].stop()

def bot():
    pass


def forward():
    pass

def backward():
    pass

def stopmotor():
    for pwm in pwm_motor:
        pwm.stop()
    GPIO.cleanup()

