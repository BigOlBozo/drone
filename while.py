#from djitellopy import tello
from time import sleep
import os
from keyboard import is_pressed as press
from time import perf_counter_ns as click
with open('log.txt','r'):
    pass
def controller():
    drone.takeoff()
    sleep(1)
    x = 0 
    doc = open('log.txt','a')
    while True:

        start = click()
        startbat = drone.get_battery()
        if press('up'):
            print('forward')
            #drone.move_forward(20,0,0)
            sleep(0.3)
        if press('down'):
            print('back')
            #drone.move_back(20,0,0)
            sleep(0.3)
        if press('left'):
            print('left')
            #drone.move_left(20,0,0)
            sleep(0.3)
        if press('right'):
            print('right')
            #drone.move_right(20,0,0)
            sleep(0.3)
        if press('space'):
            print('up')
            #drone.move_up(20,0,0)
            sleep(0.3)
        if press('left ctrl'):
            print('down')
            #drone.move_down(20,0,0)
            sleep(0.3)
        if press('enter'):
            print('land')
            #drone.land()
            break
        doc.write(f'{(drone.get_battery()-startbat)/((click()-start)/1000000000)} \n')
    doc.close()
    print('Landed')
controller()