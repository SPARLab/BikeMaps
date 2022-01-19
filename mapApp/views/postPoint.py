from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from djgeojson.serializers import Serializer as GeoJSONSerializer

from  crispy_forms.utils import render_crispy_form

from mapApp.models import Incident, Hazard, Theft, NewInfrastructure
from mapApp.forms import IncidentForm, NearmissForm, HazardForm, TheftForm, NewInfrastructureForm
from mapApp.views import alertUsers, pushNotification

from mapApp.utils.locationHelpers import retrieveFollowUpMsg, normalizeGeometry

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

@require_POST
def postNewInfrastructure(request):
    return postPoint(request, NewInfrastructureForm)

def postPoint(request, Form):
    """Submit a user point submission to the database. Normalize geometry and activate push notifications."""
    form = Form(request.POST)
    form.data = form.data.copy()

    followUpMsg = None

    # Convert coords to valid geometry
    try:
        form.data['geom'] = normalizeGeometry(form.data['geom'])
    except(ValueError):
        # TODO provide error message to user here
        JsonResponse({'success': False})
        # messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))

    # Validate and submit to db
    if form.is_valid():

      # Add any follow up modal messages
        # Check if the point was a hazard and in the areas where 311 information is available
        if "hazard" in str(type(form)):
            followUpMsg = retrieveFollowUpMsg("hazard", form.data)
        # Check if the point was an incident in area where crash info available
        if "incident" in str(type(form)):
            followUpMsg = retrieveFollowUpMsg("incident", form.data)

        point = form.save()

        # Errors with push notifications should not affect reporting
        if not settings.DEBUG:
            try: pushNotification.pushNotification(point)
            except: pass
        return JsonResponse({
            'followUpMsg': followUpMsg,
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
