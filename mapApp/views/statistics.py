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
	now = datetime.date.today()
	monthPast = now - datetime.timedelta(1*365/12)

	# Get points reported within last month
	recentIncidents = Incident.objects.filter(date__range=[monthPast, now])
	recentHazards = Hazard.objects.filter(date__range=[monthPast, now])
	recentThefts = Theft.objects.filter(date__range=[monthPast, now])

	

	context = {
		'date_now': now,
		'date_monthago': monthPast,
		'recentIncidents': recentIncidents,
		'recentHazards': recentHazards,
		'recentThefts': recentThefts

		# 'user': user, 
		# 'incidentCount': incidentPoints.count(), 
		# 'nearmissCount': nearmissPoints.count(), 
		# 'hazardCount': hazardPoints.count(), 
		# 'theftCount': theftPoints.count() 
	}

	return render(request, 'mapApp/stats.html', context)