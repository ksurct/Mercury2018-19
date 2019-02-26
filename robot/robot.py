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

class Robot:
    def __init__(self):
        self.network = RobotNetwork(WEB_SERVER_ADDRESS + ":" + WEB_SERVER_PORT)
        self.controllerData = ''
        logging.basicConfig(format="%(name)s: %(levelname)s: %(asctime)s: %(message)s", level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # To create a new output component (motor, servo, led), add a constructor here in the appropriate list, 
        # and create cooresponding fields in settings.py (ie, MOTOR_ONE_NAME). 
        # We like to keep these constants defined in settings.py in order to follow the Open / Close principle of software design.
        # Read more at: https://codeburst.io/understanding-solid-principles-open-closed-principle-e2b588b6491f
        
        #We probably want to create separate lists for motors and servos since motors need the backwards part and servos don't
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
            LauncherServoComponent(SERVO_L_NAME, SERVO_L_CHANNEL, SERVO_L_CONTROLLER_INPUT)

            # leds

            # TODO uncomment htis when these fields are programmed in settings.py
            #LEDComponent(LED_ONE_NAME, LED_ONE_CONTROLLER_INPUT)
        ]
        self.sensorList = []

        self.sensorValues = {
            'qfr': 0, 'qfl': 0, 'qbr': 0, 'qbl': 0,
			'df': 0, 'db': 0, 'dl': 0, 'dr': 0
        }

		

    def mainLoop(self):
        try:
            while True:
                #Get controller data and update motors, servos, LEDs
                self.controllerDataTuple = self.network.getControllerStatus()
                self.controllerData = self.controllerDataTuple[0]
                if(self.controllerDataTuple[1] == False):
                    self.logger.info("Unable to get controller data. Trying again soon.") #Shows error message and current time
                    sleep(2)
                    continue #This goes back to the top of the while loop and forces us to get new controller values
                            #We can do this because sending sensor data isn't as important as getting updated controller data.
                            #Plus the network is down, so it wouldn't make sense to try and send data again.   
                self.updateOutputComponents()

                self.updateSensorValuesTEST()
                self.network.updateSensorData(self.sensorValues)

        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt detected. Exiting now.")
        finally:
            #ensure robot loop gets closed
            self.logger.info("Event loop closed. Exiting program")
            GPIO.cleanup()

    def updateOutputComponents(self):
        for c in self.outputComponentList:
            if c is MotorComponent:
                c.doUpdate(self.controllerData[c.controllerInput], self.controllerData[c.backwardInput])
            else:
                c.doUpdate(self.controllerData[c.controllerInput])

    def updateSensorValues(self):
        for s in self.sensorValues:
            self.sensorValues[s] = s.doUpdate(self.sensorList[s]) #Definitely test this line when we get sensors

    def updateOutputComponentsTEST(self):
        print("Controller Data: " + ctime() + " A is " + str(self.controllerData['a']))

    def updateSensorValuesTEST(self):
        for s in self.sensorValues:
            self.sensorValues[s] = randint(0, 1000)

    def sensorUpdateThreadMethod(self):
        while True:
            self.updateSensorValuesTEST()
            self.network.updateSensorData(self.sensorValues)

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
        r = Robot()
        r.mainLoop()
    except:
        print("ERROR")
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
