from django.db import models

# Create your models here.

class SensorData(models.Model):
    qfl = models.IntegerField(default = 0)
    qfr = models.IntegerField(default = 0)
    qbl = models.IntegerField(default = 0)
    qbr = models.IntegerField(default = 0)
    df = models.IntegerField(default = 0)
    db = models.IntegerField(default = 0)
    dl = models.IntegerField(default = 0)
    dr = models.IntegerField(default = 0)

    def __str__(self):
        val = "qfl: {} | qfr: {} | qbl: {} | qbr: {}\n".format(self.qfl, self.qfr, self.qbl, self.qbr)
        val += "df: {} | db: {} | dl: {} | dr: {}\n".format(self.df, self.db, self.dl, self.dr)
        return val

    def createDictionary(self):
        val = {
            'qfl': self.qfl, 'qfr': self.qfr, 'qbl': self.qbl, 'qbr': self.qbr,
            'df': self.df, 'db': self.db, 'dl': self.dl, 'dr': self.dr
        }
        return val

