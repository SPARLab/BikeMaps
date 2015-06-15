from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from point import Point


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
                ('Vehicle, side', _('Side impact')),
                ('Vehicle, angle', _('Angle impact')),
                ('Vehicle, rear end', _('Rear end')),
                ('Vehicle, open door', _('Open vehicle door')),
            )
        ),
        (_('Person/animal'), (
                ('Another cyclist', _('Another cyclist')),
                ('Pedestrian', _('Pedestrian')),
                ('Animal', _('Animal')),
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
    RIDING_ON_CHOICES = (
        (_('Busy street'), (
                ('Busy street bike lane', _('On a painted bike lane')),
                ('Busy street, no bike facilities', _('On road with no bike facilities'))
            )
        ),
        (_('Quiet street'), (
                ('Quiet street bike lane', _('On a painted bike lane')),
                ('Quiet street, no bike facilities', _('On road with no bike facilities'))
            )
        ),
        (_('Not on the street'), (
                ('Cycle track', _('On a physically separated bike lane (cycle track)')),
                ('Mixed use trail', _('On a mixed use trail')),
                ('Sidewalk', _('On the sidewalk')),
            )
        ),
        ('Don\'t remember', _('I don\'t remember'))
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
    riding_on = models.CharField(
        _('Where were you riding your bike?'),
        max_length=50,
        choices=RIDING_ON_CHOICES,
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
    # Placeholder for automatically added weather using an HTTP_GET from rss?
    weather = models.CharField(
        _('What was the weather like?'),
        max_length=100,
        blank=True,
        null=True
    )
    ##############
