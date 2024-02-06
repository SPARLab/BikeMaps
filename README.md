BikeMaps
=========
[http://bikemaps.org]

### A [SPARLab](https://www.sparlab.org/) project.
A database driven webapp that allows users to submit cycling collisions, near misses, hazards, and thefts. Data is analyzed to detect areas/routes with high traffic and rates of incidents.

##### Dependencies
  + Python 3.6
  + Postgres 13 + PostGIS
  + psycopg2 2.8.6
  + Django 3.1.7

##### Quick Set Up
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

##### Detailed Set Up
For a more in depth tutorial on setting up the project, please refer to this [additional documentation](docs/set-up-project-mac.md).

##### Data Output

For a more in depth tutorial on querying and exporting data, please refer to the [additional documentation](docs/query-and-export-data.md).


##### People
  + Dr. Trisalyn Nelson (Project Lead)
  + Karen Laberee (Executive Director)
  + Finn Short (Developer)
  + Darren Boss (Developer)
  + Taylor Denouden (Developer)
  + Dan Willett (Developer)
