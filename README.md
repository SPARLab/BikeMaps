Bike-maps
=========
[http://bikemaps.org]

### A [SPARLab](http://www.geog.uvic.ca/spar/) project. 
A database driven webapp that allows users to submit bike accidents and near-misses. Data is analyzed to detect areas/routes with high traffic and rates of incidents. 

##### Dependancies
Postgres 9.3
PostGIS 9.3? (whatever the version you can download with postgres is)
Python 2.7
psycopg2
Django 1.7

##### Database setup
The development settings require a Postgres database called "bikeDB" accessible by user "postgres" that is not password protected.

run: 
```
createdb -U postgres bikeDB
psql -U postgres -d bikeDB -c "CREATE EXTENSON postgis;"
```

syncing the tables from the Django app requires running
```
./manage.py makemigrations
./manage.py migrate
```

Additionally, the forum Django app "Spirit" (located at http://spirit-project.com/ and developed by Esteban Castro Borsani) requires it's own cachetable and fixture data be installed
run
```
./manage.py createcachetable spirit_cache
./manage.py loaddata spirit_init
```

If all dependancies have been met, running `./manage.py runserver` should start the development server at 127.0.0.1

Should the app be run in production mode, static files will need to be collected and served from one location. This will require additional settings to be defined in /VicBikeMap/VicBikeMap/settings/prod.py which are not available in this repo for security reasons.

##### Other required Python packages
  A full list of required python packages can be found in requirements.txt and can be installed via pip 
    `pip install -r requirements.txt`


##### Data output
  Data is output by loggin into an admin account and selecting "Data to GeoJson" under the user dropdown menu in the navbar
  This geojson data can be used directly by QGis or converted to a shapefile using ogr2ogr tools.
  The easiest method to convert the output geojson text to a shapefile is to copy it from the webpage and
    past into the "Convert from GeoJSON" box at http://ogre.adc4gis.com/


##### People
  + Dr. Trisalyn Nelson (Project Lead)
  + Taylor Denouden (Developer)
  + James Stephaniuk (Developer)