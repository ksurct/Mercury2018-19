"""
    This is the file that will hold the main loop for the basestation.
    It will get input from the controller, pass that controller input onto the web server, and get sensor data from the same web server.
    Receiving the camera stream may also come through this, or it may come through a web service somewhere. TBD.
"""

"""
    We might want to set up some GUI for sensor data to change values based on what we get from the robot.
    This might be set up somewhere else and we call it from here and call methods to change values as needed.
"""
import asyncio
from xbox import Controller
import logging
from networking import BasestationNetwork

def mainLoop():
    # Setup Logging
    logging.basicConfig(format='%(name)s: %(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Get the event loop to work with
    loop = asyncio.get_event_loop()
    basestationNetwork = BasestationNetwork()

    try:
        #Make tasks and put them in loop
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Exiting now.")
    finally:
        #ensure robot loop gets closed
        loop.close()
        logger.info("Event loop closed. Exiting program")