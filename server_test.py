import socket
from multiprocessing import Process,Pipe
import time

# This Python script is a TCP server running on localhost at port 12002. 
# It is designed to interface with a drone by responding to certain commands and sending 
# information about the drone's current state.

# The server is started on the localhost at port 12002.
serverPort = 12002

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(1) # Allows one connection at a time
print("The server is ready to receive")

# Various variables are initialized to hold the state of the drone, including its current waypoint (wp), 
# operation mode (op_mode), AprilTag data (AT_visible, AT_ID, AT_dist, AT_ang, AT_coords), and 
# Time of Flight (TOF) sensor data (TOF_dist, TOF_status).

running = True          # Looping variable
wp = [0,0,1,0]          # Current waypoint
op_mode = 0             # 0: full auto, 1: waypoint, 2: manual
AT_visible = True       # True: AprilTag currently in view of camera, False: otherwise
AT_ID = 3               # ID of last visible AprilTag
AT_dist = 1.2           # Last measured distance to AprilTag in meters
AT_ang = 32             # Last measured angle of AprilTag
AT_coords = {1:[0,0],\
             3:[1,0],\
             4:[2,0],\
             7:[0,1],\
             13:[-1,-1]}   # Dictionary mapping AprilTag IDs to known (x,y) coordinates
             
# Time of flight distances
# Left, center, right
TOF_dist = [5.8,1.5,0.1]

# Time of flight status
# Left, center, right
# 0: OK
# 1: Danger
# 2: Collision imminent
TOF_status = [0, 1, 2]

# The server then enters a loop where it waits for a client to connect and send a message. 
# Once a message is received, the server responds according to the content of the message:
try:
    while running:
        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(1024).decode()
        print("received message: "+message)

        # The server is commanded to stop. 
        # It sets running to False, causing the loop to end after the current iteration.
        if message == "quit":
            # Close server (debugging)
            return_msg = "quitting"
            running = False
        
        # "forward", "backward", "right", "left", "up", "down", "stop": 
        # Manual control commands for the drone. The server doesn't currently do anything in response 
        # to these commands, but pass statements are included as placeholders where code to move the 
        # drone could be added.
        elif message == "forward":
            # Manual command move forward
            pass
        elif message == "backward":
            # Manual command move backward
            pass
        elif message == "right":
            # Manual command pivot right
            pass
        elif message == "left":
            # Manual command pivot left
            pass
        elif message == "up":
            # Manual command increase altitude
            pass
        elif message == "down":
            # Manual command decrease altitude
            pass
        elif message == "stop":
            # Manual command stop motors
            pass
        elif message == "curr wp":
            # The client is requesting the current waypoint. 
            # The server responds with the waypoint encoded as a string.
            return_msg = str(wp[0]) + "," + str(wp[1]) + "," + str(wp[2]) + "," + str(wp[3])
        
        # The client is setting the operation mode to some value X. 
        # The server updates its stored operation mode.
        elif message.split(' ')[0] == "mode":
            op_mode = int(message.split(' ')[1])
            print("new op mode: " + str(op_mode))
        elif message.split(' ')[0] == "wp":
            # The client is setting a new waypoint. The server updates its stored waypoint.
            wp[:] = [int(i) for i in message.split(' ')[1].split(',')]
        elif message == "at":
            # The client is requesting AprilTag data. 
            # The server responds with the visibility of the AprilTag, its ID, coordinates, distance, and angle if visible.
            return_msg = str(AT_visible)
            if AT_visible and (AT_ID in AT_coords):
                return_msg += "," + str(AT_ID) + "," + str(AT_coords[AT_ID][0]) + "," + str(AT_coords[AT_ID][1]) + "," + str(AT_dist) + "," + str(AT_ang)
        elif message == "tof":
            # The client is requesting time-of-flight (TOF) sensor data. 
            # The server responds with the TOF distances and statuses encoded as a string.
            return_msg = ""
            for n in range(3):
                return_msg = return_msg + str(TOF_dist[n]) + ","
            for n in range(3):
                return_msg = return_msg + str(TOF_status[n]) + ","
            return_msg = return_msg[:-1]
        else:
            # Anything else is treated as an unrecognized command.
            print("Not recognized")
            return_msg = "Not recognized"
        
        # The server sends a response to the client, then closes the connection to the client and waits for a new client to connect.
        connectionSocket.send(return_msg.encode())
        connectionSocket.close()
    print ("running = {}".format(running))
    serverSocket.close()
except:
    serverSocket.close()
    raise