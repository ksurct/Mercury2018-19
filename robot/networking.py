"""
    Class that will hold all networking information for the Pi.
    This class will define the GET request for controller data, as well as the UPDATE request for sensor data.
"""
import requests
import json
import time

class RobotNetwork:
    asyncSession = 0

    defaultControllerValues = {
        'a':0, 'b': 0, 'x': 0, 'y': 0, 'st': 0, 'se': 0,
        'rt': 0, 'lt': 0, 'rb': 0, 'lb': 0,
        'rsx': 0, 'rsy': 0, 'lsx': 0, 'lsy': 0,
        'u': 0, 'd': 0, 'l': 0, 'r': 0,
    }
    
    def __init__(self, url):
        #self.asyncSession = aiohttp.ClientSession()
        self.url = "http://" + url

    def __del__(self):
        #self.asyncSession.close()
        pass
    """
        This method will be used to GET controller data from the web server
        Once the data is received from the server, it is returned
        Ideally, this will run asynchronously
        loop argument should come from the main loop to keep consistency (I guess)
    """
    def getControllerStatus(self):
        """async with self.asyncSession.get(url) as response:
            print(response.text)
            return response.text #this is the data that is returned from the web server"""
        try:
            r = requests.get(self.url + '/controller/get/')
            return (json.loads(r.text), True)
        except (ConnectionRefusedError, ConnectionResetError, requests.exceptions.ConnectionError):
            #Above should be the list of all errors we encounter, but we can update the list if needed by just adding new errors to the list
            return (self.defaultControllerValues, False)

    def getControllerAndSensorStatus(self):
        try:
            r = requests.get(self.url + '/ControllerAndSensor/')
            return (json.loads(r.text), True)
        except (ConnectionRefusedError, ConnectionResetError, requests.exceptions.ConnectionError):
            return ([self.defaultControllerValues, {}], False)

    """
        This method will be used to PUT sensor data onto the web server
        Ideally, this method will be run asynchronously
        loop argument should come from the main loop to keep consistency (I guess)
    """
    def updateSensorData(self, sensorData):
        #self.asyncSession.put(url, data=sensorData)
        #UPDATE SENSOR DICTIONARY ONCE WE KNOW WHAT SENSORS WE WANT
        try:
            r = requests.post(self.url + '/sensors/update/' + json.dumps(sensorData) + '/')
        except (ConnectionRefusedError, ConnectionResetError, requests.exceptions.ConnectionError):
            pass