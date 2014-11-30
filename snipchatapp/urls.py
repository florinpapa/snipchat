from django.conf.urls import patterns, include, url
from snipchatapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_snippet/$', views.add_snippet, name='add_snippet'),
    url(r'^([a-z0-9]{6})/$', views.view_snippet, name='view_snippet'),
    url(r'^update/([a-z0-9]{6})/$', views.new_version, name='new_version'),
    url(r'^inline_comment_html/$', views.inline_comment_html,
        name='inline_comment_html'),
    url(r'^add_comment/([a-z0-9]{6})/$', views.add_comment,
        name='add_comment'),
    url(r'register/$', views.register, name='register'),
    url(r'log_out/$', views.log_out, name='log_out'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'login/$', views.login, name='login')
)
