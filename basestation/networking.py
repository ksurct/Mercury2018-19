"""
	File that will hold the networking class to interface with the web server.
"""
import asyncio
import aiohttp
import json
import requests
import time

class BasestationNetwork:
	asyncSession = 0
	def __init__(self, url):
		self.url = 'http://' + url
		pass
	
	def __del__(self):
		pass

	def getSensorData(self):
		r = requests.get(self.url + '/get/')
		#print(r.text)
		return r.text

	def postClientData(self, controllerData):
		r = requests.post(self.url + '/update/' + json.dumps(controllerData) + '/')
		time.sleep(.1)
		