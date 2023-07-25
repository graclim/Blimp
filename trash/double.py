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

# Setting PWM values
# The duty cycle for each motor is then initiated with the defined initial value.
# A value of means the motor is initially off.
freq1 = 100
dc1 = 0
freq2 = 100
dc2 = 0
p = GPIO.PWM(17,freq1)
pwm = GPIO.PWM(18,freq2)

p.start(dc1)
pwm.start(dc2)

# Set the initial logic output (right(), left(), top(), bot(), forward())

# Left motor's duty cycle is set to 0. Right motor's duty cycle is changed
def right():
	dc1 = 0
	p.ChangeDutyCycle(dc1)
	pwm.ChangeDutyCycle(dc2)

# Right motor's duty cycle is set to 0. Left motor's duty cycle is changed
def left():
	dc2 = 0
	p.ChangeDutyCycle(dc1)
	pwm.ChangeDutyCycle(dc2)

# buff1: Set to 1 when the vehicle is turning left, and reset to 0 when the vehicle is not turning left.
# buff2: Set to 1 when the vehicle is turning right, and reset to 0 when the vehicle is not turning right.
# buff3: Set to 1 when the vehicle is either moving forward, turning left, or turning right (any form of horizontal motion).
buff1 = 0
buff2 = 0
buff3 = 0
keep_going = False # Left
keep = False	   # Right

try:
	while True:
		print(dc1, dc2)
		command = raw_input("input:")
		if command == 'a': # turn left
			keep_going = True
		if command == 'd': # turn right
			keep = True	
		if command == 'q':
			# Left and Right duty cycles set to 0%
			dc1 = 0
			dc2 = 0
			buff1 = 0 # Left
			buff2 = 0 # Right
			buff3 = 0 # Horizontal motion
			right()
			left()
		
		# Increasing speed
		if command == 'w' and buff3 == 1:
			if buff1 == 1: # Increase speed for left
				dc1 = dc1 + 10 
				if dc1 >= 90:
					dc1 = 90
				keep_going = True	
			if buff2 == 1: # Increase speed for right
				dc2 = dc2 + 10 
				if dc2 >= 90:
					dc2 = 90
				keep = True	
		
		# Decreasing speed
		if command == 's' and buff3 == 1:
			if buff1 == 1: # Decrease speed for left
				dc1 = dc1 - 10
				if dc1 <= 5:
					dc1 = 10
				keep_going = True	
			if buff2 == 1: # Decrease speed for right
				dc2 = dc2 - 10 
				if dc2 <= 5:
					dc2 = 10
				keep = True				
		
		# Exit
		if command == 'z':
			break
	
		while keep_going: # Left
			if buff1 == 0:
				dc1 = 50
				buff3 = 1
			print('left')
			left()
			buff1 = 1 # Left
			buff2 = 0 # Right
			keep_going = False
				
		while keep: # Right
			if buff2 == 0:
				dc2 = 50
				buff3 = 1
			print('right')
			right()
			buff1 = 0 # Left
			buff2 = 1 # Right
			keep = False
		
except KeyboardInterrupt:
	print("Ctl C pressed")

# Stops the PWM signals and returns the pins to their default states. 
# This is an important step to avoid potential damage to the GPIO pins.
p.stop()
pwm.stop()	
GPIO.cleanup()