import datetime
from django.conf.urls import *
from django.http import HttpResponse
from django.template import Context, loader

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^chapter10/contacts/', include('chapter10.contacts.urls')),
    (r'^chapter10/properties/', include('chapter10.properties.urls')),
    (r'^chapter11/contacts/', include('chapter10.contacts.api_urls')),
    (r'^chapter11/properties/', include('chapter10.properties.api_urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
