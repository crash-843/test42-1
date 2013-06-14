from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import Home, Log, Edit
from .signalhandlers import connect

connect()

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'homepage/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        {'login_url': 'home'}, name='logout'),
    url(r'^edit/$', login_required(Edit.as_view()), name='edit'),
    url(r'^log/$', Log.as_view(), name='log'),
)
