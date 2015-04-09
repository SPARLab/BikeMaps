from django.conf import settings
from django.contrib.gis.db import models
from point import Point

##########
# Hazard class.
# Class for Hazard Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Hazard(Point):
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
                ('Cyclist behaviour', 'Cyclist behaviour'),
                ('Pedestrian behaviour', 'Pedestrian behaviour'),
                ('Congestion', 'Congestion'),
                ('Broken glass', 'Broken glass on road'),
                ('Other', 'Other (Please describe)')
            )
        )
    )

    BOOLEAN_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('I don\'t know', 'I don\'t know')
    )

    point = models.OneToOneField(Point, parent_link=True)

    i_type = models.CharField(
        'What type of hazard was it?',
        max_length=150,
        choices=HAZARD_CHOICES
    )
    ###########

    ############## PERSONAL DETAILS FIELDS
    # Personal details about the participant (all optional)
    regular_cyclist = models.CharField(
        'Do you bike at least once a week?',
        max_length=30,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    #######################
