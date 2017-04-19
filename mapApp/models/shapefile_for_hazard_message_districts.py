from django.contrib.gis.utils import LayerMapping
from django.db import models
from django.contrib.gis.db import models
from hazard_message_districts import HazardMessageDistricts
from django.db import IntegrityError
import os


class ShapefilesForHazardMessage(models.Model):
	added = False
	name = models.CharField("District Name", max_length=250, null=True)
	dbfFile = models.FileField(null=True)
	prjFile = models.FileField(null=True)
	shpFile = models.FileField(null=True)
	shxFile = models.FileField(null=True)

	# toString()
	def __str__(self):
		return 'District Name: %s' % self.name

	#Overwrite save
	def save(self, *args, **kwargs):
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
		MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
		path = str(self.shpFile.file)

		#Check if shapefile has already been added
		if os.path.isfile(MEDIA_ROOT+'\\'+path):
			raise IntegrityError("This shapefile has already been added to the database")
		else:
			super(ShapefilesForHazardMessage, self).save(*args, **kwargs)  # Call the "real" save() method.
			#the files are saved in the database and the the media folder
			path = str(self.shpFile.file)
			try:
				mapping = {'districtName': 'D_Name', 'districtShape': 'MultiPolygon', 'regionName': 'R_Name'}
				lm = LayerMapping(HazardMessageDistricts, path, mapping, transform=True, encoding='iso-8859-1')
				lm.save(strict=True, verbose=True)
				self.added = True
			except:
				raise IntegrityError(
					" " + self.name + " was unsuccessfuly added.")

