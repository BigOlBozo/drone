import cv2
from djitellopy import tello
from time import sleep
import os
from keyboard import is_pressed as press
from time import perf_counter_ns as click
from datetime import datetime

import time
def intializeTello():
    # CONNECT TO TELLO
    drone = tello.Tello()
    drone.connect()
    drone.for_back_velocity = 0
    drone.left_right_velocity = 0
    drone.up_down_velocity = 0
    drone.yaw_velocity = 0
    drone.speed =0
    print(drone.get_battery())
    drone.streamoff()
    drone.streamon()
    return drone

def telloGetFrame(drone,w=360,h=240):
    # GET THE IMGAE FROM TELLO
    myFrame = drone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img

drone = intializeTello()

while True:
    ## STEP 1
    img = telloGetFrame(drone)
    # DISPLAY IMAGE
    cv2.imshow("MyResult", img)
    # WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) and 0xFF == ord('q'):
    # replace the 'and' with '&amp;' 
        drone.land()
    break

def findFace(img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    myFacesListC = []
    myFaceListArea = []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFacesListC.append([cx,cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        # index of closest face
        return img,[myFacesListC[i],myFaceListArea[i]]
    else:
        return img, [[0,0],0]
    
img, c = findFace(img)