import os
import sys
import time
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

ip = '192.168.1.200'
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
arm.set_gripper_enable(True)
arm.set_gripper_mode(0)
arm.set_gripper_speed(5000)
def home():
    arm.set_servo_angle(angle=[0, 0, 0, 0, 0, -90, 0], speed=10, wait=True)

file = open("final_test.traj","r")
file.seek(0)
text = file.read()
lst = []
to_list = text.split("\n")
for i in range (len(to_list)):
    new_list = to_list[i].split(" ")
    lst.append(new_list)
int_lst = []
for i in range (len(lst)-2):
    j_lst = []
    one_line = lst[i]
    for j in range(len(lst[i])):
        # print(i)
        j_lst.append(float(lst[i][j]))
    int_lst.append(j_lst)
print('ready')
speed = 10

home()
i = 0
while i < (len(int_lst)):
    ja1 = int_lst[i][0]
    ja2 = int_lst[i][1]
    ja3 = int_lst[i][2]
    ja4 = int_lst[i][3]
    ja5 = int_lst[i][4]
    ja6 = int_lst[i][5]
    ja7 = int_lst[i][6]
    grip = int_lst[i][7]
    arm.set_servo_angle(angle=[ja1, ja2, ja3, ja4, ja5, ja6, ja7], speed=speed, wait=True)
    arm.set_gripper_position(pos=grip, wait=True)
    i = i+1

file.close()
arm.disconnect()