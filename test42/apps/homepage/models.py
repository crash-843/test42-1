from django.db import models

class Info(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    email = models.EmailField(null=True, blank=True)
    jabber = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=30,null=True, blank=True)
    contacts = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name ,self.last_name)
