#-*- coding: utf-8 -*-

from . import register

from spirit.models.topic_notification import TopicNotification
from mapApp.models import IncidentNotification, HazardNotification, TheftNotification

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