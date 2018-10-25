from django.db import models

class ControllerInput(models.Model):
    l_trigger = models.IntegerField(default = 0)
    r_trigger = models.IntegerField(default = 0)
    l_bump = models.IntegerField(default = 0)
    r_bump = models.IntegerField(default = 0)
    a = models.IntegerField(default = 0)
    b = models.IntegerField(default = 0)
    x = models.IntegerField(default = 0)
    y = models.IntegerField(default = 0)
    r_stick_x = models.IntegerField(default = 0)
    r_stick_y = models.IntegerField(default = 0)
    l_stick_x = models.IntegerField(default = 0)
    l_stick_y = models.IntegerField(default = 0)
    up = models.IntegerField(default = 0)
    down = models.IntegerField(default = 0)
    left = models.IntegerField(default = 0)
    right = models.IntegerField(default = 0)
    start = models.IntegerField(default = 0)
    select = models.IntegerField(default = 0)

    def __str__(self):
        val = "a: {} | b: {} | x: {} | y: {} | start: {} | select: {}\n".format(self.a, self.b, self.x, self.y, self.start, self.select)
        val += "r_trigger: {} | l_trigger: {} | r_bump: {} | l_bump: {}\n".format(self.r_trigger, self.l_trigger, self.r_bump, self.l_bump)
        val += "r_stick_x: {} | r_stick_y: {} | l_stick_x: {} | l_stick_y: {}".format(self.r_stick_x, self.r_stick_y, self.l_stick_x, self.l_stick_y)
        val += "upDPad: {} | downDPad: {} | leftDPad: {} | rightDPad: {}".format(self.up, self.down, self.left, self.right)
        return val

    def createDictionary(self):
        value = {
        'a':self.a, 'b': self.b, 'x': self.x, 'y': self.y, 'start': self.start, 'select': self.select,
        'r_trigger': self.r_trigger, 'l_trigger': self.l_trigger, 'r_bump': self.r_bump, 'l_bump': self.l_bump,
        'r_stick_x': self.r_stick_x, 'r_stick_y': self.r_stick_y, 'l_stick_x': self.l_stick_x, 'l_stick_y': self.l_stick_y,
        'up': self.up, 'down': self.down, 'left': self.left, 'right': self.right,
        }
        return value