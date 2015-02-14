from django.contrib.gis import admin

# Register models
from mapApp.models import Point
from mapApp.models import Incident
from mapApp.models import Hazard
from mapApp.models import Theft
# from mapApp.models import AlertArea
# from mapApp.models import IncidentNotification, HazardNotification, TheftNotification

from spirit.models import User
admin.site.register(User)

admin.site.register(Incident)
admin.site.register(Hazard)
admin.site.register(Theft)
admin.site.register(Point)



# class IncidentAdmin(admin.OSMGeoAdmin):
# 	class Meta:
# 		model = Incident
#
# 	# Map options
# 	default_lon = -13745000
# 	default_lat = 6196000
# 	default_zoom = 10
#
# 	# Allow for filtering of report date
# 	list_filter = ['report_date']
#
# 	list_display = ('pk','date','report_date', 'incident', 'incident_with','was_published_recently')
#
# 	fieldsets = [
# 	    ('Location', {'fields': ['geom']}),
# 	    ('Incident', {'fields': ['date', 'incident', 'incident_with', 'injury', 'trip_purpose']}),
# 	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
# 	    ('Personal', {'fields': ['age', 'birthmonth', 'sex', 'regular_cyclist', 'helmet', 'intoxicated'], 'classes':['collapse']}),
# 	    ('Conditions', {'fields': ['road_conditions', 'sightlines', 'cars_on_roadside', 'riding_on', 'bike_lights', 'terrain', 'direction', 'turning'], 'classes':['collapse']}),
# 	]
# admin.site.register(Incident, IncidentAdmin)
#
# class HazardAdmin(admin.OSMGeoAdmin):
# 	class Meta:
# 		model = Hazard
#
# 	# Map options
# 	default_lon = -13745000
# 	default_lat = 6196000
# 	default_zoom = 10
#
# 	# Allow for filtering of report date
# 	list_filter = ['report_date']
#
# 	list_display = ('pk','report_date','date', 'hazard','was_published_recently')
#
# 	fieldsets = [
# 	    ('Location', {'fields': ['geom']}),
# 	    ('Hazard', {'fields': ['date', 'hazard']}),
# 	    ('Detail', {'fields': ['details'], 'classes':['collapse']}),
# 	    ('Personal', {'fields': ['age', 'birthmonth', 'sex', 'regular_cyclist'], 'classes':['collapse']})
# 	]
# admin.site.register(Hazard, HazardAdmin)
#
# class TheftAdmin(admin.OSMGeoAdmin):
# 	# Map options
# 	default_lon = -13745000
# 	default_lat = 6196000
# 	default_zoom = 10
#
# 	# Allow for filtering of report date
# 	list_filter = ['date']
#
# 	list_display = ('pk','date','theft_date', 'theft','was_published_recently')
#
# 	fieldsets = [
# 	    ('Location', {'fields': ['geom']}),
# 	    ('Theft', {'fields': ['theft_date', 'theft', 'how_locked', 'lock', 'locked_to', 'lighting', 'traffic', 'police_report', 'insurance_claim']}),
# 	    ('Detail', {'fields': ['theft_detail'], 'classes':['collapse']}),
# 	    ('Personal', {'fields': ['regular_cyclist'], 'classes':['collapse']})
# 	]
# admin.site.register(Theft, TheftAdmin)
#
#
# # class AlertAreaAdmin(admin.OSMGeoAdmin):
# # 	# Map options
# # 	default_lon = -13745000
# # 	default_lat = 6196000
# # 	default_zoom = 10
#
# # 	list_display = ('pk', 'user', 'email', 'date')
#
# # 	fieldsets = [
# # 		('Area',	{'fields': ['geom']}),
# # 		('User',	{'fields': ['user','email']})
# # 	]
# # admin.site.register(AlertArea, AlertAreaAdmin)
#
#
# # admin.site.register(IncidentNotification)
# # admin.site.register(HazardNotification)
# # admin.site.register(TheftNotification)
