from django.conf import settings
from django.core import serializers as djserializer
from django.forms import widgets
from push_notifications.models import GCMDevice, APNSDevice
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from mapApp.models import Point, Incident, Hazard, Theft, Official, AlertArea,NewInfrastructure

from django.contrib.auth import get_user_model
User = get_user_model()

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
                  'sightlines', 'cars_on_roadside', 'bike_lights', 'terrain',
                  'direction', 'turning', 'age', 'birthmonth', 'sex', 'pk', 'impact','infrastructure_changed','infrastructure_changed_date')


class IncidentWeatherSerializer(GeoFeatureModelSerializer):
    # HACK There's no elegant way to serialize a one-to-one field that I could find :(
    # Nested relationships makes it hard to analyze the exported data
    weather_summary = serializers.CharField(source='weather.summary')
    weather_sunrise_time = serializers.DateTimeField(source='weather.sunrise_time')
    weather_sunset_time = serializers.DateTimeField(source='weather.sunset_time')
    weather_dawn = serializers.BooleanField(source='weather.dawn')
    weather_dusk = serializers.BooleanField(source='weather.dusk')
    weather_precip_intensity = serializers.FloatField(source='weather.precip_intensity')
    weather_precip_probability = serializers.FloatField(source='weather.precip_probability')
    weather_precip_type = serializers.CharField(source='weather.precip_type')
    weather_temperature = serializers.FloatField(source='weather.temperature')
    weather_black_ice_risk = serializers.BooleanField(source='weather.black_ice_risk')
    weather_wind_speed = serializers.FloatField(source='weather.wind_speed')
    weather_wind_bearing = serializers.FloatField(source='weather.wind_bearing')
    weather_wind_bearing_str = serializers.CharField(source='weather.wind_bearing_str')
    weather_visibility_km = serializers.FloatField(source='weather.visibility_km')

    class Meta:
        model = Incident
        geo_field = 'geom'
        fields = ('i_type', 'incident_with', 'date', 'p_type',
                  'details', 'injury', 'trip_purpose',
                  'regular_cyclist', 'helmet', 'intoxicated', 'road_conditions',
                  'sightlines', 'cars_on_roadside', 'bike_lights', 'terrain',
                  'direction', 'turning', 'age', 'birthmonth', 'sex', 'pk', 'impact', 'weather_summary',
                  'weather_sunrise_time', 'weather_sunset_time', 'weather_dawn', 'weather_dusk',
                  'weather_precip_intensity', 'weather_precip_probability', 'weather_precip_type',
                  'weather_temperature', 'weather_black_ice_risk', 'weather_wind_speed',
                  'weather_wind_bearing', 'weather_wind_bearing_str', 'weather_visibility_km')

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

class FilteredHazardSerializer(GeoFeatureModelSerializer):
    """
    Only serial hazard type, date, description and location, not demographic information.
    Initial use case is for Biko.
    """
    class Meta:
        model = Hazard
        geo_field = 'geom'
        fields = ('i_type', 'date', 'p_type',
                  'details', 'pk')


class FilteredTheftSerializer(GeoFeatureModelSerializer):
    """
    Only serial theft type, date, description and location, not demographic information.
    Initial use case is for Biko.
    """
    class Meta:
        model = Theft
        geo_field = 'geom'
        fields = ('i_type', 'date', 'p_type',
                  'details', 'pk')

class OfficialSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Official
        geo_field = 'geom'
        fields = ('official_type', 'date', 'data_source',
                  'details', 'metadata')


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
        model = APNSDevice
        fields = ('pk', 'name', 'active', 'user', 'date_created', 'registration_id')



#Changes made by Ayan 02/20/18
#added 2 serializer classes

class TinyIncidentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Incident
        geo_field = 'geom'
        fields = ('pk','date')

class TinyXHRIncidentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Incident
        geo_field = 'geom'
        fields = ('pk','i_type', 'incident_with','date','details')

class TinyHazSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hazard
        geo_field = 'geom'
        fields = ('pk','date')

class TinyXHRHazSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hazard
        geo_field = 'geom'
        fields = ('pk','i_type','date','details')

class TinyTheftSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Theft
        geo_field = 'geom'
        fields = ('pk','date')

class TinyXHRTheftSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Theft
        geo_field = 'geom'
        fields = ('pk','i_type','date','details')

class TinyNewInfrastructureSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = NewInfrastructure
        geo_field = 'geom'
        fields = ('pk','dateAdded')

class TinyXHRNewInfrastructureSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = NewInfrastructure
        geo_field = 'geom'
        fields = ('pk','infra_type','dateAdded','details')