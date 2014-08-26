from django.shortcuts import render

def termsAndConditions(request):
	return render(request, 'mapApp/ethics.html')