from django.http import HttpResponse
from django.contrib.gis.geos import Polygon

from djgeojson.serializers import Serializer as GeoJSONSerializer

from mapApp.models import Point, Incident, Hazard, Theft, Official

# Functions for returning points within a specified bounding box
# Caller sends a GET with an url parameter of bbox=xmin,ymin,xmax,ymax
# eg. http://bikemaps.org/points_api.json?bbox=180,-90,180,90

def getPointsApi(request):
    # Extract bounding box Url parameter
    bbstr = request.GET.get('bbox', '-180,-90,180,90')
    bbox = stringToPolygon(bbstr)

    # Filter for points in the bounding box
    points = list(Point.objects.filter(geom__within=bbox))

    # Serialize the points into GeoJson
    data = GeoJSONSerializer().serialize(points, indent=2, use_natural_keys=True)

    return HttpResponse(data, content_type="application/json")

# Query for collisions based on a bounding box
def getCollisionsApi(request):
    # Extract bounding box Url parameter
    bbstr = request.GET.get('bbox', '-180,-90,180,90')
    bbox = stringToPolygon(bbstr)

    # Filter for points in the bounding box
    points = list(Incident.objects.filter(p_type__exact="collision").filter(geom__within=bbox) | Incident.objects.filter(p_type__exact="fall").filter(geom__within=bbox))

    # Serialize the points into GeoJson
    data = GeoJSONSerializer().serialize(points, indent=2, use_natural_keys=True)

    return HttpResponse(data, content_type="application/json")

# Query for near misses based on a bounding box
def getNearmissApi(request):
    # Extract bounding box Url parameter
    bbstr = request.GET.get('bbox', '-180,-90,180,90')
    bbox = stringToPolygon(bbstr)

    # Filter for points in the bounding box
    points = list(Incident.objects.filter(p_type__exact="nearmiss").filter(geom__within=bbox))

    # Serialize the points into GeoJson
    data = GeoJSONSerializer().serialize(points, indent=2, use_natural_keys=True)

    return HttpResponse(data, content_type="application/json")

# Query for incidents based on a bounding box
def getIncidentsApi(request):
    # Extract bounding box Url parameter
    bbstr = request.GET.get('bbox', '-180,-90,180,90')
    bbox = stringToPolygon(bbstr)

    # Filter for points in the bounding box
    points = list(Incident.objects.filter(geom__within=bbox))

    # Serialize the points into GeoJson
    data = GeoJSONSerializer().serialize(points, indent=2, use_natural_keys=True)

    return HttpResponse(data, content_type="application/json")


# Query for hazards based on a bounding box
def getHazardsApi(request):
    # Extract bounding box Url parameter
    bbstr = request.GET.get('bbox', '-180,-90,180,90')
    bbox = stringToPolygon(bbstr)

    # Filter for points in the bounding box
    points = list(Hazard.objects.filter(geom__within=bbox))

    # Serialize the points into GeoJson
    data = GeoJSONSerializer().serialize(points, indent=2, use_natural_keys=True)

    return HttpResponse(data, content_type="application/json")


# Query for thefts based on a bounding box
def getTheftsApi(request):
    # Extract bounding box Url parameter
    bbstr = request.GET.get('bbox', '-180,-90,180,90')
    bbox = stringToPolygon(bbstr)

    # Filter for points in the bounding box
    points = list(Theft.objects.filter(geom__within=bbox))

    # Serialize the points into GeoJson
    data = GeoJSONSerializer().serialize(points, indent=2, use_natural_keys=True)

    return HttpResponse(data, content_type="application/json")


# Query for official data based on a bounding box
def getOfficialApi(request):
    # Extract bounding box Url parameter
    bbstr = request.GET.get('bbox', '-180,-90,180,90')
    bbox = stringToPolygon(bbstr)

    # Filter for points in the bounding box
    points = list(Official.objects.filter(geom__within=bbox))

    # Serialize the points into GeoJson
    data = GeoJSONSerializer().serialize(points, indent=2, use_natural_keys=True)

    return HttpResponse(data, content_type="application/json")


# Create bounding box as a polygon
def stringToPolygon(bbstr):

    bbsplt = bbstr.split(',')
    xmin, ymin, xmax, ymax = [float(x) for x in bbsplt]

    return Polygon.from_bbox((xmin, ymin, xmax, ymax))
    
