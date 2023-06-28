from pynput import keyboard
from xarm.wrapper import XArmAPI
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

ip = '192.168.1.200'

arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(2)
arm.set_state(state=0)


def home():
    arm.set_servo_angle(angle=[0, 0, 0, 0, 0, -90, 0], speed=10, wait=True)



file = open("myfile.traj", "a+")

# keypad = keyboard.Controller()
# keys = keyboard.Key()
# while True:
#     print('load')
#     if keypad.release('c'):
#         print('gripper c or o')
#     if keys == keys.esc:
#         break
#     else:
#         keypad.type('a')

with keyboard.Events() as events:
    for event in events:
        joint_angles = arm.get_servo_angle(is_radian=False)[1]
        gripper_dis = arm.get_gripper_position()[1]
        for i in range (len(joint_angles)):
            file.write(str(joint_angles[i]))
            file.write(' ')
        file.write(str(gripper_dis))
        file.write('\n')
        if event.key.char == 'c':
            print('gripper is closed')
            time.sleep(0.1)
        if event.key == event.key.esc:
            time.sleep(0.1)
            break



arm.set_mode(0)
arm.set_state(state=0)
file.close()
arm.disconnect()
