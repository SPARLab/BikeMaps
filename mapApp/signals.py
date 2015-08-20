from django.db.models.signals import post_save
from django.dispatch import receiver

from mapApp.models import Incident, Weather
from mapApp.utils.weather import get_weather

import threading

import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Incident)
def get_weather_data(sender, **kwargs):
    if(kwargs.get("created")):
        incident = kwargs.get("instance")

        # Create a new Weather instance using a non-blocking thread
        thread = WeatherThread(incident)
        thread.start()

class WeatherThread(threading.Thread):
    def __init__(self, incident):
        self.incident = incident
        super(WeatherThread, self).__init__()

    def run(self):
        data = get_weather(self.incident.geom, self.incident.date)
        Weather(
            incident        = self.incident,
            temperature_c   = data['temperatureC'],
            visibility_km   = data['visibilityKM'],
            windspeed_kmh   = data['windSpeedKMH'],
            precip_mmh      = data['precipMMH'],
            precip_prob     = data['precipProb'],
            sunrise_time    = data['sunriseTime'],
            sunset_time     = data['sunsetTime'],
            dawn            = data['dawn'],
            dusk            = data['dusk'],
            wind_dir_deg    = data['windDirDeg'],
            wind_dir_str    = data['windDirStr'],
            black_ice_risk  = data['blackIceRisk'],
            summary         = data['summary']
        ).save()
