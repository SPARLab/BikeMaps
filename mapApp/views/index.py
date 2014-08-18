from django.shortcuts import render

# Import models
from mapApp.models.incident import Incident
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft
from mapApp.models.alert_area import AlertArea

# Import forms
from mapApp.forms.incident import IncidentForm
from mapApp.forms.geofences import GeofenceForm
from mapApp.forms.edit_geom import EditForm
from mapApp.forms.hazard import HazardForm
from mapApp.forms.theft import TheftForm


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
	return {
		# Model data used by map
		'incidents': Incident.objects.all(),
		'hazards': Hazard.objects.all(),
		'thefts': Theft.objects.all(),
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": incidentForm,
		"geofenceForm": geofenceForm,
		"hazardForm": hazardForm,
		"theftForm": theftForm,
		
		"editForm": EditForm()
	}