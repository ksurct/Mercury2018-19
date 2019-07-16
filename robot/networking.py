"""
    Class that will hold all networking information for the Pi.
    This class will define the GET request for controller data, as well as the UPDATE request for sensor data.
    Same as the basestation networking controller, we use the requests library here.
        The requests class is blocking, meaning that the Pi doesn't do anything while the request call is waiting for data from the server.
        This can hurt the performance of the robot, especially if the web server is a long distance from the robot or is bogged down (which should never happen).
        Ideal control loop for the robot with asynchronous networking:
            Make async call to server to get controller data
            While waiting on the controller call to return, get the readings of the sensors (possibly asynchronously)
            When we get the updated controller data, send the sensor information to the server asynchronously
            While waiting on the response from the server, update the motor and servo positions according to the controller data we got from the first step
            When we get a response from the server about the sensor data, go back to the top of the loop
        This would let us process the data to/from the server while we are waiting on the response from the server for data we just sent/received instead of waiting on a response and then doing something with the data
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
        'lim': 50, 'hl': 1
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
        #except (ConnectionRefusedError, ConnectionResetError, requests.exceptions.ConnectionError):
        except (requests.exceptions.ConnectionError):
            #Above should be the list of all errors we encounter, but we can update the list if needed by just adding new errors to the list
            return (self.defaultControllerValues, False)

    def getControllerAndSensorStatus(self):
        try:
            r = requests.get(self.url + '/ControllerAndSensor/')
            return (json.loads(r.text), True)
        #except (ConnectionRefusedError, ConnectionResetError, requests.exceptions.ConnectionError):
        except (requests.exceptions.ConnectionError):
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
        #except (ConnectionRefusedError, ConnectionResetError, requests.exceptions.ConnectionError):
        except (requests.exceptions.ConnectionError):
            return