from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^aliases/', include('aliases.urls', namespace="aliases")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comment/', include('django.contrib.comments.urls')),
)