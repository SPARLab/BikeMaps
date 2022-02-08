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
	context = {
		# Model data used by map
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
