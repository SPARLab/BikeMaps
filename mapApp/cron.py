# For help see https://github.com/Tivix/django-cron
from django_cron import CronJobBase, Schedule

from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from mapApp.models.alert_notification import IncidentNotification, HazardNotification, TheftNotification

# DISABLED!
class UserAlertEmails(CronJobBase):
	# pass ########################## REMOVE THIS TO ENABLE
	RUN_EVERY_MINS = 1 # every 2 hours
	RETRY_AFTER_FAILURE_MINS = 5

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
	code = 'mapApp.cron.UserAlertEmails'    # a unique code

	def do(self):
		# Get all notification objects that need to be emailed
		incidentPolys = IncidentNotification.objects.filter(emailed=False)
		hazardPolys = HazardNotification.objects.filter(emailed=False)
		theftPolys = TheftNotification.objects.filter(emailed=False)
		
		# Get a list of distinct users that need to be emailed
		userSet = list(set(
			[poly.user for poly in incidentPolys] + 
			[poly.user for poly in hazardPolys] + 
			[poly.user for poly in theftPolys]
		))

		for user in userSet:
			# Get the users notification objects
			incidentPoints = incidentPolys.filter(user=user)
			hazardPoints = hazardPolys.filter(user=user)
			theftPoints = theftPolys.filter(user=user)

			# ????
			# PROFIT!!

			subject = "Monthly alerts update"
			message = "blah blah blah - insert some message about alertPoints here."
			sender = "do-not-reply@bikemaps.org"
			recipient = [user.email]
			send_mail(subject, message, sender, recipient)

			# if success: #TODO implement this check
			incidentPoints.update(emailed=True)
			hazardPoints.update(emailed=True)
			theftPoints.update(emailed=True)