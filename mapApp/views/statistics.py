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
	incidents = Incident.objects.all()#filter(incidentNotification__user=user.id)
	nearmisses = incidents.filter(incident__contains="Near collision")
	collisions = incidents.exclude(incident__contains="Near collision")

	hazards = Hazard.objects.all()
	thefts = Theft.objects.all()

	roi = AlertArea.objects.filter(user=user.id)


	context = {
		'user': user,

		'date_today': now,
		'date_lastmonth': monthPast,
	
		"geofences": roi,

		'oldCollisions': collisions.exclude(date__range=[monthPast, now]),
		'oldNearmisses': nearmisses.exclude(date__range=[monthPast, now]),
		'oldHazards': hazards.exclude(date__range=[monthPast, now]),
		'oldThefts': thefts.exclude(date__range=[monthPast, now]),

		'recentCollisions': collisions.filter(date__range=[monthPast, now]),
		'recentNearmisses': nearmisses.filter(date__range=[monthPast, now]),
		'recentHazards': hazards.filter(date__range=[monthPast, now]),
		'recentThefts': thefts.filter(date__range=[monthPast, now]),
	}

	return render(request, 'mapApp/stats.html', context)