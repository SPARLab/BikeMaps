from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


THEFT_CHOICES = (
    ('Bike', 'Bike'),
    ('Major bike component', 'Major bike component (e.g. tire, seat, handlebars, etc.)'),
    ('Minor bike component', 'Minor bike component (e.g. lights, topbar padding, bell, etc.)')
)

BOOLEAN_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

##########
# Theft class.
# Class for Theft Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Theft(models.Model):
    ########### THEFT FIELDS
    date = models.DateTimeField(
        'Date reported', 
        auto_now_add=True   # Date is set automatically when object created
    ) 
    # Spatial fields
    # Default CRS -> WGS84
    geom = models.PointField(
        'Location'
    )
    objects = models.GeoManager() # Required to conduct geographic queries

    theft_date = models.DateTimeField(
        'When did notice that you had been robbed?'
    )

    theft = models.CharField(
        'What was stolen?', 
        max_length=150, 
        choices=THEFT_CHOICES
    )

    locked = models.NullBooleanField(
        'Was your bike locked up?',
        choices=BOOLEAN_CHOICES
    )

    police_report = models.NullBooleanField(
        'Did you file a report with the police?',
        choices=BOOLEAN_CHOICES
    )
    ###########

    regular_cyclist = models.CharField(
        'Do you ride a bike often? (52+ times/year)',
        max_length=20, 
        choices=(('Y', 'Yes'), ('N', 'No'), ('I don\'t know', 'I don\'t know')), 
        blank=True, 
        null=True
    )
    #######################

    ########## DETAILS FIELDS
    theft_detail = models.TextField(
        'Please give a brief description about what happened.', 
        max_length=300, 
        blank=True, 
        null=True
    )
    ##############

    # reverses latlngs and turns tuple of tuples into list of lists
    def latlngList(self):
        return list(self.geom)[::-1]   

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.date < now

    def incident_type(self):
        return "Theft"

    # For admin site 
    was_published_recently.admin_order_field = 'date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return unicode(self.theft_date)

    class Meta:
        app_label = 'mapApp'