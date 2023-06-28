#!/usr/bin/env python3

import time
import xArrmUtlis as utlis
import cv2
import oakUtlis as oak
from pynput.keyboard import Key, Controller
import curses

from xarm.wrapper import XArmAPI
arm = XArmAPI('192.168.1.200')

# def color_of_blockXY(x, y):
#     block = ''
#     b1 = [[0,0]]
#     b2 = [[0,0]]
#     b3 = [[0,0]]

#     b1,b2,b3 = oak.findCenter()
#     cv2.destroyAllWindows()
#     if len(b1) > 1:
#         for i in range (len(b1)):
#             if b1[i] == [0,0]:
#                 b1.remove([0,0])
#     if len(b2) > 1:
#         for i in range (len(b2)-1):
#             if b2[i] == [0,0]:
#                  b2.remove([0,0])
#     if len(b3) > 1:
#         for i in range (len(b3)-1):
#             if b3[i] == [0,0]:
#                 b3.remove([0,0])

#     print(b1)
#     print(b2)
#     print(b3)
#     time.sleep(0.1)
#     if oak.color_search(b1, x, y) != [0,0]:
#         block ='b1'
#         x = oak.color_search(b1, x, y)[0]
#         y = oak.color_search(b1, x, y)[1]
#         print ('b1', oak.color_search(b1, x, y))
#     elif oak.color_search(b2, x, y) != [0,0]:
#         block = 'b2'
#         x = oak.color_search(b2, x, y)[0]
#         y = oak.color_search(b2, x, y)[1]
#         print('b2', oak.color_search(b2, x, y))
#     elif oak.color_search(b3, x, y) != [0,0]:
#         block = 'b3'
#         x = oak.color_search(b3, x, y)[0]
#         y = oak.color_search(b3, x, y)[1]
#         print('b3', oak.color_search(b3, x, y))
    
#     return block, x, y

def remove_0(b):
    if len(b) >= 1:
        if len(b) == 1:
            if b[0] == [0,0]:
                b.remove([0,0])
        else:
            for i in range (len(b)-1):
                if b[i] == [0,0]:
                    b.remove([0,0])
    return b

arm.motion_enable(enable=True)
arm.set_mode(2)
arm.set_state(state=0)
arm.set_tcp_jerk(10000)
arm.set_joint_jerk(500,is_radian=True)
arm.set_gripper_enable(True)
arm.set_gripper_mode(0)
arm.set_gripper_speed(5000)
arm.save_conf()

file = open("Data.txt", "a+")
data = []
arm.set_gripper_position(pos=800,wait=True)
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

Keyboard = Controller()

while True:
        cont = screen.getch()
        if cont == ord('c'):
            print('gripper close')
            utlis.grip_close()
            xa,ya = utlis.getxy(0)
            xc,yc = utlis.ArmToCam(xa, ya)
            print(xc, yc)
            # oak.color_of_blockXY(x,y)
            x = xc
            y = yc
            block = ''
            b1 = [[0,0]]
            b2 = [[0,0]]
            b3 = [[0,0]]

            b1,b2,b3 = oak.findCenter()
            cv2.destroyAllWindows()

            b1 = remove_0(b1)
            b2 = remove_0(b2)
            b3 = remove_0(b3)

            print(b1)
            print(b2)
            print(b3)
            time.sleep(0.1)
            if oak.color_search(b1, x, y) != [0,0]:
                block ='b1'
                x = oak.color_search(b1, x, y)[0]
                y = oak.color_search(b1, x, y)[1]
                print ('b1', oak.color_search(b1, x, y))
            elif oak.color_search(b2, x, y) != [0,0]:
                block = 'b2'
                x = oak.color_search(b2, x, y)[0]
                y = oak.color_search(b2, x, y)[1]
                print('b2', oak.color_search(b2, x, y))
            elif oak.color_search(b3, x, y) != [0,0]:
                block = 'b3'
                x = oak.color_search(b3, x, y)[0]
                y = oak.color_search(b3, x, y)[1]
                print('b3', oak.color_search(b3, x, y))
            xc = x
            yc = y
            print('block is', block)
            print(xc, yc)
            # upload = input('do you want to upload the data\n', 'if yes type "y" else type "n"')
            # if upload == 'y' or upload == 'Y':n
            file.write(block)
            file.write('\n')
            
        if cont == ord('o'):
            print('gripper open')
            utlis.grip_open()
        if cont== ord('s'):
            print('stop')
            break
        else:
            Keyboard.type('n')
            time.sleep(0.1)
arm.set_mode(0)
arm.set_state(state=0)
file.close()
arm.disconnect()