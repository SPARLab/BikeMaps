from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


THEFT_CHOICES = (
    ('Bike (value < $1000)', 'Bike (value < $1000)'),
    ('Bike (value >= $1000)', 'Bike (value >= $1000)'),
    ('Major bike component', 'Major bike component (e.g. tire, seat, handlebars, etc.)'),
    ('Minor bike component', 'Minor bike component (e.g. lights, topbar padding, bell, etc.)')
)
BOOLEAN_CHOICES = (
    ('Y', 'Yes'), 
    ('N', 'No'), 
    ('I don\'t know', 'I don\'t know')
)
HOW_LOCKED_CHOICES = (
    ('Yes', (
            ('Frame locked', 'Frame locked'),
            ('Frame and tire locked', 'Frame and tire locked'),
            ('Frame and both tires locked', 'Frame and both tires locked'),
            ('Tire(s) locked', 'Tire(s) locked'),
          )
    ),
    ('No', (
            ('Not locked', 'Not locked'),
        )
    )
)
LOCK_CHOICES = (
    ('U-Lock', 'U-Lock'),
    ('Cable lock', 'Cable lock'),
    ('U-Lock and cable', 'U-Lock and cable'),
    ('Padlock', 'Padlock'),
    ('NA', 'Not locked'),
)
LOCKED_TO_CHOICES = (
    ('Outdoor bike rack', 'At an outdoor bike rack'),
    ('Indoor bike rack', 'At an indoor bike rack (e.g. parking garage, bike room)'),
    ('Bike locker', 'Inside a bike locker'),
    ('Street sign', 'Against street sign'),
    ('Fence/railing', 'Against a fence or railing'),
    ('Bench', 'Against a public bench'),
    ('Indoors/lobby', 'Inside a building/lobby'),
    ('Other', 'Other (please describe)')
)
TRAFFIC_CHOICES = (
    ('Very High', 'Very heavy (pedestrians passing by in a nearly constant stream)'),
    ('High', 'Heavy (pedestrians passing by regularly)'),
    ('Medium', 'Moderate (irregular pedestrian with busy vehicle traffic)'),
    ('Low', 'Light (irregular pedestrian with light to moderate vehicle traffic)'),
    ('Very Low', 'Very light (little pedestrian and vehicle traffic)'),
    ('I don\'t know', 'I don\'t know')
)
LIGHTING_CHOICES =  (
    ('Good', 'Well lit (e.g. bright daylight)'),
    ('Moderate', 'Moderately well lit (e.g. streetlights, parking garage)'),
    ('Poor', 'Poorly lit (e.g. night, unlit alleyway)'),
    ('I don\'t know', 'I don\'t know')
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
        max_length=100, 
        choices=THEFT_CHOICES
    )

    how_locked = models.CharField(
        'Did you have your bike locked?',
        max_length=100,
        choices=HOW_LOCKED_CHOICES
    )

    lock = models.CharField(
        'What kind of lock were you using?',
        max_length=100,
        choices=LOCK_CHOICES
    )

    locked_to = models.CharField(
        'Where did you leave your bike?',
        max_length=100,
        choices=LOCKED_TO_CHOICES
    )

    lighting = models.CharField(
        'Which describes the lighting conditions where and when the theft occurred?',
        max_length=100,
        choices=LIGHTING_CHOICES
    )

    traffic = models.CharField(
        'Which best describes the traffic in the area where the theft occurred?',
        max_length=100,
        choices=TRAFFIC_CHOICES
    )

    police_report = models.NullBooleanField(
        'Did you file a report with the police?',
        choices=((True, 'Yes'),(False, 'No'))
    )

    insurance_claim = models.NullBooleanField(
        'Did you file an insurance claim?',
        choices=((True, 'Yes'),(False, 'No'))
    )
    ###########

    regular_cyclist = models.CharField(
        'Do you bike at least once a week?',
        max_length=30, 
        choices=BOOLEAN_CHOICES, 
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