from django.conf.urls import patterns, include, url

from aliases import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='show'),
  url(r'^(?P<alias_id>\d+)/comment/$', views.comment, name='comment')
)
