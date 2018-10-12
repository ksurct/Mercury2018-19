"""
	File that will hold the networking class to interface with the web server.
"""
import asyncio
import aiohttp

class BasestationNetwork:
	asyncSession = 0
	def __init__(self):
		self.asyncSession = aiohttp.ClientSession()
	
	def __del__(self):
		self.asyncSession.close()

	async def getSensorData(self, url):
		async with self.asyncSession.get(url) as response:
			print(response.text)
			return response.text #this is the data that is returned from the web server

	def postClientData(self, url, controllerData):
		self.asyncSession.put(url, data=controllerData)
		