from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


INCIDENT, NEARMISS, FALL, HAZARD, THEFT, UNDEFINED = xrange(6)

ACTION_CHOICES = (
    (INCIDENT, _("Incident")),
    (NEARMISS, _("Near miss")),
    (FALL, _("Fall")),
    (HAZARD, _("Hazard")),
    (THEFT, _("Theft")),
    (UNDEFINED, _("Undefined"))
)

class AlertNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))

    date = models.DateTimeField(auto_now_add=True)
    action = models.IntegerField(choices=ACTION_CHOICES, default=UNDEFINED)
    is_read = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)

    # objects = AlertNotificationManager()

    class Meta:
        app_label = 'mapApp'
        unique_together = ('user', 'point')
        ordering = ['-date', ]
        verbose_name = _("alert notification")
        verbose_name_plural = _("alert notifications")

    def get_location(self):
        return self.point.geom

    @property
    def text_action(self):
        return ACTION_CHOICES[self.action][1]

    @property
    def is_incident(self):
        return self.action == INCIDENT

    @property
    def is_nearmiss(self):
        return self.action == NEARMISS

    @property
    def is_fall(self):
        return self.action == FALL

    @property
    def is_hazard(self):
        return self.action == HAZARD
    
    @property
    def is_theft(self):
        return self.action == THEFT

    def __unicode__(self):
        return "%s" % (self.user)

    class Meta:
        abstract= True
        app_label = 'mapApp'


class IncidentNotification(AlertNotification):
    point = models.ForeignKey('mapApp.Incident', related_name='+')

class HazardNotification(AlertNotification):
    point = models.ForeignKey('mapApp.Hazard', related_name='+')

class TheftNotification(AlertNotification):
    point = models.ForeignKey('mapApp.Theft', related_name='+')
