from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.contrib.gis.geos import GEOSGeometry
from djgeojson.serializers import Serializer as GeoJSONSerializer

from  crispy_forms.utils import render_crispy_form

from mapApp.models import Incident, Hazard, Theft
from mapApp.forms import IncidentForm, HazardForm, TheftForm
from mapApp.views import alertUsers, indexContext, pushNotification

import json, math

@require_POST
def postIncident(request):
	incidentForm = IncidentForm(request.POST)
	incidentForm.data = incidentForm.data.copy()

	# Convert coords to valid geometry
	try:
		incidentForm.data['geom'] = normalizeGeometry(incidentForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))

	# Set p_type field to collision, nearmiss, or fall
	incidentForm.data['p_type'] = getIncidentType(incidentForm.data['i_type'])

	# Validate and submit to db
	if incidentForm.is_valid():
		incident = incidentForm.save()
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(incident)
			except: pass

		return JsonResponse({
	        'success': True,
			'point': GeoJSONSerializer().serialize([incident,]),
			'point_type': incident.p_type,
			'form_html': render_crispy_form(IncidentForm()),
        })

	# Else: error occurred
	incidentForm.data['geom'] = incidentForm.data['geom'].json
	form_html = render_crispy_form(incidentForm)
	return JsonResponse({'success': False, 'form_html': form_html})

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

	# Set p_type
	hazardForm.data['p_type'] = 'hazard'

	# Validate and submit to db
	if hazardForm.is_valid():
		hazard = hazardForm.save()
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(hazard)
			except: pass

		return JsonResponse({
			'success': True,
			'point': GeoJSONSerializer().serialize([hazard,]),
			'point_type': hazard.p_type,
			'form_html': render_crispy_form(HazardForm())
		})

	# Else: error occurred
	hazardForm.data['geom'] = hazardForm.data['geom'].json
	form_html = render_crispy_form(hazardForm)
	return JsonResponse({'success': False, 'form_html': form_html})

@require_POST
def postTheft(request):
	theftForm = TheftForm(request.POST)
	theftForm.data = theftForm.data.copy()

	# Convert coords to valid geometry
	try:
		theftForm.data['geom'] = normalizeGeometry(theftForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))

	# Set p_type
	theftForm.data['p_type'] = 'theft'

	# Validate and submit to db
	if theftForm.is_valid():
		theft = theftForm.save()
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(theft)
			except: pass

		return JsonResponse({
			'success': True,
			'point': GeoJSONSerializer().serialize([theft,]),
			'point_type': theft.p_type,
			'form_html': render_crispy_form(TheftForm())
		})

	# Else: error occurred
	theftForm.data['geom'] = theftForm.data['geom'].json
	form_html = render_crispy_form(theftForm)
	return JsonResponse({'success': False, 'form_html': form_html})


# Convert text string to GEOS Geometry object and correct x y coordinates if out range (-180, 180]
def normalizeGeometry(geom):
	# Convert string GEOSGeometry object to python dict
	geom = json.loads(geom)

	# Normalize to range [-180, 180) using saw tooth function
	for i, c in enumerate(geom['coordinates']):
		geom['coordinates'][i] = (c+180 - ( math.floor( (c+180)/360 ) )*360) - 180

	# Encode and return GEOSGeometry object
	return GEOSGeometry(json.dumps(geom))
