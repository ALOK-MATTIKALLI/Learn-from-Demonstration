#!/usr/bin/env python3

import xArrmUtlis as utlis
from xarm.wrapper import XArmAPI

arm = XArmAPI('192.168.1.200')
def move_final(x,y, z, destination):
    utlis.moveToxyz_final(x,y,z)
    utlis.grip_close()
    utlis.home_final()
    utlis.home_final_l()
    if destination == 1:
        utlis.home_final_d1()
    elif destination == 2:
        utlis.home_final_d2()
    elif destination == 3:
        utlis.home_final_d3()
    utlis.grip_open()
    utlis.home_final_l()
    utlis.home_final()

utlis.input_setup()
# utlis.grip_close()
utlis.grip_open()
# utlis.home()
utlis.home_new()
# utlis.home_final_l()
utlis.home_final()
utlis.home_new()
# utlis.home()

# utlis.moveToxyz_final(400,50,3)
# utlis.grip_close()
# utlis.home_final()
# utlis.home_final_l()
# utlis.home_final_d3()
# utlis.grip_open()
# utlis.home_final_l()
# utlis.home_final()

# move_final(400, 50,5, destination=2)

arm.disconnect()
