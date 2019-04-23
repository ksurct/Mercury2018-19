#!/bin/bash

# This file will run the robot_motors.py script continuously
# It waits 20 seconds before running the script
# It will wait 20 seconds before running the script again if there is an error

while true ; do
    sleep 20
    python3 /home/pi/Desktop/mercury18-19Code/Mercury2018-19/robot/robot_motors.py
done