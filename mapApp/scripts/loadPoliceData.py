# .py script to populate database with police shp files. 

# INSTRUCTIONS:
# 
# To execute, run "python manage.py shell" and then in the shell, "execfile('./mapApp/scripts/loadPoliceData.py')". 
#	This will populate the database with the police data from the .shp file.
# 
# Data can then be dumped to stdout redirect with "python manage.py dumpdata --format=xml --indent 2 mapApp.PoliceData > outFileName.xml"
# 	If data is placed in file named /appName/fixtures and names initial_data.xml/json, it will be loaded when syncdb is executed.
# 		If encoding errors arise, try changing the stated encoding in the xml document to utf-16.

import os
from django.contrib.gis.utils import LayerMapping
from mapApp.models import PoliceData

# Auto-generated 'LayerMapping' dictionary for PoliceData model
mapping = {'on_street' : 'ON_STREET',
	'at_street': 'AT_STREET',
    'fatal' : 'FATAL',
    'acc_date' : 'ACC_DATE', 
    'acc_time' : 'ACC_TIME',
    'acc_type' : 'ACC_TYPE',
    'point' : 'POINT25D'
}

data_shp = os.path.abspath(os.path.join(os.path.dirname("__file__"), '../VicBikeMap/mapApp/static/mapApp/data/BikeCollisions_VicPD_2008to2012/BikeCollisions_VicPD_2008to2012.shp'))

lm = LayerMapping(PoliceData, data_shp, mapping)
lm.save(verbose=True) # Save the layermap, imports the data.