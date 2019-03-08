import time
def runServo(channel, on, pwm, start, relativeAngle, upperbound=4095, delayTime=0.08):
    for i in range(-5, 10):
        value = start + (1/(1+2.7**(-i))) * ((relativeAngle/360) * upperbound)
        print("degree: {} to {}".format(round((start/upperbound) * 360, 4), round(value/upperbound * 360, 4)) )
        time.sleep(delayTime)
        pwm.set_pwm(channel,on,value)
#runServo(0, 0, "Pwm object", 1024, 24, 4095)
