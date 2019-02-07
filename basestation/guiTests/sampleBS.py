from sampleGUI import SensorGUI
import threading
import requests
import random
from time import sleep, time

class SampleBS:
    def __init__(self):
        self.gHandler = bsGUIHandler()

    def updateGUI(self, dict):
        self.gHandler.update(dict)

    def getData(self):
        r = requests.get('http://worldclockapi.com/api/json/est/now')
        print(r.text)
        valueDict = {
            'db': random.randint(0, 100),
            'df': random.randint(0, 100),
            'dl': random.randint(0, 100),
            'dr': random.randint(0, 100),
            'qbl': random.randint(0, 100),
            'qbr': random.randint(0, 100),
            'qfl': random.randint(0, 100),
            'qfr': random.randint(0, 100)
        }
        self.updateGUI(valueDict)

    def mainLoop(self):
        while True:
            self.getData()
            sleep(.5)

class bsGUIHandler:
    def __init__(self):
        self.sensorGUI = SensorGUI()
        self.sensorGUI.master.title("Test from basestation")
        self.thread = threading.Thread(target=self.startLoop)
        self.thread.start()

    def startLoop(self):
        self.sensorGUI.mainloop()

    def update(self, dict):
        self.sensorGUI.updateSensorValues(dict)

if __name__ == '__main__':
    bs = SampleBS()
    bs.mainLoop()
