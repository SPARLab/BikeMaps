from django.shortcuts import render
from django.http import HttpResponse

# Import models
from mapApp.models.incident import Incident
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft
from mapApp.models.alert_area import AlertArea

from django.contrib.auth.models import User
from mapApp.models.alert_notification import IncidentNotification, HazardNotification, TheftNotification

from datetime import datetime, timedelta

def stats(request):
	user = request.user

	now = datetime.now()
	monthPast = now - timedelta(1*365/12)

	# Get the user's alertable points in the last month
	recentIncidents = Incident.objects.filter(incidentNotification__user=user.id).filter(date__range=[monthPast, now])
	recentCollisions = recentIncidents.filter(incidentNotification__action=IncidentNotification.INCIDENT)
	recentNearmisses = recentIncidents.filter(incidentNotification__action=IncidentNotification.NEARMISS)

	recentHazards = Hazard.objects.filter(hazardNotification__user=user.id).filter(date__range=[monthPast, now])
	recentThefts = Theft.objects.filter(theftNotification__user=user.id).filter(date__range=[monthPast, now])


	context = {
		'user': user,

		'date_today': now,
		'date_lastmonth': monthPast,
	
		"geofences": AlertArea.objects.filter(user=user.id),

		'recentCollisions': recentCollisions,
		'recentNearmisses': recentNearmisses,
		'recentHazards': recentHazards,
		'recentThefts': recentThefts,

		'collisionsCount': recentCollisions.count(),
		'nearmissesCount': recentNearmisses.count(),
		'hazardsCount': recentHazards.count(),
		'theftsCount': recentThefts.count(),
	}

	return render(request, 'mapApp/stats.html', context)