"""
    Class that will hold all networking information for the Pi.
    This class will define the GET request for controller data, as well as the UPDATE request for sensor data.
"""
import asyncio
import aiohttp
import requests
import json

class RobotNetwork:
    asyncSession = 0
    
    def __init__(self, url):
        #self.asyncSession = aiohttp.ClientSession()
        self.url = "https://" + url + "/"

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
        r = requests.get(self.url + 'get/')
        return json.loads(r.text)

    """
        This method will be used to PUT sensor data onto the web server
        Ideally, this method will be run asynchronously
        loop argument should come from the main loop to keep consistency (I guess)
    """
    def updateSensorData(self, sensorData):
        #self.asyncSession.put(url, data=sensorData)
        #UPDATE SENSOR DICTIONARY ONCE WE KNOW WHAT SENSORS WE WANT
        r = requests.post(self.url + 'sensorData/post/', 0)# json.dumps(sensorData))