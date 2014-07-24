# For help see https://github.com/Tivix/django-cron
from django_cron import CronJobBase, Schedule

from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from mapApp.models.alert_notification import AlertNotification

# DISABLED!
class UserAlertEmails(CronJobBase):
	pass ########################## REMOVE THIS TO ENABLE
    RUN_EVERY_MINS = 120 # every 2 hours
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'mapApp.cron.UserAlertEmails'    # a unique code

    def do(self):
    	alertPolys = AlertNotification.objects.filter(emailed=False)
        userSet = list(set([poly.user for poly in alertPolys]))

        for user in userSet:
			alertPoints = alertPolys.filter(user=user)

			subject = "Weekly alerts update"
			message = "blah blah blah - insert some message about alertPoints here."
			sender = "bikemaps.org@gmail.com"
			recipient = [user.email]
			send_mail(subject, message, sender, recipient)

			# if success:
			alertPoints.update(emailed=True)


class BackupDB(CronJobBase):
	pass