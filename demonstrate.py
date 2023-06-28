#!/usr/bin/env python3

import xArrmUtlis as xarm
import oakUtlis as oak
import time
from xarm.wrapper import XArmAPI

ip = '192.168.1.200'
arm = XArmAPI(ip)

xarm.input_setup()
file = open("Data.txt","r")
file.seek(0)
text = file.read()
lst = []
to_list = text.split("\n")
# to_list.remove('')
# xarm.home_final()
xarm.home_new()

def move_final(x,y, z, destination):
    xarm.moveToxyz_final(x,y,z)
    xarm.grip_close()
    xarm.home_final()
    xarm.home_final_l()
    if destination == 1:
        xarm.home_final_d1()
    elif destination == 2:
        xarm.home_final_d2()
    elif destination == 3:
        xarm.home_final_d3()
    xarm.grip_open()
    xarm.home_final_l()
    # xarm.home_final()
    xarm.home_new()

for i in range (1000):
    b1 = []
    b2 = []
    b3 = []
    b1.append([0,0])
    b2.append([0,0])
    b3.append([0,0])
    b1,b2,b3 = oak.findCenter()
    b1 = oak.remove_0(b1)
    b2 = oak.remove_0(b2)
    b3 = oak.remove_0(b3)
    print('following are the coordinates of block b1, b2 & b3 (with respect to camera)')
    print(b1)
    print(b2)
    print(b3)
    cont = input('do you want to continue\n' + 'if yes type "y" else type "n"\n')
    if cont == 'y' or cont == 'Y':
        ##################
        print('Remove error points if found')
        for j in range (100):
            print('do you want to remove any point')
            delete = ''
            delete = str(input('if yes type "y" else type "n"\n'))
            if delete == 'y':
                b_name = 0
                b_name = int(input('enter the block number "1", "2", or "3"\n'))
                point_index = int(input('enter the point to be deleted 1st, 2nd, 3rd, etc\n'))-1
                
                if b_name == 1:
                    b1.pop(point_index)
                elif b_name == 2:
                    b2.pop(point_index)
                elif b_name == 3:
                    b3.pop(point_index)
                print(b1)
                print(b2)
                print(b3)
                print('do you want to remove another point')
                delete_new = input('if yes type "y" else type "n"\n')
                if delete_new == 'n':
                    break
            else:
                break
        ##################
        break

order = []

for i in range (len(to_list)):
    if to_list[i] == 'b1':
        order.append(1)
    elif to_list[i] == 'b2':
        order.append(2)
    elif to_list[i] == 'b3':
        order.append(3)

# print(to_list)
print("the order of the block is: ", order)
coordinate = []
for i in range (len(order)):
    if order[i] == 1:
        coordinate.append(b1[0])
    elif order[i] == 2:
        coordinate.append(b2[0])
    elif order[i] == 3:
        coordinate.append(b3[0])
print('coordinate ')
print(coordinate)
coordinate_new = []

for i in range (len(coordinate)):
    xC = coordinate[i][0]
    yC = coordinate[i][1]
    xA, yA = xarm.camToArm(xC, yC)
    coordinate_new.append([xA, yA]) 

print(coordinate_new)
z_val = 3
xarm.home_new()
move_final(x=coordinate_new[0][0], y=coordinate_new[0][1], z=z_val, destination=1)
move_final(x=coordinate_new[1][0], y=coordinate_new[1][1], z=z_val, destination=2)
move_final(x=coordinate_new[2][0], y=coordinate_new[2][1], z=z_val, destination=3)
