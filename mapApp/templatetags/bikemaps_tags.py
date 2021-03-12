from django import template
register = template.Library()

from mapApp.models import IncidentNotification, HazardNotification, TheftNotification, Point, AlertArea
import datetime

import logging
logger = logging.getLogger(__name__)


@register.simple_tag()
def has_alerts(user):
    return (
        IncidentNotification.objects.filter(user=user).filter(is_read=False).exists()\
        or \
        HazardNotification.objects.filter(user=user).filter(is_read=False).exists()\
        or \
        TheftNotification.objects.filter(user=user).filter(is_read=False).exists()
    )


@register.simple_tag()
def reports_this_week(user):
    now = datetime.datetime.now()
    lastweek = now - datetime.timedelta(days=7)

    polys = AlertArea.objects.filter(user=user)
    points = Point.objects.filter(date__range=[lastweek, now])

    if not points.exists():
        return False

    for poly in polys:
        if points.filter(geom__intersects=poly.geom).exists():
            return True
    return False
