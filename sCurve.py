from time import sleep

def runServo(channel, on, pwm1, start, relativeAngle, upperbound=4095, delayTime=0.08):
    for i in range(-14, 14):
        value = start + (1/(1+2.7**(-i/2 * (1/2)))) * ((relativeAngle/270) * upperbound)
        print("degree: {} to {}, value: {}".format(round((start/upperbound) * 270, 2), round(value/upperbound * 270, 2), round(value, 2)) )
        sleep(delayTime + abs(i**2 / 10000))
        pwm1.set_pwm(channel,on,int(value + 0.5))
#runServo(0,0,pwm,70,180,475,delayTime=0.04)
