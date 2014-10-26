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

	for g in roi:
		oldCollisions = collisions.exclude(geom__intersects=g.geom)
		oldNearmisses = nearmisses.exclude(geom__intersects=g.geom)
		oldHazards = hazards.exclude(geom__intersects=g.geom)
		oldThefts = thefts.exclude(geom__intersects=g.geom)

	context = {
		'user': user,

		'date_today': now,
		'date_lastmonth': monthPast,
	
		"geofences": roi,

		'oldCollisions': oldCollisions.exclude(date__range=[monthPast, now]),
		'oldNearmisses': oldNearmisses.exclude(date__range=[monthPast, now]),
		'oldHazards': oldHazards.exclude(date__range=[monthPast, now]),
		'oldThefts': oldThefts.exclude(date__range=[monthPast, now]),

		'recentCollisions': collisions.exclude(pk__in=oldCollisions),
		'recentNearmisses': nearmisses.exclude(pk__in=oldNearmisses),
		'recentHazards': hazards.exclude(pk__in=oldHazards),
		'recentThefts': thefts.exclude(pk__in=oldThefts),

	}

	return render(request, 'mapApp/stats.html', context)