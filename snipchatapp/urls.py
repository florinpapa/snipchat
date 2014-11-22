from django.conf.urls import patterns, include, url
from snipchatapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'add_snippet/', views.add_snippet, name='add_snippet'),
)
