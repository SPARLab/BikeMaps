from mapApp.models import Incident, Hazard, Theft, Official, AlertArea, NewInfrastructure, Weather
from mapApp import serializers as s
from django.http import Http404
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Polygon
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, generics, permissions, status
from django.views.decorators.csrf import csrf_exempt
from mapApp.permissions import IsOwnerOrReadOnly
from push_notifications.models import GCMDevice, APNSDevice
from mapApp.views import alertUsers, pushNotification

from django.contrib.auth import get_user_model
import datetime
User = get_user_model()

class CollisionList(APIView):
    """
    List all collisions, or create a new collision.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        collisions = list(Incident.objects.filter(p_type__exact="collision").filter(geom__within=bbox))

        serializer = s.IncidentSerializer(collisions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = s.IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['properties'] is not None:
               if serializer.data['properties']['pk'] is not None:
                  collision = Incident.objects.get(pk=(serializer.data['properties']['pk']))
                  alertUsers(request, collision)
                  # Errors with push notifications should not affect reporting
                  try:
                      pushNotification.pushNotification(collision)
                  except:
                      pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NearmissList(APIView):
    """
    List all hazards, or create a new hazard.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        nearmiss = list(Incident.objects.filter(p_type__exact="nearmiss").filter(geom__within=bbox))
        serializer = s.IncidentSerializer(nearmiss, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = s.IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['properties'] is not None:
               if serializer.data['properties']['pk'] is not None:
                  nearmiss = Incident.objects.get(pk=(serializer.data['properties']['pk']))
                  alertUsers(request, nearmiss)
                  # Errors with push notifications should not affect reporting
                  try:
                      pushNotification.pushNotification(nearmiss)
                  except:
                      pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HazardList(APIView):
    """
    List all hazards, or create a new hazard.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        hazards = list(Hazard.objects.exclude(expires_date__lt=datetime.datetime.now()).exclude(hazard_fixed=True).filter(geom__within=bbox))
        serializer = s.HazardSerializer(hazards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = s.HazardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['properties'] is not None:
               if serializer.data['properties']['pk'] is not None:
                  hazard = Hazard.objects.get(pk=(serializer.data['properties']['pk']))
                  alertUsers(request, hazard)
                  # Errors with push notifications should not affect reporting
                  try:
                      pushNotification.pushNotification(hazard)
                  except:
                      pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TheftList(APIView):
    """
    List all thefts, or create a new theft.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        thefts = list(Theft.objects.filter(geom__within=bbox))
        serializer = s.TheftSerializer(thefts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = s.TheftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['properties'] is not None:
               if serializer.data['properties']['pk'] is not None:
                  theft = Theft.objects.get(pk=(serializer.data['properties']['pk']))
                  alertUsers(request, theft)
                  # Errors with push notifications should not affect reporting
                  try:
                      pushNotification.pushNotification(theft)
                  except:
                      pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilteredHazardList(APIView):
    """
    List hazards, but filter attributes to hazard type, date, description and location.
    Demographic details are not included.
    Initial use case is for the provision of data to Biko.
    """
    def get(self, request, format=None):
        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '0,0,0,0')
        bbox = stringToPolygon(bbstr)
        hazards = list(Hazard.objects.filter(geom__within=bbox))
        serializer = s.FilteredHazardSerializer(hazards, many=True)
        return Response(serializer.data)

class FilteredTheftList(APIView):
    """
    List thefts, but filter attributes to theft type, date, description and location.
    Demographic details are not included.
    Initial use case is for the provision of data to Biko.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '0,0,0,0')
        bbox = stringToPolygon(bbstr)

        thefts = list(Theft.objects.filter(geom__within=bbox))
        serializer = s.FilteredTheftSerializer(thefts, many=True)
        return Response(serializer.data)

class OfficialList(APIView):
    """
    List all thefts, or create a new theft.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        official = list(Official.objects.filter(geom__within=bbox))
        serializer = s.OfficialSerializer(official, many=True)
        return Response(serializer.data)

    """ No need to allow submission of official data through the API yet
    def post(self, request, format=None):
        serializer = s.OfficialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """


class AlertAreaList(APIView):
    """
    List all alert areas, or create a new alert area.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        alertareas = list(AlertArea.objects.filter(user=request.user))
        serializer = s.AlertAreaSerializer(alertareas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = s.AlertAreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, email=self.request.user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertAreaDetail(APIView):
    """
    Retrieve, update or delete an alert area instance.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return AlertArea.objects.get(pk=pk)
        except AlertArea.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        alertarea = self.get_object(pk)
        serializer = s.AlertAreaSerializer(alertarea)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        alertarea = self.get_object(pk)
        serializer = s.AlertAreaSerializer(alertarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        alertarea = self.get_object(pk)
        alertarea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = s.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = s.UserSerializer


class GCMDeviceList(APIView):
    """
    List all GCMDevices, or create a new GCMDevice.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        #gcmDevices = list(GCMDevice.objects.filter(user=request.user))
        gcmDevices = list(GCMDevice.objects.all())
        serializer = s.GCMDeviceSerializer(gcmDevices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = s.GCMDeviceSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the registration_id is only in the GCMDevice table once
            if GCMDevice.objects.filter(registration_id = request.data['registration_id']) is not None:
                GCMDevice.objects.filter(registration_id = request.data['registration_id']).delete()
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GCMDeviceDetail(APIView):
    """
    List all GCMDevices, or create a new GCMDevice.
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, registration_id):
        try:
            return GCMDevice.objects.get(registration_id=registration_id)
        except GCMDevice.DoesNotExist:
            raise Http404

    def get(self, request, registration_id, format=None):
        gcmDevice = self.get_object(registration_id)
        serializer = s.GCMDeviceSerializer(gcmDevice)
        return Response(serializer.data)

    def put(self, request, registration_id, format=None):
        gcmDevice = self.get_object(registration_id)
        serializer = s.GCMDeviceSerializer(gcmDevice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, registration_id, format=None):
        gcmDevice = self.get_object(registration_id)
        gcmDevice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APNSDeviceList(APIView):
    """
    List all APNSDevices, or create a new APNSDevice.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        #gcmDevices = list(GCMDevice.objects.filter(user=request.user))
        apnsDevices = list(APNSDevice.objects.all())
        serializer = s.APNSDeviceSerializer(apnsDevices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = s.APNSDeviceSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the registration_id is only in the APNSDevice table once
            if APNSDevice.objects.filter(registration_id = request.data['registration_id']) is not None:
                APNSDevice.objects.filter(registration_id = request.data['registration_id']).delete()
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APNSDeviceDetail(APIView):
    """
    List all APNSDevices, or create a new APNSDevice.
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, registration_id):
        try:
            return APNSDevice.objects.get(registration_id=registration_id)
        except APNSDevice.DoesNotExist:
            raise Http404

    def get(self, request, registration_id, format=None):
        apnsDevice = self.get_object(registration_id)
        serializer = s.APNSDeviceSerializer(apnsDevice)
        return Response(serializer.data)

    def put(self, request, registration_id, format=None):
        apnsDevice = self.get_object(registration_id)
        serializer = s.APNSDeviceSerializer(apnsDevice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, registration_id, format=None):
        apnsDevice = self.get_object(registration_id)
        apnsDevice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IncidentOnlyList(APIView):
    """
    Lists incidents without joining weather data.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        incidents = list(Incident.objects.filter(geom__within=bbox))

        serializer = s.IncidentSerializer(incidents, many=True)
        return Response(serializer.data)


class IncidentList(APIView):
    """
    Old way to list all incident and weather data.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        incidents = list(Incident.objects.filter(geom__within=bbox))

        serializer = s.OldIncidentWeatherSerializer(incidents, many=True)
        return Response(serializer.data)

class IncidentWeatherList(APIView):
    """
    Faster incident weather view
    """
    def get(self, request, format=None):
        # Extract bounding box Url parameter
        try:
            bbstr = request.GET.get('bbox', '-180,-90,180,90')
            bbox = stringToPolygon(bbstr)
            queryset = Weather.objects.select_related('incident').filter(incident__geom__within=bbox)
            serializer = s.WeatherSerializer(queryset, many=True)
            return Response(serializer.data)
        except ValidationError as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# Helper - Create bounding box as a polygon
def stringToPolygon(bbstr):
    try:
        bbsplt = bbstr.split(',')
        # error here
        xmin, ymin, xmax, ymax = [float(x) for x in bbsplt]
        polygon = Polygon.from_bbox((xmin, ymin, xmax, ymax))
    except:
        raise ValidationError(f"There was a validation error parsing your bounding box, 'bbox={bbstr}'. Please entry your query param as a valid polygon in the format xmin, ymin, xmax, ymax. For example, 'bbox=-123,48,-122,49'. There should not be any parentheses or quotes in the query."
        )

    return polygon

#Changes made by Ayan 02/20/18
#added 2 REST API endpoints

class TinyCollisionList(APIView):
    """
    List all collisions
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        collisionsQuerySet = Incident.objects.filter(p_type__exact="collision").filter(geom__within=bbox).exclude(infrastructure_changed=True).order_by('-date')

        serializer = s.TinyIncidentSerializer(collisionsQuerySet, many=True)
        return Response(serializer.data)

class XHRCollisionInfo(APIView):
    """
    List detailed info for a collision
    """
    def get(self, request, format=None):

        # grab the pk and filter and find only the one record that matched
        in_pk = request.GET.get('pk')
        collisionsQuerySet = Incident.objects.get(pk=in_pk)
        serializer = s.TinyXHRIncidentSerializer(collisionsQuerySet, many=False)
        return Response(serializer.data)

class TinyNearMissList(APIView):
    """
    List all Near Misses
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        nearmissQuerySet = Incident.objects.filter(p_type__exact="nearmiss").filter(geom__within=bbox).exclude(infrastructure_changed=True).order_by('-date')

        serializer = s.TinyIncidentSerializer(nearmissQuerySet, many=True)
        return Response(serializer.data)

class XHRNearMissInfo(APIView):
    """
    List detailed info for a collision
    """
    def get(self, request, format=None):

        # grab the pk and filter and find only the one record that matched
        in_pk = request.GET.get('pk')
        collisionsQuerySet = Incident.objects.get(pk=in_pk)
        serializer = s.TinyXHRIncidentSerializer(collisionsQuerySet, many=False)
        return Response(serializer.data)

class TinyHazardList(APIView):
    """
    List all collisions
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)
		#select_related('point').
		#Hazard.objects.select_related('point').exclude(expires_date__lt=now).exclude(hazard_fixed=True).order_by('-date')[:1],
        hazardQuerySet = Hazard.objects.select_related('point').filter(geom__within=bbox).exclude(expires_date__lt=datetime.datetime.now()).exclude(hazard_fixed=True).order_by('-date')

        serializer = s.TinyHazSerializer(hazardQuerySet, many=True)
        return Response(serializer.data)

class XHRHazardInfo(APIView):
    """
    List detailed info for a collision
    """
    def get(self, request, format=None):

        # grab the pk and filter and find only the one record that matched
        in_pk = request.GET.get('pk')
        hazardQuerySet = Hazard.objects.get(pk=in_pk)
        serializer = s.TinyXHRHazSerializer(hazardQuerySet,many=False)
        return Response(serializer.data)


class TinyTheftList(APIView):
    """
    List all collisions
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)

        theftQuerySet = Theft.objects.select_related('point').all().filter(geom__within=bbox).exclude(infrastructure_changed=True).order_by('-date')
        serializer = s.TinyTheftSerializer(theftQuerySet, many=True)
        return Response(serializer.data)

class XHRTheftInfo(APIView):
    """
    List detailed info for a collision
    """
    def get(self, request, format=None):

        # grab the pk and filter and find only the one record that matched
        in_pk = request.GET.get('pk')
        theftQuerySet = Theft.objects.get(pk=in_pk)
        serializer = s.TinyXHRTheftSerializer(theftQuerySet, many=False)
        return Response(serializer.data)

class TinyNewInfrastructureList(APIView):
    """
    List all new infrastructures
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)
		#select_related('point').
        niQuerySet = NewInfrastructure.objects.select_related('point').filter(geom__within=bbox).exclude(expires_date__lt=datetime.datetime.now()).order_by('-date')
        serializer = s.TinyNewInfrastructureSerializer(niQuerySet, many=True)
        return Response(serializer.data)

class XHRNewInfrastructureInfo(APIView):
    """
    List detailed info for a new infrastructure
    """
    def get(self, request, format=None):

        # grab the pk and filter and find only the one record that matched
        in_pk = request.GET.get('pk')
        niQuerySet = NewInfrastructure.objects.get(pk=in_pk)
        serializer = s.TinyXHRNewInfrastructureSerializer(niQuerySet, many=False)
        return Response(serializer.data)
