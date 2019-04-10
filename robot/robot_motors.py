"""
	File that holds main loop for the robot
	The robot will get controller data from the web server, translate that into motor and sensor positions, and then update the positions accordingly.
	The robot will also publish sensor data to the web service for the basestation. 
	We will maybe have two separate Pis for camera and motors/servos etc. The camera Pi should have its own folder and code and such
"""
import logging
from time import sleep, ctime
from random import randint
from threading import Thread
from networking import RobotNetwork
from components import *
from settings import * # this gets us constants such as WEB_SERVER_ADDRESS
import RPi.GPIO as GPIO

class Robot_Motors:
    def __init__(self):
        self.network = RobotNetwork(WEB_SERVER_ADDRESS + ":" + WEB_SERVER_PORT)
        self.controllerData = ''
        logging.basicConfig(format="%(name)s: %(levelname)s: %(asctime)s: %(message)s", level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.servoArr = [0, 0, 0, 0, 0]

        # To create a new output component (motor, servo, led), add a constructor here in the appropriate list, 
        # and create cooresponding fields in settings.py (ie, MOTOR_ONE_NAME). 
        # We like to keep these constants defined in settings.py in order to follow the Open / Close principle of software design.
        # Read more at: https://codeburst.io/understanding-solid-principles-open-closed-principle-e2b588b6491f
        
        #We probably want to create separate lists for motors and servos since motors need the backwards part and servos don't
        GPIO.cleanup()
        self.outputComponentList = [
            # motors

            # TODO Uncomment this when these fields are programmed in Settings.py
            MotorComponent(MOTOR_FR_NAME, MOTOR_FR_CONTROLLER_INPUT, MOTOR_FR_BACKWARD_INPUT, MOTOR_FR_DIRECTION_PIN, MOTOR_FR_PWM_PIN),
            MotorComponent(MOTOR_FL_NAME, MOTOR_FL_CONTROLLER_INPUT, MOTOR_FL_BACKWARD_INPUT, MOTOR_FL_DIRECTION_PIN, MOTOR_FL_PWM_PIN),
            MotorComponent(MOTOR_BR_NAME, MOTOR_BR_CONTROLLER_INPUT, MOTOR_BR_BACKWARD_INPUT, MOTOR_BR_DIRECTION_PIN, MOTOR_BR_PWM_PIN),
            MotorComponent(MOTOR_BL_NAME, MOTOR_BL_CONTROLLER_INPUT, MOTOR_BL_BACKWARD_INPUT, MOTOR_BL_DIRECTION_PIN, MOTOR_BL_PWM_PIN),

            # servos

            # TODO uncomment this when these fields are programmed in settings.py
            # ServoComponent(SERVO_ONE_NAME, SERVO_ONE_CONTROLLER_INPUT, SERVO_ONE_CHANNEL, SERVO_ONE_HOME, SERVO_ONE_MIN, SERVO_ONE_MAX)
            LauncherServoComponent(SERVO_L_NAME, SERVO_L_CHANNEL, SERVO_L_CONTROLLER_INPUT),
            ServoComponent(SERVO_PU_NAME, SERVO_PU_CHANNEL, SERVO_PU_PRESET_DICT, SERVO_PU_MIN, SERVO_PU_MAX),
            ServoComponent(SERVO_CAM_NAME, SERVO_CAM_CHANNEL, SERVO_CAM_PRESET_DICT, SERVO_CAM_MIN, SERVO_CAM_MAX),

            # leds

            # TODO uncomment htis when these fields are programmed in settings.py
            LEDComponent(LED_ONE_NAME, LED_ONE_CONTROLLER_INPUT, LED_ONE_CHANNEL)
        ]
        #print(self.outputComponentList)
		
    def __del__(self):
        GPIO.cleanup()
        
    def mainLoop(self):
        try:
            print("Right before while true")
            while True:
                #Get controller data and update motors, servos, LEDs
                self.controllerDataTuple = self.network.getControllerStatus()
                self.controllerData = self.controllerDataTuple[0]
                #print(self.controllerData)
                if(self.controllerDataTuple[1] == False):
                    self.logger.info("Unable to get controller data. Trying again soon.") #Shows error message and current time
                    sleep(2)
                    continue #This goes back to the top of the while loop and forces us to get new controller values
                            #We can do this because sending sensor data isn't as important as getting updated controller data.
                            #Plus the network is down, so it wouldn't make sense to try and send data again. 
                self.servoArr = [self.controllerData['u'], self.controllerData['d'], self.controllerData['l'], self.controllerData['r'], self.controllerData['lsy']]  
                
                #TODO Do button debouncing for 90 degree turn code below (before self.updateOutputComponents)
                #Use an object variable (self.didTurn) that is initialized to False in __init__() to do debouncing with
                #Should probably 'continue' after doing a turn so we don't do self.updateOutputComponents


                self.updateOutputComponents()

        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt detected. Exiting now.")
        finally:
            #ensure robot loop gets closed
            self.logger.info("Event loop closed. Exiting program")
            GPIO.cleanup()
    
    def updateOutputComponents(self):
        for c in self.outputComponentList:
            #print(c)
            if isinstance(c, MotorComponent):
                #print(self.controllerData[c.controllerInput])
                c.doUpdate(self.controllerData[c.controllerInput], self.controllerData[c.backwardInput], self.controllerData['lim'])
            elif isinstance(c, ServoComponent):
                c.doUpdate(self.servoArr)
            elif isinstance(c, LauncherServoComponent):
                #print("Updating LauncherServo with value of {} channel {}".format(self.controllerData[c.controllerInput], c.channel))
                c.doUpdate(self.controllerData[c.controllerInput])
            elif isinstance(c, LEDComponent):
                c.doUpdate(self.controllerData['hl'])
                
    def updateOutputComponentsTEST(self):
        print("Controller Data: " + ctime() + " A is " + str(self.controllerData['a']))

    def outputComponentThreadMethod(self):
        while True:
            self.controllerDataTuple = self.network.getControllerStatus()
            self.controllerData = self.controllerDataTuple[0]
            if(self.controllerDataTuple[1] == False):
                self.logger.info("Unable to get controller data. Trying again soon.") #Shows error message and current time
                sleep(2)
                continue #This goes back to the top of the while loop and forces us to get new controller values
                        #We can do this because sending sensor data isn't as important as getting updated controller data.
                        #Plus the network is down, so it wouldn't make sense to try and send data again.   
            self.updateOutputComponentsTEST()

if __name__ == '__main__':
    try:
        sleep(30)
        r = Robot_Motors()
        print("Going into mainLoop")
        r.mainLoop()
    except Exception as e:
        print("ERROR {}".format(e))
        GPIO.cleanup()

    """t1 = Thread(target=r.outputComponentThreadMethod, name='OUTPUT-COMP-THREAD')
    t2 = Thread(target=r.sensorUpdateThreadMethod, name='SENSOR-THREAD')
    t1.start()
    t2.start()"""

    """GPIO.cleanup()
    m1 = MotorComponent('leftMotor', 'l_stick', 11, 18)
    m2 = MotorComponent('leftMotor', 'l_stick', 13, 15)
    val1 = 0
    val2 = 100
    while True:
        while val1 < 100:
            print(str(val1) + " " + str(val2))
            m1.doUpdate(val1)
            m2.doUpdate(val2)
            time.sleep(.1)
            val1 += 1
            val2 -= 1
        #time.sleep(1)
        while val1 > 0:
            print(str(val1) + " " + str(val2))
            m1.doUpdate(val1)
            m2.doUpdate(val2)
            time.sleep(.1)
            val1 -= 1
            val2 += 1
    #m.doUpdate(5)
    #while True:
    #    pass
    GPIO.cleanup()"""
