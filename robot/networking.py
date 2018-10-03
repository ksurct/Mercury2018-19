"""
    Class that will hold all networking information for the Pi.
    This class will define the GET request for controller data, as well as the UPDATE request for sensor data.
"""
import asyncio
import requests

"""
    This method will be used to GET controller data from the web server
    Once the data is received from the server, it is returned
    Ideally, this will run asynchronously
    loop argument should come from the main loop to keep consistency (I guess)
"""
async def getControllerStatus(loop):
    url = "OurWebServerAddress"
    r = requests.get(url)
    print(r.text)
    return r.text #this is the data that is returned from the web server

"""
    This method will be used to PUT sensor data onto the web server
    Ideally, this method will be run asynchronously
    loop argument should come from the main loop to keep consistency (I guess)
"""
async def updateSensorData(loop, sensorData):
    url = "OurWebServerAddress"
    r = requests.put(url, data = sensorData)