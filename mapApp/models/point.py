from django.conf import settings
from django.contrib.gis.db import models

import datetime
from time import strftime, gmtime
from django.utils import timezone

##########
# Hazard class.
# Class for Hazard Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Point(models.Model):
    TYPE_CHOICES = (
        ('collision', 'collision'),
        ('nearmiss', 'nearmiss'),
        ('theft', 'theft'),
        ('hazard', 'hazard'),
        ('official', 'official')
    )

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

    ########### POINT FIELDS
    report_date = models.DateTimeField(
        'Date reported',
        auto_now_add=True   # Date is set automatically when object created
    )
    # Spatial fields
    # Default CRS -> WGS84
    geom = models.PointField('Location')
    objects = models.GeoManager() # Required to conduct geographic queries

    # Personal details about the participant (all optional)
    date = models.DateTimeField(
        'When was the incident?',
        default=None
    )

    p_type = models.CharField(
        'Type of report',
        max_length=150,
        choices=TYPE_CHOICES,
    )

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

    details = models.TextField(
        'Please give a brief description of the incident',
        max_length=300,
        blank=True,
        null=True
    )

    # reverses latlngs and turns tuple of tuples into list of lists
    def latlngList(self):
        return list(self.geom)[::-1]

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.report_date < now

    # For admin site
    was_published_recently.admin_order_field = 'report_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return unicode(self.report_date)
