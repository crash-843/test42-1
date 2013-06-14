from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Info(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(null=True, blank=True)
    photo = ThumbnailerImageField(upload_to="photos", null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    jabber = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    contacts = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class LogEntry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    priortiy = models.IntegerField(default=0)
    method = models.CharField(max_length=30)
    url = models.CharField(max_length=255)
    status = models.IntegerField()

    class Meta:
        ordering = ["-priortiy", "-created"]
        get_latest_by = "created"

    def __unicode__(self):
        return "{0} {1} {2}".format(self.method,
                                    self.url,
                                    self.status)


class ActionEntry(models.Model):
    CREATE = 0
    EDIT = 1
    DELETE = 2

    ACTION_CHOICES = (
        (CREATE, 'Created'),
        (EDIT, 'Edited'),
        (DELETE, 'Deleted'),
    )

    created = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=30)
    action = models.IntegerField(choices=ACTION_CHOICES)

    class Meta:
        ordering = ["-created"]
        get_latest_by = "created"

    def __unicode__(self):
        return "{0} {1}".format(self.model, self.get_action_display())
