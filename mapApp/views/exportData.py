from django.http import HttpResponse

from djgeojson.serializers import Serializer as GeoJSONSerializer
from itertools import product
import time, json

from mapApp.models import Point, Incident, Hazard, Theft

# Decorators
from spirit.utils.decorators import administrator_required

@administrator_required
def getPoints(request):
	data = GeoJSONSerializer().serialize(Point.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_points_%s.json' % time.strftime("%x_%H-%M")
	return response

@administrator_required
def getIncidents(request):
	data = GeoJSONSerializer().serialize(Incident.objects.all(), indent=2, use_natural_keys=True)
	data = _joinPoints(data)

	response = HttpResponse(data, content_type="application/json")
	# response['Content-Disposition'] = 'attachment; filename="bikemaps_incidents_%s.json' % time.strftime("%x_%H-%M")
	return response

@administrator_required
def getHazards(request):
	data = GeoJSONSerializer().serialize(Hazard.objects.all(), indent=2, use_natural_keys=True)
	data = _joinPoints(data)

	response = HttpResponse(data, content_type="application/json")
	# response['Content-Disposition'] = 'attachment; filename="bikemaps_hazards_%s.json' % time.strftime("%x_%H-%M")
	return response

@administrator_required
def getThefts(request):
	data = GeoJSONSerializer().serialize(Theft.objects.all(), indent=2, use_natural_keys=True)
	data = _joinPoints(data)

	response = HttpResponse(data, content_type="application/json")
	# response['Content-Disposition'] = 'attachment; filename="bikemaps_thefts_%s.json' % time.strftime("%x_%H-%M")
	return response

def _joinPoints(data):
	data = json.loads(data)
	points = json.loads(GeoJSONSerializer().serialize(Point.objects.all(), indent=2, use_natural_keys=True))

	for d,p in product(data['features'], points['features']):
		if (d['id'] == p['id']):
			d['properties'].update(p['properties'])

	return json.dumps(data, indent=2)
