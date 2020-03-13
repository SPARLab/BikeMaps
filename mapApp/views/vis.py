from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from mapApp.models import AlertArea, Point

@xframe_options_exempt
def vis(request, lat=None, lng=None, zoom=None):
	context = {
		'alertAreas': AlertArea.objects.filter(user=request.user.id),
		'points': Point.objects.all().exclude(infrastructure_changed=True).exclude(p_type = "newInfrastructure")
	}
	
	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)

	return render(request, 'mapApp/vis.html', context)
