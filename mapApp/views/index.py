from django.shortcuts import render

from mapApp.models import Point, AlertArea
from mapApp.forms import IncidentForm, GeofenceForm, EditForm, HazardForm, TheftForm

def index(request, lat=None, lng=None, zoom=None):
	context = indexContext(request)

	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)

	return render(request, 'mapApp/index.html', context)


# Define default context data for the index view. Forms can be overridden to display errors (used by other views)
def indexContext(request):#, incidentForm=IncidentForm(), geofenceForm=GeofenceForm(), hazardForm=HazardForm(), theftForm=TheftForm()):
	points = Point.objects.all()

	return {
		# Model data used by map
		'collisions': points.filter(p_type__exact="collision"),
		'nearmisses': points.filter(p_type__exact="nearmiss"),
		'hazards': points.filter(p_type__exact="hazard"),
		'thefts': points.filter(p_type__exact="theft"),
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": IncidentForm,
		"geofenceForm": GeofenceForm,
		"hazardForm": HazardForm,
		"theftForm": TheftForm,

		"editForm": EditForm()
	}
