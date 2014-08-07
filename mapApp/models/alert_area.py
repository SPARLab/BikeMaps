from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


##########
# AlertArea class.
# Main class for submitted routes.
class AlertArea(models.Model):
    date = models.DateTimeField(
        'Date created', 
        auto_now_add=True   # Date is set automatically when object created
    )

    # Spatial fields
    # Default CRS -> WGS84
    geom = models.PolygonField()
    objects = models.GeoManager() # Required to conduct geographic queries

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))
    email = models.EmailField(verbose_name="Current email")

    def latlngList(self):
        return list(list(latlng)[::-1] for latlng in self.geom[0]) 

    # toString()
    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        app_label = 'mapApp'