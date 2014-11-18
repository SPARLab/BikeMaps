from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Import models
from mapApp.models.incident import Incident
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft
from mapApp.models.alert_area import AlertArea

from django.contrib.auth.models import User
from mapApp.models.alert_notification import IncidentNotification, HazardNotification, TheftNotification

@login_required
def stats(request):
	user = request.user

	# Get the user's alertable points in the last month
	incidents = Incident.objects.all()#filter(incidentNotification__user=user.id)
	nearmisses = incidents.filter(incident__contains="Near collision")
	collisions = incidents.exclude(incident__contains="Near collision")

	hazards = Hazard.objects.all()
	thefts = Theft.objects.all()

	rois = AlertArea.objects.filter(user=user.id)

	# recent sets = points that intersect an rois as defined by user and are reported in last month
	collisionsInPoly = Incident.objects.none()
	nearmissesInPoly = Incident.objects.none()
	hazardsInPoly = Hazard.objects.none()
	theftsInPoly = Theft.objects.none()
	# Find intersecting points
	for g in rois:
		collisionsInPoly = collisionsInPoly | collisions.filter(geom__intersects=g.geom)
		nearmissesInPoly = nearmissesInPoly | nearmisses.filter(geom__intersects=g.geom)
		hazardsInPoly = hazardsInPoly | hazards.filter(geom__intersects=g.geom)
		theftsInPoly = theftsInPoly | thefts.filter(geom__intersects=g.geom)

	context = {
		'user': user,

		'geofences': rois,

		'collisions': collisions,
		'nearmisses': nearmisses,
		'hazards': hazards,
		'thefts': thefts,

		'collisionsInPoly': collisionsInPoly,
		'nearmissesInPoly': nearmissesInPoly,
		'hazardsInPoly': hazardsInPoly,
		'theftsInPoly': theftsInPoly,

		# 'collisionsOutPoly': collisions.exclude(pk__in=collisionsInPoly),
		# 'nearmissesOutPoly': nearmisses.exclude(pk__in=nearmissesInPoly),
		# 'hazardsOutPoly': hazards.exclude(pk__in=hazardsInPoly),
		# 'theftsOutPoly': thefts.exclude(pk__in=theftsInPoly),
	}

	return render(request, 'mapApp/stats.html', context)
