from django.db import models

# Create your models here.

class SensorData(models.Model):
    qfl = models.DecimalField(default = 0, max_digits=20, decimal_places=15)
    qfr = models.DecimalField(default = 0, max_digits=20, decimal_places=15)
    qbl = models.DecimalField(default = 0, max_digits=20, decimal_places=15)
    qbr = models.DecimalField(default = 0, max_digits=20, decimal_places=15)
    df = models.DecimalField(default = 0, max_digits=20, decimal_places=15)
    db = models.DecimalField(default = 0, max_digits=20, decimal_places=15)
    dl = models.DecimalField(default = 0, max_digits=20, decimal_places=15)
    dr = models.DecimalField(default = 0, max_digits=20, decimal_places=15)

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

