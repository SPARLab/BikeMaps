from django.shortcuts import render

from mapApp.models import Incident, Theft, Hazard, Official, AlertArea
from mapApp.forms import IncidentForm, HazardForm, TheftForm, GeofenceForm, EditForm
import datetime

def index(request, lat=None, lng=None, zoom=None):
	incidents = Incident.objects.select_related('point').all()
	now = datetime.datetime.now()

	context = {
		# Model data used by map
		'collisions': incidents.filter(p_type__exact="collision"),
		'nearmisses': incidents.filter(p_type__exact="nearmiss"),
		'hazards': Hazard.objects.select_related('point').exclude(expires_date__lt=now),
		'thefts': Theft.objects.select_related('point').all(),
		# 'officials': officialResult,
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": IncidentForm(),
		"hazardForm": HazardForm(),
		"theftForm": TheftForm(),

		"geofenceForm": GeofenceForm(),
		"editForm": EditForm()
	}

	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)

	return render(request, 'mapApp/index.html', context)
