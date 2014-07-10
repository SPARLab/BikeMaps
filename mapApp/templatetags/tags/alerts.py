#-*- coding: utf-8 -*-

from . import register

from spirit.models.topic_notification import TopicNotification
from mapApp.models import AlertArea

@register.assignment_tag()
def has_alerts(user):
	userAlertAreas = AlertArea.objects.filter(user=user)
	result = [area for area in userAlertAreas if area.has_alerts()]

	return (
		len(result) or \
		TopicNotification.objects.for_access(user=user)\
			.filter(is_read=False)\
			.exists())