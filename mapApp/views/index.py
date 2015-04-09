from django.shortcuts import render
from django.http import HttpResponse

from mapApp.models import Incident, Theft, Hazard, Official, AlertArea
from mapApp.forms import IncidentForm, GeofenceForm, EditForm, HazardForm, TheftForm
from django.core.cache import cache

def index(request, lat=None, lng=None, zoom=None):
	context = indexContext(request)

	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)

	return render(request, 'mapApp/index.html', context)


# Define default context data for the index view. Forms can be overridden to display errors (used by other views)
def indexContext(request, incidentForm=IncidentForm(), geofenceForm=GeofenceForm(), hazardForm=HazardForm(), theftForm=TheftForm()):
	# Try to get official reports from cache
	officials = cache.get('officialObjects')
	if not officials:
		# If cache miss, get from database and put in cache
		officials = Official.objects.all()
		cache.set('officialObjects', 60*60)
	# else:
	# 	return HttpResponse("Cache hit!")

	return {
		# Model data used by map
		'collisions': Incident.objects.filter(p_type__exact="collision") | Incident.objects.filter(p_type__exact="fall"),
		'nearmisses': Incident.objects.filter(p_type__exact="nearmiss"),
		'hazards': Hazard.objects.all(),
		'thefts': Theft.objects.all(),
		'officials': officials,
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": incidentForm,
		"geofenceForm": geofenceForm,
		"hazardForm": hazardForm,
		"theftForm": theftForm,

		"editForm": EditForm()
	}
