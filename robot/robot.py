"""
	File that holds main loop for the robot
	The robot will get controller data from the web server, translate that into motor and sensor positions, and then update the positions accordingly.
	The robot will also publish sensor data to the web service for the basestation. 
	We will maybe have two separate Pis for camera and motors/servos etc. The camera Pi should have its own folder and code and such
"""
import asyncio
import logging
from time import time
from networking import RobotNetwork
from components import *

class Robot:
	def __init__(self):
		self.network = RobotNetwork('10.135.79.80:8000')
		self.controllerData = ''
		logging.basicConfig(format="%(name)s: %(levelname)s: %(asctime)s: %(message)s", level=logging.INFO)
		self.logger = logging.getLogger(__name__)
		self.loop = asyncio.get_event_loop()
		self.outputComponentList = []
		self.sensorList = []
		

	def mainLoop(self):
		try:
			#loop.run_forever()
			while True:
				start_time = time()
				#Get controller data and update motors, servos, LEDs
				self.controllerData = self.network.getControllerStatus()
				#print(self.controllerData)
				for c in self.outputComponentList:
					c.doUpdate(self.controllerData[c.controllerInput])

				#Get sensor data and push to the web server
				for s in self.sensorList:
					s.doUpdate()
				############################
				# UNCOMMENT THE LINE BELOW ONCE WE KNOW WHAT SENSORS WE NEED AND SUCH
				#self.network.updateSensorData(self.sensorList)
				############################
				final_time = time() - start_time
				self.logger.info('Loop time is {0:.6f}'.format(final_time))
		except KeyboardInterrupt:
			self.logger.info("Keyboard interrupt detected. Exiting now.")
		finally:
			#ensure robot loop gets closed
			self.loop.close()
			self.logger.info("Event loop closed. Exiting program")

if __name__ == '__main__':
	r = Robot()
	r.mainLoop()
