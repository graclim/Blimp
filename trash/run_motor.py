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
		command = raw_input("input: ")
		
		if command == 'a': # Turn left
			keep_left = True
		elif command == 'd': # Turn right
			keep_right = True	
		elif command == 'w': # Forward
			keep_for = True
		elif command == 'u': # Top
		    keep_up = True
		elif command == 'j': # Down
		    keep_down = True
		elif command == 'r': # Stop two motors
			# Left and Right duty cycles set to 0%
			dc1 = 0
			dc2 = 0
			# Set to 0 to indicate not turning left, not turning right, no horizontal motion and not forwards
			buff1 = buff2 = buff3 = buff4 = 0
			right()
			left()
			forward()
		elif command == 'i': # Stop bottom motor
			# Bottom and Top duty cycles set to 0%
			dc3 = 0
			dc4 = 0
			# Set to 0 to indicate not going up, not going down and no verticalmotion
			buff5 = buff6 = buff7 = 0
			top()
			bot()

		# H and K increase or decrease the speed of vertical motion, if the vehicle is moving up or down.
		if command == 'h' and buff7 == 1:
			if buff5 == 1: # Increase speed for goingup when it is going up
				dc3 = dc3 + 10 
				if dc3 >= 90:
					dc3 = 90
				keep_up = True	
			if buff6 == 1: # Increase speed for goingdown when it is going down
				dc4 = dc4 + 10 
				if dc4 >= 90:
					dc4 = 90
				keep_down = True	
		if command == 'k' and buff7 == 1:
			if buff5 == 1: # Decrease speed for goingup when it is going up
				dc3 = dc3 - 10 
				if dc3 <= 5:
					dc3 = 10
				keep_up = True	
			if buff6 == 1: # Decrease speed for goingdown when it is going down
				dc4 = dc4 - 10 
				if dc4 <= 5:
					dc4 = 10
				keep_down = True	
			 
		# Q and E increase or decrease the speed of forward motion or turning, depending on the current motion.
		if command == 'q' and buff3 == 1:
			if buff4 == 1: # Increase speed for forward when it is going forward
				dc2 = dc2 + 10 
				if dc2 >= 90:
					dc2 = 90
				dc1 = dc1 + 10 
				if dc1 >= 90:
					dc1 = 90
				keep_for = True	
			if buff1 == 1: # Increase speed for left when it is going left
				dc1 = dc1 + 10 
				if dc1 >= 90:
					dc1 = 90
				keep_going = True
			if buff2 == 1: # Increase speed for right when it is going right
				dc2 = dc2 + 10 
				if dc2 >= 90:
					dc2 = 90
				keep = True
		if command == 'e' and buff3 == 1:
			if buff4 == 1: # Decrease speed for forward when it is going forward
				dc1 = dc1 - 10
				if dc1 <= 5:
					dc1 = 10
				dc2 = dc2 - 10 
				if dc2 <= 5:
					dc2 = 10
				keep_for = True		
			if buff1 == 1: # Decrease speed for left when it is going left
				dc1 = dc1 - 10
				if dc1 <= 5:
					dc1 = 10
				keep_going = True	
			if buff2 == 1: # Decrease speed for right when it is going right
				dc2 = dc2 - 10 
				if dc2 <= 5:
					dc2 = 10
				keep = True					
		
		# Stops all motion and cleans up the GPIO pins before breaking the loop and ending the program.
		if command == 'z':
			top.stop()
			left.stop()
			right.stop()
			GPIO.cleanup()
			break
	
		while keep_going: # Left
			if buff1 == 0:
				dc1 = 50
				buff3 = 1
			print('left')
			left()
			buff1 = 1 # Left
			buff4 = 0 # Forward
			buff2 = 0 # Right
			keep_going = False
				
		while keep: # Right
			if buff2 == 0:
				dc2 = 50
				buff3 = 1
			print('right')
			right()
			buff1 = 0 # Left
			buff4 = 0 # Forward
			buff2 = 1 # Right
			keep = False
		
		while keep_for: # Forward
			if buff4 == 0:
				dc1 = dc2 = 50
				buff3 = 1
			print('forward')
			forward()
			buff4 = 1 # Forward
			buff1 = buff2 = 0 # Left and Right
			keep_for = False
		
		while keep_up: # Going up
			if buff5 == 0:
				dc3 = 50
				buff7 = 1
			print('going up')
			top()
			buff5 = 1 # Up
			buff6 = 0 # Down
			keep_up = False
		
		while keep_down: # Going down
			if buff6 == 0:
				dc4 = 50
				buff7 = 1
			print('going up')
			bot()
			buff6 = 1 # Down
			buff5 = 0 # Up
			keep_down = False
    
except KeyboardInterrupt:
	print("Ctl C pressed")
	# Stops the PWM signals to all four motors, and returns the pins to their default states. 
	# This is an important step to avoid potential damage to the GPIO pins.
	top.stop()
	left.stop()
	right.stop()
	GPIO.cleanup()