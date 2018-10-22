import sys
sys.path.append('..')
from robot.components import MotorComponent
from basestation.xbox import Controller
import time

motor = MotorComponent('leftMotor', 'l_stick_vertical', 11, 12)
Controller.init()
controller = Controller(0)
while True:
    controller.update()
    controllerValue = round(-10*controller.left_y(), 1)
    print(controllerValue)
    time.sleep(.1)
    motor.doUpdate(controllerValue)