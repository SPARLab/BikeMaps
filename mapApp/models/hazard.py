from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from .point import Point
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
                ('Blind corner', _('Blind corner or turn')),
                ('Bike lane disappears', _('Bike lane disappears')),
                ('Vehicles enter exit', _('Vehicles entering/exiting roadway')),
                ('Dooring risk', _('Dooring risk zone')),
                ('Vehicle in bike lane', _('Vehicle use of bike lane')),
                ('Dangerous intersection', _('Dangerous intersection')),
                ('Dangerous vehicle left turn', _('Dangerous vehicle left turn')),
                ('Dangerous vehicle right turn', _('Dangerous vehicle right turn')),
                ('Sensor does not detect bikes', _('Sensor does not pick up bikes')),
                ('Steep hill', _('Steep hill - bike speed affected')),
                ('Narrow road', _('Narrow road')),
                ('Pedestrian conflict zone', _('Pedestrian conflict zone')),
                ('Other infrastructure', _('Other (Please describe)')),
            )
        ),
        (_('Environmental'), (
                ('Icy/Snowy', _('Icy/Snowy')),
                ('Poor visibility', _('Poor visibility (fog, snow, smoke etc.)')),
                ('Broken glass', _('Broken glass on road')),
                ('Wet leaves', _('Wet leaves on road')),
                ('Gravel rocks or debris', _('Gravel, rocks or debris on road/path')),
                ('Construction', _('Construction')),
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

    point = models.OneToOneField(Point,on_delete=models.CASCADE, parent_link=True)

    hazard_category = models.CharField(
        _('Please select the category of hazard you are reporting:'),
        max_length=100,
        choices=HAZARD_CATEGORIES,
        null=True,
        blank=True
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
        'Curb': td(weeks=52),
        'Island': td(weeks=52),
        'Train track': td(weeks=52),
        'Pothole': td(weeks=52),
        'Road surface': td(weeks=52),
        'Poor signage': td(weeks=52),
        'Speed limits': td(weeks=52),
        'Blind corner': td(weeks=52),
        'Bike lane disappears': td(weeks=52),
        'Vehicles enter exit': td(weeks=52),
        'Dooring risk': td(weeks=52),
        'Vehicle in bike lane': td(weeks=52),
        'Dangerous intersection': td(weeks=52),
        'Dangerous vehicle left turn': td(weeks=52),
        'Dangerous vehicle right turn': td(weeks=52),
        'Sensor does not detect bikes': td(weeks=52),
        'Steep hill': td(weeks=52),
        'Narrow road': td(weeks=52),
        'Pedestrian conflict zone': td(weeks=52),
        'Other infrastructure': td(weeks=52),
        'Icy/Snowy': td(weeks=1),
        'Poor visibility': td(weeks=1),
        'Broken glass': td(weeks=1),
        'Wet leaves': td(weeks=1),
        'Gravel rocks or debris': td(weeks=2),
        'Construction': td(weeks=4),
        'Other': td(weeks=4),
        'Parked car': td(days=1),
        'Traffic flow': td(weeks=52),
        'Driver behaviour': td(weeks=52),
        'Cyclist behaviour': td(weeks=52),
        'Pedestrian behaviour': td(weeks=52),
        'Congestion': td(weeks=52),
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
        return self._editable_categories[self.hazard_category]
    is_editable.boolean = True
    is_editable.short_description = 'Editable? (Visibility can be change on CRD page)'

    def save(self, *args, **kwargs):
        # Set expires time
        if self._expires_delta[self.i_type]:
            self.expires_date = self.date + self._expires_delta[self.i_type]

        # Set p_type
        self.p_type = "hazard"
        super(Hazard, self).save(*args, **kwargs) # Call the "real" save() method.
