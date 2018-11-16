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

pwm.set_pwm_freq(60)

network = RobotNetwork('http://10.135.79.80:8000/')

#360 is stopped, Higher is counter, and lower in clockwise

try:
    while True:
        #webStatus = network.getControllerStatus()
        #if (webStatus["a"] == 1):
        pwm.set_pwm(0, 0, 400)
        print ("ON")
        time.sleep(3)
        #else:
        pwm.set_pwm(0, 0, 0)
        print ("OFF")
        time.sleep(1)
except KeyboardInterrupt:
    pass

pwm.set_pwm(0, 0, 0)
GPIO.cleanup();