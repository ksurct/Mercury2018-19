"""
	File that will hold the networking class to interface with the web server.
"""
import asyncio
import aiohttp
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
		pass
	
	def __del__(self):
		pass

	def getSensorData(self):
		r = requests.get(self.url + '/get/')
		#print(r.text)
		return r.text

	def postClientData(self, controllerData):
		try:
			r = requests.post(self.url + '/update/' + json.dumps(controllerData) + '/')
			time.sleep(.1)
		except (ConnectionRefusedError, ConnectionResetError, ConnectionError, requests.exceptions.ConnectionError) as err:
			print("Error sending data to web server. Will retry in 2 seconds: " + time.ctime())
			time.sleep(2)
		