from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from django.contrib.gis.geos import GEOSGeometry
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
import time

# Import models
from django.contrib.auth.models import User, Group
from mapApp.models.incident import Incident
from mapApp.models.route import Route
from mapApp.models.alert_area import AlertArea
from mapApp.models.alert_notification import IncidentNotification, HazardNotification, TheftNotification
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft

# Import forms
from mapApp.forms.incident import IncidentForm
from mapApp.forms.route import RouteForm
from mapApp.forms.contact import EmailForm
from mapApp.forms.geofences import GeofenceForm
from mapApp.forms.edit_geom import EditForm
from mapApp.forms.hazard import HazardForm
from mapApp.forms.theft import TheftForm

# Used for downloading data
from spirit.utils.decorators import administrator_required
from django.contrib.auth.decorators import login_required
from djgeojson.serializers import Serializer as GeoJSONSerializer


def index(request, lat=None, lng=None, zoom=None):
	context = indexContext(request)

	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)
	
	return render(request, 'mapApp/index.html', context)


# Define default context data for the index view. Forms can be overridden to display errors (used by other views)
def indexContext(request, incidentForm=IncidentForm(), routeForm=RouteForm(), geofenceForm=GeofenceForm(), hazardForm=HazardForm(), theftForm=TheftForm()):
	return {
		# Model data used by map
		'incidents': Incident.objects.all(),
		'hazards': Hazard.objects.all(),
		'thefts': Theft.objects.all(),
		"routes": Route.objects.all(),
		"geofences": AlertArea.objects.filter(user=request.user.id),

		# Form data used by map
		"incidentForm": incidentForm,
		"routeForm": routeForm,
		"geofenceForm": geofenceForm,
		"hazardForm": hazardForm,
		"theftForm": theftForm,
		
		"editForm": EditForm()
	}


def about(request):
	return render(request, 'mapApp/about.html', {"emailForm": EmailForm()})

@require_POST
def contact(request):
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

		try:
			send_mail(subject, message, sender, recipients)
		except BadHeaderError:
			messages.error(request, '<strong>Invalid Header.</strong> Illegal characters found.')

		messages.success(request, '<strong>Thank you!</strong><br>We\'ll do our best to get back to you.')
		emailForm = EmailForm() # Clear the form

	return render(request, 'mapApp/about.html', {"emailForm": emailForm})

@require_POST
def postRoute(request):
	routeForm = RouteForm(request.POST)
	routeForm.data = routeForm.data.copy()

	# Convert string coords to valid geometry object
	try:
		routeForm.data['line'] = GEOSGeometry(routeForm.data['line'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>Invalid geometry data.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

	if routeForm.is_valid():
		routeForm.save()
		routeForm = RouteForm() # Clear the form
		messages.success(request, '<strong>Thank you!</strong><br>Your route was successfully added.')

	return render(request, 'mapApp/index.html', indexContext(request, routeForm=routeForm))

@require_POST
def postIncident(request):
	incidentForm = IncidentForm(request.POST)
	incidentForm.data = incidentForm.data.copy()
	
	# Convert coords to valid geometry
	try:
		incidentForm.data['geom'] = GEOSGeometry(incidentForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>No point was selected for this type of report.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

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

@require_POST
def postHazard(request):
	hazardForm = HazardForm(request.POST)
	hazardForm.data = hazardForm.data.copy()
	
	# Convert coords to valid geometry
	try :
		hazardForm.data['geom'] = GEOSGeometry(hazardForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>No point was selected for this type of report.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

	if hazardForm.is_valid():
		hazard = hazardForm.save()
		alertUsers(request, hazard)
		
		messages.success(request, '<strong>Thank you!</strong><br>Your hazard marker was successfully added.')			
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(hazard.latlngList()[0]),		\
				"lng":str(hazard.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		)) 

	else: # Show form errors 
		return render(request, 'mapApp/index.html', indexContext(request, hazardForm=hazardForm))

@require_POST
def postTheft(request):
	theftForm = TheftForm(request.POST)
	theftForm.data = theftForm.data.copy()
	
	# Convert coords to valid geometry
	try:
		theftForm.data['geom'] = GEOSGeometry(theftForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>No point was selected for this type of report.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

	if theftForm.is_valid():
		theft = theftForm.save()
		alertUsers(request, theft)
		
		messages.success(request, '<strong>Thank you!</strong><br>Your theft marker was successfully added.')			
		return HttpResponseRedirect(reverse('mapApp:index', \
			kwargs=({										\
				"lat":str(theft.latlngList()[0]),		\
				"lng":str(theft.latlngList()[1]),		\
				"zoom":str(18)								\
			})												\
		)) 

	else: # Show form errors 
		return render(request, 'mapApp/index.html', indexContext(request, theftForm=theftForm))


def alertUsers(request, incident):
	intersectingPolys = AlertArea.objects.filter(geom__intersects=incident.geom) #list of AlertArea objects
	usersToAlert = list(set([poly.user for poly in intersectingPolys])) # get list of distinct users to alert

	INCIDENT, NEARMISS, HAZARD, THEFT, UNDEFINED = xrange(5)
	
	if (incident.incident_type() == "Collision"):
		action = INCIDENT
		Notification = IncidentNotification

	elif (incident.incident_type() == "Near miss"):
		action = NEARMISS
		Notification = IncidentNotification

	elif (incident.incident_type() == "Hazard"):
		action = HAZARD
		Notification = HazardNotification

	elif (incident.incident_type() == "Theft"):
		action = THEFT
		Notification = TheftNotification

	else:
		action = UNDEFINED

	for user in usersToAlert:	
		Notification(user=user, point=incident, action=action).save()

@require_POST
@login_required
def postAlertPolygon(request):
	geofenceForm = GeofenceForm(request.POST)
	geofenceForm.data = geofenceForm.data.copy()

	# Create valid attributes for user and geom fields
	try:
		geofenceForm.data['user'] = request.user.id
		geofenceForm.data['geom'] = GEOSGeometry(geofenceForm.data['geom'])
	except(ValueError):
		messages.error(request, '<strong>Error</strong><br>Invalid geometry data.')
		return HttpResponseRedirect(reverse('mapApp:index')) 

	if geofenceForm.is_valid():
		# Save new model object, send success message to the user
		geofenceForm.save()
		messages.success(request, 'You will now receive alerts for the area traced.')

	return HttpResponseRedirect(reverse('mapApp:index'))


@administrator_required
def getIncidents(request):
	data = GeoJSONSerializer().serialize(Incident.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_incidents_%s.json' % time.strftime("%x_%H-%M")
	return response

@administrator_required
def getHazards(request):
	data = GeoJSONSerializer().serialize(Hazard.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_hazards_%s.json' % time.strftime("%x_%H-%M")
	return response

@administrator_required
def getThefts(request):
	data = GeoJSONSerializer().serialize(Theft.objects.all(), indent=2, use_natural_keys=True)

	response = HttpResponse(data, content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="bikemaps_thefts_%s.json' % time.strftime("%x_%H-%M")
	return response

@login_required
def readAlertPoint(request, type, alertID):
	if type == 'collision' or type == 'nearmiss':
		alert = get_object_or_404(IncidentNotification.objects.filter(user=request.user), pk=alertID)
	if type == 'hazard':
		alert = get_object_or_404(HazardNotification.objects.filter(user=request.user), pk=alertID)
	if type == 'theft':
		alert = get_object_or_404(TheftNotification.objects.filter(user=request.user), pk=alertID)
		
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

@require_POST
@administrator_required
def editShape(request):
	editForm = EditForm(request.POST)
	if editForm.is_valid():

		pks = editForm.cleaned_data['editPk'].split(';')[:-1]
		newGeoms = editForm.cleaned_data['editGeom'].split(';')[:-1]
		editType = editForm.cleaned_data['editType']
		objTypes = editForm.cleaned_data['objType'].split(';')[:-1]

		# Edit/Delete each object
		for pk, newGeom, objType in zip(pks, newGeoms, objTypes):
			# Get the correct model dataset
			if objType == 'incident':
				objectSet = Incident.objects.all()
			elif objType == 'theft':
				objectSet = Theft.objects.all()
			elif objType == 'hazard':
				objectSet = Hazard.objects.all()
			elif objType == 'polygon':
				objectSet = AlertArea.objects.filter(user=request.user)
			else:
				return HttpResponseRedirect(reverse('mapApp:index'))

			# Edit
			if(editType == 'edit'):
				shapeEdited = get_object_or_404(objectSet, pk=pk)
				try:
					shapeEdited.geom = GEOSGeometry(newGeom)	# edit the object geometry
				except(ValueError):
					messages.error(request, '<strong>Error</strong><br>Invalid geometry error.')
					return HttpResponseRedirect(reverse('mapApp:index')) 
				shapeEdited.save()
			
			# Delete
			elif (editType == 'delete'):
				shapeEdited = get_object_or_404(objectSet, pk=pk)
				shapeEdited.delete() 	# delete the object

		message = str(len(pks)) + ' ' + editType + ('s' if len(pks)>1 else '') + ' successful'
		messages.success(request, message)
		
	return HttpResponseRedirect(reverse('mapApp:index'))