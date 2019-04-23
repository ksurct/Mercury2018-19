#!/bin/bash



#while true ; do
#	if ifconfig wlan0 | grep -q "inet" ; then
#		#echo "Network is fine"
#		sleep 5
#	else
#		#echo "Network needs to restart"
#		sudo ifconfig wlan0 up
#		sleep 10
#	fi
#done

sudo ifconfig wlan0 down
sleep 10
sudo ifconfig wlan0 up
sleep 5