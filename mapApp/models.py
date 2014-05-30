from django.contrib.gis.db import models


import datetime
from django.utils import timezone


############
# Response options for CharField data types
# 

# Collision
COLLISION_TYPES = [
    ('Vehicle collision', 'Collision with a motor vehicle'),
    ('Vehicle door collision','Collision with an open vehicle door'),
    ('Surface feature collision','Collision with a surface feature (e.g., train tracks, pothole, rock)'),
    ('Infrastructure collision','Collision with route infrastructure (e.g., post, curb, planter, lane divider)'),
    ('Person/animal collision','Collision with other person or animal (i.e., cyclist, pedestrian, skater, dog)'),
    ('Fall trying to avoid collision','Fall while trying to avoid a collision'),
    ('Fall in other circumstances','Fall in other circumstances'),
]

# Near miss
NEAR_MISS_TYPES = [
    ('Vehicle near collision', 'Near collision with a motor vehicle'),
    ('Vehicle door near collision','Near collision with an open vehicle door'),
    ('Surface feature near collision','Near collision with a surface feature (e.g., train tracks, pothole, rock)'),
    ('Infrastructure near collision','Near collision with route infrastructure (e.g., post, curb, planter, lane divider)'),
    ('Person/animal near collision','Near collision with other person or animal (i.e., cyclist, pedestrian, skater, dog)'),
    ('Near fall trying to avoid collision','Near fall while trying to avoid a collisioin'),
    ('Near fall in other circumstances','Near fall due to other circumstances'),
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


PURPOSE_CHOICES = (
    ("Commute", "To/from work or school"), 
    ("Exercise or recreation", "Exercise or recreation"), 
    ("Social reason", "Social reason (e.g., movies, visit friends)"), 
    ("Personal business", "Personal business"),
    ("During work", "During work")
)
TIMING_CHOICES = ( # NOT USED CURRENTLY
    ("Dawn", "Dawn"),
    ("Morning", "Morning"),
    ("Midday", "Midday"),
    ("Dusk", "Dusk/evening"),
    ("Night", "Night")
) 
DISTANCE_CHOICES = ( # NOT USED CURRENTLY
    ("<2", "<2"),
    ("2 - <5", "2 - <5"),
    ("5 - <10", "5 - <10"),
    ("10 - <20", "10 - <20"),
    ("20+")
) # in (km)
ROAD_COND_CHOICES = (
    ('Dry', 'Dry'),
    ('Wet','Wet'),
    ('Icy','Icy'),
    ('Snowy','Snowy')
)
SIGHTLINES_CHOICES = (
    ('Good', 'Good'),
    ('Poor', 'Poor'),
    ('Don\'t Remember', 'Don\'t Remember')
)
BIKE_INFRASTRUCTURE_CHOICES = (
    ('None', 'None'),
    ('Painted bike lane', 'Painted bike lane'),
    ('Off street bike path', 'Off street bike path'),
    ('Other', 'Other') # Necessary? Ask Trisalyn
)
LIGHTS_CHOICES = (
    ("NL", "No Lights"),
    ("FB", "Front and back lights"),
    ("F", "Front lights only"),
    ("B", "Back lights only")
)
TERRAIN_CHOICES = (
    ('Uphill', 'Uphill'), 
    ('Downhill','Downhill'),
    ('Flat', 'Flat'),
    ('Don\'t remember', 'I don\'t remember')
)
AGE_CHOICES = (
    ("<19", "19 or under"),
    ("19-29","19-29"),
    ("30-39", "30-39"),
    ("40-49", "40-49"),
    ("50-59","50-59"),
    ("60-69","60-69"),
    (">70", "70 or over")
)

BOOLEAN_CHOICES = (
    (True, "Yes"),
    (False, "No")
)

##########
# Incident class.
# Main class for Incident Report. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
# Captures all data about the accident and environmental conditions when the bike incident occurred.
class Incident(models.Model):
    # Required fields
    report_date = models.DateTimeField(
        'Date reported', 
        auto_now_add=True   # Date is set automatically when object created
    ) 
    incident_date = models.DateTimeField(
        'When was the incident?'
    )

    incident = models.CharField(
        'What happened?', 
        max_length=100, 
        choices=INCIDENT_CHOICES
    )
    incident_detail = models.TextField(
        'Please give a brief description of the incident', 
        max_length=300, 
        blank=True, 
        null=True
    )

    # Spatial fields
    # Default CRS -> WGS84
    point = models.PointField(
        'Location'
    )
    objects = models.GeoManager() # Required to conduct geographic queries


    #### Move following to new models?
    # Trip and environment details (all optional)
    trip_purpose = models.CharField(
        'What was the purpose of your trip?', 
        max_length=50, 
        choices=PURPOSE_CHOICES, 
        blank=True, 
        null=True
    )
    road_conditions = models.CharField(
        'What were the road conditions?', 
        max_length=5, 
        choices=ROAD_COND_CHOICES, 
        blank=True, 
        null=True
    )
    sightlines = models.CharField(
        'How were the sight lines?', 
        max_length=20, 
        choices=SIGHTLINES_CHOICES, 
        blank=True, 
        null=True
    )
    cars_on_roadside = models.NullBooleanField(
        'Were there cars parked on the roadside',
        choices= BOOLEAN_CHOICES # Without this, field has 'Unknown' for None rather than the desired "---------"
    )
    bike_infrastructure = models.CharField(
        'What kind of bike infrastructure was there?', 
        max_length=20, 
        choices=BIKE_INFRASTRUCTURE_CHOICES, 
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
    helmet = models.NullBooleanField(
        'Were you wearing a helmet?',
        choices= BOOLEAN_CHOICES # Without this, field has 'Unknown' for None rather than the desired "---------"
    )

    # Injury details (all optional)
    injury = models.NullBooleanField(
        'Did you require medical attention?',
        choices= BOOLEAN_CHOICES # Without this, field has 'Unknown' for None rather than the desired "---------"
    )
    injury_detail = models.TextField(
        'Describe any injuries you sustained', 
        max_length=300, 
        blank=True, 
        null=True
    )

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
        max_length=1, 
        choices=(('M', 'Male'), ('F', 'Female')), 
        blank=True, 
        null=True
    )
    regular_cyclist = models.NullBooleanField(
        'Do you ride a bike often? (52+ times/year)',
        choices= BOOLEAN_CHOICES # Without this, field has 'Unknown' for None rather than the desired "---------"
    )


    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.report_date < now

    was_published_recently.admin_order_field = 'report_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # A non elegant way to mach up self.incident to a generalized incident_type string
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