from django.conf import settings
from django.core import serializers as djserializer
from django.forms import widgets
from push_notifications.models import GCMDevice, APNSDevice
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from mapApp.models import Point, Incident, Hazard, Theft, Official, AlertArea
from spirit.models import User


# Serializers for use by restAPI view

class PointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Point
        geo_field = 'geom'
        fields = ('i_type', 'incident_with', 'date', 'p_type',
                  'details')


class IncidentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Incident
        geo_field = 'geom'
        fields = ('i_type', 'incident_with', 'date', 'p_type',
                  'details', 'injury', 'trip_purpose',
                  'regular_cyclist', 'helmet', 'intoxicated', 'road_conditions',
                  'sightlines', 'cars_on_roadside', 'riding_on', 'bike_lights', 'terrain',
                  'direction', 'turning', 'age', 'birthmonth', 'sex', 'pk')


class HazardSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hazard
        geo_field = 'geom'
        fields = ('i_type', 'date', 'p_type',
                  'details', 'age', 'birthmonth', 'sex', 'regular_cyclist', 'pk')


class TheftSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Theft
        geo_field = 'geom'
        fields = ('i_type', 'date', 'p_type',
                  'details', 'how_locked', 'lock', 'locked_to',
                  'lighting', 'traffic', 'police_report', 'police_report_num',
                  'insurance_claim', 'insurance_claim_num', 'regular_cyclist', 'pk')


class OfficialSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Official
        geo_field = 'geom'
        fields = ('official_type', 'date', 'data_source',
                  'details')


class AlertAreaSerializer(GeoFeatureModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = AlertArea
        geo_field = 'geom'
        fields = ('user', 'email', 'pk')


class UserSerializer(serializers.ModelSerializer):
    alertarea_set = serializers.PrimaryKeyRelatedField(many=True, queryset=AlertArea.objects.all())

    class Meta:
        model = User
        fields = ( 'username', 'email', 'id', 'alertarea_set')


class GCMDeviceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta: 
        model = GCMDevice
        fields = ('pk', 'name', 'active', 'user', 'date_created', 'registration_id')


class APNSDeviceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = GCMDevice
        fields = ('name', 'active', 'user', 'date_created', 'registration_id')



