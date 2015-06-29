from django.shortcuts import render

from mapApp.models import AlertArea, Point

def vis(request, lat=None, lng=None, zoom=None):
	context = {
		'alertAreas': AlertArea.objects.filter(user=request.user.id),
		'points': Point.objects.all()
	}
	
	# Add zoom and center data if present
	if not None in [lat, lng, zoom]:
		context['lat']= float(lat)
		context['lng']= float(lng)
		context['zoom']= int(zoom)

	return render(request, 'mapApp/vis.html', context)
