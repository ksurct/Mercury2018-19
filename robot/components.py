"""
    File that will hold the source code for hardware that will be controlled by the Pi.
    All of the servos, motors, sensors, LEDs, etc. will be here.
"""

class Component:
    def __init__(self):
        #Make sure that everything has an init method
        raise NotImplementedError()

    def doUpdate(self, value):
        #Make sure everything has a method that can be called by the main method
        raise NotImplementedError()

class SensorComponent(Component):
    def __init__(self, name, controllerInput, channel):
        self.name = name
        self.controllerInput = controllerInput
        self.channel = channel

    def __del__(self):
        #Don't know if we will use anything here
        pass

    async def getSensorValues(self):
        #Get sensor values from robot asynchronously and return them in some data type
        pass

class MotorComponent(Component):
    def __init__(self, name, controllerInput):
        self.name = name
        self.controllerInput = controllerInput

    def __del__(self):
        #Make sure robot stops moving
        self.updateSpeed(0)
        pass

    async def updateSpeed(self, value):
        #Update motor speed
        pass

    def doUpdate(self, value):
        #This is the method we will call from the main loop when parsing controller data
        pass

class ServoComponent(Component):
    def __init__(self, name, controllerInput, homePosition):
        self.name = name
        self.controllerInput = controllerInput
        self.homePosition = homePosition

    def __del__(self):
        #Make servo return to some predefined "home" position
        pass

    async def updatePosition(self, value):
        #Update servo position
        pass
    
    def doUpdate(self, value):
        #Method called from main loop when parsing data
        pass

class LEDComponent(Component):
    def __init__(self, name, controllerInput):
        self.name = name
        self.controllerInput = controllerInput
        self.currentValue = 0

    def __del__(self):
        #Make sure lights are turned off
        pass

    def updateValue(self, value):
        #Update LED value based on value and self.currentValue
        pass

    def doUpdate(self, value):
        #Method that is called from the main loop when parsing controller data
        pass