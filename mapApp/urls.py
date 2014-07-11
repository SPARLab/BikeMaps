from django.conf.urls import patterns, url

from mapApp import views



urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<lat>-?\d{1,3}\.?\d*)_(?P<lng>-?\d{1,3}\.?\d*)/(?P<zoom>\d+)/$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^incident_submit/$', views.postIncident, name='postIncident'),
	url(r'^route_submit/$', views.postRoute, name='postRoute'),
	url(r'^new_alert/$', views.postAlertPolygon, name='postAlertPolygon'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^incidents.json$', views.getIncidents, name='getIncidents'),
	url(r'^readAlert/(?P<alertID>\d+)/$', views.readAlertPoint, name='readAlertPoint')
	
)