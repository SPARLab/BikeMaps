from django.utils.translation import ugettext as _
from django.shortcuts import render

from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage

from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from mapApp.forms import EmailForm

# @cache_page(60 * 60)
@xframe_options_exempt
def about(request):
	return render(request, 'mapApp/about.html', {"emailForm": EmailForm()})

@require_POST
def contact(request):
	emailForm = EmailForm(request.POST)

	if emailForm.is_valid():
		subject = '[BikeMaps] '+ emailForm.cleaned_data['subject']
		message = emailForm.cleaned_data['message']
		sender = emailForm.cleaned_data['sender']
		cc_myself = emailForm.cleaned_data['cc_myself']

		recipients = ['admin@bikemaps.org','tech-support@bikemaps.org']
		cc = [sender] if cc_myself else []

		email = EmailMessage(subject, message, 'admin@bikemaps.org', recipients, headers = {'Reply-To': sender}, cc = cc)

		try:
			email.send()
			messages.success(request, '<strong>' + _('Thank you!') + '</strong><br>' + _('We\'ll do our best to get back to you soon.'))
			emailForm = EmailForm() # Clear the form
		except BadHeaderError:
			messages.error(request, '<strong>'+ _('Invalid Header.') + '</strong>' + _('Illegal characters found.'))

	return render(request, 'mapApp/about.html', {"emailForm": emailForm})
