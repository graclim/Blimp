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

# The script uses various variables (buff1 through buff7, keep_going, keep, keep_up, keep_down, keep_for) 
# to keep track of the current motion and speed of the vehicle, and to decide whether a command to change 
# speed applies to the current motion. 

# buff1: Set to 1 when the vehicle is turning left, and reset to 0 when the vehicle is not turning left.
# buff2: Set to 1 when the vehicle is turning right, and reset to 0 when the vehicle is not turning right.
# buff3: Set to 1 when the vehicle is either moving forward, turning left, or turning right (any form of horizontal motion).
# buff4: Set to 1 specifically when the vehicle is moving forward, and reset to 0 when it is not moving forward.
# buff5: Set to 1 when the vehicle is going up, and reset to 0 when the vehicle is not going up.
# buff6: Set to 1 when the vehicle is going down, and reset to 0 when the vehicle is not going down.
# buff7: Set to 1 when the vehicle is either going up or going down (any form of vertical motion).

buff1 = buff2 = buff3 = buff4 = buff5 = buff6 = buff7 = 0

keep_left = False
keep_right = False
keep_up = False
keep_down = False
keep_for = False

try:
	while True:
		# FIGURE OUT HOW THIS WORKS
		command = input("input: ")
		
		top.ChangeDutyCycle(10)
		
		if command == 'a': # Turn left
			keep_left = True
		if command == 'd': # Turn right
			keep_right = True	
		if command == 'w': # Forward
			keep_for = True
		if command == 'u': # Up
			keep_up = True
		if command == 'j':
			keep_down = True
			
		if keep_left:
			left.ChangeDutyCycle(10)
		if keep_right:
			right.ChangeDutyCycle(10)
		if keep_for:
			left.ChangeDutyCycle(10)
			right.ChangeDutyCycle(10)
		if keep_up:
			top.ChangeDutyCycle(20)
		if keep_left:
			left.ChangeDutyCycle(10)
			
		# Stops all motion and cleans up the GPIO pins before breaking the loop and ending the program.
		if command == 'z':
			top.stop()
			left.stop()
			right.stop()
			GPIO.cleanup()
			quit()

except KeyboardInterrupt:
	print("Ctl C pressed")
	# Stops the PWM signals to all four motors, and returns the pins to their default states. 
	# This is an important step to avoid potential damage to the GPIO pins.
	top.stop()
	left.stop()
	right.stop()
	GPIO.cleanup()