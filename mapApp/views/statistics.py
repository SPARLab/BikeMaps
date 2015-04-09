from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from django.contrib.auth.models import User
from mapApp.models.alert_notification import IncidentNotification, HazardNotification, TheftNotification

from mapApp.models import Incident, Hazard, Theft, AlertArea, Point

@login_required
def stats(request):
	user = request.user

	# Get the user's alertable points in the last month
	collisions = Incident.objects.filter(p_type__exact="collision") | Incident.objects.filter(p_type__exact="fall")
	nearmisses = Incident.objects.filter(p_type__exact="nearmiss")
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
	}

	return render(request, 'mapApp/stats.html', context)

@cache_page(60 * 15)
def vis(request):
	collisions = Incident.objects.filter(p_type__exact="collision")
	nearmisses = Incident.objects.filter(p_type__exact="nearmiss")

	context = {
		'collisions': collisions,
		'nearmisses': nearmisses,
		'hazards': Hazard.objects.all(),
		'thefts': Theft.objects.all(),
		'points': Point.objects.all()
	}
	return render(request, 'mapApp/vis.html', context)
