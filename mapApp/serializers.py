from django.conf import settings
from django.forms import widgets
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
        fields = ('i_type', 'date', 'p_type',
                  'details')


class HazardSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hazard
        geo_field = 'geom'
        fields = ('i_type', 'date', 'p_type',
                  'details')


class TheftSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Theft
        geo_field = 'geom'
        fields = ('i_type', 'date', 'p_type',
                  'details')


class OfficialSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Official
        geo_field = 'geom'
        fields = ('official_type', 'date', 'data_source',
                  'details')


class AlertAreaSerializer(GeoFeatureModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = AlertArea
        geo_field = 'geom'
        fields = ('user', 'email', 'user', 'pk')


class UserSerializer(serializers.ModelSerializer):
    alertarea_set = serializers.PrimaryKeyRelatedField(many=True, queryset=AlertArea.objects.all())

    class Meta:
        model = User
        fields = ( 'username', 'email', 'id', 'alertarea_set')



