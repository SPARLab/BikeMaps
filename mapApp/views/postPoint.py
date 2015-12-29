from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.contrib.gis.geos import GEOSGeometry
from djgeojson.serializers import Serializer as GeoJSONSerializer

from  crispy_forms.utils import render_crispy_form

from mapApp.models import Incident, Hazard, Theft
from mapApp.forms import IncidentForm, NearmissForm, HazardForm, TheftForm
from mapApp.views import alertUsers, pushNotification

import json, math

import logging
logger = logging.getLogger(__name__)

@require_POST
def postIncident(request):
	return postPoint(request, IncidentForm)

@require_POST
def postNearmiss(request):
	return postPoint(request, NearmissForm)


@require_POST
def postHazard(request):
	return postPoint(request, HazardForm)

@require_POST
def postTheft(request):
	return postPoint(request, TheftForm)

def postPoint(request, Form):
	"""Submit a user point submission to the database. Normalize geometry and activate push notifications."""
	form = Form(request.POST)
	form.data = form.data.copy()

	# Convert coords to valid geometry
	try:
		form.data['geom'] = normalizeGeometry(form.data['geom'])
	except(ValueError):
		# TODO provide error message to user here
		JsonResponse({'success': False})
		# messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))

	# Validate and submit to db
	if form.is_valid():
		point = form.save()
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(point)
			except: pass

		return JsonResponse({
			'success': True,
			'point': GeoJSONSerializer().serialize([point,]),
			'point_type': point.p_type,
			'form_html': render_crispy_form(Form())
		})
	else:
		logger.debug("Form not valid")

	# Else: error occurred
	form.data['geom'] = form.data['geom'].json
	form_html = render_crispy_form(form)
	return JsonResponse({'success': False, 'form_html': form_html})

def normalizeGeometry(geom):
	"""Convert text string to GEOS Geometry object and correct x y coordinates if out range (-180, 180]."""
	# Convert string GEOSGeometry object to python dict
	geom = json.loads(geom)

	# Normalize longitude to range [-180, 180) using saw tooth function
	c = geom['coordinates'][0]
	geom['coordinates'][0] = (c+180 - ( math.floor( (c+180)/360 ) )*360) - 180

	# Normalize latitude to range [-90, 90) using saw tooth function
	c = geom['coordinates'][1]
	geom['coordinates'][1] = (c+90 - ( math.floor( (c+90)/180 ) )*180) - 90

	# Encode and return GEOSGeometry object
	return GEOSGeometry(json.dumps(geom))
