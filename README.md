BikeMaps
=========
[http://bikemaps.org]

### A [SPARLab](http://www.geog.uvic.ca/spar/) project.
A database driven webapp that allows users to submit bike accidents and near-misses. Data is analyzed to detect areas/routes with high traffic and rates of incidents.

##### Dependencies
  + Python 2.7
  + Postgres 9.3 + PostGIS
  + psycopg2
  + Django 1.8

##### Database setup
The development settings require a Postgres database called "bikeDB" accessible by user "postgres" that is not password protected. Be sure to add the postGIS extension. From the terminal, run:
```
createdb -U postgres bikeDB
psql -U postgres -d bikeDB -c "CREATE EXTENSION postgis;"
```

Syncing the tables from the Django app requires running
```
./manage.py makemigrations
./manage.py migrate
```

A full list of required python packages can be found in requirements.txt and can be installed via pip
    `pip install -r requirements.txt`

If all dependencies have been met, running `./manage.py runserver` should start the development server at 127.0.0.1:8000

_Note: There are additional requirements for serving this application in a production setting, and the relevant Django documentation should be consulted in this scenario. This repo does not provide production settings for security reasons._


##### Data output
  Data is output by logging into an admin account and selecting the relevant "Export" link under the user dropdown menu in the navbar
  This geojson data can be used directly by QGis or converted to a shapefile using ogr2ogr tools.
  The easiest method to convert the output geojson text to a shapefile is to copy it from the webpage and
    past into the "Convert from GeoJSON" box at http://ogre.adc4gis.com/


##### People
  + Dr. Trisalyn Nelson (Project Lead)
  + Taylor Denouden (Developer)
  + Darren Boss (Developer)
