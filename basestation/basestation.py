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
        'a':0, 'b': 0, 'x': 0, 'y': 0, 'st': 0, 'se': 0,
        'rt': 0, 'lt': 0, 'rb': 0, 'lb': 0,
        'rsx': 0, 'rsy': 0, 'lsx': 0, 'lsy': 0,
        'u': 0, 'd': 0, 'l': 0, 'r': 0,
        }
        self.defaultControllerValues = {
        'a':0, 'b': 0, 'x': 0, 'y': 0, 'st': 0, 'se': 0,
        'rt': 12, 'lt': 0, 'rb': 0, 'lb': 0,
        'rsx': 0, 'rsy': 0, 'lsx': 0, 'lsy': 0,
        'u': 0, 'd': 0, 'l': 0, 'r': 0,
        }
        self.basestationNetwork = BasestationNetwork('70.179.163.182:8000') #address for Dummy at Reece's apartment - subject to change closer to comp
        #self.basestationNetwork = BasestationNetwork('0490f3a8.ngrok.io')

    def mainLoop(self):
        # Setup Logging
        logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Get the event loop to work with
        loop = asyncio.get_event_loop()
        #self.basestationNetwork.postClientData(self.defaultControllerValues)
        
        try:
            #Make tasks and put them in loop
            #self.postDataTest()
            print("Inside try")
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
            self.basestationNetwork.postClientData(self.controllerData)

    def getDataTest(self):
        data = self.basestationNetwork.getSensorData()
        print(data)

    def getControllerData(self):
        self.controller.update()
        self.controllerData['a'] = 1 if self.controller.a() else 0
        self.controllerData['b'] = 1 if self.controller.b() else 0
        self.controllerData['x'] = 1 if self.controller.x() else 0
        self.controllerData['y'] = 1 if self.controller.y() else 0
        self.controllerData['st'] = 1 if self.controller.select_button() else 0 #this is switched in xbox file
        self.controllerData['se'] = 1 if self.controller.start_button() else 0
        self.controllerData['rt'] = int(self.controller.right_trigger() >> 3)
        self.controllerData['lt'] = int(self.controller.left_trigger() >> 3) 
        self.controllerData['rb'] = 1 if self.controller.right_bumper() else 0
        self.controllerData['lb'] = 1 if self.controller.left_bumper() else 0
        r_stick_x = round(self.controller.right_x(), 1)
        r_stick_y = round(self.controller.right_y(), 1)
        l_stick_x = round(self.controller.left_x(), 1)
        l_stick_y = round(self.controller.left_y(), 1)
        self.controllerData['rsx'] = int(10*r_stick_x) if abs(r_stick_x) > 0.1 else 0
        self.controllerData['rsy'] = int(-10*r_stick_y) if abs(r_stick_y) > 0.1 else 0
        self.controllerData['lsx'] = int(10*l_stick_x) if abs(l_stick_x) > 0.1 else 0
        self.controllerData['lsy'] = int(-10*l_stick_y) if abs(l_stick_y) > 0.1 else 0
        self.controllerData['u'] = 1 if str(self.controller.hat).strip() == 'u' else 0
        self.controllerData['d'] = 1 if str(self.controller.hat).strip() == 'd' else 0
        self.controllerData['l'] = 1 if str(self.controller.hat).strip() == 'l' else 0
        self.controllerData['r'] = 1 if str(self.controller.hat).strip() == 'r' else 0

        #print(self.controllerData)
        
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    b = Basestation()
    b.mainLoop()
        
