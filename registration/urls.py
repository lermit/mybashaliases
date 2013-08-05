from django.conf.urls import patterns, url

from registration import views

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^profile/$', views.my_profile, name='my_profile'),
)
