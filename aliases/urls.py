from django.conf.urls import patterns, include, url

from aliases import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^submit/$', views.submit, name='submit'),
  url(r'^(?P<pk>\d+)/rank/add/$', views.index, name='rank_add'),
  url(r'^(?P<pk>\d+)/rank/sub/$', views.index, name='rank_sub'),
  url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='show'),
)
