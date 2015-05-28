from django.conf.urls import patterns, url, include
from userApp import views

urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', }, name='logout'), #Override next page to go to home
    url(r'^profile/$', views.profile, name='profile'),
    url('^', include('django.contrib.auth.urls')),
)
