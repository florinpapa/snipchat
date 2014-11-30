from django.conf.urls import patterns, include, url
from snipchatapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_snippet/$', views.add_snippet, name='add_snippet'),
    url(r'^([a-z0-9]{6})/$', views.view_snippet, name='view_snippet'),
    url(r'^update/([a-z0-9]{6})/$', views.new_version, name='new_version'),
)
