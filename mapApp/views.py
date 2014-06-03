from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import GEOSGeometry, Point, fromstr

from mapApp.models import Incident, PoliceData
from mapApp.forms import IncidentForm

def index(request):
	formErrors = False
	form = IncidentForm()

	if request.method == 'POST':
		form = IncidentForm(request.POST)
		
		# Convert string coords to valid geometry object
		form.data = form.data.copy()	# Copy to allow mutation of value
		#Try:?		
		pnt = fromstr(form.data['point'])
		form.data['point'] = GEOSGeometry(pnt)
		#Catch(failure)?

		if form.is_valid():
			# create database entry
			form.save()	
			# redirect to clean index
			return HttpResponseRedirect(reverse('mapApp:index')) 
		
		else:
			# display modal with highlighted errors
			formErrors = True

	context = {
		'incidents': Incident.objects.all(),
		'police_data': PoliceData.objects.all(),
		"form": form, 	#the form to be rendered
		"formErrors": formErrors
	}
	return render(request, 'mapApp/index.html', context)

def about(request):
	context = {
		'incidents': Incident.objects.all(),
	}

	return render(request, 'mapApp/about.html', context)

def sponsors(request):
	return render(request, 'mapApp/sponsors.html')

def contact(request):
	return render(request, 'mapApp/contact.html')

