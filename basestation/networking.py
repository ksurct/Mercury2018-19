"""
	File that will hold the networking class to interface with the web server.
"""
import asyncio
import aiohttp
import json
import requests

class BasestationNetwork:
	asyncSession = 0
	def __init__(self):
		pass
	
	def __del__(self):
		pass

	def getSensorData(self, url):
		r = requests.get('http://' + url + '/')
		print(r.text)
		return r.text

	def postClientData(self, url, controllerData):
		r = requests.post('http://' + url + json.dumps(controllerData) + '/')
		