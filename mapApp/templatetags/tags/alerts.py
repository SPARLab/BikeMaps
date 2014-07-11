#-*- coding: utf-8 -*-

from . import register

from spirit.models.topic_notification import TopicNotification
from mapApp.models import AlertNotification

@register.assignment_tag()
def has_alerts(user):
	return (
		AlertNotification.objects.filter(user=user).filter(is_read=False).exists()\
		or \
		TopicNotification.objects.for_access(user=user)\
			.filter(is_read=False)\
			.exists())