from mapApp.models import Incident, Weather
from mapApp.utils.weather import get_weather
import threading
import time

maxconnections = 1
semaphore = threading.Semaphore(maxconnections)

def run():
    """ Create Weather instances for all Incidents in the application database if they do not already exist
    """
    start_t = time.time()
    threads = []
    processed = 0

    for incident in Incident.objects.all():
        if hasattr(incident, 'weather'):
            continue
        else:
            # Create a new Weather instance using a non-blocking thread
            processed += 1
            thread = WeatherThread(incident)
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    end_t = time.time()
    print processed, "Incidents processed in", end_t - start_t, "s"

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
        semaphore.release()
