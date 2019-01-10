from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from point import Point

import logging
logger = logging.getLogger(__name__)

##########
# Incident class.
# Main class for Incident Report. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
# Captures all data about the accident and environmental conditions when the bike incident occurred.
class Incident(Point):
    ############
    # Response options for CharField data types
    #
    INCIDENT_CHOICES = (
        (_('Collision'), (
                ('Collision with stationary object or vehicle', _('Collision with a stationary object or vehicle')),
                ('Collision with moving object or vehicle', _('Collision with a moving object or vehicle')),
            )
        ),
        (_('Near miss'), (
                ('Near collision with stationary object or vehicle', _('Near miss with a stationary object or vehicle')),
                ('Near collision with moving object or vehicle', _('Near miss with a moving object or vehicle')),
            )
        ),
        (_('Fall'), (
                ('Fall', _('Lost control and fell')),
            )
        )
    )
    INCIDENT_WITH_CHOICES = (
        (_('Vehicle'), (
                ('Vehicle, head on', _('Head on')),
                ('Vehicle, rear end', _('Rear end')),
                ('Vehicle, turning right', _('Turning right')),
                ('Vehicle, turning left', _('Turning left')),
                ('Vehicle, passing', _('Passing')),
                ('Vehicle, open door', _('Open vehicle door')),
            )
        ),
        (_('Person/animal'), (
                ('Another cyclist', _('Another cyclist')),
                ('Pedestrian', _('Pedestrian')),
                ('Animal', _('Animal')),
                ('E-scooter', _('E-scooter')),
            )
        ),
        (_('Infrastructure'), (
                ('Curb', _('Curb')),
                ('Train Tracks', _('Train Tracks')),
                ('Pothole', _('Pothole')),
                ('Lane divider', _('Lane divider')),
                ('Sign/Post', _('Sign/Post')),
                ('Roadway', _('Roadway')),
            )
        ),
        ('Other', _('Other (please describe)'))
    )

    INJURY_CHOICES = (
        (_('Yes'), (
                ('Injury, no treatment', _('Medical treatment not required')),
                ('Injury, saw family doctor', _('Saw a family doctor')),
                ('Injury, hospital emergency visit', _('Visited the hospital emergency dept.')),
                ('Injury, hospitalized', _('Overnight stay in hospital'))
            )
        ),
        (_('No'), (
                ('No injury', _('No injury')),
            )
        ),
        (_('Unknown'), (
            ('Unknown', _('I don\'t know')),
        )
         )
    )

    PURPOSE_CHOICES = (
        ('Commute', _('To/from work or school')),
        ('Exercise or recreation', _('Exercise or recreation')),
        ('Social reason', _('Social reason (e.g., movies, visit friends)')),
        ('Personal business', _('Personal business')),
        ('During work', _('During work'))
    )
    ROAD_COND_CHOICES = (
        ('Dry', _('Dry')),
        ('Wet', _('Wet')),
        ('Loose sand, gravel, or dirt', _('Loose sand, gravel, or dirt')),
        ('Icy', _('Icy')),
        ('Snowy', _('Snowy')),
        ('Don\'t remember', _('I don\'t remember'))
    )
    SIGHTLINES_CHOICES = (
        ('No obstructions', _('No obstructions')),
        ('View obstructed', _('View obstructed')),
        ('Glare or reflection', _('Glare or reflection')),
        ('Obstruction on road', _('Obstruction on road')),
        ('Don\'t Remember', _('Don\'t Remember'))
    )
    LIGHTS_CHOICES = (
        ('NL', _('No Lights')),
        ('FB', _('Front and back lights')),
        ('F', _('Front lights only')),
        ('B', _('Back lights only')),
        ('Don\'t remember', _('I don\'t remember'))

    )
    TERRAIN_CHOICES = (
        ('Uphill', _('Uphill')),
        ('Downhill', _('Downhill')),
        ('Flat', _('Flat')),
        ('Don\'t remember', _('I don\'t remember'))
    )
    BOOLEAN_CHOICES = (
        ('Y', _('Yes')),
        ('N', _('No')),
        ('I don\'t know', _('I don\'t know'))
    )
    CARDINAL_DIRECTIONS_CHOICES = (
        ('N', _('N')),
        ('NE', _('NE')),
        ('E', _('E')),
        ('SE', _('SE')),
        ('S', _('S')),
        ('SW', _('SW')),
        ('W', _('W')),
        ('NW', _('NW')),
        ('I don\'t know', _('I don\'t know'))
    )
    TURNING_CHOICES = (
        ('Heading straight', _('Heading straight')),
        ('Turning left', _('Turning left')),
        ('Turning right', _('Turning right')),
        ('I don\'t remember', _('I don\'t remember'))
    )
    INCIDENT_IMPACT_CHOICES = (
        ('None', _('No impact')),
        ('More careful', _('I\'m now more careful about where/when/how I ride')),
        ('Bike less', _('I bike less')),
        ('More careful and bike less', _('I\'m now more careful about where/when/how I ride AND I bike less')),
        ('Stopped biking', _('I haven\'t biked since')),
        ('Too soon', _('Too soon to say')),
        ('Witness', _('I was not directly involved'))
    )
    BICYCLE_TYPE_CHOICES = (
        ('Personal', _('Personal (my own bicycle or a friend\'s)')),
        ('Bike share', _('Bike share')),
        ('Bike rental', _('Bike rental')),
        ('E-scooter', _('E-scooter'))
    )
    EBIKE_CHOICES = (
        ('Yes', _('Yes')),
        ('No', _('No')),
        ('I don\'t know', _('I don\'t know'))
    )
    PERSONAL_INVOLVEMENT_CHOICES = (
        ('Yes', _('Yes, this happened to me')),
        ('No', _('No, I witnessed this happen to someone else'))
    )
    WITNESS_VEHICLE_CHOICES = (
        ('Bicycle', _('Bicycle')),
        ('E-scooter', _('E-scooter')),
        ('Pedestrian', _('I was a pedestrian')),
        ('Driving', _('I was driving')),
    )

    ############
    # FIELDS
    point = models.OneToOneField(Point, parent_link=True)

    i_type = models.CharField(
        _('What type of incident was it?'),
        max_length=150,
        choices=INCIDENT_CHOICES
    )
    incident_with = models.CharField(
        _('What sort of object did you collide or nearly collide with?'),
        max_length=100,
        choices=INCIDENT_WITH_CHOICES
    )
    injury = models.CharField(
        _('Were you injured?'),
        max_length=50,
        choices= INJURY_CHOICES # Without this, field has 'Unknown' for None rather than the desired '---------'
    )
    trip_purpose = models.CharField(
        _('What was the purpose of your trip?'),
        max_length=50,
        choices=PURPOSE_CHOICES,
        blank=True,
        null=True
    )
    regular_cyclist = models.CharField(
        _('Do you bike at least once a week?'),
        max_length=50,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    helmet = models.CharField(
        _('Were you wearing a helmet?'),
        max_length=50,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    intoxicated = models.CharField(
        _('Were you intoxicated?'),
        max_length=50,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    road_conditions = models.CharField(
        _('What were the road conditions?'),
        max_length=50,
        choices=ROAD_COND_CHOICES,
        blank=True,
        null=True
    )
    sightlines = models.CharField(
        _('How were the sight lines?'),
        max_length=50,
        choices=SIGHTLINES_CHOICES,
        blank=True,
        null=True
    )
    cars_on_roadside = models.CharField(
        _('Were there cars parked on the roadside'),
        max_length=50,
        choices= BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    bike_lights = models.CharField(
        _('Were you using bike lights?'),
        max_length=200,
        choices=LIGHTS_CHOICES,
        blank=True,
        null=True
    )
    terrain = models.CharField(
        _('What was the terrain like?'),
        max_length=50,
        choices=TERRAIN_CHOICES,
        blank=True,
        null=True
    )
    direction = models.CharField(
        _('What direction were you heading?'),
        max_length=50,
        choices=CARDINAL_DIRECTIONS_CHOICES,
        blank=True,
        null=True
    )
    turning = models.CharField(
        _('How were you moving?'),
        max_length=50,
        choices=TURNING_CHOICES,
        blank=True,
        null=True
    )
    intersection = models.CharField(
        _('Did the incident occur at an intersection?'),
        max_length=50,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    aggressive = models.CharField(
        _('Was the driver aggressive?'),
        max_length=50,
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True
    )
    impact = models.CharField(
        _('How did this incident impact your bicycling?'),
        max_length=50,
        choices=INCIDENT_IMPACT_CHOICES,
        null=True
    )

    bicycle_type = models.CharField(
        _('What type of bicycle were you riding?'),
        max_length=20,
        choices=BICYCLE_TYPE_CHOICES,
        blank=True,
        null=True
    )

    ebike = models.CharField(
        _('Did the incident involve a pedal-assist electric bike (eBike)?'),
        max_length=20,
        choices=EBIKE_CHOICES,
        blank=True,
        null=True
    )

    witness_vehicle = models.CharField(
        _('What were you riding?'),
        max_length=20,
        choices=WITNESS_VEHICLE_CHOICES,
        blank=True,
        null=True
    )

    personal_involvement = models.CharField(
        _('Were you directly involved in the incident?'),
        max_length=20,
        choices=PERSONAL_INVOLVEMENT_CHOICES
    )



    ##############

    def save(self, *args, **kwargs):
        self.p_type = self._getIncidentType()
        super(Incident, self).save(*args, **kwargs)

    def _getIncidentType(self):
        """Return "collision" or "nearmiss" pending on the type of incident a user selected."""
        usr_choice = self.i_type
        for t,choice in Incident.INCIDENT_CHOICES:
            for p,q in choice:
                if p == usr_choice:
                    if t == _("Near miss"):
                        return "nearmiss"
                    return "collision"
