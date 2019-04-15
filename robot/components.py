"""
    File that will hold the source code for hardware that will be controlled by the Pi.
    All of the servos, motors, sensors, LEDs, etc. will be here.
"""
import RPi.GPIO as GPIO
import Adafruit_PCA9685
from time import sleep
from threading import Thread

GPIO.setmode(GPIO.BOARD)

class Component:
    def __init__(self, controllerInput):
        #Make sure that everything has an init method
        raise NotImplementedError()

    def doUpdate(self, value):
        #Make sure everything has a method that can be called by the main method
        raise NotImplementedError()

class SensorComponent(Component):
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel

    def __del__(self):
        #Don't know if we will use anything here
        pass

    def getSensorValues(self):
        #Get sensor values from robot asynchronously and return them in some data type
        pass

    def doUpdate(self, value):
        return self.getSensorValues()

class MotorComponent():
    def __init__(self, name, controllerInput, backwardInput, directionPin, pwmPin):
        GPIO.setmode(GPIO.BOARD)
        self.name = name
        self.controllerInput = controllerInput
        self.backwardInput = backwardInput
        self.directionPin = directionPin
        self.pwmPin = pwmPin
        self.motorPower = 0

        GPIO.setup(self.directionPin, GPIO.OUT)
        GPIO.setup(self.pwmPin, GPIO.OUT)
        GPIO.output(self.directionPin, False)

        self.PWM = GPIO.PWM(self.pwmPin, 1000) #set PWM to 1000 Hz as a max frequency
        self.PWM.start(0)
        self.PWM.ChangeDutyCycle(0)

    def __del__(self):
        #Make sure robot stops moving
        self.updateSpeed(0)

    def updateSpeed(self, value):
        #Update motor speed
        if (value < 0):
            #Motor going in reverse
            GPIO.output(self.directionPin, True)
            pwm = -int(value)
            if (pwm > 100):
                pwm = 100
        elif (value > 0):
            #Motor going forwards
            GPIO.output(self.directionPin, False)
            pwm = int(value)
            if (pwm > 100):
                pwm = 100
        else:
            GPIO.output(self.directionPin, False)
            pwm = 0
        self.motorPower = pwm
        self.PWM.ChangeDutyCycle(pwm)

    def doUpdate(self, value, doBackwards, limiter):
        #This is the method we will call from the main loop when parsing controller data
        value *= (limiter / 8191) #This translates the trigger range of 0 to 8191 into the pwm range of 0 to limiter (max of 100)
        if (doBackwards == 1):
            value *= -1
        if ('left' in self.name):
            self.updateSpeed(-1 * value)
        elif ('right' in self.name):
            self.updateSpeed(value)
        else:
            print("Not updating the motor")

class ServoComponent(Component):
    def __init__(self, name, channel, presetDict, minVal, maxVal):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(40)
        self.name = name
        self.channel = channel
        self.presetDictionary = presetDict
        self.currentPosition = 182
        self.sCurveThread = Thread()
        self.min = minVal
        self.max = maxVal
        self.currentAngle = self.calcAngleFromPosition(self.currentPosition) # Set the initial angle


        self.pwm.set_pwm(self.channel, 0, self.currentPosition)

    def __del__(self):
        #Make servo return to some predefined "home" position
        self.updatePosition(self.presetDictionary['home'])
        pass

    def calcAngleFromPosition(self, position):
        # calculates current angle based on max, min and current location
        return (position - self.min)/(self.max - self.min)*90

    def updatePosition(self, valueArr):
        #Update servo position
        """
            Format for valueArr:
            ['up', 'down', 'left', 'right', 'lStickY']
        """

        # Calculate the current angle
        self.currentAngle = self.calcAngleFromPosition(self.currentPosition)

        #self.pwm.set_pwm_freq(40)
        if (self.name == 'picky-uppy'):
            #TODO Change 120s in sCurve thread once we figure out relative angle stuff with servo
            if (valueArr[0] == 1):
                #Drop ball in launcher, bypass sCurve
                self.pwm.set_pwm(self.channel, 0, self.presetDictionary['deposit'])
                self.currentPosition = self.presetDictionary['deposit']
            elif (valueArr[1] == 1):
                #All the way down
                self.sCurveThread = Thread(target=self.sCurve, args=(0, self.currentPosition, 120))
                self.sCurveThread.start()
                self.currentPosition = self.currentPosition + 120
                # I just wanted something else to commit
            elif (valueArr[2] == 1):
                #All the way down
                self.sCurveThread = Thread(target=self.sCurve, args=(0, self.currentPosition, 120))
                self.sCurveThread.start()
                self.currentPosition = self.currentPosition + 120
            elif (valueArr[3] == 1):
                #All the way down
                self.sCurveThread = Thread(target=self.sCurve, args=(0, self.currentPosition, 120))
                self.sCurveThread.start()
                self.currentPosition = self.currentPosition + 120
            elif (valueArr[4] != 0):
                if (self.currentPosition - valueArr[4] > self.max):
                    self.currentPosition = self.max
                elif (self.currentPosition - valueArr[4] < self.min):
                    self.currentPosition = self.min
                else:
                    self.currentPosition = self.currentPosition - valueArr[4]
                self.pwm.set_pwm(self.channel, 0, self.currentPosition)
            #print(self.currentPosition)
                
        elif (self.name == 'camera'):
            #TODO Figure out how to get relative angle based on currentPosition and the presetDictionary and do the same idea as picky-uppy
            pass

    
    def doUpdate(self, valueArr):
        #Method called from main loop when parsing data
        """
            Format for valueArr:
            ['up', 'down', 'left', 'right', 'lStickY']
        """
        return self.updatePosition(valueArr)

    def sCurve(self, on, start, relativeAngle, upperbound=4095, delayTime=0.08):
        for i in range(-14, 14):
            value = start + (1/(1+2.7**(-i/2 * (1/2)))) * ((relativeAngle/270) * upperbound)
            print("degree: {} to {}, value: {}".format(round((start/upperbound) * 270, 2), round(value/upperbound * 270, 2), round(value, 2)) )
            sleep(delayTime + abs(i**2 / 10000))
            self.pwm.set_pwm(self.channel,on,int(value + 0.5))

class LauncherServoComponent(Component):
    def __init__(self, name, channel, controllerInput):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.name = name
        self.channel = channel
        self.controllerInput = controllerInput
        self.pwm.set_pwm_freq(40)
        self.pwm.set_pwm(self.channel, 0, 210)
        self.on = False
        self.moveThread = Thread()

    def __del__(self):
        self.pwm.set_pwm(self.channel, 0, 210)

    def updatePosition(self, value):
        #self.pwm.set_pwm_freq(333)
        if (value == 0 and self.on == True): #MAKE THIS WHERE IT STOPS MOVING
            self.moveThread = Thread(target=self.turnOffThread)
            #self.moveThread.start()
            self.pwm.set_pwm(self.channel, 0, 210)
            sleep(.1)
            self.on = False
        elif (value == 1): #MAKE THIS WHERE IT IS MOVING
            print("UPDATE LAUNCHER")
            self.moveThread = Thread(target=self.turnOnThread)
            #self.moveThread.start()
            self.pwm.set_pwm(self.channel, 0, 250)
            self.on = True
            sleep(.1)
        return True

    def doUpdate(self, value):
        return self.updatePosition(value)
    
    def turnOnThread(self):
        #self.pwm.set_pwm_freq(333)
        self.pwm.set_pwm(self.channel, 0, 3400)
        
    def turnOffThread(self):
        #self.pwm.set_pwm_freq(333)
        self.pwm.set_pwm(self.channel, 0, 1800)


class LEDComponent(Component):
    def __init__(self, name, controllerInput, channel):
        self.name = name
        self.controllerInput = controllerInput
        self.currentValue = 0
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(40)
        self.channel = channel

    def __del__(self):
        self.pwm.set_pwm(self.channel, 0, 0)

    def updateValue(self, value):
        self.pwm.set_pwm(self.channel, 0, value)

    def doUpdate(self, value):
        if (value == 0):
            self.updateValue(0)
        else:
            self.updateValue(4095)
