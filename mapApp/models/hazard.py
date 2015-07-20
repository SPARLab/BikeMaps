from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from point import Point
import datetime

##########
# Hazard class.
# Class for Hazard Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Hazard(Point):
    HAZARD_CATEGORIES = (
        ('infrastructure', _('Infrastructure')),
        ('environmental', _('Environmental')),
        ('human behaviour', _('Human Behaviour'))
    )

    HAZARD_CHOICES = (
        (_('Infrastructure'), (
                ('Curb', _('Curb')),
                ('Island', _('Island')),
                ('Train track', _('Train track')),
                ('Pothole', _('Pothole')),
                ('Road surface', _('Road surface')),
                ('Poor signage', _('Poor signage')),
                ('Speed limits', _('Speed limits')),
                ('Other infrastructure', _('Other (Please describe)')),
            )
        ),
        (_('Environmental'), (
                ('Poor visibility', _('Poor visibility')),
                ('Broken glass', _('Broken glass on road')),
                ('Wet leaves', _('Wet leaves on road')),
                ('Other', _('Other (Please describe)'))
            )
        ),
        (_('Human Behaviour'), (
                ('Poor visibility', _('Poor visibility')),
                ('Parked car', _('Parked car')),
                ('Traffic flow', _('Traffic flow')),
                ('Driver behaviour', _('Driver behaviour')),
                ('Cyclist behaviour', _('Cyclist behaviour')),
                ('Pedestrian behaviour', _('Pedestrian behaviour')),
                ('Congestion', _('Congestion')),
                ('Other', _('Other (Please describe)'))
            )
        ),
    )

    BOOLEAN_CHOICES = (
        ('Y', _('Yes')),
        ('N', _('No')),
        ('I don\'t know', _('I don\'t know'))
    )

    point = models.OneToOneField(Point, parent_link=True)

    hazard_category = models.CharField(
        _('Please select the category of hazard you are reporting:'),
        max_length=100,
        choices=HAZARD_CATEGORIES
    )

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

    ################ EXPIRES AUTOREMOVE FIELDS
    # These fields control if a hazard point has been removed from the map
    expires_date = models.DateTimeField(
        blank=True,
        null=True
    )
    hazard_fixed = models.BooleanField(
        _('Has this been fixed?'),
        default=False
    )
    hazard_fixed_date = models.DateTimeField(
        blank=True,
        null=True
    )

    td = datetime.timedelta
    _expires_delta = {
        'Curb': False,
        'Island': False,
        'Train track': False,
        'Pothole': False,
        'Road surface': False,
        'Poor signage': False,
        'Speed limits': False,
        'Other infrastructure': False,
        'Poor visibility': False,
        'Parked car': td(days=1),
        'Traffic flow': False,
        'Driver behaviour': False,
        'Cyclist behaviour': False,
        'Pedestrian behaviour': False,
        'Congestion': False,
        'Broken glass': td(weeks=2),
        'Wet leaves': td(weeks=1),
        'Other': False,
    }

    def is_expired(self):
        if self.expires_date:
            return (datetime.datetime.now() > self.expires_date)
        else:
            return self.hazard_fixed
    is_expired.boolean = True
    is_expired.short_description = 'Expired? (Hidden on map)'

    _editable_categories = {
        'infrastructure': True,
        'environmental': False,
        'human behaviour': False,
    }
    def is_editable(self):
        return self._editable_categories([self.hazard_category])
    is_editable.boolean = True
    is_editable.short_description = 'Editable? (Visibility can be change on CRD page)'

    def save(self, *args, **kwargs):
        if self._expires_delta[self.i_type]:
            self.expires_date = self.date + self._expires_delta[self.i_type]

        self.p_type = "hazard"
        super(Hazard, self).save(*args, **kwargs) # Call the "real" save() method.
