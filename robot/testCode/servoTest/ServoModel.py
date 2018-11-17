
class servo_model:
    def __init__(self, positionDeg, maxDeg, minDeg, maxVel, maxAcc):
        self.position = positionDeg
        self.max = maxDeg
        self.min = minDeg
        self.maxVel = maxVel
        self.maxAcc = maxAcc

    def display_servo(self):
        print("Position: {0}", self.position)
        return self.position