import os
import sys
import time
# import winsound
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI
from pynput import keyboard
ip = '192.168.1.200'

arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

fre = 2000  # in Hz
dur = 500  # in mili sec


# Turn on manual mode before recording
arm.set_mode(2)
arm.set_state(0)

# winsound.Beep(fre, dur)

arm.start_record_trajectory()
if keyboard.Events() != 0:
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.esc:
                break
            else:
                print('Received event {}'.format(event))
                print('Received key {}'.format(event.key))
            break
# Analog recording process, here with delay instead
time.sleep(20)
print('stop')
# winsound.Beep(fre, dur)
time.sleep(1)

arm.stop_record_trajectory()
arm.save_record_trajectory('r_test1.traj')

# Turn off manual mode after recording
arm.set_mode(0)
arm.set_state(0)

######################################################################

arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)


arm.load_trajectory('r_test1.traj')
arm.playback_trajectory()