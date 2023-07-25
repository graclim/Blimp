# import GPIO package and time
import time 
import RPi.GPIO as GPIO

# Setting GPIO pins to be referred to their BOARD number (1-40)
GPIO.setmode(GPIO.BOARD)

# Disable warnings
GPIO.setwarnings(False)	

# Setting up the GPIO pins
GPIO.setup(18, GPIO.OUT) # top
GPIO.setup(8, GPIO.OUT)  # left
GPIO.setup(40, GPIO.OUT) # right

# Setting frequency (frequency of PWM / How long one period is)
freq1 = freq2 = freq3 = 1000

# Create PWM Object
top = GPIO.PWM(18, freq1)
left = GPIO.PWM(8, freq2)
right = GPIO.PWM(40, freq3)

# Start PWM generation of a specified duty cycle
top.start(0)
left.start(0)
right.start(0)
	
count = 0 

# Testing forward, stop, right, and left
try:
	
	while True:

		# The top motor is always on to keep the blimp flying
		top.ChangeDutyCycle(10)

		print('time ' + str(count))
		
		if count == 13:
			count = 0
		
		elif count == 1:
			left.ChangeDutyCycle(10)
			right.ChangeDutyCycle(0)
			print('left')
		
		elif count == 4:
			left.ChangeDutyCycle(0)
			right.ChangeDutyCycle(0)
			print('stop')
		
		elif count == 5:
			left.ChangeDutyCycle(0)
			right.ChangeDutyCycle(10)
			print('right')
			
		elif count == 8:
			left.ChangeDutyCycle(0)
			right.ChangeDutyCycle(0)
			print('stop')
		
		elif count == 9:
			left.ChangeDutyCycle(10)
			right.ChangeDutyCycle(10)
			print('forward')
			
		elif count == 12:
			left.ChangeDutyCycle(0)
			right.ChangeDutyCycle(0)
			print('stop')
		
		time.sleep(1)	
		count += 1	
		
except KeyboardInterrupt:
	print("Ctl C pressed")
	# Stops the PWM signals to all four motors, and returns the pins to their default states. 
	# This is an important step to avoid potential damage to the GPIO pins.
	top.stop()
	left.stop()
	right.stop()
	GPIO.cleanup()