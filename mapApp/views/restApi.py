from mapApp.models import Incident, Hazard, Theft, Official, AlertArea
from mapApp.serializers import IncidentSerializer, HazardSerializer, TheftSerializer, OfficialSerializer, AlertAreaSerializer, UserSerializer, GCMDeviceSerializer
from django.http import Http404
from django.contrib.gis.geos import Polygon
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, generics, permissions, status
from spirit.models import User
from django.views.decorators.csrf import csrf_exempt
from mapApp.permissions import IsOwnerOrReadOnly
from push_notifications.models import GCMDevice, APNSDevice

class CollisionList(APIView):
    """
    List all collisions, or create a new collision.
    """
    def get(self, request, format=None):
      
        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)
        
        collisions = list(Incident.objects.filter(p_type__exact="collision").filter(geom__within=bbox) | Incident.objects.filter(p_type__exact="fall").filter(geom__within=bbox))

        serializer = IncidentSerializer(collisions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        serializer = IncidentSerializer(nearmiss, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HazardList(APIView):
    """
    List all thefts, or create a new theft.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)
        
        hazards = list(Hazard.objects.filter(geom__within=bbox))
        serializer = HazardSerializer(hazards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HazardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        serializer = TheftSerializer(thefts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TheftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfficialList(APIView):
    """
    List all thefts, or create a new theft.
    """
    def get(self, request, format=None):

        # Extract bounding box Url parameter
        bbstr = request.GET.get('bbox', '-180,-90,180,90')
        bbox = stringToPolygon(bbstr)
        
        official = list(Official.objects.filter(geom__within=bbox))
        serializer = OfficialSerializer(official, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OfficialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertAreaList(APIView):
    """
    List all alert areas, or create a new alert area.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    
    def get(self, request, format=None):
        alertareas = list(AlertArea.objects.filter(user=request.user))
        serializer = AlertAreaSerializer(alertareas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlertAreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
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
        serializer = AlertAreaSerializer(alertarea)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        alertarea = self.get_object(pk)
        serializer = AlertAreaSerializer(alertarea, data=request.data)
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
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GCMDeviceList(APIView):
    """
    List all GCMDevices, or create a new GCMDevice.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    
    def get(self, request, format=None):
        #gcmDevices = list(GCMDevice.objects.filter(user=request.user))
        gcmDevices = list(GCMDevice.objects.all())
        serializer = GCMDeviceSerializer(gcmDevices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GCMDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GCMDeviceDetail(APIView):
    """
    List all GCMDevices, or create a new GCMDevice.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return GCMDevice.objects.get(pk=pk)
        except GCMDevice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        gcmDevice = self.get_object(pk)
        serializer = GCMDeviceSerializer(gcmDevice)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        gcmDevice = self.get_object(pk)
        serializer = GCMDeviceSerializer(gcmDevice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        gcmDevice = self.get_object(pk)
        gcmDevice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
   


# Helper - Create bounding box as a polygon
def stringToPolygon(bbstr):

    bbsplt = bbstr.split(',')
    xmin, ymin, xmax, ymax = [float(x) for x in bbsplt]

    return Polygon.from_bbox((xmin, ymin, xmax, ymax))
