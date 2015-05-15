from django.conf.urls import patterns, url
from mapApp import views

urlpatterns = patterns('',
	# Index page
	url(r'^$', views.index, name='index'),
	url(r'^(?P<lat>-?\d{1,3}\.?\d*)_(?P<lng>-?\d{1,3}\.?\d*)/(?P<zoom>\d+)/?$', views.index, name='index'),

	# About page
	url(r'^about/$', views.about, name='about'),

	# Called from user notifications list
	url(r'^read_alert/(?P<type>\w+)/(?P<alertID>\d+)/$', views.readAlertPoint, name='readAlertPoint'),

	# Called upon geometry object creation on map
	url(r'^incident_submit/$', views.postIncident, name='postIncident'),
	url(r'^hazard_submit/$', views.postHazard, name='postHazard'),
	url(r'^theft_submit/$', views.postTheft, name='postTheft'),
	url(r'^poly_submit/$', views.postAlertPolygon, name='postAlertPolygon'),

	# Called from email form
	url(r'^contact/$', views.contact, name='contact'),

	# Called by admin data export button
	url(r'^points.json$', views.getPoints, name='getPoints'),
	url(r'^incidents.json$', views.getIncidents, name='getIncidents'),
	url(r'^hazards.json$', views.getHazards, name='getHazards'),
	url(r'^thefts.json$', views.getThefts, name='getThefts'),

	# Called when user edits or deletes an alert area
	url(r'edit/$', views.editShape, name='editShape'),

	# Terms and conditions page
	url(r'terms_and_conditions/$', views.termsAndConditions, name='termsAndConditions'),


	url(r'stats/$', views.stats, name='stats'),
	url(r'recent/$', views.recentReports, name='recent'),

	url(r'vis/$', views.vis, name='vis'),
	url(r'alerts/$', views.recentReports, name='alerts'),
)
