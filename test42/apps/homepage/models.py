from django.db import models

class Info(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name ,self.last_name)
