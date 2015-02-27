from django.conf import settings
from django.contrib.gis.db import models
from point import Point

import datetime
from time import strftime, gmtime
from django.utils import timezone

##########
# Official class.
# Class for storing official data. Contains fields that official data should be modified to fit as best as possible.
class Official(models.Model):
    geom = models.PointField('Location')
    objects = models.GeoManager() # Required to conduct geographic queries

    report_date = models.DateTimeField(
        auto_now_add=True   # Date is set automatically when object created
    )
    date = models.DateField(
        blank=True,
        null=True
    )
    time = models.TimeField(
        blank=True,
        null=True
    )

    p_type = models.CharField(
        default="official",
        max_length=150,
    )
    official_type = models.CharField(
        default="Vehicle collision",
        max_length=200,
    )
    data_source = models.CharField(
        max_length=200,
    )
    metadata = models.CharField(
        max_length=500,
    )
    details = models.TextField(
        max_length=300,
        blank=True,
        null=True
    )
