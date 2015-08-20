from django.contrib.gis import admin

# Register models
from mapApp.models import Point, Incident, Hazard, Theft, Official, AdministrativeArea, Weather

# admin.site.register(Official)
class PointAdmin(admin.OSMGeoAdmin):
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
	    ('Personal', {'fields': ['age', 'birthmonth', 'sex', ], 'classes':['collapse']})
	]
admin.site.register(Point, PointAdmin)

class WeatherInline(admin.StackedInline):
	model = Weather

class IncidentAdmin(PointAdmin):
	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('Incident', {'fields': ['date', 'i_type', 'incident_with', 'injury', 'trip_purpose']}),
	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
	    ('Personal', {'fields': ['age', 'birthmonth', 'sex', 'regular_cyclist', 'helmet', 'intoxicated'], 'classes':['collapse']}),
	    ('Conditions', {'fields': ['road_conditions', 'sightlines', 'cars_on_roadside', 'riding_on', 'bike_lights', 'terrain', 'direction', 'turning'], 'classes':['collapse']}),
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
	    ('Personal', {'fields': ['age', 'birthmonth', 'sex', 'regular_cyclist'], 'classes':['collapse']})
	]
admin.site.register(Hazard, HazardAdmin)

class TheftAdmin(PointAdmin):
	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('Theft', {'fields': ['date', 'i_type', 'how_locked', 'lock', 'locked_to', 'lighting', 'traffic', 'police_report', 'insurance_claim']}),
	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
	    ('Personal', {'fields': ['regular_cyclist'], 'classes':['collapse']})
	]
admin.site.register(Theft, TheftAdmin)

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
