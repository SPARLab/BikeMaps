from django.contrib.gis.geos import Polygon
from django.shortcuts import render


from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from mapApp.models import Incident, Theft, Hazard, Official, AlertArea, NewInfrastructure
from mapApp.forms import IncidentForm, NearmissForm, HazardForm, TheftForm, NewInfrastructureForm, GeofenceForm, EditForm
import datetime

import logging
logger = logging.getLogger(__name__)

@xframe_options_exempt
def index(request, lat=None, lng=None, zoom=None):
	incidents = Incident.objects.select_related('point').all()
	now = datetime.datetime.now()

	context = {
		# Model data used by map

		# NOTE: all points are limited to cumulative 10000 points. This should be considered a temporary fix until there are some limitations on the requested data.
		# Only displaying official data for Germany based on a bounding box
		'''
		'collisions': incidents.filter(p_type__exact="collision").exclude(infrastructure_changed=True).order_by('-date')[:1],
		'nearmisses': incidents.filter(p_type__exact="nearmiss").exclude(infrastructure_changed=True).order_by('-date')[:1],
		'hazards': Hazard.objects.select_related('point').exclude(expires_date__lt=now).exclude(hazard_fixed=True).order_by('-date')[:1],
		'thefts': Theft.objects.select_related('point').all().exclude(infrastructure_changed=True).order_by('-date')[:1],
		'''

		#'collisions': incidents.all()[:1],
		#'nearmisses': incidents.all()[:1],
		#'hazards': Hazard.objects.all()[:1],
		#'thefts': Theft.objects.all()[:1],
		#'newInfrastructures': NewInfrastructure.objects.select_related('point').exclude(expires_date__lt=now).order_by('-date')[:2500],
		'officials': Official.objects.filter(geom__within=(Polygon.from_bbox((5,47,15,55)))),
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": IncidentForm(),
		"nearmissForm": NearmissForm(),
		"hazardForm": HazardForm(),
		"theftForm": TheftForm(),
		"newInfrastructureForm": NewInfrastructureForm(),
		"geofenceForm": GeofenceForm(),
		"editForm": EditForm()
	}

	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)

	return render(request, 'mapApp/index.html', context)
