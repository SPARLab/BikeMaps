from django.contrib.gis import admin

# Register your models here.
from mapApp.models import Incident, Route, AlertArea, AlertNotification

from spirit.models import User
admin.site.register(User)

# class PersonStacked(admin.StackedInline):
#     model = Person
#     verbose_name_plural = "Person"

class IncidentAdmin(admin.OSMGeoAdmin):
	# Map options
	default_lon = -13745000
	default_lat = 6196000
	default_zoom = 10

	# Allow for filtering of report date
	list_filter = ['date']

	list_display = ('pk','date','incident_date', 'incident', 'incident_with','was_published_recently')

	fieldsets = [
	    ('Location', {'fields': ['geom']}),
	    ('Incident', {'fields': ['incident_date', 'incident', 'incident_with', 'injury', 'trip_purpose']}),
	    ('Detail', {'fields': ['incident_detail'], 'classes':['collapse']}),
	    ('Personal', {'fields': ['age', 'sex', 'regular_cyclist', 'helmet', 'intoxicated'], 'classes':['collapse']}),
	    ('Conditions', {'fields': ['road_conditions', 'sightlines', 'cars_on_roadside', 'riding_on', 'bike_lights', 'terrain'], 'classes':['collapse']}),
	]
admin.site.register(Incident, IncidentAdmin)


class AlertAreaAdmin(admin.OSMGeoAdmin):
	# Map options
	default_lon = -13745000
	default_lat = 6196000
	default_zoom = 10

	list_display = ('user', 'email', 'date')

	fieldsets = [
		('Area',	{'fields': ['geom']}),
		('User',	{'fields': ['user','email']})
	]
admin.site.register(AlertArea, AlertAreaAdmin)


class RouteAdmin(admin.OSMGeoAdmin):
	# Map options
	default_lon = -13745000
	default_lat = 6196000
	default_zoom = 10

	# Allow for filtering of report date
	list_filter = ['report_date']

	list_display = ('report_date','trip_purpose', 'frequency','was_published_recently')

	fieldsets = [
		('Route',	{'fields': ['geom']}),
		('Details',	{'fields': ['trip_purpose','frequency']})
	]
admin.site.register(Route, RouteAdmin)



admin.site.register(AlertNotification)