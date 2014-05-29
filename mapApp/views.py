from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import GEOSGeometry, Point, fromstr

from mapApp.models import Incident
from mapApp.forms import IncidentForm

def index(request):
	if request.method == 'POST':
		form = IncidentForm(request.POST)
		
		# Copy to allow mutation of value
		form.data = form.data.copy()

		# Convert string coords to valid geometry object
		pnt = fromstr(form.data['point'])
		form.data['point'] = GEOSGeometry(pnt)
		

		if form.is_valid():
			form.save()		# create object
			#	redirect to index again or to "thank you" page
			form = IncidentForm() # Clean form
		else:
			pass
			# 	Display index with form open and error messages

	else:
		form = IncidentForm()

	context = {
		'incidents': Incident.objects.all(),
		"form": form, 	#the form to be rendered
		# "modal_open": 'hide'
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

