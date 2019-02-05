"""
	File that holds main loop for the robot
	The robot will get controller data from the web server, translate that into motor and sensor positions, and then update the positions accordingly.
	The robot will also publish sensor data to the web service for the basestation. 
	We will maybe have two separate Pis for camera and motors/servos etc. The camera Pi should have its own folder and code and such
"""
import asyncio
import logging
from time import sleep
from networking import RobotNetwork
from components import *
from settings import * # this gets us constants such as WEB_SERVER_ADDRESS

class Robot:
    def __init__(self):
        self.network = RobotNetwork(WEB_SERVER_ADDRESS + ":" + WEB_SERVER_PORT)
        self.controllerData = ''
        logging.basicConfig(format="%(name)s: %(levelname)s: %(asctime)s: %(message)s", level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.loop = asyncio.get_event_loop()

        # To create a new output component (motor, servo, led), add a constructor here in the appropriate list, 
        # and create cooresponding fields in settings.py (ie, MOTOR_ONE_NAME). 
        # We like to keep these constants defined in settings.py in order to follow the Open / Close principle of software design.
        # Read more at: https://codeburst.io/understanding-solid-principles-open-closed-principle-e2b588b6491f  
        self.outputComponentList = [
            # motors

            # TODO Uncomment this when these fields are programmed in Settings.py
            # MotorComponent(MOTOR_ONE_NAME, MOTOR_ONE_CONTROLLER_INPUT, MOTOR_ONE_DIRECTION_PIN, MOTOR_ONE_PWM_PIN),
            # MotorComponent(MOTOR_TWO_NAME, MOTOR_TWO_CONTROLLER_INPUT, MOTOR_TWO_DIRECTION_PIN, MOTOR_TWO_PWM_PIN),
            # MotorComponent(MOTOR_THREE_NAME, MOTOR_THREE_CONTROLLER_INPUT, MOTOR_THREE_DIRECTION_PIN, MOTOR_THREE_PWM_PIN),
            # MotorComponent(MOTOR_FOUR_NAME, MOTOR_FOUR_CONTROLLER_INPUT, MOTOR_FOUR_DIRECTION_PIN, MOTOR_FOUR_PWM_PIN),

            # servos

            # TODO uncomment htis when these fields are programmed in settings.py
            # ServoComponent(SERVO_ONE_NAME, SERVO_ONE_CONTROLLER_INPUT, SERVO_ONE_CHANNEL, SERVO_ONE_HOME, SERVO_ONE_MIN, SERVO_ONE_MAX)

            # leds

            # TODO uncomment htis when these fields are programmed in settings.py
            #LEDComponent(LED_ONE_NAME, LED_ONE_CONTROLLER_INPUT)
        ]
        self.sensorList = []

		

    def mainLoop(self):
        try:
            while True:
                #Get controller data and update motors, servos, LEDs
                self.controllerDataTuple = self.network.getControllerStatus()
                self.controllerData = self.controllerDataTuple[0]
                if(self.controllerDataTuple[1] == False):
                    self.logger.info("Unable to get controller data. Trying again soon.") #Shows error message and current time
                    sleep(1)
                    continue #This goes back to the top of the while loop and forces us to get new controller values
                            #We can do this because sending sensor data isn't as important as getting updated controller data.
                            #Plus the network is down, so it wouldn't make sense to try and send data again.
                
                #print(self.controllerData) #Just used this to make sure everything worked, can uncomment if needed, but don't use during competition
                #for c in self.outputComponentList:
                    #c.doUpdate(self.controllerData[c.controllerInput])

                #Get sensor data and push to the web server
                for s in self.sensorList:
                    s.doUpdate()
                ############################
                # UNCOMMENT THE LINE BELOW ONCE WE KNOW WHAT SENSORS WE NEED AND SUCH
                #self.network.updateSensorData(self.sensorList)
                ############################
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt detected. Exiting now.")
        finally:
            #ensure robot loop gets closed
            self.loop.close()
            self.logger.info("Event loop closed. Exiting program")

if __name__ == '__main__':
    r = Robot()
    r.mainLoop()
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
