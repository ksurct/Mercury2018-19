#!/bin/bash

# This file automatically reconnects the wifi on the pi if it drops, used for LOS tests
# DO NOT RUN THIS FILE WITHOUT A & AT THE END OF THE FILE BECAUSE THERE IS AN INFINITE LOOP SO THE REST OF THE SYSTEM WON'T START I ALREADY MADE THIS MISTAKE PLEASE DON'T DO IT AGAIN

while true ; do
	if ifconfig wlan0 | grep -q "inet" ; then
		#echo "Network is fine"
		sleep 5
	else
		#echo "Network needs to restart"
		sudo ifconfig wlan0 up
		sleep 10
	fi
done