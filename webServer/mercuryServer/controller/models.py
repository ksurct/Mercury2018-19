from django.db import models

class ControllerInput(models.Model):
    a = models.IntegerField(default = 0)
    b = models.IntegerField(default = 0)
    x = models.IntegerField(default = 0)
    y = models.IntegerField(default = 0)
    st = models.IntegerField(default = 0)
    se = models.IntegerField(default = 0)
    rt = models.IntegerField(default = 0)
    lt = models.IntegerField(default = 0)
    rb = models.IntegerField(default = 0)
    lb = models.IntegerField(default = 0)
    rsx = models.IntegerField(default = 0)
    rsy = models.IntegerField(default = 0)
    lsx = models.IntegerField(default = 0)
    lsy = models.IntegerField(default = 0)
    u = models.IntegerField(default = 0)
    d = models.IntegerField(default = 0)
    l = models.IntegerField(default = 0)
    r = models.IntegerField(default = 0)
    

    def __str__(self):
        val = "a: {} | b: {} | x: {} | y: {} | st: {} | se: {}\n".format(self.a, self.b, self.x, self.y, self.st, self.se)
        val += "rt: {} | lt: {} | rb: {} | lb: {}\n".format(self.rt, self.lt, self.rb, self.lb)
        val += "rsx: {} | rsy: {} | lsx: {} | lsy: {}".format(self.rsx, self.rsy, self.lsx, self.lsy)
        val += "u: {} | d: {} | l: {} | r: {}".format(self.u, self.d, self.l, self.r)
        return val

    def createDictionary(self):
        value = {
        'a':self.a, 'b': self.b, 'x': self.x, 'y': self.y, 'start': self.st, 'select': self.se,
        'r_trigger': self.rt, 'l_trigger': self.lt, 'r_bump': self.rb, 'l_bump': self.lb,
        'r_stick_x': self.rsx, 'r_stick_y': self.rsy, 'l_stick_x': self.lsx, 'l_stick_y': self.lsy,
        'up': self.u, 'down': self.d, 'left': self.l, 'right': self.r,
        }
        return value