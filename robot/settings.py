#Settings file for different components on the robot

##############
# IMPORTANT NOTE:
# ALL pin settings are in board mode, which is the Pin# column (outer-most) on the Pi Header print-out
##############

###################################
#   Networking Settings
###################################
#WEB_SERVER_ADDRESS = "129.130.10.251" #Game Jam hookup
WEB_SERVER_ADDRESS = "10.135.79.80" #IP for Reece's apartment: "70.179.163.182"
WEB_SERVER_PORT = "8000"

###################################
#   Sensor Settings
###################################


###################################
#   Motor Settings
###################################

# Complete these fields when these motors are connected

#Motor 1 on Front Motors Board
MOTOR_FR_NAME = "front-right"
MOTOR_FR_CONTROLLER_INPUT = 'rt'
MOTOR_FR_BACKWARD_INPUT = 'rb'
MOTOR_FR_DIRECTION_PIN = 31
MOTOR_FR_PWM_PIN = 11

#Motor 2 on Front Motors Board
MOTOR_FL_NAME = "front-left"
MOTOR_FL_CONTROLLER_INPUT = 'lt'
MOTOR_FL_BACKWARD_INPUT = 'lb'
MOTOR_FL_DIRECTION_PIN = 32
MOTOR_FL_PWM_PIN = 13

#Motor 2 on Back Motors Board
MOTOR_BR_NAME = "back-right"
MOTOR_BR_CONTROLLER_INPUT = 'rt'
MOTOR_BR_BACKWARD_INPUT = 'rb'
MOTOR_BR_DIRECTION_PIN = 33
MOTOR_BR_PWM_PIN = 15

#Motor 1 on Back Motors Board
MOTOR_BL_NAME = "back-left"
MOTOR_BL_CONTROLLER_INPUT = 'lt'
MOTOR_BL_BACKWARD_INPUT = 'lb'
MOTOR_BL_DIRECTION_PIN = 36
MOTOR_BL_PWM_PIN = 16

###################################
#   Servo Settings
###################################

# Complete these fields when servos are connected.
SERVO_ONE_NAME = ""
SERVO_ONE_CONTROLLER_INPUT = ''
SERVO_ONE_CHANNEL = 0
SERVO_ONE_HOME = 0
SERVO_ONE_MIN = 0
SERVO_ONE_MAX = 255

SERVO_L_NAME = "Launcher"
SERVO_L_CONTROLLER_INPUT = 'st'
SERVO_L_CHANNEL = 0

###################################
#   LED Settings
###################################

# Complete these fields when LEDs are connected.
LED_ONE_NAME = ""
LED_ONE_CONTROLLER_INPUT = ''
