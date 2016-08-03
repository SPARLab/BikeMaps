from django.shortcuts import render

def cert(request):
    context = {}
    
    return render(request, 'mapApp/bikemaps.org.html', context)
