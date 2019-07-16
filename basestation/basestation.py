"""
    This is the file that will hold the main loop for the basestation.
    It will get input from the controller, pass that controller input onto the web server, and get sensor data from the same web server.
"""

from xbox import Controller
import logging
from networking import BasestationNetwork
import time
import requests
from sensorGUI import SensorGUI
from threading import Thread, Lock

"""
    We use this lock class to make sure that only one thread is accessing the data at once.
    This prevents dirty reads, which is where one thread is reading data as another thread is writing to it, meaning the first thread is reading old data.
"""
class SensorDataLock:
    def __init__(self):
        self.lock = Lock()
        self.values = {
			'dfl': 0, 'dfr': 0, 'dsl': 0, 'dsr': 0 
		}

    def requestData(self):
        self.lock.acquire() #gives the lock to the thread once it is available
        tempValues = -1
        try:
            tempValues = self.values
        finally:
            self.lock.release() #returns the lock to any thread
            return tempValues

    def updateData(self, newValues):
        self.lock.acquire()
        try:
            self.values = newValues
        finally:
            self.lock.release()

"""
    Same idea as the lock above, only this is for the controller data as opposed to sensor data
"""
class ControlDataLock():
    def __init__(self):
        self.lock = Lock()
        self.data = {
        'a':0, 'b': 0, 'x': 0, 'y': 0, 'st': 0, 'se': 0,
        'rt': 0, 'lt': 0, 'rb': 0, 'lb': 0,
        'rsx': 0, 'rsy': 0, 'lsx': 0, 'lsy': 0,
        'u': 0, 'd': 0, 'l': 0, 'r': 0,
        'hl': 0, 'lim': 50
        }

    def requestControlData(self):
        self.lock.acquire()
        temp = self.data
        self.lock.release()
        return temp

    def updateController(self, data): #Data should be the values from the controller
        self.lock.acquire()
        for c in data:
            self.data[c] = data[c]
        self.lock.release()

    def updateGUIParams(self, data): #Data should only be hl and lim
        self.lock.acquire()
        for g in data:
            self.data[g] = data[g]
        self.lock.release()

"""
    Main driving class behind the basestation and GUI
"""
class Basestation:
    def __init__(self, sensorLock=None, controlDataLock=None):
        print("Calibration in progress... DO NOT TOUCH CONTROLLER!!!!!!!!!!!")
        time.sleep(1) #TODO Change this back to 3 once testing is done
        Controller.init()
        self.tempControlData = {
        'a':0, 'b': 0, 'x': 0, 'y': 0, 'st': 0, 'se': 0,
        'rt': 0, 'lt': 0, 'rb': 0, 'lb': 0,
        'rsx': 0, 'rsy': 0, 'lsx': 0, 'lsy': 0,
        'u': 0, 'd': 0, 'l': 0, 'r': 0
        #'hl': 0, 'lim': 50
        }
        self.controller = Controller(0)
        self.controllerData = controlDataLock
        self.sensorLock = sensorLock
        #self.basestationNetwork = BasestationNetwork('70.179.163.182:8000') #address for Dummy at Reece's apartment - subject to change closer to comp
        self.basestationNetwork = BasestationNetwork('localhost:8000') #address for server running on this computer

    """
        Main loop for the basestation class. This is where we get controller data and send it to the server. 
        The postDataTest method will get data from the controller, update the lock object, then send that data to the web server.
        When sending controller data to the web server, the response is the latest sensor information on the server. See server comments as to why this is.
    """
    def mainLoop(self):
        # Setup Logging
        logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        try:
            #Make tasks and put them in loop
            #print("Inside try")
            while True:
                self.postDataTest() #Gets controller data and pushes to web server
                time.sleep(.1)
                #tempSensData = self.getDataTest() #Get sensor data from web server
                #self.sensorLock.updateData(tempSensData) #Update shared sensor dictionary
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected. Exiting now.")

        finally:
            logger.info("Finished with basestation mainLoop")

    def postDataTest(self):
        self.getControllerData()
        self.controllerData.updateController(self.tempControlData)
        sensorDict = self.basestationNetwork.postClientData(self.controllerData.requestControlData())
        self.sensorLock.updateData(sensorDict)

    def getDataTest(self): #This method isn't used anymore - everything goes through the poorly-named postDataTest method
        data = self.basestationNetwork.getSensorData()
        return data

    def getControllerData(self):
        self.controller.update()
        self.tempControlData['a'] = 1 if self.controller.a() else 0
        self.tempControlData['b'] = 1 if self.controller.b() else 0
        self.tempControlData['x'] = 1 if self.controller.x() else 0
        self.tempControlData['y'] = 1 if self.controller.y() else 0
        self.tempControlData['st'] = 1 if self.controller.select_button() else 0 #this is switched in xbox file
        self.tempControlData['se'] = 1 if self.controller.start_button() else 0
        self.tempControlData['rt'] = int(self.controller.right_trigger() >> 3) + 4096 #adding 4096 starts the trigger at 0
        self.tempControlData['lt'] = int(self.controller.left_trigger() >> 3) + 4096 #adding 4096 starts the trigger at 0
        self.tempControlData['rb'] = 1 if self.controller.right_bumper() else 0
        self.tempControlData['lb'] = 1 if self.controller.left_bumper() else 0
        r_stick_x = round(self.controller.right_x(), 1)
        r_stick_y = round(self.controller.right_y(), 1)
        l_stick_x = round(self.controller.left_x(), 1)
        l_stick_y = round(self.controller.left_y(), 1)
        self.tempControlData['rsx'] = int(10*r_stick_x) if abs(r_stick_x) > 0.1 else 0
        self.tempControlData['rsy'] = int(-10*r_stick_y) if abs(r_stick_y) > 0.1 else 0
        self.tempControlData['lsx'] = int(10*l_stick_x) if abs(l_stick_x) > 0.1 else 0
        self.tempControlData['lsy'] = int(-10*l_stick_y) if abs(l_stick_y) > 0.1 else 0
        self.tempControlData['u'] = 1 if str(self.controller.hat).strip() == 'u' else 0
        self.tempControlData['d'] = 1 if str(self.controller.hat).strip() == 'd' else 0
        self.tempControlData['l'] = 1 if str(self.controller.hat).strip() == 'l' else 0
        self.tempControlData['r'] = 1 if str(self.controller.hat).strip() == 'r' else 0

        #print(self.controllerData)

"""
    This is the code that is run when the script is called from the command line.
    It created instances of all objects needed to run the basestation and starts a thread to run the basestation class.
    The reason we start a thread of the basestation class instead of the GUI class is that the GUI must run on the thread that the script was started from.
        This is a limitation of the Tkinter framework, nothing we can do about it.
    This program runs until the GUI is closed.
"""
if __name__ == '__main__':
    sdl = SensorDataLock()
    cdl = ControlDataLock()
    g = SensorGUI(sensorLock=sdl, controlDataLock=cdl)
    b = Basestation(sensorLock=sdl, controlDataLock=cdl)
    t = Thread(name="Basestation Thread", target=b.mainLoop, daemon=True)
    t.start()
    g.after(100, g.getSensorValues)
    g.mainloop()
    print("GUI is finished running, should exit")
        
