from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.contrib.gis.geos import GEOSGeometry
import json, math, datetime
from django.contrib import messages

# Decorators
from django.views.decorators.http import require_POST

from mapApp.models import Incident, Hazard, Theft
from mapApp.forms import IncidentForm, HazardForm, TheftForm
from mapApp.views import alertUsers, indexContext

@require_POST
def postIncident(request):
	incidentForm = IncidentForm(request.POST)
	incidentForm.data = incidentForm.data.copy()

	# Convert coords to valid geometry
	try:
		incidentForm.data['geom'] = normalizeGeometry(incidentForm.data['geom'])
		dt = datetime.datetime.strptime(incidentForm.data['date'], "%Y-%m-%d %H:%M")
		incidentForm.data['time'] = dt.time()
		incidentForm.data['date'] = dt.date()
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>There was an error with the form submission.')
		return HttpResponseRedirect(reverse('mapApp:index'))

	# Set p_type field to collision, nearmiss, or fall
	incidentForm.data['p_type'] = getIncidentType(incidentForm.data['incident_type'])

	# Validate and submit to db
	if incidentForm.is_valid():
		incident = incidentForm.save()
		alertUsers(request, incident)

		messages.success(request, '<strong>Thank you!</strong><br>Your incident marker was successfully added.')
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(incident.latlngList()[0]),		\
				"lng":str(incident.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		))
	else: # Show form errors
		return render(request, 'mapApp/index.html', indexContext(request, incidentForm=incidentForm))

def getIncidentType(usr_choice):
	for t,choice in Incident.INCIDENT_CHOICES:
		for p,q in choice:
			if p == usr_choice:
				return t.replace(" ", "").lower()

@require_POST
def postHazard(request):
	hazardForm = HazardForm(request.POST)
	hazardForm.data = hazardForm.data.copy()

	# Convert coords to valid geometry
	try :
		hazardForm.data['geom'] = normalizeGeometry(hazardForm.data['geom'])
		dt = datetime.datetime.strptime(hazardForm.data['date'], "%Y-%m-%d %H:%M")
		hazardForm.data['time'] = dt.time()
		hazardForm.data['date'] = dt.date()
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>There was an error with the form submission.')
		return HttpResponseRedirect(reverse('mapApp:index'))

	# Set p_type
	hazardForm.data['p_type'] = 'hazard'

	if hazardForm.is_valid():
		hazard = hazardForm.save()
		alertUsers(request, hazard)

		messages.success(request, '<strong>Thank you!</strong><br>Your hazard marker was successfully added.')
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(hazard.latlngList()[0]),		\
				"lng":str(hazard.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		))

	else: # Show form errors
		return HttpResponse(hazardForm)
		return render(request, 'mapApp/index.html', indexContext(request, hazardForm=hazardForm))

@require_POST
def postTheft(request):
	theftForm = TheftForm(request.POST)
	theftForm.data = theftForm.data.copy()

	# Convert coords to valid geometry
	try:
		theftForm.data['geom'] = normalizeGeometry(theftForm.data['geom'])
		dt = datetime.datetime.strptime(theftForm.data['date'], "%Y-%m-%d %H:%M")
		theftForm.data['time'] = dt.time()
		theftForm.data['date'] = dt.date()
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>There was an error with the form submission.')
		return HttpResponseRedirect(reverse('mapApp:index'))

	# Set p_type
	theftForm.data['p_type'] = 'theft'

	if theftForm.is_valid():
		theft = theftForm.save()
		alertUsers(request, theft)

		messages.success(request, '<strong>Thank you!</strong><br>Your theft marker was successfully added.')
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(theft.latlngList()[0]),		\
				"lng":str(theft.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		))

	else: # Show form errors
		return render(request, 'mapApp/index.html', indexContext(request, theftForm=theftForm))

# Convert text string to GEOS Geometry object and correct x y coordinates if out range (-180, 180]
def normalizeGeometry(geom):
	# Convert string GEOSGeometry object to python dict
	geom = json.loads(geom)

	# Normalize to range [-180, 180) using saw tooth function
	for i, c in enumerate(geom['coordinates']):
		geom['coordinates'][i] = (c+180 - ( math.floor( (c+180)/360 ) )*360) - 180

	# Encode and return GEOSGeometry object
	return GEOSGeometry(json.dumps(geom))
