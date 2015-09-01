from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from mapApp.models import Incident, Weather
from mapApp.utils.weather import get_weather

import threading

@receiver(post_save, sender=Incident)
def get_weather_data(sender, **kwargs):
    if(kwargs.get("created") and settings.FORECAST_IO_API_KEY != 'debug'):
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
            incident           = self.incident,
            summary            = data['summary'],
            sunrise_time       = data['sunrise_time'],
            sunset_time        = data['sunset_time'],
            dawn               = data['dawn'],
            dusk               = data['dusk'],
            precip_intensity   = data['precip_intensity'],
            precip_probability = data['precip_probability'],
            precip_type        = data['precip_type'],
            temperature        = data['temperature'],
            black_ice_risk     = data['black_ice_risk'],
            wind_speed         = data['wind_speed'],
            wind_bearing       = data['wind_bearing'],
            wind_bearing_str   = data['wind_bearing_str'],
            visibility_km      = data['visibility_km'],
        ).save()
