from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from django.contrib.gis.geos import GEOSGeometry
import json
import math
from django.contrib import messages
from django.conf import settings

# Decorators
from django.views.decorators.http import require_POST

from mapApp.models import Incident, Hazard, Theft
from mapApp.forms import IncidentForm, HazardForm, TheftForm
from mapApp.views import alertUsers, indexContext, pushNotification

@require_POST
def postIncident(request):
	incidentForm = IncidentForm(request.POST)
	incidentForm.data = incidentForm.data.copy()

	# Convert coords to valid geometry
	try:
		incidentForm.data['geom'] = normalizeGeometry(incidentForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))
		return HttpResponseRedirect(reverse('mapApp:index'))

	# Set p_type field to collision, nearmiss, or fall
	incidentForm.data['p_type'] = getIncidentType(incidentForm.data['i_type'])

	# Validate and submit to db
	if incidentForm.is_valid():
		incident = incidentForm.save()
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(incident)
			except: pass

		messages.success(request, '<strong>' + _('Thank you!') + '</strong><br>' + _('Your incident marker was successfully added.'))
		return redirect(incident)

	else: # Show form errors
		incidentForm.data['geom'] = incidentForm.data['geom'].json
		return render(request, 'mapApp/index.html', indexContext(request, incidentForm=incidentForm))

def getIncidentType(usr_choice):
	for t,choice in Incident.INCIDENT_CHOICES:
		for p,q in choice:
			if p == usr_choice:
				if t == "Fall": return "collision"
				else: return t.replace(" ", "").lower()

@require_POST
def postHazard(request):
	hazardForm = HazardForm(request.POST)
	hazardForm.data = hazardForm.data.copy()

	# Convert coords to valid geometry
	try :
		hazardForm.data['geom'] = normalizeGeometry(hazardForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))
		return HttpResponseRedirect(reverse('mapApp:index'))

	# Set p_type
	hazardForm.data['p_type'] = 'hazard'

	if hazardForm.is_valid():
		hazard = hazardForm.save()
		alertUsers(request, hazard)
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(hazard)
			except: pass

		#messages.success(request, resp.results.message_id)

		messages.success(request, '<strong>' + _('Thank you!') + '</strong><br>' + _('Your hazard marker was successfully added.'))
		return redirect(hazard)

	else: # Show form errors
		hazardForm.data['geom'] = hazardForm.data['geom'].json
		return render(request, 'mapApp/index.html', indexContext(request, hazardForm=hazardForm))

@require_POST
def postTheft(request):
	theftForm = TheftForm(request.POST)
	theftForm.data = theftForm.data.copy()

	# Convert coords to valid geometry
	try:
		theftForm.data['geom'] = normalizeGeometry(theftForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))
		return HttpResponseRedirect(reverse('mapApp:index'))

	# Set p_type
	theftForm.data['p_type'] = 'theft'

	if theftForm.is_valid():
		theft = theftForm.save()
		alertUsers(request, theft)
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(theft)
			except: pass

		messages.success(request, '<strong>' + _('Thank you!') + '</strong><br>' + _('Your theft marker was successfully added.'))
		return redirect(theft)

	else: # Show form errors
		theftForm.data['geom'] = theftForm.data['geom'].json
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
