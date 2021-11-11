# Exporting subsets of Bikemaps data - example based approach
There isn't a way to externally connect to the remote Bikemaps database. Data must either be exported directly using command line psql on the server, or all of the data can be exported in json format using the Django Admin page and filtered with a script.

This query has a geographic component, so I wanted to be able to use some built in PostGIS functions and am using the directly psql option.

## Query generation
The data request was for any data from North America that includes e-bikes or e-scooters. The geographic data and details field (a description of the incident) are in the 'mapApp_point' table, while other fields relating to ebikes and escooters were in the 'mapApp_incident' table. The incident table includes both 'collision or fall' and 'near miss' incidents. I didn't see any ebike related fields in the hazards or theft tables so these are omitted for now. All queries are run against a view that combines the incident and points table.

### Querying for ebike data
The query searches for any one of the following conditions:
1. bicycle type is 'E-scooter'
2. ebike is 'Yes'
3. incident_with is 'E-scooter'
4. details contains a case-insensitive search for 'e-scooter', 'escooter', 'e-bike', or 'ebike'

### Querying for North American data
I used bboxfinder.com to create a very rough rectangular bounding box around North America. This is an initial option and might need to be refined (for ex, box includes northern tip of South America). I used ST_Intersects to check if the point geom was within my bounding box as defined by ST_MakeEnvelope.

``` sql
with incident_view as (SELECT * FROM "mapApp_incident" LEFT JOIN "mapApp_point" ON ("mapApp_incident".point_id = "mapApp_point".id))
SELECT count(*) FROM incident_view WHERE
ST_Intersects(geom, ST_MakeEnvelope(-168.15, 6.583333, -19.65, 90, 4326)) AND
(bicycle_type = 'E-scooter' OR
ebike = 'Yes' OR
incident_with = 'E-scooter' OR
details ilike '%e-scooter%' OR
details ilike '%e-bike%' OR
details ilike '%escooter%' OR
details ilike '%ebike%');
```

Logging onto the production server, connecting to the database using psql, and running the query returned 184 rows.

## Exporting data
I added all the column names to the query, transformed the geom type to separate lat and long columns, and joined the tables directly without creating a view.

``` sql
SELECT
report_date,
date,
ST_Y (ST_Transform (geom, 4326)) AS lat,
ST_X (ST_Transform (geom, 4326)) AS long,
p_type,
age,
birthmonth,
sex,
details,
source,
infrastructure_changed,
infrastructure_changed_date,
i_type,
incident_with,
injury,
trip_purpose,
regular_cyclist,
helmet,
intoxicated,
road_conditions,
sightlines,
cars_on_roadside,
bike_lights,
terrain,
direction,
turning,
intersection,
aggressive,
impact,
bicycle_type,
ebike,
witness_vehicle,
personal_involvement,
riding_on
FROM "mapApp_incident"
LEFT JOIN "mapApp_point" ON "mapApp_incident".point_id = "mapApp_point".id
WHERE
ST_Intersects(geom, ST_MakeEnvelope(-168.15, 6.583333, -19.65, 90, 4326)) AND
(bicycle_type = 'E-scooter' OR
ebike = 'Yes' OR
incident_with = 'E-scooter' OR
details ilike '%e-scooter%' OR
details ilike '%e-bike%' OR
details ilike '%escooter%' OR
details ilike '%ebike%');
```

The psql command 'copy' was used to output the results to a csv file:

``` sql
\copy (select * from "mapApp_incident" limit 5) TO '~/test_output_file.csv' CSV HEADER
```

'copy' requires the entire query to be on one line, so replacing line breaks with spaces and removing the closing semi colon gives the command:

``` sql
\copy (SELECT report_date, date, ST_Y (ST_Transform (geom, 4326)) AS lat, ST_X (ST_Transform (geom, 4326)) AS long, p_type, age, birthmonth, sex, details, source, infrastructure_changed, infrastructure_changed_date, i_type, incident_with, injury, trip_purpose, regular_cyclist, helmet, intoxicated, road_conditions, sightlines, cars_on_roadside, bike_lights, terrain, direction, turning, intersection, aggressive, impact, bicycle_type, ebike, witness_vehicle, personal_involvement, riding_on FROM "mapApp_incident"  LEFT JOIN "mapApp_point" ON "mapApp_incident".point_id = "mapApp_point".id WHERE ST_Intersects(geom, ST_MakeEnvelope(-168.15, 6.583333, -19.65, 90, 4326)) AND (bicycle_type = 'E-scooter' OR ebike = 'Yes' OR incident_with = 'E-scooter' OR details ilike '%e-scooter%' OR details ilike '%e-bike%' OR details ilike '%escooter%' OR details ilike '%ebike%')) TO '~/NA_ebike_data.csv' CSV HEADER
```

The file was then copied to my local using rsync.
``` bash
rsync -a username@remote_host:/home/bm_admin/NA_ebike_data.csv /Users/finn
```

### Notes
- table names have to be double quoted because capital letters made them case sensitive
- did not do any date transformation, output in default timestamp with timezone format
- used SRID 4326 for postGIS functions, which represents lat/long coordinates using WGS84 standard
