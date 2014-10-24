from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone



class AlertNotification(models.Model):
    INCIDENT, NEARMISS, HAZARD, THEFT, UNDEFINED = xrange(5)

    ACTION_CHOICES = (
        (INCIDENT, _("Incident")),
        (NEARMISS, _("Near miss")),
        (HAZARD, _("Hazard")),
        (THEFT, _("Theft")),
        (UNDEFINED, _("Undefined"))
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))

    date = models.DateTimeField(auto_now_add=True)
    action = models.IntegerField(choices=ACTION_CHOICES, default=UNDEFINED)
    is_read = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)

    # objects = AlertNotificationManager()


    def get_location(self):
        return self.point.geom

    @property
    def text_action(self):
        return ACTION_CHOICES[self.action][1]

    @property
    def is_incident(self):
        return self.action == self.INCIDENT

    @property
    def is_nearmiss(self):
        return self.action == self.NEARMISS

    @property
    def is_hazard(self):
        return self.action == self.HAZARD
    
    @property
    def is_theft(self):
        return self.action == self.THEFT

    def __unicode__(self):
        return "%s" % (self.user)

    class Meta:
        app_label = 'mapApp'
        unique_together = ('user', 'point')
        ordering = ['-date', ]
        verbose_name = _("alert notification")
        verbose_name_plural = _("alert notifications")

        abstract= True
        app_label = 'mapApp'


class IncidentNotification(AlertNotification):
    point = models.ForeignKey('mapApp.Incident', related_name='incidentNotification')

class HazardNotification(AlertNotification):
    point = models.ForeignKey('mapApp.Hazard', related_name='hazardNotification')

class TheftNotification(AlertNotification):
    point = models.ForeignKey('mapApp.Theft', related_name='theftNotification')
