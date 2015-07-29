from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone

class AbstractPolygon(models.Model):
    """ Abstract class to define a polygon area associated with some user. Contains methods to return simplified coordinate list."""
    date = models.DateTimeField(
        'Date created',
        auto_now_add=True   # Date is set automatically when object created
    )
    # Spatial fields
    # Default CRS -> WGS84
    geom = models.PolygonField()
    objects = models.GeoManager() # Required to conduct geographic queries

    def latlngList(self):
        return list(list(latlng)[::-1] for latlng in self.geom[0])

    class Meta:
        abstract = True

class AlertArea(AbstractPolygon):
    """ Class that defines a polygon area of interest where the associated user receives push notifications, and alerts """
    email = models.EmailField(verbose_name="Current email")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))

    # toString()
    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        app_label = 'mapApp'


class AdministrativeArea(models.Model):
    """ Class that defines an area where a user has administrative power to mark infrastructure hazards as resolved """
    date = models.DateTimeField(
        'Date created',
        auto_now_add=True   # Date is set automatically when object created
    )
    # Spatial fields
    # Default CRS -> WGS84
    geom = models.MultiPolygonField()
    objects = models.GeoManager() # Required to conduct geographic queries


    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("users"), blank=True)
    description = models.CharField(max_length=200)

    def latlngList(self):
        return list(list(latlng)[::-1] for latlng in self.geom[0])

    # toString()
    def __unicode__(self):
        return unicode(self.description)

    class Meta:
        app_label = 'mapApp'
