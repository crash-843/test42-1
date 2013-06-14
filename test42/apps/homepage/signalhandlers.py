from django.db.models.signals import post_save, post_delete
from .models import ActionEntry


def ced_callback(sender, **kwargs):
    if sender != ActionEntry:
        created = kwargs.get('created')
        signal = kwargs.get('signal')
        action = {
            post_save: ActionEntry.CREATE if created else ActionEntry.EDIT,
            post_delete: ActionEntry.DELETE
        }.get(signal)
        ActionEntry.objects.create(model=sender.__name__, action=action)


def connect():
    post_save.connect(ced_callback)
    post_delete.connect(ced_callback)
