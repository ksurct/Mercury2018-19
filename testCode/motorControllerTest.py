import sys
sys.path.append('..')
from robot.components import MotorComponent
import time

motor = MotorComponent('leftMotor', 'l_stick_vertical', 11, 12)
x = -10.0
while (x <= 10):
    motor.doUpdate(x)
    print(x)
    time.sleep(.1)
    x += .1
time.sleep(2)
motor.doUpdate(0)
