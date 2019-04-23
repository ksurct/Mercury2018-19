def updateSpeed(self):
	KP = .2
	KD = .01
	KI = .005
	TARGET = 5
	
	right_speed = 1
	left_speed = 1
	
	prev_error = 0
	sum_error = 0
	
	error = TARGET - self.sensorData['dsr']
	sum_error += error
	adjust = (error * KP) + (prev_error + KD) + (sum_error + KI)
	
	prev_error = error
	
	if (adjust < 0)
		right_speed = 1
		left_speed += adjust
	else 
		left_speed = 1
		right_speed -= adjust