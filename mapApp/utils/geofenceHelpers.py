from django.contrib.gis.geos import GEOSGeometry
import json, math
from mapApp.utils.geofencePolygonsHazards import greaterVancouver, withinGreaterVancouver, outsideGreaterVancouver, ontario
from mapApp.utils.geofencePolygonsRaffle import santaBarbara
from mapApp.utils.sbSimple import sb

def retrieveFollowUpMsg(formType, data):
    #grab latitude and longitude from form
    longitude =  data['geom'][0]
    latitude = data['geom'][1]

    #Check if hazard point fell in areas
    if (formType == "hazard"):
        if point_in_poly(longitude,latitude,greaterVancouver['coordinates']):
            for polygon in withinGreaterVancouver:
                if point_in_poly(longitude, latitude, withinGreaterVancouver[polygon]["coordinates"]):
                    return withinGreaterVancouver[polygon]["message"]
        else:
            for polygon in outsideGreaterVancouver:
                if point_in_poly(longitude, latitude, outsideGreaterVancouver[polygon]["coordinates"]):
                    return outsideGreaterVancouver[polygon]["message"]
    elif (formType == "incident"):
        if point_in_poly(longitude, latitude, ontario["coordinates"]):
            return ontario["message"]

    # Check if point of any type falls within active raffle area
        # Note: This raffle doesn't overlap with any of the existing geofences, otherwise would need to handle returning two popups

    print(sb["coordinates"])
    if point_in_poly(longitude, latitude, sb["coordinates"]):
        return sb["message"]

    #  Question: does point in poly work for multipolygons? no
    # if point_in_poly(longitude, latitude, santaBarbara["features"][0]["geometry"]["coordinates"][0]):
    #     print('in first poly')
    #     return santaBarbara["message"]
    # if point_in_poly(longitude, latitude, santaBarbara["features"][0]["geometry"]["coordinates"][1]):
    #     print('in second poly')
    #     return santaBarbara["message"]
    # if point_in_poly(longitude, latitude, santaBarbara["features"][0]["geometry"]["coordinates"][2]):
    #     print('in third poly')
    #     return santaBarbara["message"]


    return None

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
