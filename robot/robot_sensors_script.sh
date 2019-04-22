#!/bin/bash

# This file will run the robot_sensors.py script continuously
# It waits 20 seconds before running the script
# It will wait 20 seconds before running the script again if there is an error

while true ; do
    sleep 20
    python /home/pi/Desktop/Mercury2018-19/robot/robot_sensors.py
done