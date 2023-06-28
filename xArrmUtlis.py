#!/usr/bin/env python3

import os
import sys
import time

from xarm.wrapper import XArmAPI

ip = '192.168.1.200'
arm = XArmAPI(ip)

def input_setup():

    sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)
    arm.set_tcp_jerk(10000)
    arm.set_joint_jerk(500,is_radian=True)
    arm.set_gripper_enable(True)
    arm.set_gripper_mode(0)
    arm.set_gripper_speed(5000)
    # arm.set_tcp_offset([0,0,172,0,0,0], is_radian=False)
    arm.save_conf()

input_setup()

def home():
    arm.set_servo_angle(angle=[0, 0, 0, 0, 0, -90, 0], speed=20, wait=True)
    waitIfMoving()

def home_new():
    arm.set_servo_angle(angle=[0, -70, 0, 0, 0, 40, 0], speed=20, wait=True)
    waitIfMoving()

def home_right():
    arm.set_servo_angle(angle=[-90, 0, 0, 0, -90, -40, 0], speed=20, wait=True)
    waitIfMoving()

def home_left():
    arm.set_servo_angle(angle=[90, 0, 0, 10, 90, -40, 0], speed=20, wait=True)
    waitIfMoving()

def home_final():
    arm.set_servo_angle(angle=[0, -50, 0, 10, 0, 60, 0], speed=20, wait=True)
    waitIfMoving()

def home_final_l():
    arm.set_servo_angle(angle=[90, -50, 0, 10, 0, 60, 0], speed=20, wait=True)
    waitIfMoving()

def home_final_d1():
    arm.set_servo_angle(angle=[90, 10, 0, 35, 0, 20, 0], speed=20, wait=True)
    waitIfMoving()

def home_final_d2():
    arm.set_servo_angle(angle=[90, 5, 0, 35, 0, 25, 0], speed=20, wait=True)
    waitIfMoving()

def home_final_d3():
    arm.set_servo_angle(angle=[90, -2, 0, 42, 0, 43, 0], speed=20, wait=True)
    waitIfMoving()

def positon(cX,cY,cZ,cRoll,cPitch,cYaw,speed,radian=False,delay=True, path='y'):
    pre = arm.get_position()[1]
    pX = pre[0]
    pY = pre[1]
    pZ = pre[2]
    pRoll = pre[3]
    pPitch = pre[4]
    pYaw = pre[5]
    if path == 'x':
        arm.set_position(x=pX, y=pY,z=pZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=pY,z=pZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=pZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=cZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=cZ,roll=cRoll,pitch=cPitch,yaw=cYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
    elif path == 'y':
        arm.set_position(x=pX, y=pY,z=pZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=pX, y=cY,z=pZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=pZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=cZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=cZ,roll=cRoll,pitch=cPitch,yaw=cYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
    elif path == 'z':
        arm.set_position(x=pX, y=pY,z=pZ,roll=pRoll,pitch=pPitch,yaw=pYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=pX, y=pY,z=cZ,roll=cRoll,pitch=cPitch,yaw=cYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=pX, y=cY,z=cZ,roll=cRoll,pitch=cPitch,yaw=cYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=cZ,roll=cRoll,pitch=cPitch,yaw=cYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()
        arm.set_position(x=cX, y=cY,z=cZ,roll=cRoll,pitch=cPitch,yaw=cYaw, speed=speed,is_radian=radian,wait=delay)
        waitIfMoving()

def waitIfMoving():
    time.sleep(0.01)
    while arm.get_is_moving() == True:
        pass
    time.sleep(0.01)

def camToArm(xcam, ycam):
    xarm = 833-ycam
    yarm = 267-xcam
    # print('arm point', xarm, yarm)
    return xarm, yarm

def ArmToCam(xarm, yarm):
    xcam = 267 - yarm
    ycam = 833 - xarm
    # print('cam point', xcam, ycam)
    return xcam, ycam

def getxy(decimalPlace):
    if decimalPlace == 0:
        x = int(arm.get_position()[1][0])
        y = int(arm.get_position()[1][1])
    else:
        x = round(arm.get_position()[1][0], decimalPlace)
        y = round(arm.get_position()[1][1], decimalPlace)
    return x, y

def grip_close():
    arm.set_gripper_position(490,True, speed=500)
    waitIfMoving()
    time.sleep(1.0)

def grip_open():
    arm.set_gripper_position(850,True, speed=500)
    waitIfMoving()
    time.sleep(1.0)

def moveToxyz(x,y,z):
    p = 'y'
    if y < -60 and x < 500:
        home_right()
        # utlis.home_new()
        print('right')
        p = 'x'
    elif y > 60 and x < 500:
        home_left()
        # utlis.home_new()
        print('left')
        y = y - 20
        p = 'x'
    else:
        home_new()

    spd = 10
    print(arm.get_position())
    time.sleep(0.5)
    positon(cX=x, cY=y, cZ=z, cRoll=180, cPitch=-40, cYaw=0, speed=spd, path=p)

def moveToxyz_final(x,y,z):
    p = 'y'
    if y < -60 and x < 500:
        home_right()
        # utlis.home_new()
        print('right')
        p = 'x'
    elif y > 60 and x < 500:
        home_left()
        # utlis.home_new()
        print('left')
        y = y - 20
        p = 'x'
    else:
        home_final()

    spd = 20
    print(arm.get_position())
    time.sleep(0.5)
    positon(cX=x, cY=y, cZ=z, cRoll=180, cPitch=0, cYaw=0, speed=spd, path=p)

