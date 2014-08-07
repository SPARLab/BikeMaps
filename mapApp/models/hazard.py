from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


HAZARD_CHOICES = (
    ('Collision hazard', 'Collision hazard'),
    ('Falling hazard', 'Falling hazard'),
    ('Scraping/cutting hazard', 'Scraping/cutting hazard')
)

HAZARD_OBJECT_CHOICES = (
    ('Car/Truck', 'Car/Truck'),
    ('Vehicle door', 'Vehicle door'),
    ('Another cyclist', 'Another cyclist'),
    ('Curb', 'Curb'),
    ('Pedestrian/Person', 'Pedestrian/Person'),
    ('Train Tracks', 'Train Tracks'),
    ('Pothole', 'Pothole'),
    ('Lane divider', 'Lane divider'),
    ('Animal', 'Animal'),
    ('Sign/Post', 'Sign/Post'),
    ('Infrastructure needing repair', 'Infrastructure needing repair'),
    ('Dangerous infrastructure', 'Dangerous infrastructure')
)

AGE_CHOICES = (
    ("<19", "19 or under"),
    ("19-29","19 - 29"),
    ("30-39", "30 - 39"),
    ("40-49", "40 - 49"),
    ("50-59","50 - 59"),
    ("60-69","60 - 69"),
    (">70", "70 or over")
)


##########
# Hazard class.
# Class for Hazard Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Hazard(models.Model):
    ########### HAZARD FIELDS
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

    hazard_date = models.DateTimeField(
        'When did you notice the hazard?'
    )

    hazard = models.CharField(
        'What type of hazard was it?', 
        max_length=150, 
        choices=HAZARD_CHOICES
    )

    hazard_object = models.CharField(
        'If applicable, what sort of object presented the hazard?',
        max_length=100,
        choices=HAZARD_OBJECT_CHOICES,
        blank=True,
        null=True
    )
    ###########

    ############## PERSONAL DETAILS FIELDS
    # Personal details about the participant (all optional)
    age = models.CharField(
        'Please tell us which age category you fit into', 
        max_length=15, 
        choices=AGE_CHOICES, 
        blank=True, 
        null=True
    ) 
    sex = models.CharField(
        'Please select your sex', 
        max_length=6, 
        choices=(('M', 'Male'), ('F', 'Female')), 
        blank=True, 
        null=True
    )
    regular_cyclist = models.CharField(
        'Do you ride a bike often? (52+ times/year)',
        max_length=20, 
        choices=(('Y', 'Yes'), ('N', 'No'), ('I don\'t know', 'I don\'t know')), 
        blank=True, 
        null=True
    )
    #######################

    ########## DETAILS FIELDS
    hazard_detail = models.TextField(
        'Please give a brief description of the hazard', 
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
        return "Hazard"

    # For admin site 
    was_published_recently.admin_order_field = 'date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return unicode(self.hazard_date)

    class Meta:
        app_label = 'mapApp'