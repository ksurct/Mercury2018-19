import threading
import requests
import random
from time import sleep, time
import sampleGUI

class guiHandler:
    def __init__(self):
        self.gui = sampleGUI.SensorGUI()
        self.gui.master.title('#SensorsRKewl')

    def startGUI(self):
        self.gui.mainloop()

    def updateData(self, valueDict):
        self.gui.updateSensorValues(valueDict)

class SampleBS:
    def __init__(self, gHandler):
        self.g = gHandler

    def getData(self):
        r = requests.get('http://worldclockapi.com/api/json/est/now')
        print(r.text)
        valueDict = {
            'db': random.uniform(0, 100),
            'df': random.uniform(0, 100),
            'dl': random.uniform(0, 100),
            'dr': random.uniform(0, 100),
            'qbl': random.uniform(0, 100),
            'qbr': random.uniform(0, 100),
            'qfl': random.uniform(0, 100),
            'qfr': random.uniform(0, 100)
        }
        return valueDict

    def mainLoop(self):
        while True:
            self.g.updateData(self.getData())
            sleep(.5)

if __name__ == '__main__':
    g = guiHandler()
    bs = SampleBS(g)
    t = threading.Thread(target=bs.mainLoop)
    t.start()
