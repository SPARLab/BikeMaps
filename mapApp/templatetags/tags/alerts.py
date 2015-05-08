#-*- coding: utf-8 -*-

from . import register

from spirit.models.topic_notification import TopicNotification
from mapApp.models import IncidentNotification, HazardNotification, TheftNotification, Point, AlertArea
import datetime

import logging
logger = logging.getLogger(__name__)

@register.assignment_tag()
def has_alerts(user):
	return (
		IncidentNotification.objects.filter(user=user).filter(is_read=False).exists()\
		or \
		HazardNotification.objects.filter(user=user).filter(is_read=False).exists()\
		or \
		TheftNotification.objects.filter(user=user).filter(is_read=False).exists()\
		or \
		TopicNotification.objects.for_access(user=user)\
			.filter(is_read=False)\
			.exists())

@register.assignment_tag()
def reports_this_week(user):

	now = datetime.datetime.now()
	lastweek = now - datetime.timedelta(days=7)

	polys = AlertArea.objects.filter(user=user)
	points = Point.objects.filter(date__range=[lastweek, now])

	if not points.exists():
		return False

	for poly in polys:
		if points.filter(geom__intersects=poly.geom):
			return True
