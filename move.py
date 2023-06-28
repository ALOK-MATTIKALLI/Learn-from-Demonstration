# input x and y from camera and moving the xarm to that point

#!/usr/bin/env python3

import xArrmUtlis as utlis

from xarm.wrapper import XArmAPI

ip = '192.168.1.200'
arm = XArmAPI(ip)

utlis.input_setup()

utlis.grip_open()
utlis.home_new()
print('x value should be between (310, 810)')
print('y value should be between (-175, 195)')
xin = (int(input('enter the value of x:')))
yin = (int(input('enter the value of y:')))
# x,y = utlis.camToArm(xin,yin)
x = xin
y = yin
print(x,y)
z = 20

utlis.moveToxyz(x,y,z)
utlis.grip_close()

utlis.grip_open()
utlis.home_new()

arm.disconnect()