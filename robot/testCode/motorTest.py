from robot.components import MotorComponent
from basestation.xbox import Controller
import time

motor = MotorComponent('leftMotor', 'l_stick_vertical', 11, 12)
Controller.init()
controller = Controller(0)
while True:
    controllerValue = round(controller.left_y(), 1)
    print(controllerValue)
    time.sleep(.05)
    #motor.doUpdate(controllerValue)
