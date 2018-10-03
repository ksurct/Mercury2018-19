"""
	File that holds main loop for the robot
	The robot will get controller data from the web server, translate that into motor and sensor positions, and then update the positions accordingly.
	The robot will also publish sensor data to the web service for the basestation. 
	We will maybe have two separate Pis for camera and motors/servos etc. The camera Pi should have its own folder and code and such
"""
import asyncio
import logging
import networking

def mainLoop():
	logging.basicConfig(format="%(name)s: %(levelname)s: %(asctime)s: %(message)s", level=logging.INFO)
	logger = logging.getLogger(__name__)
	loop = asyncio.get_event_loop()

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		logger.info("Keyboard interrupt detected. Exiting now.")
	finally:
		#ensure robot loop gets closed

		loop.close()
		logger.info("Event loop closed. Exiting program")