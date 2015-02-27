from django.conf import settings
from django.contrib.gis.db import models
from point import Point

##########
# Official class.
# Class for storing official data. Contains fields that official data should be modified to fit as best as possible.
class Official(Point):
    point = models.OneToOneField(Point, parent_link=True)

    official_type = models.CharField(
        max_length=200,
    )
    data_source = models.CharField(
        max_length=200,
    )
    metadata = models.CharField(
        max_length=500,
    )
    who_added = models.CharField(
        max_length=100,
    )
