from django.db import models

# Create your models here.
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

    