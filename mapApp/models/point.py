from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from django.urls import reverse
from django.db.models import Manager as GeoManager


import datetime
from time import strftime, gmtime
from .gender import Gender

##########
# Point class.
# Serves as abstract model inheritance class for all user generated map data points


class Point(models.Model):
    TYPE_CHOICES = (
        ('collision', _('collision')),
        ('nearmiss', _('nearmiss')),
        ('theft', _('theft')),
        ('hazard', _('hazard')),
        ('newInfrastructure', _('newInfrastructure')),
        ('official', _('official'))
    )

    YOUNGEST_AGE = 13
    youngestYear = int(strftime("%Y", gmtime())) - YOUNGEST_AGE
    AGE_CHOICES = []
    for y in range(100):
        AGE_CHOICES.append((str(youngestYear-y), str(youngestYear-y)))

    from calendar import month_name as month
    MONTH_CHOICES = (
        ('1', _('January')),
        ('2', _('February')),
        ('3', _('March')),
        ('4', _('April')),
        ('5', _('May')),
        ('6', _('June')),
        ('7', _('July')),
        ('8', _('August')),
        ('9', _('September')),
        ('10', _('October')),
        ('11', _('November')),
        ('12', _('December'))
    )

    SEX_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('Other', _('Other'))
    )

    SOURCE_CHOICES = (
        ('BikeMaps team', _('Directly from the BikeMaps.org team')),
        ('BikeMaps swag', _(
            'BikeMaps.org swag (e.g., seat cover, water bottle, etc.) without meeting the team')),
        ('Traditional media', _('Traditional media (newspaper, TV, radio)')),
        ('Another website', _('Link from another website')),
        ('Word of mouth', _('Word of mouth')),
        ('Social media', _('Social media (e.g., Twitter, Instagram, Facebook)')),
        ('Other', _('Other')),
        ('Don\'t remember', _('I don\'t remember'))
    )

    # POINT FIELDS
    report_date = models.DateTimeField(
        _('Date reported'),
        auto_now_add=True   # Date is set automatically when object created
    )
    # Spatial fields
    # Default CRS -> WGS84
    geom = models.PointField(_('Location'))
    objects = GeoManager()  # Required to conduct geographic queries

    date = models.DateTimeField(
        _('When was the incident?'),
        default=None
    )

    p_type = models.CharField(
        _('Type of report'),
        max_length=150,
        choices=TYPE_CHOICES
    )

    # Personal details about the participant (all optional)
    age = models.CharField(
        _('What is your birth year?'),
        max_length=15,
        choices=AGE_CHOICES,
        blank=True,
        null=True
    )
    birthmonth = models.CharField(
        _('What is your birth month?'),
        max_length=15,
        choices=MONTH_CHOICES,
        blank=True,
        null=True
    )

    sex = models.CharField(
        _('Please select your sex'),
        max_length=10,
        choices=SEX_CHOICES,
        blank=True,
        null=True
    )

    gender = models.ManyToManyField(
        Gender,
        blank=True,
        null=True
    )

    gender_additional = models.TextField(
        _("If you selected 'another option', optionally describe here:"),
        max_length=100,
        default='',
        blank=True,
        null=True
    )

    details = models.TextField(
        _('Please give a brief description of the incident'),
        max_length=500,
        default=None,
        blank=True,
        null=True
    )

    source = models.CharField(
        _('Where did you first find out about BikeMaps.org?'),
        max_length=20,
        choices=SOURCE_CHOICES,
        blank=True,
        null=True
    )

    infrastructure_changed = models.BooleanField(
        _('Has the infrastructure been changed?'),
        default=False
    )
    infrastructure_changed_date = models.DateTimeField(
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse('mapApp:index', kwargs={'lat': str(self.latlngList()[0]), 'lng': str(self.latlngList()[1]), 'zoom': str(18)})

    # reverses latlngs and turns tuple of tuples into list of lists
    def latlngList(self):
        return list(self.geom)[::-1]

    def was_published_recently(self):
        now = datetime.datetime.now()
        return now - datetime.timedelta(weeks=1) <= self.report_date <= now

    # For admin site
    was_published_recently.admin_order_field = 'report_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return str(self.report_date)
