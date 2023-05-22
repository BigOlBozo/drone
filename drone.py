from djitellopy import tello
from time import sleep
import os
from keyboard import is_pressed as press
from time import perf_counter_ns as click
from datetime import datetime
os.system('cls')

drone = tello.Tello()
drone.connect()

#camera
import cv2
import time 

global img
drone.streamon()


def controller(starttime,stbat, now):
    lr, ud, bf, yv = 0,0,0,0
    speed = 50
    if press('p'): #picture
        cv2.imwrite(f'C:\\Users\\alfrost1@cps.edu\\Desktop\\drone\\{time.time()}.jpg', img)
        sleep(0.2)
    if press('f'):
        drone.takeoff()
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
    if press('g'):
        drone.land()
        print('land')
    if press('i'):
        drone.flip('f')
        sleep(.5)
    if press('k'):
        drone.flip('b')
        sleep(.5)
    if press('j'):
        drone.flip('l')
        sleep(.5)
    if press('l'):
        drone.flip('r')
        sleep(.5)
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
            break
        vals = controller(starttime,stbat,now)
        drone.send_rc_control(vals[0],vals[1],vals[2],vals[3])
        try: #img
            img = drone.get_frame_read().frame
            img = cv2.resize(img, (360,240))
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        except:
            print('Error')
            pass
    #log 
    doc = open('log.txt','a')
    doc.write(f'{now.strftime("%m/%d/%Y %H:%M:%S")} Flight Time: {(click()-starttime)/1000000000} Battery: {drone.get_battery()} Battery Loss:{drone.get_battery()-stbat}\n')
    doc.close()
    ###

run()

