# For help see https://github.com/Tivix/django-cron
from django_cron import CronJobBase, Schedule

from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404
from django.template import loader, Context

from django.contrib.auth.models import User
from mapApp.models.alert_notification import IncidentNotification, HazardNotification, TheftNotification

# DISABLED!
class UserAlertEmails(CronJobBase):
	# pass ########################## REMOVE THIS TO ENABLE
	RUN_EVERY_MINS = 1 # every 1 minute
	RETRY_AFTER_FAILURE_MINS = 5

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
	code = 'mapApp.cron.UserAlertEmails'    # a unique code

	def do(self):
		pass
		# # Get all notification objects that need to be emailed
		# incidentPolys = IncidentNotification.objects.filter(emailed=False)
		# hazardPolys = HazardNotification.objects.filter(emailed=False)
		# theftPolys = TheftNotification.objects.filter(emailed=False)
		
		# # Get a list of distinct users that need to be emailed
		# userSet = list(set(
		# 	[poly.user for poly in incidentPolys] + 
		# 	[poly.user for poly in hazardPolys] + 
		# 	[poly.user for poly in theftPolys]
		# ))

		# for user in userSet:
		# 	# Get the users notification objects
		# 	incidentPoints = incidentPolys.filter(user=user.id)
		# 	hazardPoints = hazardPolys.filter(user=user.id)
		# 	theftPoints = theftPolys.filter(user=user.id)

		# 	# separate nearmiss and incident points
		# 	nearmissPoints = incidentPoints.filter(action=IncidentNotification.NEARMISS)
		# 	incidentPoints = incidentPolys.filter(action=IncidentNotification.INCIDENT)

		# 	# Turn these points into a chart, etc
		# 	# Get counts like this
		# 	# 	nearmissPoints.count()


		# 	# Add the points to the email message
		# 	template = loader.get_template('mapApp/email.html')
		# 	d = Context({ 
		# 		'user': user, 
		# 		'incidentCount': incidentPoints.count(), 
		# 		'nearmissCount': nearmissPoints.count(), 
		# 		'hazardCount': hazardPoints.count(), 
		# 		'theftCount': theftPoints.count() 
		# 	})
		# 	html_content = template.render(d)


		# 	# ????
		# 	# PROFIT!!

		# 	# Send the message
		# 	subject = "Monthly alerts update"
		# 	text_content = "blah blah blah - insert some message about alertPoints here."
		# 	sender = "do-not-reply@bikemaps.org"
		# 	recipient = [user.email]
		# 	send_mail(subject, text_content, sender, recipient, html_message=html_content)

			# if success: #TODO implement this check

			# Mark the theft notification object as having been emailed
			# incidentPoints.update(emailed=True)
			# nearmissPoints.update(emailed=True)
			# hazardPoints.update(emailed=True)
			# theftPoints.update(emailed=True)