"""
	File that will hold the networking class to interface with the web server.
	We use the requests library to do all of the web calls that we need.
		Pro of requests:
			Super easy to use
		Con of requests:
			Blocking class, meaning that the program will sit and do nothing while we wait on a response from the server. 
				This isn't that big of a problem on the basestation, but it is a bigger issue on the robot.
"""
import json
import requests
import time
import logging

class BasestationNetwork:
	asyncSession = 0
	def __init__(self, url):
		self.url = 'http://' + url
		logging.getLogger("requests").setLevel(logging.WARNING)
		logging.getLogger("urllib3").setLevel(logging.WARNING)
		self.defaultSensorValues = {
			'qfr': 0, 'qfl': 0, 'qbr': 0, 'qbl': 0,
			'df': 0, 'db': 0, 'dl': 0, 'dr': 0
		}
		pass
	
	def __del__(self):
		pass

	def getSensorData(self):
		try:
			r = requests.get(self.url + '/sensors/get/')
			return json.loads(r.text)
		except (ConnectionRefusedError, ConnectionResetError, ConnectionError, requests.exceptions.ConnectionError) as err:
			print("Error getting data from web server. Will retry in 2 seconds: " + time.ctime())
			time.sleep(2)
			return self.defaultSensorValues

	def postClientData(self, controllerData):
		try:
			r = requests.post(self.url + '/controller/update/' + json.dumps(controllerData) + '/')
			return json.loads(r.text)
			time.sleep(.1)
		except (ConnectionRefusedError, ConnectionResetError, ConnectionError, requests.exceptions.ConnectionError) as err:
			print("Error sending data to web server. Will retry in 2 seconds: " + time.ctime())
			time.sleep(2)
		