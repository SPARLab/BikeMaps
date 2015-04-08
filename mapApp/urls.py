from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
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
	url(r'^new_alert/$', views.postAlertPolygon, name='postAlertPolygon'),

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

        # Called by app to retrieve points wihtin a given bounding box
        url(r'^points_api.json$', views.getPointsApi, name='getPoints'),
        url(r'^collisions_api.json$', views.getCollisionsApi, name='getCollisions'),
        url(r'^nearmiss_api.json$', views.getNearmissApi, name='getNearmiss'),
        url(r'^incidents_api.json$', views.getIncidentsApi, name='getIncidents'),
        url(r'^hazards_api.json$', views.getHazardsApi, name='getHazards'),
        url(r'^thefts_api.json$', views.getTheftsApi, name='getThefts'),
        url(r'^official_api.json$', views.getOfficialApi, name='getOfficial'),
)

urlpatterns += format_suffix_patterns([
    url(r'^collisions/$', views.CollisionList.as_view(), name='hazard-list'),
    url(r'^nearmiss/$', views.NearmissList.as_view(), name='near-miss-list'),
    url(r'^hazards/$', views.HazardList.as_view(), name='hazard-list'),
    url(r'^thefts/$', views.TheftList.as_view(), name='theft-list'),
    url(r'^official/$', views.OfficialList.as_view(), name='hazard-list'),
    url(r'^alertareas/$', views.AlertAreaList.as_view(), name='alertarea-list'),
    url(r'^alertareas/(?P<pk>[0-9]+)/$', views.AlertAreaDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^gcmdevices/$', views.GCMDeviceList.as_view(), name='gcmdevice-list')
])
