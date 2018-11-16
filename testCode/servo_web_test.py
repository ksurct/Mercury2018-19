#This is test code to sweep a servo
import sys
sys.path.append("..")
import RPi.GPIO as GPIO
import time as time
from robot.networking import RobotNetwork

GPIO.setmode(GPIO.BOARD) #ALWAYS USE BOARD FOR CONSISTENCY BECAUSE WHY NOT
GPIO.setup(18, GPIO.OUT)

servo = GPIO.PWM(18,50)
servo.start(0)
network = RobotNetwork('http://0490f3a8.ngrok.io/')
#network = RobotNetwork('http://ksurct-dummy.localtunnel.me/')

try:
    while True:
        webStatus = network.getControllerStatus()
        if (webStatus["a"] == 1):
            servo.ChangeDutyCycle(10)
        else:
            servo.ChangeDutyCycle(100)
except KeyboardInterrupt:
    pass

servo.stop()
GPIO.cleanup();
