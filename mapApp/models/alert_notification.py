from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


INCIDENT, NEARMISS, UNDEFINED = xrange(3)

ACTION_CHOICES = (
    (INCIDENT, _("Incident")),
    (NEARMISS, _("Near miss")),
    (UNDEFINED, _("Undefined"))
)

class AlertNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))
    point = models.ForeignKey('mapApp.Incident', related_name='+')

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

    def __unicode__(self):
        return "%s" % (self.user)

    class Meta:
        app_label = 'mapApp'