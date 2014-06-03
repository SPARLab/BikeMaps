# .py script to populate database with police shp files. 

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