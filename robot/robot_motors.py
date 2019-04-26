"""
	File that holds main loop for the robot motors and servos
	The robot will get controller data from the web server, translate that into motor and sensor positions, and then update the positions accordingly.
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

        self.turn90DegFlag = False
        
        # Create drive state
        # Drive state options are: "active", "auto", "danger", "dangerActive"
        # active - control the robot as normal
        # auto - engage autopilot to keep the robot moving forward, straight
        # danger - The front right sensor is reading a wall too close, stop movement momentarily
        # dangerActive - The front right sensor is reading too close, but we've waited long enough to be able to move
        self.driveState = "active" # default to active
        self.outOfAuto = False

        # To create a new output component (motor, servo, led), add a constructor here in the appropriate list, 
        # and create cooresponding fields in settings.py (ie, MOTOR_ONE_NAME). 
        # We like to keep these constants defined in settings.py in order to follow the Open / Close principle of software design.
        # Read more at: https://codeburst.io/understanding-solid-principles-open-closed-principle-e2b588b6491f
        
        GPIO.cleanup()
        self.outputComponentList = [
            # motors

            MotorComponent(MOTOR_FR_NAME, MOTOR_FR_CONTROLLER_INPUT, MOTOR_FR_BACKWARD_INPUT, MOTOR_FR_DIRECTION_PIN, MOTOR_FR_PWM_PIN),
            MotorComponent(MOTOR_FL_NAME, MOTOR_FL_CONTROLLER_INPUT, MOTOR_FL_BACKWARD_INPUT, MOTOR_FL_DIRECTION_PIN, MOTOR_FL_PWM_PIN),
            MotorComponent(MOTOR_BR_NAME, MOTOR_BR_CONTROLLER_INPUT, MOTOR_BR_BACKWARD_INPUT, MOTOR_BR_DIRECTION_PIN, MOTOR_BR_PWM_PIN),
            MotorComponent(MOTOR_BL_NAME, MOTOR_BL_CONTROLLER_INPUT, MOTOR_BL_BACKWARD_INPUT, MOTOR_BL_DIRECTION_PIN, MOTOR_BL_PWM_PIN),

            # servos

            LauncherServoComponent(SERVO_L_NAME, SERVO_L_CHANNEL, SERVO_L_CONTROLLER_INPUT),
            ServoComponent(SERVO_PU_NAME, SERVO_PU_CHANNEL, SERVO_PU_PRESET_DICT, SERVO_PU_MIN, SERVO_PU_MAX),
            ServoComponent(SERVO_CAM_NAME, SERVO_CAM_CHANNEL, SERVO_CAM_PRESET_DICT, SERVO_CAM_MIN, SERVO_CAM_MAX),

            # leds

            LEDComponent(LED_ONE_NAME, LED_ONE_CONTROLLER_INPUT, LED_ONE_CHANNEL)
        ]
		
    def __del__(self):
        GPIO.cleanup()
        
    def mainLoop(self):
        try:
            dangerCount = 0 # initialize this variable for state transition logic

            print("Right before while true")
            while True:
                #Get controller data and update motors, servos, LEDs
                """
                self.controllerSensorDataTuple = self.network.getControllerAndSensorStatus()
                self.controllerSensorData = self.controllerSensorDataTuple[0]
                self.controllerData = self.controllerSensorData[0] #CONTROLLER DATA FROM THE BASESTATION
                self.sensorData = self.controllerSensorData[1] #SENSOR DATA FROM SECOND PI
                #print(self.controllerData)
                if(self.controllerSensorDataTuple[1] == False):
                    self.logger.info("Unable to get controller data. Trying again soon.") #Shows error message and current time
                    sleep(2)
                    self.updateMotorComponents()
                    continue #This goes back to the top of the while loop and forces us to get new controller values
                """
                self.controllerDataTuple = self.network.getControllerStatus()
                self.controllerData = self.controllerDataTuple[0]
                if(self.controllerDataTuple[1] == False):
                    self.logger.info("Unable to get controller data. Trying again soon.") #Shows error message and current time
                    sleep(2)
                    self.updateMotorComponents()
                self.servoArr = [self.controllerData['u'], self.controllerData['d'], self.controllerData['l'], self.controllerData['r'], self.controllerData['lsy']]  
                
                #if (self.driveState == 'active'):
                if (self.controllerData['b'] == 1):
                    if (self.turn90DegFlag == False):
                        self.turn90DegFlag = True
                        self.turn90CW()
                        continue
                elif (self.controllerData['x'] == 1):
                    if (self.turn90DegFlag == False):
                        self.turn90DegFlag = True
                        self.turn90CCW()
                        continue
                else:
                    self.turn90DegFlag = False
                    self.updateOutputComponents()
                """
                elif (self.driveState == 'auto'):
                    if (self.sensorData['dsr'] < 305 and self.sensorData['dsl'] < 305):
                        self.updateMotorComponents(forceLim=100, auto=True)
                    else:
                        self.driveState = 'active'
                        self.outOfAuto = True
                        
                elif (self.driveState == 'dangerActive'):
                    self.updateOutputComponents()
                
                # Read Sensor data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
                # Determine next state
                if (self.driveState == "active"):
                    # TODO figure out how to read from sensors here
                    
                    if (self.sensorsShowDanger()):
                        self.driveState = "danger"
                        dangerCount = 0
                    elif(self.controllerData['se'] == 1 and self.outOfAuto == False):
                        self.driveState = "auto"
                    else:
                        self.outOfAuto = False
                    
                elif (self.driveState == "auto"):
                    # TODO figure out how to read from sensors here
                    if (self.sensorsShowDanger()):
                        self.driveState = "danger"
                        dangerCount = 0
                    elif(self.sensorData['dsr'] > 305 or self.sensorData['dsl'] > 305):
                        self.driveState = "active"
                    
                elif (self.driveState == "danger"):
                    if (self.controllerData['lb'] == 1 and self.controllerData['rb'] == 1 and self.controllerData['lt'] != 0 and self.controllerData['rt'] != 0):
                        # TODO update motors
                        self.updateMotorComponents()
                    elif (dangerCount > DANGER_COUNT_THRESHOLD):
                        self.driveState = 'dangerActive'
                        dangerCount = 0
                    else:
                        dangerCount += 1
                elif (self.driveState == "dangerActive"):
                    # TODO figure out how to read from sensors here
                    
                    if(self.sensorsShowDanger() == False):
                        self.dangerState = "active"
                    
                else:
                    # This is bad maybe throw error or set driveState to active here
                    self.driveState = 'active'
                """


        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt detected. Exiting now.")
        finally:
            #ensure robot loop gets closed
            self.logger.info("Event loop closed. Exiting program")
            GPIO.cleanup()
    """
    def sensorsShowDanger(self):
        for s in self.sensorData:
            if (self.sensorData[s] < 60 and s != 'dfr'): #We have the check for not dfr since that's the one in front of picky-uppy
                return True
        return False
    """
    def turn90CW(self):
        for m in self.outputComponentList:
            if (isinstance(m, MotorComponent)):
                if ('left' in m.name):
                    m.doUpdate(8191, 0, 100)
                elif ('right' in m.name):
                    m.doUpdate(8191, 1, 100)
        sleep(.5) #TODO Update this value with the correct sleep time
        for m in self.outputComponentList:
            if (isinstance(m, MotorComponent)):
                if ('left' in m.name):
                    m.doUpdate(0, 0, 100)
                elif ('right' in m.name):
                    m.doUpdate(0, 0, 100)

    def turn90CCW(self):
        for m in self.outputComponentList:
            if (isinstance(m, MotorComponent)):
                if ('left' in m.name):
                    m.doUpdate(8191, 1, 100)
                elif ('right' in m.name):
                    m.doUpdate(8191, 0, 100)
        sleep(.5) #TODO Update this value with the correct sleep time
        for m in self.outputComponentList:
            if (isinstance(m, MotorComponent)):
                if ('left' in m.name):
                    m.doUpdate(0, 0, 100)
                elif ('right' in m.name):
                    m.doUpdate(0, 0, 100)
    
    def updateOutputComponents(self):
        for c in self.outputComponentList:
            if isinstance(c, MotorComponent):
                #print("Doing update on MotorComponent {}".format(c.name))
                c.doUpdate(self.controllerData[c.controllerInput], self.controllerData[c.backwardInput], self.controllerData['lim'])
            elif isinstance(c, ServoComponent):
                c.doUpdate(self.servoArr)
            elif isinstance(c, LauncherServoComponent):
                c.doUpdate(self.controllerData[c.controllerInput])
            elif isinstance(c, LEDComponent):
                c.doUpdate(self.controllerData['hl'])

    def updateMotorComponents(self, forceLim=40, auto=False):
        for c in self.outputComponentList:
            if isinstance(c, MotorComponent):
                if (auto == True):
                    c.doUpdate(8191, 0, forceLim)
                else:
                    c.doUpdate(self.controllerData[c.controllerInput], self.controllerData[c.backwardInput], forceLim) #Force limit of 40 so we move slowly
                
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
            self.updateOutputComponentsTEST()

if __name__ == '__main__':
    try:
        #sleep(30) This sleep is now handled in robot_motors_script.sh
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
