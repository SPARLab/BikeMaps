from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from point import Point

##########
# Hazard class.
# Class for Hazard Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Hazard(Point):
    HAZARD_CHOICES = (
        (_('Infrastructure'), (
                ('Curb', _('Curb')),
                ('Island', _('Island')),
                ('Train track', _('Train track')),
                ('Pothole', _('Pothole')),
                ('Road surface', _('Road surface')),
                ('Poor signage', _('Poor signage')),
                ('Speed limits', _('Speed limits')),
                ('Other infrastructure', _('Other infrastructure')),
            )
        ),
        (_('Other'), (
                ('Poor visibility', _('Poor visibility')),
                ('Parked car', _('Parked car')),
                ('Traffic flow', _('Traffic flow')),
                ('Driver behaviour', _('Driver behaviour')),
                ('Cyclist behaviour', _('Cyclist behaviour')),
                ('Pedestrian behaviour', _('Pedestrian behaviour')),
                ('Congestion', _('Congestion')),
                ('Broken glass', _('Broken glass on road')),
                ('Other', _('Other (Please describe)'))
            )
        )
    )

    BOOLEAN_CHOICES = (
        ('Y', _('Yes')),
        ('N', _('No')),
        ('I don\'t know', _('I don\'t know'))
    )

    point = models.OneToOneField(Point, parent_link=True)

    i_type = models.CharField(
        _('What type of hazard was it?'),
        max_length=150,
        choices=HAZARD_CHOICES
    )
    ###########

    ############## PERSONAL DETAILS FIELDS
    # Personal details about the participant (all optional)
    regular_cyclist = models.CharField(
        _('Do you bike at least once a week?'),
        max_length=30,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    #######################
