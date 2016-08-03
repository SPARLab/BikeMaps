from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from mapApp import views

urlpatterns = [
	# Index page
	url(r'^$', views.index, name='index'),
	url(r'^@(?P<lat>-?\d{1,3}\.\d*),(?P<lng>-?\d{1,3}\.\d*),(?P<zoom>\d+)z/?$', views.index, name='index'),

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

	# Called when user edits or deletes an alert area
	url(r'^edit/$', views.editShape, name='editShape'),

	# Urls for editing hazard visibility on map
	url(r'^edit_hazards/$', views.editHazards, name='editHazards'),
	url(r'^update_hazard/$', views.updateHazard, name='updateHazard'),

	# Terms and conditions page
	url(r'^terms_and_conditions/$', views.termsAndConditions, name='termsAndConditions'),

        # Disclaimer page
        url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),

	url(r'^recent/$', views.recentReports, name='recent'),

	url(r'^vis/$', views.vis, name='vis'),
	url(r'^vis/@(?P<lat>-?\d{1,3}\.\d*),(?P<lng>-?\d{1,3}\.\d*),(?P<zoom>\d+)z/?$', views.vis, name='vis'),

	url(r'^alerts/$', views.recentReports, name='alerts'),

        url(r'^bikemaps.org.html', views.cert, name='cert'),
]

urlpatterns += format_suffix_patterns([
    url(r'^incidents/?$', views.IncidentList.as_view(), name='incident-list'),
    url(r'^collisions/?$', views.CollisionList.as_view(), name='collision-list'),
    url(r'^nearmiss/?$', views.NearmissList.as_view(), name='nearmiss-list'),
    url(r'^hazards/?$', views.HazardList.as_view(), name='hazard-list'),
    url(r'^thefts/?$', views.TheftList.as_view(), name='theft-list'),
    url(r'^official/$', views.OfficialList.as_view(), name='official-list'),
    url(r'^alertareas/$', views.AlertAreaList.as_view(), name='alertarea-list'),
    url(r'^alertareas/(?P<pk>[0-9]+)/$', views.AlertAreaDetail.as_view()),
    # url(r'^users/$', views.UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^gcmdevices/$', views.GCMDeviceList.as_view(), name='gcmdevice-list'),
    url(r'^gcmdevices/(?P<registration_id>.+)/$', views.GCMDeviceDetail.as_view(), name='gcmdevice-detail'),
    url(r'^apnsdevices/$', views.APNSDeviceList.as_view(), name='apnsdevice-list'),
    url(r'^apnsdevices/(?P<registration_id>.+)/$', views.APNSDeviceDetail.as_view(), name='apnsdevice-detail'),
], allowed=['json'])
