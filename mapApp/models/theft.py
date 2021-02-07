from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from .point import Point

##########
# Theft class.
# Class for Theft Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Theft(Point):
    THEFT_CHOICES = (
        ('Bike (value < $1000)', _('Bike (value < $1000)')),
        ('Bike (value >= $1000)', _('Bike (value >= $1000)')),
        ('Major bike component', _('Major bike component (e.g. tire, seat, handlebars, etc.)')),
        ('Minor bike component', _('Minor bike component (e.g. lights, topbar padding, bell, etc.)'))
    )
    BOOLEAN_CHOICES = (
        ('Y', _('Yes')),
        ('N', _('No')),
        ('I don\'t know', _('I don\'t know'))
    )
    HOW_LOCKED_CHOICES = (
        (_('Yes'), (
                ('Frame locked', _('Frame locked')),
                ('Frame and tire locked', _('Frame and tire locked')),
                ('Frame and both tires locked', _('Frame and both tires locked')),
                ('Tire(s) locked', _('Tire(s) locked')),
              )
        ),
        (_('No'), (
                ('Not locked', _('Not locked')),
            )
        )
    )
    LOCK_CHOICES = (
        ('U-Lock', _('U-Lock')),
        ('Cable lock', _('Cable lock')),
        ('U-Lock and cable', _('U-Lock and cable')),
        ('Padlock', _('Padlock')),
        ('NA', _('Not locked')),
    )
    LOCKED_TO_CHOICES = (
        ('Outdoor bike rack', _('At an outdoor bike rack')),
        ('Indoor bike rack', _('At an indoor bike rack (e.g. parking garage, bike room)')),
        ('Bike locker', _('Inside a bike locker')),
        ('Street sign', _('Against street sign')),
        ('Fence/railing', _('Against a fence or railing')),
        ('Bench', _('Against a public bench')),
        ('Indoors/lobby', _('Inside a building/lobby')),
        ('Other', _('Other (please describe)'))
    )
    TRAFFIC_CHOICES = (
        ('Very High', _('Very heavy (pedestrians passing by in a nearly constant stream)')),
        ('High', _('Heavy (pedestrians passing by regularly)')),
        ('Medium', _('Moderate (irregular pedestrian with busy vehicle traffic)')),
        ('Low', _('Light (irregular pedestrian with light to moderate vehicle traffic)')),
        ('Very Low', _('Very light (little pedestrian and vehicle traffic)')),
        ('I don\'t know', _('I don\'t know'))
    )
    LIGHTING_CHOICES =  (
        ('Good', _('Well lit (e.g. bright daylight)')),
        ('Moderate', _('Moderately well lit (e.g. streetlights, parking garage)')),
        ('Poor', _('Poorly lit (e.g. night, unlit alleyway)')),
        ('I don\'t know', _('I don\'t know'))
    )

    #################### FIELDS
    point = models.OneToOneField(Point, parent_link=True)

    i_type = models.CharField(
        _('What was stolen?'),
        max_length=100,
        choices=THEFT_CHOICES
    )

    how_locked = models.CharField(
        _('Did you have your bike locked?'),
        max_length=100,
        choices=HOW_LOCKED_CHOICES
    )

    lock = models.CharField(
        _('What kind of lock were you using?'),
        max_length=100,
        choices=LOCK_CHOICES
    )

    locked_to = models.CharField(
        _('Where did you leave your bike?'),
        max_length=100,
        choices=LOCKED_TO_CHOICES
    )

    lighting = models.CharField(
        _('Which describes the lighting conditions where and when the theft occurred?'),
        max_length=100,
        choices=LIGHTING_CHOICES
    )

    traffic = models.CharField(
        _('Which best describes the traffic in the area where the theft occurred?'),
        max_length=100,
        choices=TRAFFIC_CHOICES
    )

    police_report = models.NullBooleanField(
        _('Did you file a report with the police?'),
        choices=((True, _('Yes')),(False, _('No')))
    )

    police_report_num = models.CharField(
        _('If you filed a police report, what is the report number?'),
        max_length=100,
        blank=True,
        null=True
    )

    insurance_claim = models.NullBooleanField(
        _('Did you file an insurance claim?'),
        choices=((True, _('Yes')),(False, _('No')))
    )

    insurance_claim_num = models.CharField(
        _('If you filed an insurance claim, what is the claim number?'),
        max_length=100,
        blank=True,
        null=True
    )
    ###########

    regular_cyclist = models.CharField(
        _('Do you bike at least once a week?'),
        max_length=30,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    #######################

    def save(self, *args, **kwargs):
        self.p_type = "theft"
        super(Theft, self).save(*args, **kwargs)
