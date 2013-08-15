from django.conf.urls import patterns, include, url

from aliases import views

urlpatterns = patterns('',
  url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^submit/$', views.SubmitView.as_view(), name='submit'),
  url(r'^rate/(?P<pk>\d+)/$', views.RateView.as_view(), name='rate'),
  url(r'^tagged/(?P<tag_slug>[\w-]+)/$', views.TaggedView.as_view(), name='tagged'),
  url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='show'),
)
