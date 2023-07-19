# import the necessary packages 

print("1")

from picamera.array import PiRGBArray

print("2")

from picamera import PiCamera

print("3")

import time

print("4")

import cv2

print("5")

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()

print("6")

camera.resolution = (640, 480)

print("7")

# allow the camera to warmup
time.sleep(0.1)
while True:
    camera.capture('/home/pi/Desktop/image.jpg')
    test1 =cv2.imread('/home/pi/Desktop/image.jpg')
    gray=cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',gray)
    cv2.waitKey(5)
    print("0")




