# import GPIO package and time
import time 
import RPi.GPIO as GPIO

# Setting GPIO pins to be referred to their Broadcom SOC channel numbers (the name fo the GPIO pin)
GPIO.setmode(GPIO.BCM)

# Disable warnings
GPIO.setwarnings(False)

# An analog input is a variable and can have multiple states
GPIO.setup(17,GPIO.OUT) #AIN2 (Analog Input 2)
GPIO.setup(18,GPIO.OUT) #AIN1 (Analog Input 1)

# When AIN1 is HIGH and AIN2 is LOW, the motor turns in one direction
# When AIN1 is LOW and AIN2 is HIGH, the motor turns in the opposite direction

# Clockwise
def clockwise():
	GPIO.output(17,GPIO.LOW)
	GPIO.output(18,GPIO.HIGH)

# Counter Clockwise
def counterclockwise():
	GPIO.output(17,GPIO.HIGH)
	GPIO.output(18,GPIO.LOW)
	
count = 0
keep_going = True
keep = False

try:
	while keep_going:
		print('Counter Clockwise')
		counterclockwise()
		keep_going = False
		keep = True
			
	time.sleep(5)	

	while keep:
		print('Clockwise')
		clockwise()
		keep = False
		
	time.sleep(5)
		
except KeyboardInterrupt:
	print("Ctl C pressed")
	
GPIO.cleanup()