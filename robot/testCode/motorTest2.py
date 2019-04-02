import RPi.GPIO as GPIO
from time import sleep

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
        print(self.name)
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
            GPIO.output(self.directionPin, False)
            pwm = -int(value)
            if (pwm > 100):
                pwm = 100
        elif (value > 0):
            #Motor going forwards
            GPIO.output(self.directionPin, True)
            pwm = int(value)
            if (pwm > 100):
                pwm = 100
        else:
            GPIO.output(self.directionPin, False)
            pwm = 0
        self.motorPower = pwm
        self.PWM.ChangeDutyCycle(pwm)
        print("Motor {} is now at {}".format(self.name, pwm))

    def doUpdate(self, value, doBackwards):
        #This is the method we will call from the main loop when parsing controller data
        value *= (100/8191) #This translates the trigger range of 0 to 8191 into the pwm range of 0 to 100
        if (doBackwards == 1):
            value *= -1
        if ('left' in self.name):
            self.updateSpeed(-1 * value)
        elif ('right' in self.name):
            self.updateSpeed(value)
        else:
            print("Not updating the motor")
        
if __name__ == '__main__':
    motor = MotorComponent('motor', 'test', 'test', 33, 11)
    print("Direction pin is LOW")
    GPIO.output(motor.directionPin, False)
    for i in range(25, 80, 5):
        print(i)
        motor.PWM.ChangeDutyCycle(i)
        sleep(1)
    motor.PWM.ChangeDutyCycle(50)
    sleep(.5)
    motor.PWM.ChangeDutyCycle(25)
    sleep(.5)
    motor.PWM.ChangeDutyCycle(0)
    sleep(.5)
    
    print("Direction pin is HIGH")
    GPIO.output(motor.directionPin, True)
    for i in range(25, 80, 5):
        print(i)
        motor.PWM.ChangeDutyCycle(i)
        sleep(1)
    motor.PWM.ChangeDutyCycle(50)
    sleep(.5)
    motor.PWM.ChangeDutyCycle(25)
    sleep(.5)
    motor.PWM.ChangeDutyCycle(0)
    sleep(.5)