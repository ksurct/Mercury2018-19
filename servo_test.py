import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

servo = GPIO.PWM(18,500)
servo.start(0)
try:
    while True:
        for dc in range(20,100,1):
            servo.ChangeDutyCycle(dc)
            time.sleep(0.1)
            print (dc)
        for dc in range(100,20,-1):
            servo.ChangeDutyCycle(dc)
            time.sleep(0.1)
            print (dc)
except KeyboardInterrupt:
    pass
servo.stop()
GPIO.cleanup();