from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url('', include('test42.apps.homepage.urls')),

    # Examples:
    # url(r'^$', 'test42.views.home', name='home'),
    # url(r'^test42/', include('test42.foo.urls')),

    url(r'^admin_tools/', include('admin_tools.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax-upload/', include('ajax_upload.urls')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += patterns(
        'django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
