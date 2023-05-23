from djitellopy import tello
from time import sleep
import os
from keyboard import is_pressed as press
from time import perf_counter_ns as click
from datetime import datetime
import numpy as np
import time
os.system('cls')

drone = tello.Tello()
drone.connect()

#camera
import cv2

drone.streamon()
drone.send_rc_control(0, 0, 25, 0)
#time.sleep(2.2)
w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0


def findFace(img):
 
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
 
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
 
    myFaceListC = []
 
    myFaceListArea = []
 
    for (x, y, w, h) in faces:
 
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
        cx = x + w // 2
 
        cy = y + h // 2
 
        area = w * h
 
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
 
        myFaceListC.append([cx, cy])
 
        myFaceListArea.append(area)
 
    if len(myFaceListArea) != 0:
 
        i = myFaceListArea.index(max(myFaceListArea))
 
        return img, [myFaceListC[i], myFaceListArea[i]]
 
    else:
 
        return img, [[0, 0], 0]
    


def trackFace( info, w, pid, pError):
 
    area = info[1]
 
    x, y = info[0]
 
    fb = 0
 
    error = x - w // 2
 
    speed = pid[0] * error + pid[1] * (error - pError)
 
    speed = int(np.clip(speed, -100, 100))
 
    if area > fbRange[0] and area < fbRange[1]:
 
        fb = 0
 
    elif area > fbRange[1]:
 
        fb = -20
 
    elif area < fbRange[0] and area != 0:
 
        fb = 20
 
    if x == 0:
 
        speed = 0
 
        error = 0
 
    #print(speed, fb)
 
    drone.send_rc_control(0, fb, 0, speed)
 
    return error






def controller(starttime,stbat, now, img):
    lr, ud, bf, yv = 0,0,0,0
    speed = 50
    
    if press('p'): #picture
        cv2.imwrite(f'C:\\Users\\alfrost1@cps.edu\\Desktop\\drone\\{datetime.now()}.jpg', img)
        sleep(0.2)

    if press('f'): 
        drone.takeoff()
    if press('g'):
        drone.land()

    if press('w'): 
        print('forward')
        ud = 200
    if press('s'):
        print('back')
        ud = -200

    if press('a'):
        print('left')
        lr = -speed
    if press('d'):
        print('right')
        lr = speed

    if press('space'):
        print('up')
        bf = speed
    if press('shift'):
        print('down')
        bf = -speed

    if press('e'):
        yv = 200
    if press('q'):
        yv = -200
    
    if press('up'):
        drone.flip('f')
        sleep(0.3)
    if press('down'):
        drone.flip('b')
        sleep(0.3)
    if press('left'):
        drone.flip('l')
        sleep(0.3)
    if press('right'):
        drone.flip('r')
        sleep(0.3)
    
    return [lr,ud,bf,yv]

def run():
    print(f'Battery: {drone.get_battery()} Temp: {drone.get_temperature()}') #start msg
    sleep(1)
    stbat = drone.get_battery() #start battery
    now = datetime.now() #date time for log
    starttime = click() #start time for duration
    while True:
        if press('enter'): #kill switch
            drone.land()
            drone.streamoff()
            break
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (720,480))
        img, info = findFace(img)
        pError = trackFace(info, w, pid, pError)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
        vals = controller(starttime,stbat,now,img)
        drone.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    #log 
    doc = open('log.txt','a')
    doc.write(f'{now.strftime("%m/%d/%Y %H:%M:%S")} Flight Time: {(click()-starttime)/1000000000} Battery: {drone.get_battery()} Battery Loss:{drone.get_battery()-stbat}\n')
    doc.close()
    ###

run()

