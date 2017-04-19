from django.db import models
from django.contrib.gis.db import models

class HazardMessageDistricts(models.Model):
	# Outlines of districts that 311 info is available for
	districtName = models.CharField("District Name", max_length=250, null = True)
	regionName = models.CharField("Region Name", max_length=250, null = True)
	# Spatial fields
	# Default CRS -> WGS84
	districtShape = models.MultiPolygonField(null = True)
	objects = models.GeoManager()  # Required to conduct geographic queries







