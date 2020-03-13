from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def termsAndConditions(request):
	return render(request, 'mapApp/ethics.html')
