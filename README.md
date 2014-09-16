Bike-maps
=========
######TODO: Flesh out Readme

[http://bikemaps.org]

### A [SPARLab](http://www.geog.uvic.ca/spar/) project. 
A database driven webapp that allows users to submit bike accidents and near-misses. Data is analyzed to detect areas/routes with high traffic and rates of incidents. 


##### Requirements
  A full list of requirements can be found in requirements.txt and can be easily installed via pip 
    `pip install -r requirements.txt`


##### People
  + Dr. Trisalyn Nelson (Project Lead)
  + Taylor Denouden (Developer)
  + James Stephaniuk (Developer)


##### Setup
  Starting this django project requires the following:
  Prereqs:
  * A postgresql database named bikeDB with postgis extension installed 
  * Install all required python packages by navigating to the project root and running
    `pip install -r requirements.txt`

  Then to get things going, run the following commands:
        ```python manage.py migrate
        python manage.py loaddata spirit_init
        python manage.py createcachetable spirit_cache
        python manage.py collectstatic # If on production server only```

  Then running `python manage.py runserver` and visiting localhost:8000
   should display the dev version of the website

  Change email password in settings.py to allow for new account creation and emails to admin from contact link


##### Data output
  Data is output by loggin into an admin account and selecting "Data to GeoJson" under the user dropdown menu in the navbar
  This geojson data can be used directly by QGis or converted to a shapefile using ogr2ogr tools.
  The easiest method to convert the output geojson text to a shapefile is to copy it from the webpage and
    past into the "Convert from GeoJSON" box at http://ogre.adc4gis.com/
