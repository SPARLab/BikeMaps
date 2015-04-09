from django.shortcuts import render
from django.views.decorators.cache import cache_page

@cache_page(60 * 60)
def termsAndConditions(request):
	return render(request, 'mapApp/ethics.html')
