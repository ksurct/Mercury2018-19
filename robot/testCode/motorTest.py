import sys
sys.path.append('..')
from robot.components import MotorComponent
#from basestation.xbox import Controller
import time

motor = MotorComponent('leftMotor', 'l_stick_vertical', 11, 12)
controllerValue = 0
while True:
    controllerValue += 5
    print(controllerValue)
    time.sleep(.05)
    motor.doUpdate(controllerValue)
