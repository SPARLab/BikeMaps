from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.db import models
from .point import Point

import datetime

##########
# New infrastructure class.
# Class for New Infrastructure reports. Contains all required, non-required, and spatial fields.
# Points in this class can only be added by administrators
class NewInfrastructure(Point):

    ############
    # FIELDS
    point = models.OneToOneField(Point, on_delete=models.CASCADE, parent_link=True)

    infra_type = models.CharField(
        _('What type of new infrastructure is it?'),
        max_length=150
    )

    dateAdded = models.DateTimeField(
        _('When was the new infrastructure added?'),
        default=None
    )

    infraDetails = models.TextField(
        _('Please give a brief description of the new infrastructure'),
        max_length=300,
        blank=True,
        null=True,
        default="Previously reported incidents and hazards in the area were reset."
    )

    ################ EXPIRES AUTOREMOVE FIELDS
    # This field controls if a new infrastructure point should be displayed on the map
    expires_date = models.DateTimeField(
        _('When should the new infrastructure icon expire?'),
        blank=True,
        null=True
    )

    def is_expired(self):
        if self.expires_date:
            return (datetime.datetime.now() > self.expires_date)
        else:
            return self.infrastructure_changed
    is_expired.boolean = True
    is_expired.short_description = 'Expired? (Hidden on map)'

    def save(self, *args, **kwargs):
        # Set p_type
        self.p_type = "newInfrastructure"
        self.date = self.dateAdded
        self.details = self.infraDetails

        super(NewInfrastructure, self).save(*args, **kwargs) # Call the "real" save() method.
