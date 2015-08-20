from django.db import models
from mapApp.models import Incident

class Weather(models.Model):
    """ Container for all weather associated with an Incident via one-to-one field """

    incident = models.OneToOneField(Incident, primary_key=True)

    temperature_c = models.FloatField()
    visibility_km = models.FloatField()
    windspeed_kmh = models.FloatField()
    precip_mmh = models.FloatField()
    precip_prob = models.FloatField()
    sunrise_time = models.DateTimeField()
    sunset_time = models.DateTimeField()
    dawn = models.BooleanField()
    dusk = models.BooleanField()
    wind_dir_deg = models.FloatField()
    wind_dir_str = models.CharField(max_length=5)
    black_ice_risk = models.BooleanField()
    summary = models.CharField(max_length=250)

    # toString()
    def __unicode__(self):
        return unicode(self.summary)
