from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from django.core.mail import send_mail

from django.contrib.auth.models import User, Group
from mapApp.models import Incident, Route, AlertArea
from mapApp.forms import IncidentForm, RouteForm, EmailForm, GeofenceForm

# Used for downloading data
from spirit.utils.decorators import administrator_required
from djgeojson.serializers import Serializer as GeoJSONSerializer


def index(request):
	context = {
		'incidents': Incident.objects.all(),
		"incidentForm": IncidentForm(), 	#the form to be rendered
		"incidentFormErrors": False,

		"routes": Route.objects.all(),
		"routeForm": RouteForm(),
		"routeFormErrors": False,

		"geofence": AlertArea.objects.all(),
		"geofenceForm": GeofenceForm(),
		"geofenceFormErrors": False
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

				"geofence": AlertArea.objects.all(),
				"geofenceForm": GeofenceForm(),
				"geofenceFormErrors": False,

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
		incidentForm.data['geom'] = GEOSGeometry(incidentForm.data['geom'])

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

				"geofence": AlertArea.objects.all(),
				"geofenceForm": GeofenceForm(),
				"geofenceFormErrors": False,
				
				"routes": Route.objects.all(),
				"routeForm": RouteForm(),
				"routeFormErrors": False
			})
	
	else:
		return HttpResponseRedirect(reverse('mapApp:index')) 


def postAlertPolygon(request):
	if request.method == 'POST':
		geofenceForm = GeofenceForm(request.POST)
		
		# Convert string coords to valid geometry object
		geofenceForm.data = geofenceForm.data.copy()
		geofenceForm.data['geofence'] = GEOSGeometry(geofenceForm.data['geofence'])

		if geofenceForm.is_valid():
			geofenceForm.save()
			messages.success(request, 'You will now recieve alerts for the area was traced.')
			return HttpResponseRedirect(reverse('mapApp:index')) 
		
		else:
			# Form is not valid, display modal with highlighted errors 
			return render(request, 'mapApp/index.html', {
				'incidents': Incident.objects.all(),
				"incidentForm": IncidentForm(),
				"incidentFormErrors": False,

				"geofence": AlertArea.objects.all(),
				"geofenceForm": geofenceForm,
				"geofenceFormErrors": True,
				
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

			contact_group = Group.objects.get(name="admin contact")
			members = contact_group.user_set.all()
			recipients = []
			for r in members:
				recipients.append(r.email) 
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

@administrator_required
def getIncidents(request):
	data = GeoJSONSerializer().serialize(Incident.objects.all(), indent=2, use_natural_keys=True)
	return HttpResponse(data, content_type="application/json")