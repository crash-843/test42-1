from django.contrib import admin
from .models import Info, LogEntry, ActionEntry


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('created', 'method', 'url', 'status', 'priortiy')


class ActionEntryAdmin(admin.ModelAdmin):
    list_display = ('created', 'model', 'action')

admin.site.register(Info)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(ActionEntry, ActionEntryAdmin)
