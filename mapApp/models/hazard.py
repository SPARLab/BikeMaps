from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from time import strftime, gmtime
from django.utils import timezone


##########
# Hazard class.
# Class for Hazard Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Hazard(models.Model):
    HAZARD_CHOICES = (
        ('Infrastructure', (
                ('Curb', 'Curb'),
                ('Island', 'Island'),
                ('Train track', 'Train track'),
                ('Pothole', 'Pothole'),
                ('Road surface', 'Road surface'),
                ('Poor signage', 'Poor signage'),
                ('Speed limits', 'Speed limits'),
                ('Other infrastructure', 'Other infrastructure'),
            )
        ),
        ('Other', (
                ('Poor visibility', 'Poor visibility'),
                ('Parked car', 'Parked car'),
                ('Traffic flow', 'Traffic flow'),
                ('Driver behaviour', 'Driver behaviour'),
                ('Pedestrian behaviour', 'Pedestrian behaviour'),
                ('Congestion', 'Congestion'),
                ('Broken glass', 'Broken glass on road'),
                ('Other', 'Other (Please describe)')
            )
        )
    )

    # AGE_CHOICES = (("2001", "2001"), ("2000", "2000") ... ("1915", "1915")) Based on current year minus youngest age a person can report and year for 100-year-old
    YOUNGEST_AGE = 13
    youngestYear = int(strftime("%Y", gmtime())) - YOUNGEST_AGE
    AGE_CHOICES = []
    for y in xrange(100):
        AGE_CHOICES.append((str(youngestYear-y), str(youngestYear-y))) 

    from calendar import month_name as month
    MONTH_CHOICES = [(str(i+1), str(month[i+1])) for i in xrange(12)]
        
    SEX_CHOICES = (
        ('M', 'Male'), 
        ('F', 'Female'),
        ('Other', 'Other')
    )
    BOOLEAN_CHOICES = (
        ('Y', 'Yes'), 
        ('N', 'No'), 
        ('I don\'t know', 'I don\'t know')
)

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
    ###########

    ############## PERSONAL DETAILS FIELDS
    # Personal details about the participant (all optional)
    age = models.CharField(
        'What is your birth year?', 
        max_length=15, 
        choices=AGE_CHOICES, 
        blank=True, 
        null=True
    ) 
    birthmonth = models.CharField(
        'What is your birth month?', 
        max_length=15, 
        choices=MONTH_CHOICES, 
        blank=True, 
        null=True
    ) 
    sex = models.CharField(
        'Please select your sex', 
        max_length=10, 
        choices=SEX_CHOICES, 
        blank=True, 
        null=True
    )
    regular_cyclist = models.CharField(
        'Do you bike at least once a week?',
        max_length=30, 
        choices=BOOLEAN_CHOICES, 
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