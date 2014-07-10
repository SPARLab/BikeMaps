#-*- coding: utf-8 -*-

from django import template.Library() as register


from spirit.models.topic_notification import TopicNotification
from mapApp.models import AlertAreas

@register.assignment_tag()
def has_alerts(user):
    return (\
        TopicNotification.objects.for_access(user=user)\
            .filter(is_read=False)\
            .exists()\
        or AlertAreas.objects.for_access(user=user)\
            .filter(has_alerts=True)\
            .exists()\
        )