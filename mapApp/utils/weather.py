# Alex Goudine
# GEOG 490 - Webscraping and Database Design
# Scrapes weather data from forecast.io and returns a dict of the relevant information

# Modified by Taylor Denouden
# Shortened script and made into a simple function in which geom and date data can be passed
# Added more efficient and robust cardinal direction lookup
# Removed test for unlimited visibility to maintain data type consistency in database
# Removed test to see if rider was travelling in the same direction in favor of storing the cardinal wind direction only
# Updated docstring

import urllib.request
import json
from datetime import datetime
import time
from django.conf import settings

def get_weather(coords, date):
    """ Generate a dict of weather data for a location at a given time

    Keyword arguments:
    coords -- decimal degree coordinates of location. Format is [longitude, latitude]
    date -- a python datetime object
    """
    (lng, lat) = coords
    DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    # A call is made to the API using the provided key
    APIkey = settings.FORECAST_IO_API_KEY
    physicalURL = "https://api.forecast.io/forecast/"+APIkey+"/"+str(lat)+","+str(lng)+","+datetime.isoformat(date)+"?units=ca"
    response = json.loads( urllib.request.urlopen(physicalURL).read() )

    c = response['currently']
    d = response['daily']['data'][0]

    sunrise = d.get('sunriseTime', None)
    sunset = d.get('sunsetTime', None)

    return {
        'summary': c.get('summary', ''),
        'sunrise_time': datetime.utcfromtimestamp(sunrise + response['offset']*60*60) if sunrise else None,
        'sunset_time': datetime.utcfromtimestamp(sunset + response['offset']*60*60) if sunset else None,
        'dawn': (sunrise-30*60 <= time.mktime(date.timetuple()) <= sunrise) if sunrise else False,
        'dusk': (sunset <= time.mktime(date.timetuple()) <= sunrise+30*60) if sunrise else False,
        'precip_intensity': c.get('precipIntensity', -1),
        'precip_probability': c.get('precipProbability', -1),
        'precip_type': c.get('precipType', ""),
        'temperature': c.get('temperature', -1),
        'black_ice_risk': c.get('temperature', 100) <= -18 or (c.get('precipIntensity', -1) > 0 and c.get('temperature', 100) <= 0),
        'wind_speed': c.get('windSpeed', -1),
        'wind_bearing': c.get('windBearing', -1),
        'wind_bearing_str': DIRECTIONS[int((c.get('windBearing') + 22.5) // 45 % 8)] if c.get('windBearing') else "",
        'visibility_km': c.get('visibility', -1), # if visibilityKM == 16.09 it is unlimited
    }
