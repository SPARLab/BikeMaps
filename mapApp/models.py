from django.contrib.gis.db import models

import datetime
from django.utils import timezone


############
# Response options for CharField data types
# 

# Collision
COLLISION_TYPES = [
    ('Single vehicle striking fixed object','Single vehicle striking fixed object (e.g., curb, sign, planter)'),
    ('Single vehicle striking a moving object', 'Single vehicle striking a moving object (e.g., pedestrian, inline skater, animal)'),
    ('Multi vehicle collision with moving vehicle', 'Multi vehicle collision with moving vehicle'),
    ('Multi vehicle collision with parked vehicle', 'Multi vehicle collision with parked vehicle'),
    ('Single vehicle losing control on roadway', 'Single vehicle losing control on roadway')
]

# Near miss
NEAR_MISS_TYPES = [
    ('Near collision with a fixed object', 'Near collision with a fixed object (e.g., curb, sign, planter)'),
    ('Near collision with a moving object', 'Near collision with a moving object (e.g., pedestrian, inline skater, animal)'),
    ('Near collision with a moving vehicle', 'Near collision with a moving vehicle'),
    ('Near collision with a parked vehicle', 'Near collision with a parked vehicle')
]

INCIDENT_WITH_CHOICES = [
    ('Car/Truck', 'Car/Truck'),
    ('Vehicle door', 'Vehicle door'),
    ('Another cyclist', 'Another cyclist'),
    ('Curb', 'Curb'),
    ('Pedestrian/Person', 'Pedestrian/Person'),
    ('Train Tracks', 'Train Tracks'),
    ('Pothole', 'Pothole'),
    ('Lane divider', 'Lane divider'),
    ('Animal', 'Animal'),
    ('Sign/Post', 'Sign/Post')
]

# Theft
THEFT_TYPES = [
    ('Theft','Theft'),
]

# Hazard
HAZARD_TYPES = [
    ('Hazard','Hazard')
]

INCIDENT_CHOICES = tuple(COLLISION_TYPES + NEAR_MISS_TYPES) #+ THEFT_TYPES + HAZARD_TYPES)

INJURY_CHOICES = [
    ('No injury', 'No injury'),
    ('Injury, not hospitalized', 'Injury, not hospitalized'),
    ('Injury, hospitalized', 'Injury, hospitalized')
]

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
    ('No', 'No'),
    ('View obstructed', 'View obstructed'),
    ('Glare or reflection', 'Glare or reflection'),
    ('Obstruction on road', 'Obstruction on road'),
    ('Don\'t Remember', 'Don\'t Remember')
)
RIDING_ON_CHOICES = (
    ('Painted bike lane', 'On a painted bike lane'),
    ('Off street bike path', 'On an off street bike path'),
    ('Street', 'On the road'),
    ('Sidewalk', 'On the sidewalk'),
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
AGE_CHOICES = (
    ("<19", "19 or under"),
    ("19-29","19 - 29"),
    ("30-39", "30 - 39"),
    ("40-49", "40 - 49"),
    ("50-59","50 - 59"),
    ("60-69","60 - 69"),
    (">70", "70 or over")
)

BOOLEAN_CHOICES = (
    (True, "Yes"),
    (False, "No")
)

FREQUENCY_CHOICES = (
    ("15+/wk", "15 or more"),
    ("10-14/wk", "10 - 14"),
    ("6-8/wk","6 - 8"),
    ("2-4/wk", "2 - 4"),
    ("<2/wk","less than twice a week"),
)

##########
# Incident class.
# Main class for Incident Report. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
# Captures all data about the accident and environmental conditions when the bike incident occurred.
class Incident(models.Model):
    ########### INCIDENT FIELDS
    report_date = models.DateTimeField(
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
        'What sort of object was the collision or near collision with?',
        max_length=100,
        choices=INCIDENT_WITH_CHOICES
    )

    # Injury details (all optional)
    injury = models.CharField(
        'Were you injured?',
        max_length=30,
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

    ########## DETAILS FIELDS
    incident_detail = models.TextField(
        'Please give a brief description of the incident', 
        max_length=300, 
        blank=True, 
        null=True
    )
    ##############

    ############## PERSONAL DETAILS FIELDS
    # Personal details about the participant (all optional)
    age = models.CharField(
        'Please tell us which age category you fit into', 
        max_length=15, 
        choices=AGE_CHOICES, 
        blank=True, 
        null=True
    ) 
    sex = models.CharField(
        'Please select your sex', 
        max_length=6, 
        choices=(('M', 'Male'), ('F', 'Female')), 
        blank=True, 
        null=True
    )
    regular_cyclist = models.CharField(
        'Do you ride a bike often? (52+ times/year)',
        max_length=20, 
        choices=(('Y', 'Yes'), ('N', 'No'), ('I don\'t know', 'I don\'t know')), 
        blank=True, 
        null=True
    )
    helmet = models.CharField(
        'Were you wearing a helmet?',
        max_length=20, 
        choices=(('Y', 'Yes'), ('N', 'No'), ('Don\'t remember', 'I don\'t remember')), 
        blank=True, 
        null=True
    )
    intoxicated = models.CharField(
    'Were you intoxicated?',
    max_length=20, 
    choices=(('Y', 'Yes'), ('N', 'No'), ('Don\'t remember', 'I don\'t remember')), 
    blank=True, 
    null=True
    )
    #######################

    ############### CONDITIONS FIELDS
    road_conditions = models.CharField(
        'What were the road conditions?', 
        max_length=30, 
        choices=ROAD_COND_CHOICES, 
        blank=True, 
        null=True
    )
    sightlines = models.CharField(
        'How were the sight lines?', 
        max_length=30, 
        choices=SIGHTLINES_CHOICES, 
        blank=True, 
        null=True
    )
    cars_on_roadside = models.CharField(
        'Were there cars parked on the roadside',
        max_length=30, 
        choices= (('Y', 'Yes'), ('N', 'No'), ('Don\'t remember', 'I don\'t remember')),
        blank=True, 
        null=True
    )
    riding_on = models.CharField(
        'Where were you riding your bike?', 
        max_length=20, 
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
        max_length=20, 
        choices=TERRAIN_CHOICES, 
        blank=True, 
        null=True
    )
    ########################


    # reverses latlngs and turns tuple of tuples into list of lists
    def latlngList(self):
        return list(self.geom)[::-1]
        

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.report_date < now

    was_published_recently.admin_order_field = 'report_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # A non elegant way to match up self.incident to a generalized incident_type string
    def incident_type(self):
        TYPES = [
            (COLLISION_TYPES, "Collision"), 
            (NEAR_MISS_TYPES, "Near miss"), 
            (THEFT_TYPES, "Theft"),
            (HAZARD_TYPES, "Hazard")
        ]

        for (TYPE, typStr) in TYPES: # Loop through tuples in each TYPE
            for tup in TYPE:
                 if self.incident in tup:
                    return typStr 
                    

    def __unicode__(self):
        return unicode(self.incident_date)


##########
# Routes class.
# Main class for submitted routes.
class Route(models.Model):
    # Spatial fields
    # Default CRS -> WGS84
    line = models.LineStringField()
    objects = models.GeoManager() # Required to conduct geographic queries

    report_date = models.DateTimeField(
    'Date reported', 
    auto_now_add=True   # Date is set automatically when object created
    ) 

    trip_purpose = models.CharField(
        'What is the reason you usually ride this route?', 
        max_length=50, 
        choices=PURPOSE_CHOICES, 
    )

    # Personal details about the participant (all optional)
    frequency = models.CharField(
        'How many times per week do you ride this route?', 
        max_length=15, 
        choices=FREQUENCY_CHOICES
    )

    # reverses latlngs and turns tuple of tuples into list of lists
    def latlngList(self):
        return list(list(latlng)[::-1] for latlng in self.line) 

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.report_date < now

    was_published_recently.admin_order_field = 'report_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    def __unicode__(self):
        return unicode(self.report_date)


##########
# AlertArea class.
# Main class for submitted routes.
# class AlertArea(models.Model):
#     # Spatial fields
#     # Default CRS -> WGS84
#     geofence = models.PolygonField()
#     objects = models.GeoManager() # Required to conduct geographic queries

#     user = models.ForeignKey()

#     def __unicode__(self):
#         # reverses latlngs and turns tuple of tuples into list of lists
#         return list(list(latlng)[::-1] for latlng in self.line) 
