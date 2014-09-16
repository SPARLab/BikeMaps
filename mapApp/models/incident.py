from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from time import strftime, gmtime
from django.utils import timezone


############
# Response options for CharField data types
# 
INCIDENT_CHOICES = (
    ('Collision', (
            ('Collision with stationary object or vehicle', 'Collision with a stationary object or vehicle'),
            ('Collision with moving object or vehicle', 'Collision with a moving object or vehicle'),
        )
    ),
    ('Near miss', (
            ('Near collision with stationary object or vehicle', 'Near miss with a stationary object or vehicle'),
            ('Near collision with moving object or vehicle', 'Near miss with a moving object or vehicle'),
        )
    ),
    ('Fall', (
            ('Fall', 'Lost control and fell'),
        )
    )
)
INCIDENT_WITH_CHOICES = (
    ('Vehicle', (
            ('Vehicle, head on', 'Head on'),
            ('Vehicle, side', 'Side impact'),
            ('Vehicle, angle', 'Angle impact'),
            ('Vehicle, rear end', 'Rear end'),
            ('Vehicle, open door', 'Open vehicle door'),
        )
    ),
    ('Person/animal', (
            ('Another cyclist', 'Another cyclist'),
            ('Pedestrian', 'Pedestrian'),
            ('Animal', 'Animal'),
        )
    ),
    ('Infrastructure', (
            ('Curb', 'Curb'),
            ('Train Tracks', 'Train Tracks'),
            ('Pothole', 'Pothole'),
            ('Lane divider', 'Lane divider'),
            ('Sign/Post', 'Sign/Post'),
            ('Roadway', 'Roadway'),
        )
    ),
    ('Other', 'Other (please describe)')
)

INJURY_CHOICES = (
    ('Yes', (
            ('Injury, no treatment', 'Medical treatment not required'),
            ('Injury, saw family doctor', 'Saw a family doctor'),
            ('Injury, hospital emergency visit', 'Visited the hospital emergency dept.'),
            ('Injury, hospitalized', 'Overnight stay in hospital')
        )
    ),
    ('No', (
            ('No injury', 'No injury'),
        )
    )
)

PURPOSE_CHOICES = (
    ("Commute", "To/from work or school"), 
    ("Exercise or recreation", "Exercise or recreation"), 
    ("Social reason", "Social reason (e.g., movies, visit friends)"), 
    ("Personal business", "Personal business"),
    ("During work", "During work")
)
ROAD_COND_CHOICES = (
    ('Dry', 'Dry'),
    ('Wet','Wet'),
    ('Loose sand, gravel, or dirt', 'Loose sand, gravel, or dirt'),
    ('Icy','Icy'),
    ('Snowy','Snowy'),
    ('Don\'t remember', 'I don\'t remember')
)
SIGHTLINES_CHOICES = (
    ('No obstructions', 'No obstructions'),
    ('View obstructed', 'View obstructed'),
    ('Glare or reflection', 'Glare or reflection'),
    ('Obstruction on road', 'Obstruction on road'),
    ('Don\'t Remember', 'Don\'t Remember')
)
RIDING_ON_CHOICES = (
    ('Busy street', (
            ('Busy street bike lane', 'On a painted bike lane'),
            ('Busy street, no bike facilities', 'On road with no bike facilities')
        )
    ),
    ('Quiet street', (
            ('Quiet street bike lane', 'On a painted bike lane'),
            ('Quiet street, no bike facilities', 'On road with no bike facilities')
        )
    ),
    ('Not on the street', (
            ('Cycle track', 'On a physically separated bike lane (cycle track)'),
            ('Mixed use trail', 'On a mixed use trail'),
            ('Sidewalk', 'On the sidewalk'),
        )
    ),
    ('Don\'t remember', 'I don\'t remember')
)
LIGHTS_CHOICES = (
    ("NL", "No Lights"),
    ("FB", "Front and back lights"),
    ("F", "Front lights only"),
    ("B", "Back lights only"),
    ('Don\'t remember', 'I don\'t remember')

)
TERRAIN_CHOICES = (
    ('Uphill', 'Uphill'), 
    ('Downhill','Downhill'),
    ('Flat', 'Flat'),
    ('Don\'t remember', 'I don\'t remember')
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
CARDINAL_DIRECTIONS_CHOICES = (
    ('N','N'),
    ('NE','NE'),
    ('E','E'),
    ('SE','SE'),
    ('S','S'),
    ('SW','SW'),
    ('W','W'),
    ('NW', 'NW'),
    ('I don\'t know', 'I don\'t know')
)
TURNING_CHOICES = (
    ('Heading straight','Heading straight'),
    ('Turning left','Turning left'),
    ('Turning right','Turning right'),
    ('I don\'t remember', 'I don\'t remember')
)


##########
# Incident class.
# Main class for Incident Report. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
# Captures all data about the accident and environmental conditions when the bike incident occurred.
class Incident(models.Model):
    ########### INCIDENT FIELDS
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

    incident_date = models.DateTimeField(
        'When was the incident?'
    )

    incident = models.CharField(
        'What type of incident was it?', 
        max_length=150, 
        choices=INCIDENT_CHOICES
    )

    incident_with = models.CharField(
        'What sort of object did you collide or nearly collide with?',
        max_length=100,
        choices=INCIDENT_WITH_CHOICES
    )

    # Injury details (all optional)
    injury = models.CharField(
        'Were you injured?',
        max_length=50,
        choices= INJURY_CHOICES # Without this, field has 'Unknown' for None rather than the desired "---------"
    )

    trip_purpose = models.CharField(
        'What was the purpose of your trip?', 
        max_length=50, 
        choices=PURPOSE_CHOICES, 
        blank=True, 
        null=True
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
        max_length=50, 
        choices=BOOLEAN_CHOICES, 
        blank=True, 
        null=True
    )
    helmet = models.CharField(
        'Were you wearing a helmet?',
        max_length=50, 
        choices=BOOLEAN_CHOICES, 
        blank=True, 
        null=True
    )
    intoxicated = models.CharField(
    'Were you intoxicated?',
    max_length=50, 
    choices=BOOLEAN_CHOICES, 
    blank=True, 
    null=True
    )
    #######################

    ############### CONDITIONS FIELDS
    road_conditions = models.CharField(
        'What were the road conditions?', 
        max_length=50, 
        choices=ROAD_COND_CHOICES, 
        blank=True, 
        null=True
    )
    sightlines = models.CharField(
        'How were the sight lines?', 
        max_length=50, 
        choices=SIGHTLINES_CHOICES, 
        blank=True, 
        null=True
    )
    cars_on_roadside = models.CharField(
        'Were there cars parked on the roadside',
        max_length=50, 
        choices= BOOLEAN_CHOICES,
        blank=True, 
        null=True
    )
    riding_on = models.CharField(
        'Where were you riding your bike?', 
        max_length=50, 
        choices=RIDING_ON_CHOICES, 
        blank=True, 
        null=True
    )
    bike_lights = models.CharField(
        'Were you using bike lights?', 
        max_length=200, 
        choices=LIGHTS_CHOICES, 
        blank=True, 
        null=True
    )
    terrain = models.CharField(
        'What was the terrain like?', 
        max_length=50, 
        choices=TERRAIN_CHOICES, 
        blank=True, 
        null=True
    )
    direction = models.CharField(
        'What direction were you heading?', 
        max_length=50, 
        choices=CARDINAL_DIRECTIONS_CHOICES, 
        blank=True, 
        null=True
    )
    turning = models.CharField(
        'How were you moving?',
        max_length=50,
        choices=TURNING_CHOICES,
        blank=True,
        null=True
    )
    ########################

    ########## DETAILS FIELDS
    incident_detail = models.TextField(
        'Please give a brief description of the incident', 
        max_length=300, 
        blank=True, 
        null=True
    )

    # Placeholder for automatically added weather using an HTTP_GET from rss?
    weather = models.CharField(
        'What was the weather like?', 
        max_length=100, 
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
        for (kind, choices) in INCIDENT_CHOICES:
            for c in choices:
                if self.incident in c: return kind

    # For admin site 
    was_published_recently.admin_order_field = 'date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return unicode(self.incident_date)

    class Meta:
        app_label = 'mapApp'