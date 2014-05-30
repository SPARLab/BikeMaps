from django.contrib.gis import admin

# Register your models here.
from mapApp.models import Incident

# class PersonStacked(admin.StackedInline):
#     model = Person
#     verbose_name_plural = "Person"

class IncidentAdmin(admin.OSMGeoAdmin):
	# Map options
	default_lon = -13745000
	default_lat = 6196000
	default_zoom = 10

	# Allow for filtering of report date
	list_filter = ['report_date']

	list_display = ('report_date','incident_date', 'incident_type', 'incident','was_published_recently','point')

	fieldsets = [
		('Incident information',	{'fields': ['incident_date','incident','incident_detail']}),
		('Location',	{'fields': ['point']}),
		('Trip details',	{'fields': ['trip_purpose', 'road_conditions','sightlines','cars_on_roadside','bike_infrastructure','bike_lights','terrain','helmet'], 'classes':['collapse']}),
		('Injury',	{'fields': ['injury','injury_detail'], 'classes':['collapse']}),
		('Person',	{'fields': ['age','sex','regular_cyclist'], 'classes':['collapse']})
	]


admin.site.register(Incident, IncidentAdmin)