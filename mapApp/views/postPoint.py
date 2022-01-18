from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.contrib.gis.geos import GEOSGeometry
from djgeojson.serializers import Serializer as GeoJSONSerializer

from  crispy_forms.utils import render_crispy_form

from mapApp.models import Incident, Hazard, Theft, NewInfrastructure
from mapApp.forms import IncidentForm, NearmissForm, HazardForm, TheftForm, NewInfrastructureForm
from mapApp.views import alertUsers, pushNotification
from mapApp.utils.locationPolygons import outlineOfGreaterVancouver, burnaby, coquitlam, delta, districtOfNorthVancouver, districtOfWestVancouver, mapleRidge, newWestminster, pittMeadows, portCoquitlam, portMoody, richmond, surrey, townshipOfLangley, vancouver, whiterock, edmonton, kelowna

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

        #Check if the point was a hazard and in the areas where 311 popups are available
        if "hazard" in str(type(form)):
            followUpMsg = threeOneOnePopUp(form.data)

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

def threeOneOnePopUp(data):
    message = None
    #grab latitude and longitude from form
    longitude =  data['geom'][0]
    latitude = data['geom'][1]

    #Check if point fell in areas
    if point_in_poly(longitude,latitude,outlineOfGreaterVancouver):
        if point_in_poly(longitude,latitude,burnaby):
            message = "Report this hazard to Burnaby authorities by calling 1-604-294-7440"

        if point_in_poly(longitude,latitude,burnaby):
            message = "To report this hazard to the City Of North Vancouver authorities: <br> Download the CityFix App from <a href=\"http://www.cnv.org/online-services/city-fix\" style=\"color: white\">here</a>"

        if point_in_poly(longitude,latitude,coquitlam):
            message = "Report this hazard to Coquitlam authorities by calling 1-604-927-3500"

        if point_in_poly(longitude,latitude,delta):
            message = "To report this hazard to Delta authorities:<br> 1) Call 1-604-946-3260 <br> 2) Report online <a href=\"http://www.delta.ca/your-government/contact-us/talk-to-delta\" style=\"color:white\">here</a>"

        if point_in_poly(longitude,latitude,districtOfNorthVancouver):
            message = "To report this hazard to the District of North Vancouver authorities:<br> 1) Call 1-604-990-2450 <br> 2) Email eng@dnv.org"

        if point_in_poly(longitude,latitude,districtOfWestVancouver):
            message = "To report this hazard to the District of West Vancouver authorities:<br> 1) Call 1-604-925-7020 <br> 2) Email ecounter@westvancouver.ca"

        if point_in_poly(longitude,latitude,mapleRidge):
            message = "Report this hazard online to Maple Ridge authorities <a href=\"http://mapleridge.ca/FormCenter/Service-Request-Form-5/Service-Request-Form-45\" style=\"color:white\">here</a>"

        if point_in_poly(longitude,latitude,newWestminster):
            message = "To report this hazard to New Westminster authorities:<br> 1) Report online <a href=\"https://www.newwestcity.ca/services/online-services/report-a-problem\" style=\"color:white\">here</a> <br> 2) Download the SeeClickFix App from <a href=\"http://seeclickfix.com/apps\" style=\"color:white\">here</a>"

        if point_in_poly(longitude,latitude,pittMeadows):
            message = "Report this hazard to Pitt Meadows authorities by calling 1-604-465-2434"

        if point_in_poly(longitude,latitude,portCoquitlam):
            message = "To report this hazard to Port Coquitlam authorities:<br> 1) Call 1-604-927-5496 <br> 2) Email publicworks@portcoquitlam.ca"

        if point_in_poly(longitude,latitude,portMoody):
            message = "Report this hazard to Port Moody authorities by calling 1-604-469-4574"

        if point_in_poly(longitude,latitude,richmond):
            message = "Report this hazard online to Richmond authorities <a href=\"http://www.richmond.ca/contact/customerfeedback/RequestService.aspx\" style=\"color:white\">here</a>"

        if point_in_poly(longitude,latitude,surrey):
            message = "To report this hazard to Surrey authorities:<br> 1) Download the Surrey Request App from <a href=\"http://www.surrey.ca/city-services/12082.aspx\" style=\"color:white\">here</a> <br> 2) Report online <a href=\"http://www.surrey.ca/city-services/667.aspx\" style=\"color:white\">here</a>"

        if point_in_poly(longitude,latitude,townshipOfLangley):
            message = "Report this hazard online to the Township of Langley authorities <a href\"http://www.tol.ca/Services-Contact/Report-a-Problem\" style=\"color:white\">here</a>"

        if point_in_poly(longitude,latitude,vancouver):
            message = "To report this hazard to Vancouver authorities:<br> 1) Call 3-1-1 <br> 2) Report online <a href=\"http://vancouver.ca/vanconnect-desktop.aspx\" style=\"color:white\">here</a> <br> 3) Download the VanConnect App from <a href=\"http://vancouver.ca/vanconnect.aspx\" style=\"color:white\">here</a>"

        if point_in_poly(longitude,latitude,whiterock):
            message = "Report this hazard to White Rock authorities by calling 1-604-541-2181"

    if point_in_poly(longitude,latitude, edmonton):
        message = "Report this hazard to Edmonton authorities by downloading the 311 App from <a href=\"https://www.edmonton.ca/programs_services/edmonton-311-app.aspx\" style=\"color:white\">here</a>"

    if point_in_poly(longitude,latitude, kelowna):
        message = "Report this hazard online to Kelowna authorities <a href=\"https://apps.kelowna.ca/iService_Requests/request.cfm?id=265&sid=97\" style=\"color:white\">here</a>"

    return message

def normalizeGeometry(geom):
    """Convert text string to GEOS Geometry object and correct x y coordinates if out range (-180, 180]."""
    # Convert string GEOSGeometry object to python dict
    geom = json.loads(geom)

    # Normalize longitude to range [-180, 180) using saw tooth function
    ch = geom['coordinates'][0]
    geom['coordinates'][0] = (ch+180 - ( math.floor( (ch+180)/360 ) )*360) - 180

    # Normalize latitude to range [-90, 90) using saw tooth function
    ch = geom['coordinates'][1]
    geom['coordinates'][1] = (ch+90 - ( math.floor( (ch+90)/180 ) )*180) - 90

    # Encode and return GEOSGeometry object
    return GEOSGeometry(json.dumps(geom), srid=4326)

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".
####This code was found here: http://geospatialpython.com/2011/01/point-in-polygon.html
####x = longitude, y = latitude
def point_in_poly(x,y,poly):
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside
