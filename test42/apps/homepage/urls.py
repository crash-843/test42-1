from django.conf.urls import patterns, url
from .views import Home, Log, Edit

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^edit/$', Edit.as_view(), name='edit'),
    url(r'^log/$', Log.as_view(), name='log'),
)
