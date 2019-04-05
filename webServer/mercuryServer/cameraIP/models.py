from django.db import models

# Create your models here.
class cameraIP(models.Model):
    cameraIPstr = models.CharField(max_length=50)

    def __str__(self):
        return self.cameraIPstr