from django.db import models

# Create your models here.

class SensorData(models.Model):
    #qfl = models.IntegerField(default = 0)
    #qfr = models.IntegerField(default = 0)
    #qbl = models.IntegerField(default = 0)
    #qbr = models.IntegerField(default = 0)
    dfl = models.IntegerField(default = 0)
    dfr = models.IntegerField(default = 0)
    dsl = models.IntegerField(default = 0)
    dsr = models.IntegerField(default = 0)
    #da = models.IntegerField(default = 0)

    def __str__(self):
        #val = "qfl: {} | qfr: {} | qbl: {} | qbr: {}\n".format(self.qfl, self.qfr, self.qbl, self.qbr)
        val = "dfl: {} | dfr: {} | dsl: {} | dsr: {}\n".format(self.dfl, self.dfr, self.dsl, self.dsr)
        return val

    def createDictionary(self):
        val = {
            #'qfl': self.qfl, 'qfr': self.qfr, 'qbl': self.qbl, 'qbr': self.qbr,
            'dfl': self.dfl, 'dfr': self.dfr, 'dsl': self.dsl, 'dsr': self.dsr#, 'da': self.da
        }
        return val

