#This is test code to sweep a servo
import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import time as time
from robot.networking import RobotNetwork

#from __future__ import division

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

pwm.set_pwm_freq(60)

network = RobotNetwork('10.135.79.80:8000')

try:
    while True:
        #webStatus = network.getControllerStatus()
        #if (webStatus["a"] == 1):
        pwm.set_pwm(0, 0, 300)
        print ("400")
        time.sleep(1)
        #else:
        pwm.set_pwm(0, 0, 100)
        print ("300")
        time.sleep(1)
except KeyboardInterrupt:
    pass

pwm.set_pwm(0, 0, 0)
GPIO.cleanup();