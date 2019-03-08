import RPi.GPIO as GPIO
import Adafruit_PCA9685
from time import sleep
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Use these settings for launcher
# Power supply set to 7.4V and 2A
# Remember to press the blue output button on the power supply

#These make it go backwards
input('Press enter to start the launcher')
pwm.set_pwm_freq(333)
pwm.set_pwm(0, 0, 3400)
#input('press to end')

#Stop test
input('Press enter to stop')
pwm.set_pwm_freq(333)
pwm.set_pwm(0, 0, 1800)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#pwm.set_pwm_freq(500)


"""val = 0
while val != -3:
    pwm.set_pwm(0, val, 0)
    val = int(input("Put in value: "))
pwm.set_all_pwm(0, 0)    """
#GPIO.cleanup()

#pwm.set_pwm(0, 4000, 0)

#pwm.set_pwm(0, 0, 2450) for f = 4000
#didnt move, maybe this is stop?
#input('continue')
#pwm.set_pwm(0, 0, 0)


#brute force to make it go

#pwm.set_pwm_freq(1000) # this made it go with
#pwm.set_pwm(0, 0, 2000)

'''
# forwards
print('forwards')
pwm.set_pwm_freq(500) # this also made it go
pwm.set_pwm(0, 0, 1000)
input('Press this once started')

#Stop test
input('stop')
pwm.set_pwm_freq(333)
pwm.set_pwm(0, 0, 1800)

#input('continue')

#These make it go backwards
input('backwards')
pwm.set_pwm_freq(333)
pwm.set_pwm(0, 0, 3400)


#input('continue')

#Stop test
input('stop')
pwm.set_pwm_freq(333)
pwm.set_pwm(0, 0, 1800)
'''
'''
print('Running Experiemnt')
pwm.set_pwm_freq(333)

lower_bound = 1725
upper_bound = 1961

pwm_range = upper_bound - lower_bound
pwm_var = lower_bound

n_iterations = 61

for x in range(1,n_iterations):
    pwm.set_pwm(0,0,pwm_var)
    print('pwm is: ' + str(pwm_var))
    pwm_var += int(pwm_range/n_iterations)
    sleep(1)
'''


pwm.set_pwm(0, 0, 0)
