from django.shortcuts import render

from mapApp.models import AlertArea, Point

def vis(request):
	context = {
		'alertAreas': AlertArea.objects.filter(user=request.user.id),
		'points': Point.objects.all()
	}
	return render(request, 'mapApp/vis.html', context)
