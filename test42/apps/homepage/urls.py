from django.conf.urls import patterns, include, url
from .views import Home, Log

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^log/$', Log.as_view(), name='log'),
)
