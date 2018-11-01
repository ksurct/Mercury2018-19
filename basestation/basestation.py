"""
    This is the file that will hold the main loop for the basestation.
    It will get input from the controller, pass that controller input onto the web server, and get sensor data from the same web server.
    Receiving the camera stream may also come through this, or it may come through a web service somewhere. TBD.
"""

"""
    We might want to set up some GUI for sensor data to change values based on what we get from the robot.
    This might be set up somewhere else and we call it from here and call methods to change values as needed.
"""
import asyncio
from xbox import Controller
import logging
from networking import BasestationNetwork
import time

class Basestation:
    def __init__(self):
        print("Calibration in progress... DO NOT TOUCH CONTROLLER!!!!!!!!!!!")
        time.sleep(3)
        Controller.init()
        self.controller = Controller(0)
        self.controllerData = {
        'a':0, 'b': 0, 'x': 0, 'y': 0, 'start': 0, 'select': 0,
        'r_trigger': 0, 'l_trigger': 0, 'r_bump': 0, 'l_bump': 0,
        'r_stick_x': 0, 'r_stick_y': 0, 'l_stick_x': 0, 'l_stick_y': 0,
        'up': 0, 'down': 0, 'left': 0, 'right': 0,
        }
        self.defaultControllerValues = {
        'a':0, 'b': 0, 'x': 0, 'y': 3, 'start': 0, 'select': 0,
        'r_trigger': 12, 'l_trigger': 0, 'r_bump': 1, 'l_bump': 0,
        'r_stick_x': 0, 'r_stick_y': -5, 'l_stick_x': 0, 'l_stick_y': 0,
        'up': 0, 'down': 0, 'left': 0, 'right': 0,
        }
        self.basestationNetwork = BasestationNetwork()

    def mainLoop(self):
        # Setup Logging
        logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Get the event loop to work with
        loop = asyncio.get_event_loop()
        self.basestationNetwork.postClientData('localhost:8000/update/', self.defaultControllerValues)
        
        try:
            #Make tasks and put them in loop
            #self.postDataTest()
            while True:
                #self.getControllerData()
                #print(self.controllerData)
                self.postDataTest()
            #loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected. Exiting now.")
        finally:
            #ensure robot loop gets closed
            loop.close()
            logger.info("Event loop closed. Exiting program")

    #@asyncio.coroutine
    def postDataTest(self):
        for i in range(0, 50):
            self.getControllerData()
            print(self.controllerData)
            print(self.controllerData['a'])
            self.basestationNetwork.postClientData('10.131.79.184:8000/update/', self.controllerData)

    def getControllerData(self):
        self.controller.update()
        self.controllerData['a'] = 1 if self.controller.a() else 0
        self.controllerData['b'] = 1 if self.controller.b() else 0
        self.controllerData['x'] = 1 if self.controller.x() else 0
        self.controllerData['y'] = 1 if self.controller.y() else 0
        self.controllerData['start'] = 1 if self.controller.select_button() else 0 #this is switched in xbox file
        self.controllerData['select'] = 1 if self.controller.start_button() else 0
        self.controllerData['r_trigger'] = int(self.controller.right_trigger() >> 3)
        self.controllerData['l_trigger'] = int(self.controller.left_trigger() >> 3) 
        self.controllerData['r_bump'] = 1 if self.controller.right_bumper() else 0
        self.controllerData['l_bump'] = 1 if self.controller.left_bumper() else 0
        r_stick_x = round(self.controller.right_x(), 1)
        r_stick_y = round(self.controller.right_y(), 1)
        l_stick_x = round(self.controller.left_x(), 1)
        l_stick_y = round(self.controller.left_y(), 1)
        self.controllerData['r_stick_x'] = int(10*r_stick_x) if abs(r_stick_x) > 0.1 else 0
        self.controllerData['r_stick_y'] = int(-10*r_stick_y) if abs(r_stick_y) > 0.1 else 0
        self.controllerData['l_stick_x'] = int(10*l_stick_x) if abs(l_stick_x) > 0.1 else 0
        self.controllerData['l_stick_y'] = int(-10*l_stick_y) if abs(l_stick_y) > 0.1 else 0
        self.controllerData['up'] = 1 if str(self.controller.hat).strip() == 'u' else 0
        self.controllerData['down'] = 1 if str(self.controller.hat).strip() == 'd' else 0
        self.controllerData['left'] = 1 if str(self.controller.hat).strip() == 'l' else 0
        self.controllerData['right'] = 1 if str(self.controller.hat).strip() == 'r' else 0

        #print(self.controllerData)
        
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    b = Basestation()
    b.mainLoop()
        
