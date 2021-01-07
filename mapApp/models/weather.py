from django.db import models
from mapApp.models import Incident

class Weather(models.Model):
    """ Container for all weather associated with an Incident via one-to-one field """

    incident = models.OneToOneField(Incident, primary_key=True)

    summary = models.CharField("Summary", max_length=250)
    sunrise_time = models.DateTimeField("Sunrise time")
    sunset_time = models.DateTimeField("Sunset time")
    dawn = models.BooleanField("The accident occurred at dawn")
    dusk = models.BooleanField("The accident occurred at dusk")
    precip_intensity = models.FloatField("Precipitation intensity (mm/h)")
    precip_probability = models.FloatField("Precipitation probability")
    precip_type = models.CharField("Type of precipitation", max_length=50)
    temperature = models.FloatField("Temperature (C)")
    black_ice_risk = models.BooleanField("Black ice risk present")
    wind_speed = models.FloatField("Wind speed (km/h)")
    wind_bearing = models.FloatField("Wind bearing (deg)")
    wind_bearing_str = models.CharField("Wind bearing", max_length=5)
    visibility_km = models.FloatField("Visibility (km)")

    # toString()
    def __unicode__(self):
        return str(self.summary)

    class Meta:
        verbose_name = "Weather"
        verbose_name_plural = "Weather"
