from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from django.core.mail import send_mail

from mapApp.models import Incident, Route
from mapApp.forms import IncidentForm, RouteForm, EmailForm


def index(request):
	context = {
		'incidents': Incident.objects.all(),
		"incidentForm": IncidentForm(), 	#the form to be rendered
		"incidentFormErrors": False,

		"routes": Route.objects.all(),
		"routeForm": RouteForm(),
		"routeFormErrors": False
	}
	return render(request, 'mapApp/index.html', context)


def postRoute(request):
	if request.method == 'POST':
		routeForm = RouteForm(request.POST)

		# Convert string coords to valid geometry object
		routeForm.data = routeForm.data.copy()
		routeForm.data['line'] = GEOSGeometry(routeForm.data['line'])

		if routeForm.is_valid():
			routeForm.save()
			messages.success(request, '<strong>Thank you!</strong><br>Your route was successfully added.')
			return HttpResponseRedirect(reverse('mapApp:index')) 
		else:
			# Form is not valid, display modal with highlighted errors 
			return render(request, 'mapApp/index.html', {
				'incidents': Incident.objects.all(),
				"incidentForm": IncidentForm(),
				"incidentFormErrors": False,

				"routes": Route.objects.all(),
				"routeForm": routeForm,
				"routeFormErrors": True
			})
	
	else:
		return HttpResponseRedirect(reverse('mapApp:index')) 


def postIncident(request):
	if request.method == 'POST':
		incidentForm = IncidentForm(request.POST)
		
		# Convert string coords to valid geometry object
		incidentForm.data = incidentForm.data.copy()
		incidentForm.data['point'] = GEOSGeometry(incidentForm.data['point'])

		if incidentForm.is_valid():
			incidentForm.save()
			messages.success(request, '<strong>Thank you!</strong><br>Your incident marker was successfully added.')
			return HttpResponseRedirect(reverse('mapApp:index')) 
		
		else:
			# Form is not valid, display modal with highlighted errors 
			return render(request, 'mapApp/index.html', {
				'incidents': Incident.objects.all(),
				"incidentForm": incidentForm,
				"incidentFormErrors": True,
				
				"routes": Route.objects.all(),
				"routeForm": RouteForm(),
				"routeFormErrors": False
			})
	
	else:
		return HttpResponseRedirect(reverse('mapApp:index')) 


def about(request):
	return render(request, 'mapApp/about.html', {"emailForm": EmailForm()})


def contact(request):
	if request.method == 'POST':
		emailForm = EmailForm(request.POST)


		if emailForm.is_valid():
			subject = emailForm.cleaned_data['subject']
			message = emailForm.cleaned_data['message']
			sender = emailForm.cleaned_data['sender']
			cc_myself = emailForm.cleaned_data['cc_myself']

			recipients = ['taylordenouden@gmail.com']
			if cc_myself:
				recipients.append(sender)

			send_mail(subject, message, sender, recipients)

			messages.success(request, '<strong>Thank you!</strong><br>We\'ll do our best to get back to you.')
			return HttpResponseRedirect(reverse('mapApp:about')) 
		
		else:
			# Form is not valid, display modal with highlighted errors 
			return render(request, 'mapApp/about.html', {
				"emailForm": emailForm,
				"emailFormErrors": True,
			})
	
	else:
		return HttpResponseRedirect(reverse('mapApp:about')) 
