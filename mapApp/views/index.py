from django.shortcuts import render

from mapApp.models import Incident, Theft, Hazard, Official, AlertArea
from mapApp.forms import IncidentForm, GeofenceForm, EditForm, HazardForm, TheftForm

from itertools import chain
from django.core.cache import cache
import pickle
# import logging
# logger = logging.getLogger(__name__)

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
	# Cache official collisions in slices to stay below 1Mb cache limit of memcached
	CACHE_SLICE = 1000
	oLen = Official.objects.count()
	officialResult = Official.objects.none()

	cacheKeys = [ ("officials_" + str(i)) for i in xrange(oLen/CACHE_SLICE + 1) ]
	officialsPickled = cache.get_many(cacheKeys)

	for key in cacheKeys:
		if key not in officialsPickled.keys():
			i = int(key.split("_")[1])*CACHE_SLICE
			officialSlice = Official.objects.all()[i:i+CACHE_SLICE]
			cache.set(key, pickle.dumps(officialSlice), 60*60)
		else:
			officialSlice = pickle.loads(officialsPickled[key])

		officialResult = list(chain(officialResult, officialSlice)) # Concat slice and result querysets

	# Put all incidents in django cache
	incidents = Incident.objects.only('p_type', 'id').select_related('point').all()

	return {
		# Model data used by map
		'collisions': incidents.filter(p_type__exact="collision"),
		'nearmisses': incidents.filter(p_type__exact="nearmiss"),
		'hazards': Hazard.objects.select_related('point').all(),
		'thefts': Theft.objects.select_related('point').all(),
		'officials': officialResult,
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": incidentForm,
		"geofenceForm": geofenceForm,
		"hazardForm": hazardForm,
		"theftForm": theftForm,

		"editForm": EditForm()
	}
