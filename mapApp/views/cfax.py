from django.shortcuts import render
from django.http import HttpResponse

# Import models
from mapApp.models.incident import Incident
from mapApp.models.hazard import Hazard
from mapApp.models.theft import Theft

import datetime

def cfax(request):
    user = request.user

    # Get the user's alertable points in the last month
    incidents = Incident.objects.all()#filter(incidentNotification__user=user.id)
    nearmisses = incidents.filter(incident__contains="Near collision")
    collisions = incidents.exclude(incident__contains="Near collision")

    hazards = Hazard.objects.all()
    thefts = Theft.objects.all()

    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)

    context = {
        "now": now.isoformat(),
        'yesterday': yesterday.isoformat(),

        'collisions': collisions.filter(incident_date__range=[yesterday, now]),
        'nearmisses': nearmisses.filter(incident_date__range=[yesterday, now]),
        'hazards': hazards.filter(hazard_date__range=[yesterday, now]),
        'thefts': thefts.filter(theft_date__range=[yesterday, now]),
    }

    return render(request, 'mapApp/cfax.html', context)
