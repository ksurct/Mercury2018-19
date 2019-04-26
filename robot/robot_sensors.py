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
from components import SensorComponent
import RPi.GPIO as GPIO
from settings import * # this gets us constants such as WEB_SERVER_ADDRESS
import Queue_for_lpf as QueueLPF

class Robot_Sensors:
    def __init__(self):
        self.network = RobotNetwork(WEB_SERVER_ADDRESS + ":" + WEB_SERVER_PORT)
        self.controllerData = ''
        logging.basicConfig(format="%(name)s: %(levelname)s: %(asctime)s: %(message)s", level=logging.INFO)
        self.logger = logging.getLogger(__name__)



        # To create a new output component (motor, servo, led), add a constructor here in the appropriate list, 
        # and create cooresponding fields in settings.py (ie, MOTOR_ONE_NAME). 
        # We like to keep these constants defined in settings.py in order to follow the Open / Close principle of software design.
        # Read more at: https://codeburst.io/understanding-solid-principles-open-closed-principle-e2b588b6491f
        
        # Create our list of sensors. The first input argument is the channel on 
        # the multiplexer.
        """
        tof0 = VL53L0X.VL53L0X(TCA9548A_Num=TOF0_CHANNEL_NUM, TCA9548A_Addr=TCA9548A_I2C_ADDR) #TCA9548A_I2C_ADDR = 0x70
        tof1 = VL53L0X.VL53L0X(TCA9548A_Num=TOF1_CHANNEL_NUM, TCA9548A_Addr=TCA9548A_I2C_ADDR)
        tof2 = VL53L0X.VL53L0X(TCA9548A_Num=TOF2_CHANNEL_NUM, TCA9548A_Addr=TCA9548A_I2C_ADDR)
        tof3 = VL53L0X.VL53L0X(TCA9548A_Num=TOF3_CHANNEL_NUM, TCA9548A_Addr=TCA9548A_I2C_ADDR)

        # TODO does this need to be a dictionary to
        #  work with the for loop
        self.sensorList = {
            'dfr' : tof1,
            'dfl' : tof2,
            'dsl' : tof3,
            'dsr' : tof0
        }
        
        # This was the ranging mode that we tested with.
        # Maybe we can optimize this further, if we want.
        tof0.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        tof2.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        tof3.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        
        # Create our Queues for filtering
        lpf0 = QueueLPF.Queue(SENSOR_FILTERING_QUEUE_LEN)
        lpf1 = QueueLPF.Queue(SENSOR_FILTERING_QUEUE_LEN)
        lpf2 = QueueLPF.Queue(SENSOR_FILTERING_QUEUE_LEN)
        lpf3 = QueueLPF.Queue(SENSOR_FILTERING_QUEUE_LEN)

        self.lfp_list = {
            'dfr' : lpf1,
            'dfl' : lpf2,
            'dsl' : lpf3,
            'dsr' : lpf0
        }
        """
        self.sensorList = [
            SensorComponent(name="dfr", mult_addr=TCA9548A_I2C_ADDR, sens_channel=1),
            SensorComponent(name="dfl", mult_addr=TCA9548A_I2C_ADDR, sens_channel=2),
            SensorComponent(name="dsl", mult_addr=TCA9548A_I2C_ADDR, sens_channel=3),
            SensorComponent(name="dsr", mult_addr=TCA9548A_I2C_ADDR, sens_channel=0),
        ]
        
        self.sensorValues = {
            'dfr': 0, 
            'dfl': 0, 
            'dsl': 0, 
            'dsr': 0,
        }
        
        # Setup timing for sensors
        self.timing = 0
        for s in self.sensorList:
            temp = s.sensorObject.get_timing()
            if (temp > self.timing):
                self.timing = temp
        if (self.timing < 20000):
            self.timing = 20000
        
    def __del__(self):
        for s in self.sensorList:
            s.sensorObject.stop_ranging()

    def mainLoop(self):
        try:
            while True:
                #Get sensor data and push it to the website
                self.updateSensorValues()
                self.network.updateSensorData(self.sensorValues)
                #print(self.sensorValues)
                sleep(self.timing/1000000.00)

        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt detected. Exiting now.")
        finally:
            #ensure robot loop gets closed
            self.logger.info("Event loop closed. Exiting program")
            GPIO.cleanup()

    def updateSensorValues(self):
        for s in self.sensorList:
            #self.sensorValues[s] = s.doUpdate(self.sensorList[s]) #Definitely test this line when we get sensors
            # Alternatively, don't use sensor components
            #self.sensorValues[s] = self.sensorList[s].get_distance()
            
            # Get the distance from the cooresponding sensor
            distance = s.doUpdate()
            if (distance == 0):
                continue
            
            """
            # If full, create room the the next input
            if self.lfp_list[s].isFull():
                self.lfp_list[s].DeQueue()

            # Add the distance to the queue
            self.lfp_list[s].EnQueue(distance)
            
            # Set the sensor value equal to the average
            self.sensorValues[s] = self.lfp_list[s].get_avg_val()
            """
            self.sensorValues[s.name] = distance


    def updateSensorValuesTEST(self):
        for s in self.sensorValues:
            self.sensorValues[s] = randint(0, 1000)

    def sensorUpdateThreadMethod(self):
        while True:
            self.updateSensorValuesTEST()
            self.network.updateSensorData(self.sensorValues)

if __name__ == '__main__':
    try:
        r = Robot_Sensors()
        r.mainLoop()
    except Exception as e:
        print("ERROR {}".format(e))
        #GPIO.cleanup()

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
