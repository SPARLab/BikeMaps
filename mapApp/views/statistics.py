from django.shortcuts import render
from django.http import HttpResponse

# Import models
from mapApp.models.incident import Incident
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft
from mapApp.models.alert_area import AlertArea

from django.contrib.auth.models import User
from mapApp.models.alert_notification import IncidentNotification, HazardNotification, TheftNotification

import datetime

def stats(request):
	user = request.user

	now = datetime.date.today()
	monthPast = now - datetime.timedelta(1*365/12)

	# Get the user's alertable points in the last month
	recentIncidents = IncidentNotification.objects.filter(user=user.id).filter(date__range=[monthPast, now])
	recentCollisions = recentIncidents.filter(action=IncidentNotification.INCIDENT)
	recentNearmisses = recentIncidents.filter(action=IncidentNotification.NEARMISS)

	recentHazards = HazardNotification.objects.filter(user=user.id).filter(date__range=[monthPast, now])
	recentThefts = TheftNotification.objects.filter(user=user.id).filter(date__range=[monthPast, now])

	context = {
		'user': user,

		'date_today': now,
		'date_lastmonth': monthPast,
	
		# 'recentIncidents': Incident.objects.filter(date__range=[monthPast, now]),
		# 'recentHazards': Hazard.objects.filter(date__range=[monthPast, now]),
		# 'recentThefts': Theft.objects.filter(date__range=[monthPast, now]),

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