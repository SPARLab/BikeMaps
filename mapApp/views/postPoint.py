from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.contrib.gis.geos import GEOSGeometry
from djgeojson.serializers import Serializer as GeoJSONSerializer

from crispy_forms.utils import render_crispy_form

from mapApp.models import Incident, Hazard, Theft
from mapApp.forms import IncidentForm, NearmissForm, HazardForm, TheftForm
from mapApp.views import alertUsers, pushNotification
from mapApp.models import HazardMessageDistricts

from django.contrib.gis.db import models

import json, math

@require_POST
def postIncident(request):
	return postPoint(request, IncidentForm)

@require_POST
def postNearmiss(request):
	return postPoint(request, NearmissForm)

@require_POST
def postHazard(request):
	return postPoint(request, HazardForm)

@require_POST
def postTheft(request):
	return postPoint(request, TheftForm)

def postPoint(request, Form):
	"""Submit a user point submission to the database. Normalize geometry and activate push notifications."""
	form = Form(request.POST)
	form.data = form.data.copy()
	
	hazardHasMessage = False;
	
	# Convert coords to valid geometry
	try:
		form.data['geom'] = normalizeGeometry(form.data['geom'])
	except(ValueError):
		# TODO provide error message to user here
		JsonResponse({'success': False})
		# messages.error(request, '<strong>' + _('Error') + '</strong><br>' + _('No point was selected for this type of report.'))

	# Validate and submit to db
	if form.is_valid():
	
		#Check if the point was a hazard and in the areas where 311 popups are available
		if "hazard" in str(type(form)):
			message = threeOneOnePopUp(form.data)
			if message!=None:
				hazardHasMessage = True
	
		point = form.save()
		
		# Errors with push notifications should not affect reporting
		if not settings.DEBUG:
			try: pushNotification.pushNotification(point)
			except: pass
		if hazardHasMessage==False:
			return JsonResponse({
				'hazardHasMessage' : False,
				'hazardMessage': None,
				'success': True,
				'point': GeoJSONSerializer().serialize([point,]),
				'point_type': point.p_type,
				'form_html': render_crispy_form(Form())
			})
		#If incident was a hazard and a 311 popup was included return this JsonResponse
		else:
			return JsonResponse({
				'hazardHasMessage' : True,
				'hazardMessage': message,
				'success': True,
				'point': GeoJSONSerializer().serialize([point,]),
				'point_type': point.p_type,
				'form_html': render_crispy_form(Form())
			})
	else:
		logger.debug("Form not valid")

	# Else: error occurred
	form.data['geom'] = form.data['geom'].json
	form_html = render_crispy_form(form)
	return JsonResponse({'success': False, 'form_html': form_html})

def threeOneOnePopUp(data):

	message = None

	greaterVancouver = HazardMessageDistricts.objects.all().filter(districtName='Greater Vancouver')

	# Check if point fell in areas in Greater Vancouver
	try:
		if greaterVancouver[0].districtShape.contains(data['geom']):

			dictOfMessages={}
			dictOfMessages['Burnaby'] = "To report this hazard to Burnaby authorities:<br>1) Call 1-604-294-7440"
			dictOfMessages['City of North Vancouver'] = "To report this hazard to the City Of North Vancouver authorities:<br>1) Download the CityFix App by clicking <a href=\"http://www.cnv.org/online-services/city-fix\" style=\"color: white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['Coquitlam'] = "To report this hazard to Coquitlam authorities:<br>1) Call 1-604-927-3500"
			dictOfMessages['Delta'] =  "To report this hazard to Delta authorities:<br>1) Call 1-604-946-3260 <br>2) Report online by clicking <a href=\"http://www.delta.ca/your-government/contact-us/talk-to-delta\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['District of North Vancouver'] = "To report this hazard to the District of North Vancouver authorities:<br>1) Call 1-604-990-2450 <br>2) Email eng@dnv.org"
			dictOfMessages['Maple Ridge'] = "To report this hazard to Maple Ridge authorities:<br>1) Report online by clicking <a href=\"http://mapleridge.ca/FormCenter/Service-Request-Form-5/Service-Request-Form-45\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['New WestMinster'] = "To report this hazard to New Westminster authorities:<br>1) Report online by clicking <a href=\"https://www.newwestcity.ca/services/online-services/report-a-problem\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a> <br>2) Download the SeeClickFix App by clicking <a href=\"http://seeclickfix.com/apps\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['Pitt Meadows'] = "To report this hazard to Pitt Meadows authorities:<br>1) Call 1-604-465-2434"
			dictOfMessages['Port Coquitlam'] = "To report this hazard to Port Coquitlam authorities:<br>1) Call 1-604-927-5496 <br>2) Email publicworks@portcoquitlam.ca"
			dictOfMessages['Port Moody'] = "To report this hazard to Port Moody authorities:<br>1) Call 1-604-469-4574"
			dictOfMessages['Richmond'] = "To report this hazard to Richmond authorities:<br>1) Report online by clicking <a href=\"http://www.richmond.ca/contact/customerfeedback/RequestService.aspx\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['Surrey'] = "To report this hazard to Surrey authorities:<br>1) Download the Surrey Request App by clicking <a href=\"http://www.surrey.ca/city-services/12082.aspx\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a> <br>2) Report online by clicking <a href=\"http://www.surrey.ca/city-services/667.aspx\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['Township Of Langley'] = "To report this hazard to the Township of Langley authorities:<br>1) Click <a href=\"http://www.tol.ca/Services-Contact/Report-a-Problem\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['Vancouver'] = "To report this hazard to Vancouver authorities:<br>1) Call 3-1-1 <br>2) Report online by clicking <a href=\"http://vancouver.ca/vanconnect-desktop.aspx\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a> <br>3) Download the VanConnect App by clicking <a href=\"http://vancouver.ca/vanconnect.aspx\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfMessages['West Vancouver'] = "To report this hazard to the District of West Vancouver authorities:<br>1) Call 1-604-925-7020 <br>2) Email ecounter@westvancouver.ca"
			dictOfMessages['White Rock'] = "To report this hazard to White Rock authorities:<br>1) Call 1-604-541-2181"

			#Get districts from Vancouver from DB
			vancouverObjects = HazardMessageDistricts.objects.all().filter(regionName='Greater Vancouver')

			#Cycle through data to check if point fell in polygon, will return when finds the correct location
			for district in vancouverObjects:
				if district.districtShape.contains(data['geom']):
					try:
						return dictOfMessages[district.districtName]
					except:
						print
						print "Message for " + district.districtName + " hasn't been added to dictOfMessages"
						print

	except:
		print "Greater Vancouver shapefile hasn't been added to the database"

	alberta = HazardMessageDistricts.objects.all().filter(districtName='Alberta')
	try:
		if alberta[0].districtShape.contains(data['geom']):
			dictOfAlbertaMessages = {}
			dictOfAlbertaMessages['Edmonton'] = "To report this hazard to Edmonton authorities:<br>1) Download the 311 App by clicking <a href=\"https://www.edmonton.ca/programs_services/edmonton-311-app.aspx\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			dictOfAlbertaMessages['Lethbridge'] = "To report this hazard to Lethbridge authorities:<br>1)  Report online by clicking <a href=\"http://www.lethbridge.ca/living-here/Service-Request/Pages/default.aspx\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"

			# Get districts from Alberta from DB
			albertaObjects = HazardMessageDistricts.objects.all().filter(regionName='Alberta')

			# Cycle through data to check if point fell in polygon, will return when finds the correct location
			for district in albertaObjects:
				if district.districtShape.contains(data['geom']) and district.districtName!="Alberta":
					print district.districtName
					try:
						return dictOfAlbertaMessages[district.districtName]
					except:
						print
						print "Message for " + district.districtName + " hasn't been added to dictOfMessages"
						print
	except:
		print "Alberta shapefile hasn't been added to the database"


	kelowna = HazardMessageDistricts.objects.all().filter(districtName='Kelowna')
	try:
		if kelowna[0].districtShape.contains(data['geom']):
			message = "To report this hazard to Kelowna authorities:<br>1) Report online by clicking <a href=\"https://apps.kelowna.ca/iService_Requests/request.cfm?id=265&sid=97\" style=\"color:white\" target=\"_blank\"><strong>here</strong></a>"
			return message
	except:
		print "Kelowna hasn't been added to the database"


def normalizeGeometry(geom):
	"""Convert text string to GEOS Geometry object and correct x y coordinates if out range (-180, 180]."""
	# Convert string GEOSGeometry object to python dict
	geom = json.loads(geom)

	# Normalize longitude to range [-180, 180) using saw tooth function
	c = geom['coordinates'][0]
	geom['coordinates'][0] = (c+180 - ( math.floor( (c+180)/360 ) )*360) - 180

	# Normalize latitude to range [-90, 90) using saw tooth function
	c = geom['coordinates'][1]
	geom['coordinates'][1] = (c+90 - ( math.floor( (c+90)/180 ) )*180) - 90

	# Encode and return GEOSGeometry object
	return GEOSGeometry(json.dumps(geom))
