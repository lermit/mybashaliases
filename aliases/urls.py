from django.conf.urls import patterns, include, url

from aliases import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^submit/$', views.submit, name='submit'),
  url(r'^rate/(?P<pk>\d+)/$', views.rate, name='rate'),
  url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='show'),
)
