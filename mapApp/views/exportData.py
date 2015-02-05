from django.http import HttpResponse

from djgeojson.serializers import Serializer as GeoJSONSerializer
import time

# Decorators
from spirit.utils.decorators import administrator_required

# Models
from mapApp.models.incident import Incident
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft


@administrator_required
def getIncidents(request):
	data = GeoJSONSerializer().serialize(Incident.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_incidents_%s.json' % time.strftime("%x_%H-%M")
	return response

@administrator_required
def getHazards(request):
	data = GeoJSONSerializer().serialize(Hazard.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_hazards_%s.json' % time.strftime("%x_%H-%M")
	return response

@administrator_required
def getThefts(request):
	data = GeoJSONSerializer().serialize(Theft.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_thefts_%s.json' % time.strftime("%x_%H-%M")
	return response
