from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


FREQUENCY_CHOICES = (
    ("15+/wk", "15 or more"),
    ("10-14/wk", "10 - 14"),
    ("6-8/wk","6 - 8"),
    ("2-4/wk", "2 - 4"),
    ("<2/wk","less than twice a week"),
)

PURPOSE_CHOICES = (
    ("Commute", "To/from work or school"), 
    ("Exercise or recreation", "Exercise or recreation"), 
    ("Social reason", "Social reason (e.g., movies, visit friends)"), 
    ("Personal business", "Personal business"),
    ("During work", "During work")
)

##########
# Routes class.
# Main class for submitted routes.
class Route(models.Model):
    # Spatial fields
    # Default CRS -> WGS84
    geom = models.LineStringField()
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
        return list(list(latlng)[::-1] for latlng in self.geom) 

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.report_date < now

    # For admin site
    was_published_recently.admin_order_field = 'report_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return unicode(self.report_date)

    class Meta:
        app_label = 'mapApp'