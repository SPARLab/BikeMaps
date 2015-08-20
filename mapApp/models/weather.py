from django.db import models
from mapApp.models import Incident

class Weather(models.Model):
    """ Container for all weather associated with an Incident via one-to-one field """

    incident = models.OneToOneField(Incident, primary_key=True)

    temperature_c = models.FloatField("Temperature (C)")
    visibility_km = models.FloatField("Visibility (km)")
    windspeed_kmh = models.FloatField("Wind speed (km/h)")
    precip_mmh = models.FloatField("Precipitation intensity (mm/h)")
    precip_prob = models.FloatField("Precipitation probability")
    sunrise_time = models.DateTimeField("Sunrise time")
    sunset_time = models.DateTimeField("Sunset time")
    dawn = models.BooleanField("The accident occurred at dawn")
    dusk = models.BooleanField("The accident occurred at dusk")
    wind_dir_deg = models.FloatField("Wind origin (deg)")
    wind_dir_str = models.CharField("Wind origin", max_length=5)
    black_ice_risk = models.BooleanField("Black ice risk present")
    summary = models.CharField("Summary", max_length=250)

    # toString()
    def __unicode__(self):
        return unicode(self.summary)

    class Meta:
        verbose_name = "Weather"
        verbose_name_plural = "Weather"
