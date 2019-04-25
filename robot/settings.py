#Settings file for different components on the robot

##############
# IMPORTANT NOTE:
# ALL pin settings are in board mode, which is the Pin# column (outer-most) on the Pi Header print-out
##############

###################################
#   Networking Settings
###################################
#WEB_SERVER_ADDRESS = "129.130.10.251" #Game Jam hookup
WEB_SERVER_ADDRESS = "10.135.79.80"
#WEB_SERVER_ADDRESS = "70.179.163.182" #IP for Reece's apartment
WEB_SERVER_PORT = "8000"

###################################
#   Sensor Settings
###################################

# TODO update these arguments with actual physical channels when we setup the hardware
TOF0_CHANNEL_NUM = 0
TOF1_CHANNEL_NUM = 1
TOF2_CHANNEL_NUM = 2
TOF3_CHANNEL_NUM = 3
TCA9548A_I2C_ADDR = 0x70

SENSOR_FILTERING_QUEUE_LEN = 2

###################################
#   Motor Settings
###################################

# Complete these fields when these motors are connected

#Motor 1 on Front Motors Board
MOTOR_FR_NAME = "front-right"
MOTOR_FR_CONTROLLER_INPUT = 'rt'
MOTOR_FR_BACKWARD_INPUT = 'rb'
MOTOR_FR_DIRECTION_PIN = 33
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
MOTOR_BR_DIRECTION_PIN = 31
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
SERVO_PU_NAME = 'picky-uppy'
SERVO_PU_CHANNEL = 1
SERVO_PU_PRESET_DICT = {'deposit': 155, 'down': 360, 'contain': 325, 'home': 182}
SERVO_PU_MIN = 154
SERVO_PU_MAX = 360

SERVO_CAM_NAME = 'camera'
SERVO_CAM_CHANNEL = 2
SERVO_CAM_PRESET_DICT = {}
SERVO_CAM_MIN = 2
SERVO_CAM_MAX = 255

SERVO_L_NAME = "Launcher"
SERVO_L_CONTROLLER_INPUT = 'st'
SERVO_L_CHANNEL = 0

###################################
#   LED Settings
###################################

# Complete these fields when LEDs are connected.
LED_ONE_NAME = "LEDs"
LED_ONE_CONTROLLER_INPUT = 'y'
LED_ONE_CHANNEL = 3

###################################
# State transition code
###################################
DANGER_COUNT_THRESHOLD = 30 # This hasn't been tested, we can probably optimize here