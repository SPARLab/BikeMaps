## TODO 
    # Implement location and route classes
    # Link response from incident type to instantiate collision/near-miss/theft/hazard object
    # Setup database for PostgreSQL/PostGIS, currently working off of development server


# OBJECT TREE
#
# Incident/
#         |
#         /Location
#         |
#         /Person
#         |
#         /Incident_type--/Collision--/Environment
#                         |           |
#                         |           /Route
#                         |           |  
#                         |           /Injury
#                         |
#                         |
#                         /Near_Miss--/Environment
#                         |           |
#                         |           /Route
#                         |
#                         |
#                         /Theft------/*some classes
#                         |
#                         |
#                         /Hazard-----/*some classes


from django.db import models

import datetime
from django.utils import timezone


##########
# Location class
# Primary class for storing location information. Should be reusable for theft and 
# hazards reports etc, which may be implemented later.
class Location(models.Model):
    pass
    #location = #SOME LOCATION FIELDS

    def __unicode__(self):
        return ""


#########
# Route class
# To be implemented class for storing route information either input manual (ie by tracing on map)
# or by uploading data from a mobile application (possible .gsx files)
class Route(models.Model):
    pass

    #rec-ride or commute?

    def __unicode__(self):
        return ""


##########
# Accident class.
# Main class for Incident Report. Contains required and non-required fields. Captures all data about the accident and environmental conditions when the bike incident occurred.
# Always associated with a Report object. Only some of these details are required.
INCIDENT_TYPE_CHOICES = (
    ('Collision', 'Collision'),
    ('Near miss', 'Near miss')#,
    #('Theft', 'Theft'),
    #('Hazard', 'Hazard')
)
class Incident(models.Model):
    # Required fields
    rep_date = models.DateTimeField('Date reported', auto_now_add=True)
    incident_date = models.DateTimeField('Date of incident')
    location = models.ForeignKey(Location, null=True, blank=True, default=None)

    incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPE_CHOICES)
    # Need to get type to invoke creation of Collision, Near_Miss, Theft, or Hazard object. But how?

    #Optional field
    #person = models.OneToOneField(Person, null=True, blank=True, default=None)

    def __unicode__(self):
        return unicode(self.incident_date)



ROAD_COND_CHOICES = (('D', 'Dry'),('W','Wet'),('I','Icy'),('S','Snowy'))
SIGHTLINES_CHOICES = (('Good', 'Good sightlines'), ('Poor', 'Poor Sightlines'), ('Don\'t Remember', 'Dont\'t Remember'))
BIKE_INFRASTRUCTURE_CHOICES = (('None', 'None'),('Painted bike lane', 'Off street bike path'), ('Other', 'Other'))
LIGHTS_CHOICES = (("NL", "No Lights"),("FB", "Front and back lights"),("F", "Front lights only"),("B", "Back lights only"))
TERRAIN_CHOICES = (('Uphill', 'Uphill'), ('Downhill','Downhill'),('Flat', 'Flat'),('Don\'t remember', 'I don\'t remember'))

class Environment(models.Model): #All fields optional
    road_conditions = models.CharField(max_length=5, choices=ROAD_COND_CHOICES)
    sightlines = models.CharField(max_length=20, choices=SIGHTLINES_CHOICES)
    cars_on_roadside = models.NullBooleanField('Cars parked on roadside')
    bike_infrastructure = models.CharField(max_length=20, choices=BIKE_INFRASTRUCTURE_CHOICES)
    bike_lights_used = models.CharField(max_length=200, choices=LIGHTS_CHOICES)
    terrain = models.CharField(max_length=20, choices=TERRAIN_CHOICES)
    helmet = models.NullBooleanField('helmet worn')

    def __unicode__(self):
        return "Environment"


class Injury(models.Model): #All fields optional
    medical_attention = models.NullBooleanField('Medical attention was required')
    description = models.TextField('Description of any injuries sustained', max_length=300)

    def __unicode__(self):
        return "Injury"


class Near_Miss(models.Model): #All fields optional
    environment = models.ForeignKey(Environment)
    route = models.ForeignKey(Route)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return "Near_Miss"


class Collision(models.Model): #All fields optional
    incident = models.OneToOneField(Incident)
    environment = models.ForeignKey(Environment)
    route = models.ForeignKey(Route)
    injury = models.ForeignKey(Injury)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return "Collision"

# class Theft(models.Model):
#     def __unicode__(self):
#         return ""

# class Hazard(models.Model):
#     def __unicode__(self):
#         return ""

############
# Person class
# Serves to capture any reported data about the individual involved in the accident.
# Person details are optionally reported by end users and should be nullable/optional.
class Person(models.Model):
    incident = models.OneToOneField(Incident, blank=True, null=True) 
    age = models.IntegerField(max_length=2, blank=True, null=True)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)

    def __unicode__(self):
        return ("%d%s" % (self.age, self.sex))