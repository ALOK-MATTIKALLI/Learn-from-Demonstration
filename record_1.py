import curses
from xarm.wrapper import XArmAPI
import os
import sys
import time
from pynput.keyboard import Key, Controller

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

ip = '192.168.1.200'
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(2)
arm.set_state(state=0)

def home():
    arm.set_servo_angle(angle=[0, 0, 0, 0, 0, -90, 0], speed=10, wait=True)

file = open("final_test.traj", "a+")
arm.set_gripper_position(pos=800,wait=True)
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

Keyboard = Controller()
pre_joint = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
while True:
        print('load')
        joint_angles = []
        joint_ang = arm.get_servo_angle(is_radian=False)[1]
        for i in range(len(joint_ang)):
            joint_angles.append(round(joint_ang[i]))
        gripper_dis = arm.get_gripper_position()[1]
        if gripper_dis > 795:
            gripper_dis = 800

        cont = screen.getch()
        if cont == ord('c'):
            print('gripper')
            gripper_dis = 400
            for i in range (len(joint_angles)):
                file.write(str(joint_angles[i]))
                file.write(' ')
            file.write(str(gripper_dis))
            file.write('\n')
            arm.set_gripper_position(pos=gripper_dis,wait=True)
            print('gripper is closed')
            time.sleep(0.1)
        if cont == ord('o'):
            print('gripper')
            gripper_dis = 800
            for i in range (len(joint_angles)):
                file.write(str(joint_angles[i]))
                file.write(' ')
            file.write(str(gripper_dis))
            file.write('\n')
            arm.set_gripper_position(pos=gripper_dis,wait=True)
            print('gripper is open')
            pre_joint = joint_angles
            time.sleep(0.1)
        if cont== ord('s'):
            print('stop')
            time.sleep(0.1)
            pre_joint = joint_angles
            break
        else:
            if joint_angles != pre_joint:
                for i in range (len(joint_angles)):
                    file.write(str(joint_angles[i]))
                    file.write(' ')
                file.write(str(gripper_dis))
                file.write('\n')
            Keyboard.type('n')
            time.sleep(0.1)
            pre_joint = joint_angles

print('complete')
arm.set_mode(0)
arm.set_state(state=0)
file.close()
arm.disconnect()
