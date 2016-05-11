from django.shortcuts import render

def disclaimer(request):
	return render(request, 'mapApp/disclaimer.html')
