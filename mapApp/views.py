from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from django.core.mail import send_mail

from django.contrib.auth.models import User, Group
from mapApp.models import Incident, Route, AlertArea, AlertNotification
from mapApp.forms import IncidentForm, RouteForm, EmailForm, GeofenceForm, EditForm

# Used for downloading data
from spirit.utils.decorators import administrator_required
from django.contrib.auth.decorators import login_required
from djgeojson.serializers import Serializer as GeoJSONSerializer

import time

def index(request, lat=None, lng=None, zoom=None):
	context = indexContext(request)

	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)
	
	return render(request, 'mapApp/index.html', context)


# Define default context data for the index view. Forms can be overridden to display errors (used by other views)
def indexContext(request, incidentForm=IncidentForm(), routeForm=RouteForm(), geofenceForm=GeofenceForm()):
	return {
		# Model data used by map
		'incidents': Incident.objects.all(),
		"routes": Route.objects.all(),
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": incidentForm,
		"routeForm": routeForm,
		"geofenceForm": geofenceForm,
		"editForm": EditForm()
	}


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

			adminContacts = Group.objects.get(name="admin contact").user_set.all()
			recipients = []
			
			for contact in adminContacts:
				recipients.append(contact.email) 
			if cc_myself:
				recipients.append(sender)

			send_mail(subject, message, sender, recipients)
			messages.success(request, '<strong>Thank you!</strong><br>We\'ll do our best to get back to you.')
			emailForm = EmailForm() # Clear the form

	return render(request, 'mapApp/about.html', {"emailForm": emailForm})


def postRoute(request):
	if request.method == 'POST':
		routeForm = RouteForm(request.POST)

		# Convert string coords to valid geometry object
		routeForm.data = routeForm.data.copy()
		routeForm.data['line'] = GEOSGeometry(routeForm.data['line'])

		if routeForm.is_valid():
			routeForm.save()
			routeForm = RouteForm() # Clear the form
			messages.success(request, '<strong>Thank you!</strong><br>Your route was successfully added.')

	return render(request, 'mapApp/index.html', indexContext(request, routeForm=routeForm))


def postIncident(request):
	if request.method == 'POST':
		incidentForm = IncidentForm(request.POST)
		
		# Convert coords to valid geometry
		incidentForm.data = incidentForm.data.copy()
		incidentForm.data['geom'] = GEOSGeometry(incidentForm.data['geom'])

		if incidentForm.is_valid():
			incident = incidentForm.save()
			alertUsers(request, incident)
			
			messages.success(request, '<strong>Thank you!</strong><br>Your incident marker was successfully added.')			
			return HttpResponseRedirect(reverse('mapApp:index', \
				kwargs=({										\
					"lat":str(incident.latlngList()[0]),		\
					"lng":str(incident.latlngList()[1]),		\
					"zoom":str(18)								\
				})												\
			)) 

		else: # Show form errors 
			return render(request, 'mapApp/index.html', indexContext(request, incidentForm=incidentForm))
	
	else: # Redirect to index if not a post request
		return HttpResponseRedirect(reverse('mapApp:index')) 

	def alertUsers(request, incident):
		intersectingPolys = AlertArea.objects.filter(geom__intersects=incident.geom) #list of AlertArea objects
		usersToAlert = list(set([poly.user for poly in intersectingPolys])) # get list of distinct users to alert

		# FIX THIS MAGIC
		if (incident.incident_type() == "Collision"):
			action = 0
		elif (incident.incident_type() == "Near miss"):
			action = 1
		else:
			action = 2

		for user in usersToAlert:
			AlertNotification(user=user, point=incident, action=action).save()


@login_required
def postAlertPolygon(request):
	if request.method == 'POST':
		geofenceForm = GeofenceForm(request.POST)

		# Create valid attributes for user and geom fields 
		geofenceForm.data = geofenceForm.data.copy()
		geofenceForm.data['user'] = request.user.id
		geofenceForm.data['geom'] = GEOSGeometry(geofenceForm.data['geom'])

		if geofenceForm.is_valid():
			# Save new model object, send success message to the user
			geofenceForm.save()
			messages.success(request, 'You will now receive alerts for the area was traced.')

	return HttpResponseRedirect(reverse('mapApp:index'))


@administrator_required
def getIncidents(request):
	data = GeoJSONSerializer().serialize(Incident.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_incidents_%s.json' % time.strftime("%x_%H-%M")
	return response


@login_required
def readAlertPoint(request, alertID):
	alert = get_object_or_404(AlertNotification.objects.filter(user=request.user), pk=alertID)
	if (alert):
		alert.is_read=True
		alert.save()
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(alert.point.latlngList()[0]), 	\
				"lng":str(alert.point.latlngList()[1]), 	\
				"zoom":str(18)								\
			})												\
		))
	
	else:
		return HttpResponseRedirect(reverse('mapApp:index')) 


@login_required
def editAlertArea(request):
	if(request.method == 'POST'):
		editForm = EditForm(request.POST)
		
		if editForm.is_valid():
			editType = editForm.cleaned_data['editType']
			pks = editForm.cleaned_data['editPk'].split(';')[:-1]
			userAreas = AlertArea.objects.filter(user=request.user)

			if(editType == 'edit'):
				newGeoms = editForm.cleaned_data['editGeom'].split(';')[:-1]
				for pk, newGeom in zip(pks, newGeoms):
					polyEdited = get_object_or_404(userAreas, pk=pk)
					polyEdited.geom = GEOSGeometry(newGeom)	# edit the object geometry
					polyEdited.save()
		
			elif (editType == 'delete'):
				for pk in pks:		
					polyEdited = get_object_or_404(userAreas, pk=pk)
					polyEdited.delete() 	# delete the object

			message = str(len(pks)) + ' ' + editType + ('s' if len(pks)>1 else '') + ' successful'
			messages.success(request, message)
	return HttpResponseRedirect(reverse('mapApp:index'))


@administrator_required
def editPoint(request):
	if(request.method == 'POST'):
		editForm = EditForm(request.POST)
		
		if editForm.is_valid():
			editType = editForm.cleaned_data['editType']
			pointEdited = get_object_or_404(Incident.objects, pk=editForm.cleaned_data['editPk'])

			if(editType == 'edit'):
				pointEdited.geom = GEOSGeometry(editForm.cleaned_data['editGeom'])	# edit the object geometry
				pointEdited.save()
				messages.success(request, 'Points were edited')
		
			elif (editType == 'delete'):
				pointEdited.delete() 	# delete the object
				messages.success(request, 'Points were deleted')
			
	return HttpResponseRedirect(reverse('mapApp:index'))