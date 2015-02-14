from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime

from mapApp.models import Incident, Hazard, Theft, AlertArea

@login_required
def recentReports(request):
    user = request.user

    # Get the user's alertable points in the last month
    incidents = Incident.objects.all()#filter(incidentNotification__user=user.id)
    nearmisses = incidents.filter(incident__contains="Near collision")
    collisions = incidents.exclude(incident__contains="Near collision")

    hazards = Hazard.objects.all()
    thefts = Theft.objects.all()

    # Get only points that intersect user alert areas
    rois = AlertArea.objects.filter(user=user.id)
    # recent sets = points that intersect an rois as defined by user and are reported in last month
    collisionsInPoly = Incident.objects.none()
    nearmissesInPoly = Incident.objects.none()
    hazardsInPoly = Hazard.objects.none()
    theftsInPoly = Theft.objects.none()
    # Find intersecting points
    for g in rois:
        collisionsInPoly = collisionsInPoly | collisions.filter(geom__intersects=g.geom)
        nearmissesInPoly = nearmissesInPoly | nearmisses.filter(geom__intersects=g.geom)
        hazardsInPoly = hazardsInPoly | hazards.filter(geom__intersects=g.geom)
        theftsInPoly = theftsInPoly | thefts.filter(geom__intersects=g.geom)

    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=7)

    context = {
        "now": now.isoformat(),
        'yesterday': yesterday.isoformat(),

        'collisions': collisionsInPoly.filter(incident_date__range=[yesterday, now]),
        'nearmisses': nearmissesInPoly.filter(incident_date__range=[yesterday, now]),
        'hazards': hazardsInPoly.filter(hazard_date__range=[yesterday, now]),
        'thefts': theftsInPoly.filter(theft_date__range=[yesterday, now]),

        'geofences': rois
    }

    return render(request, 'mapApp/recent_reports.html', context)
