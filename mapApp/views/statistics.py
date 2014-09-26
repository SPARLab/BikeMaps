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
	recentNotificationIncidents = IncidentNotification.objects.filter(user=user).filter(date__range=[monthPast, now])
	recentNotificationHazards = HazardNotification.objects.filter(user=user).filter(date__range=[monthPast, now])
	recentNotificationThefts = TheftNotification.objects.filter(user=user).filter(date__range=[monthPast, now])

	context = {
		'user': user,

		'date_today': now,
		'date_lastmonth': monthPast,
	
		'recentIncidents': Incident.objects.filter(date__range=[monthPast, now]),
		'recentHazards': Hazard.objects.filter(date__range=[monthPast, now]),
		'recentThefts': Theft.objects.filter(date__range=[monthPast, now]),

		'recentNotificationIncidents': recentNotificationIncidents,
		'recentNotificationHazards': recentNotificationHazards,
		'recentNotificationThefts': recentNotificationThefts,

		'recentIncidentsNotificationCount': recentNotificationIncidents.count(),
		'recentHazardsNotificationCount': recentNotificationHazards.count(),
		'recentTheftsNotificationCount': recentNotificationThefts.count(),
	}

	return render(request, 'mapApp/stats.html', context)