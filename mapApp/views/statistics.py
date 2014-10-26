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
from django.utils import timezone


def stats(request):
	user = request.user

	now = timezone.now()
	monthPast = now - timedelta(1*365/12)

	# Get the user's alertable points in the last month
	incidents = Incident.objects.all()#filter(incidentNotification__user=user.id)
	nearmisses = incidents.filter(incident__contains="Near collision")
	collisions = incidents.exclude(incident__contains="Near collision")

	hazards = Hazard.objects.all()
	thefts = Theft.objects.all()

	roi = AlertArea.objects.filter(user=user.id)

	# recent sets = points that intersect an roi as defined by user and are reported in last month
	recentCollisions = Incident.objects.none()
	recentNearmisses = Incident.objects.none()
	recentHazards = Hazard.objects.none()
	recentThefts = Theft.objects.none()
	# Find intersecting points
	for g in roi:
		recentCollisions = recentCollisions | collisions.filter(geom__intersects=g.geom)
		recentNearmisses = recentNearmisses | nearmisses.filter(geom__intersects=g.geom)
		recentHazards = recentHazards | hazards.filter(geom__intersects=g.geom)
		recentThefts = recentThefts | thefts.filter(geom__intersects=g.geom)
	# Filter by date
	recentCollisions = recentCollisions.filter(date__range=[monthPast, now])
	recentNearmisses = recentNearmisses.filter(date__range=[monthPast, now])
	recentHazards = recentHazards.filter(date__range=[monthPast, now])
	recentThefts = recentThefts.filter(date__range=[monthPast, now])

	context = {
		'user': user,

		'date_today': now,
		'date_lastmonth': monthPast,
	
		"geofences": roi,

		'recentCollisions': recentCollisions,
		'recentNearmisses': recentNearmisses,
		'recentHazards': recentHazards,
		'recentThefts': recentThefts,

		'otherCollisions': collisions.exclude(pk__in=recentCollisions),
		'otherNearmisses': nearmisses.exclude(pk__in=recentNearmisses),
		'otherHazards': hazards.exclude(pk__in=recentHazards),
		'otherThefts': thefts.exclude(pk__in=recentThefts),

	}

	return render(request, 'mapApp/stats.html', context)