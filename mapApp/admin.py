from django.contrib.gis import admin

# Register models
from mapApp.models import Point, Incident, Hazard, Theft, Official, AdministrativeArea, Weather, NewInfrastructure, Gender

# We need to get the OpenLayers API over HTTPS. By default GeoDjango uses HTTP, so we need to
# subclass OSMGeoAdmin and override the URL source for the API
class SecureOSMGeoAdmin(admin.OSMGeoAdmin):
	openlayers_url='https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'

class GenderAdmin(admin.ModelAdmin):
	# use default config
    pass

admin.site.register(Gender, GenderAdmin)

# admin.site.register(Official)
class PointAdmin(SecureOSMGeoAdmin):
	# Map options
	default_lon = -13745000
	default_lat = 6196000
	default_zoom = 10

	# Allow for filtering of report date
	list_filter = ['report_date', 'date', 'p_type']
	list_display = ('pk','p_type','report_date','date','was_published_recently')

	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('Point', {'fields': ['date', 'p_type']}),
	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
	    ('Personal', {'fields': ['age', 'birthmonth', 'gender', 'gender_additional', ], 'classes':['collapse']})
	]
admin.site.register(Point, PointAdmin)

class WeatherInline(admin.StackedInline):
	model = Weather

class IncidentAdmin(PointAdmin):
	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('Incident', {'fields': ['date', 'i_type', 'incident_with', 'ebike', 'ebike_class', 'ebike_speed', 'injury', 'impact', 'trip_purpose','infrastructure_changed','infrastructure_changed_date']}),
	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
	    ('Personal', {'fields': ['age', 'birthmonth', 'gender', 'gender_additional', 'regular_cyclist', 'helmet', 'intoxicated'], 'classes':['collapse']}),
	    ('Conditions', {'fields': ['road_conditions', 'sightlines', 'cars_on_roadside', 'bike_lights', 'terrain', 'direction', 'turning'], 'classes':['collapse']}),
	]
	inlines = [
		WeatherInline,
	]
admin.site.register(Incident, IncidentAdmin)

class HazardAdmin(PointAdmin):
	list_display = ('pk','p_type','report_date','date','was_published_recently', 'is_expired', 'hazard_fixed_date', 'expires_date')
	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('Hazard', {'fields': ['date', 'i_type', 'hazard_category', 'hazard_fixed', 'hazard_fixed_date', 'expires_date']}),
	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
	    ('Personal', {'fields': ['age', 'birthmonth', 'gender', 'gender_additional', 'regular_cyclist'], 'classes':['collapse']})
	]
admin.site.register(Hazard, HazardAdmin)

class TheftAdmin(PointAdmin):
	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('Theft', {'fields': ['date', 'i_type', 'how_locked', 'lock', 'locked_to', 'lighting', 'traffic', 'police_report', 'insurance_claim','infrastructure_changed','infrastructure_changed_date']}),
	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
	    ('Personal', {'fields': ['regular_cyclist'], 'classes':['collapse']})
	]
admin.site.register(Theft, TheftAdmin)

class NewInfrastructureAdmin(PointAdmin):
	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('NewInfrastructure', {'fields': ['dateAdded','infra_type','expires_date']}),
		('Detail', {'fields': ['infraDetails']})
	]
admin.site.register(NewInfrastructure, NewInfrastructureAdmin)

class HazardAdminsInline(admin.TabularInline):
    model = AdministrativeArea.users.through

class AdminAreaAdmin(admin.OSMGeoAdmin):
	# Map options
	default_lon = -13745000
	default_lat = 6196000
	default_zoom = 10

	list_display = ('description','date')
	search_fields = ['description', 'users', 'users__related_email']

	fields = ['geom', 'description']

	inlines = [
		HazardAdminsInline
	]
	exclude = ('users',)

admin.site.register(AdministrativeArea, AdminAreaAdmin)


# class AlertAreaAdmin(admin.OSMGeoAdmin):
# 	# Map options
# 	default_lon = -13745000
# 	default_lat = 6196000
# 	default_zoom = 10

# 	list_display = ('pk', 'user', 'email', 'date')

# 	fieldsets = [
# 		('Area',	{'fields': ['geom']}),
# 		('User',	{'fields': ['user','email']})
# 	]
# admin.site.register(AlertArea, AlertAreaAdmin)


# admin.site.register(IncidentNotification)
# admin.site.register(HazardNotification)
# admin.site.register(TheftNotification)
