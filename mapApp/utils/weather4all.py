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
        semaphore.acquire()
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
        semaphore.release()
