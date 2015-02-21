from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.shortcuts import get_object_or_404

from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages

# Decorators
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from mapApp.models import Incident, Hazard, Theft, AlertArea, IncidentNotification, HazardNotification, TheftNotification
from mapApp.forms import GeofenceForm

@require_POST
@login_required
def postAlertPolygon(request):
	geofenceForm = GeofenceForm(request.POST)
	geofenceForm.data = geofenceForm.data.copy()

	# Create valid attributes for user and geom fields
	try:
		geofenceForm.data['user'] = request.user.id
		geofenceForm.data['geom'] = GEOSGeometry(geofenceForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>Invalid geometry data.')
		return HttpResponseRedirect(reverse('mapApp:index'))

	if geofenceForm.is_valid():
		# Save new model object, send success message to the user
		geofenceForm.save()
		messages.success(request, 'You will now receive alerts for the area traced.')

	return HttpResponseRedirect(reverse('mapApp:index'))

def alertUsers(request, incident):
	intersectingPolys = AlertArea.objects.filter(geom__intersects=incident.geom) #list of AlertArea objects
	usersToAlert = list(set([poly.user for poly in intersectingPolys])) # get list of distinct users to alert

	if (incident.p_type == "collision"): Notification = IncidentNotification; action = Notification.INCIDENT
	elif (incident.p_type == "nearmiss"): Notification = IncidentNotification; action = Notification.NEARMISS
	elif (incident.p_type == "hazard"): Notification = HazardNotification; action = Notification.HAZARD
	elif (incident.p_type == "theft"): Notification = TheftNotification; action = Notification.THEFT

	for user in usersToAlert:
		Notification(user=user, point=incident, action=action).save()

@login_required
def readAlertPoint(request, type, alertID):
	if type == 'collision' or type == 'nearmiss' or type == 'fall':
		alert = get_object_or_404(IncidentNotification.objects.filter(user=request.user), pk=alertID)
	if type == 'hazard':
		alert = get_object_or_404(HazardNotification.objects.filter(user=request.user), pk=alertID)
	if type == 'theft':
		alert = get_object_or_404(TheftNotification.objects.filter(user=request.user), pk=alertID)

	if (alert):
		alert.is_read=True
		alert.save()
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(alert.point.latlngList()[0]), 	\
				"lng":str(alert.point.latlngList()[1]), 	\
				"zoom":str(18)								\
			})												\
		))

	else:
		return HttpResponseRedirect(reverse('mapApp:index'))
