# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date created')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('email', models.EmailField(max_length=75, verbose_name=b'Current email')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HazardNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action', models.IntegerField(default=4, choices=[(0, 'Incident'), (1, 'Near miss'), (2, 'Hazard'), (3, 'Theft'), (4, 'Undefined')])),
                ('is_read', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
                'verbose_name': 'alert notification',
                'verbose_name_plural': 'alert notifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncidentNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action', models.IntegerField(default=4, choices=[(0, 'Incident'), (1, 'Near miss'), (2, 'Hazard'), (3, 'Theft'), (4, 'Undefined')])),
                ('is_read', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
                'verbose_name': 'alert notification',
                'verbose_name_plural': 'alert notifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date reported')),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name=b'Location')),
                ('date', models.DateTimeField(default=None, verbose_name=b'When was the incident?')),
                ('p_type', models.CharField(max_length=150, verbose_name=b'Type of report', choices=[(b'collision', b'collision'), (b'nearmiss', b'nearmiss'), (b'theft', b'theft'), (b'hazard', b'hazard'), (b'fall', b'fall'), (b'official', b'official')])),
                ('age', models.CharField(blank=True, max_length=15, null=True, verbose_name=b'What is your birth year?', choices=[(b'2002', b'2002'), (b'2001', b'2001'), (b'2000', b'2000'), (b'1999', b'1999'), (b'1998', b'1998'), (b'1997', b'1997'), (b'1996', b'1996'), (b'1995', b'1995'), (b'1994', b'1994'), (b'1993', b'1993'), (b'1992', b'1992'), (b'1991', b'1991'), (b'1990', b'1990'), (b'1989', b'1989'), (b'1988', b'1988'), (b'1987', b'1987'), (b'1986', b'1986'), (b'1985', b'1985'), (b'1984', b'1984'), (b'1983', b'1983'), (b'1982', b'1982'), (b'1981', b'1981'), (b'1980', b'1980'), (b'1979', b'1979'), (b'1978', b'1978'), (b'1977', b'1977'), (b'1976', b'1976'), (b'1975', b'1975'), (b'1974', b'1974'), (b'1973', b'1973'), (b'1972', b'1972'), (b'1971', b'1971'), (b'1970', b'1970'), (b'1969', b'1969'), (b'1968', b'1968'), (b'1967', b'1967'), (b'1966', b'1966'), (b'1965', b'1965'), (b'1964', b'1964'), (b'1963', b'1963'), (b'1962', b'1962'), (b'1961', b'1961'), (b'1960', b'1960'), (b'1959', b'1959'), (b'1958', b'1958'), (b'1957', b'1957'), (b'1956', b'1956'), (b'1955', b'1955'), (b'1954', b'1954'), (b'1953', b'1953'), (b'1952', b'1952'), (b'1951', b'1951'), (b'1950', b'1950'), (b'1949', b'1949'), (b'1948', b'1948'), (b'1947', b'1947'), (b'1946', b'1946'), (b'1945', b'1945'), (b'1944', b'1944'), (b'1943', b'1943'), (b'1942', b'1942'), (b'1941', b'1941'), (b'1940', b'1940'), (b'1939', b'1939'), (b'1938', b'1938'), (b'1937', b'1937'), (b'1936', b'1936'), (b'1935', b'1935'), (b'1934', b'1934'), (b'1933', b'1933'), (b'1932', b'1932'), (b'1931', b'1931'), (b'1930', b'1930'), (b'1929', b'1929'), (b'1928', b'1928'), (b'1927', b'1927'), (b'1926', b'1926'), (b'1925', b'1925'), (b'1924', b'1924'), (b'1923', b'1923'), (b'1922', b'1922'), (b'1921', b'1921'), (b'1920', b'1920'), (b'1919', b'1919'), (b'1918', b'1918'), (b'1917', b'1917'), (b'1916', b'1916'), (b'1915', b'1915'), (b'1914', b'1914'), (b'1913', b'1913'), (b'1912', b'1912'), (b'1911', b'1911'), (b'1910', b'1910'), (b'1909', b'1909'), (b'1908', b'1908'), (b'1907', b'1907'), (b'1906', b'1906'), (b'1905', b'1905'), (b'1904', b'1904'), (b'1903', b'1903')])),
                ('birthmonth', models.CharField(blank=True, max_length=15, null=True, verbose_name=b'What is your birth month?', choices=[(b'1', b'January'), (b'2', b'February'), (b'3', b'March'), (b'4', b'April'), (b'5', b'May'), (b'6', b'June'), (b'7', b'July'), (b'8', b'August'), (b'9', b'September'), (b'10', b'October'), (b'11', b'November'), (b'12', b'December')])),
                ('sex', models.CharField(blank=True, max_length=10, null=True, verbose_name=b'Please select your sex', choices=[(b'M', b'Male'), (b'F', b'Female'), (b'Other', b'Other')])),
                ('details', models.TextField(max_length=300, null=True, verbose_name=b'Please give a brief description of the incident', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Official',
            fields=[
                ('point', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='mapApp.Point')),
                ('official_type', models.CharField(max_length=200)),
                ('data_source', models.CharField(max_length=200)),
                ('metadata', models.CharField(max_length=500)),
                ('who_added', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('mapApp.point',),
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('point', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='mapApp.Point')),
                ('incident_type', models.CharField(max_length=150, verbose_name=b'What type of incident was it?', choices=[(b'Collision', ((b'Collision with stationary object or vehicle', b'Collision with a stationary object or vehicle'), (b'Collision with moving object or vehicle', b'Collision with a moving object or vehicle'))), (b'Near miss', ((b'Near collision with stationary object or vehicle', b'Near miss with a stationary object or vehicle'), (b'Near collision with moving object or vehicle', b'Near miss with a moving object or vehicle'))), (b'Fall', ((b'Fall', b'Lost control and fell'),))])),
                ('incident_with', models.CharField(max_length=100, verbose_name=b'What sort of object did you collide or nearly collide with?', choices=[(b'Vehicle', ((b'Vehicle, head on', b'Head on'), (b'Vehicle, side', b'Side impact'), (b'Vehicle, angle', b'Angle impact'), (b'Vehicle, rear end', b'Rear end'), (b'Vehicle, open door', b'Open vehicle door'))), (b'Person/animal', ((b'Another cyclist', b'Another cyclist'), (b'Pedestrian', b'Pedestrian'), (b'Animal', b'Animal'))), (b'Infrastructure', ((b'Curb', b'Curb'), (b'Train Tracks', b'Train Tracks'), (b'Pothole', b'Pothole'), (b'Lane divider', b'Lane divider'), (b'Sign/Post', b'Sign/Post'), (b'Roadway', b'Roadway'))), (b'Other', b'Other (please describe)')])),
                ('injury', models.CharField(max_length=50, verbose_name=b'Were you injured?', choices=[(b'Yes', ((b'Injury, no treatment', b'Medical treatment not required'), (b'Injury, saw family doctor', b'Saw a family doctor'), (b'Injury, hospital emergency visit', b'Visited the hospital emergency dept.'), (b'Injury, hospitalized', b'Overnight stay in hospital'))), (b'No', ((b'No injury', b'No injury'),))])),
                ('trip_purpose', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What was the purpose of your trip?', choices=[(b'Commute', b'To/from work or school'), (b'Exercise or recreation', b'Exercise or recreation'), (b'Social reason', b'Social reason (e.g., movies, visit friends)'), (b'Personal business', b'Personal business'), (b'During work', b'During work')])),
                ('regular_cyclist', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Do you bike at least once a week?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('helmet', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Were you wearing a helmet?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('intoxicated', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Were you intoxicated?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('road_conditions', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What were the road conditions?', choices=[(b'Dry', b'Dry'), (b'Wet', b'Wet'), (b'Loose sand, gravel, or dirt', b'Loose sand, gravel, or dirt'), (b'Icy', b'Icy'), (b'Snowy', b'Snowy'), (b"Don't remember", b"I don't remember")])),
                ('sightlines', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'How were the sight lines?', choices=[(b'No obstructions', b'No obstructions'), (b'View obstructed', b'View obstructed'), (b'Glare or reflection', b'Glare or reflection'), (b'Obstruction on road', b'Obstruction on road'), (b"Don't Remember", b"Don't Remember")])),
                ('cars_on_roadside', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Were there cars parked on the roadside', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('riding_on', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Where were you riding your bike?', choices=[(b'Busy street', ((b'Busy street bike lane', b'On a painted bike lane'), (b'Busy street, no bike facilities', b'On road with no bike facilities'))), (b'Quiet street', ((b'Quiet street bike lane', b'On a painted bike lane'), (b'Quiet street, no bike facilities', b'On road with no bike facilities'))), (b'Not on the street', ((b'Cycle track', b'On a physically separated bike lane (cycle track)'), (b'Mixed use trail', b'On a mixed use trail'), (b'Sidewalk', b'On the sidewalk'))), (b"Don't remember", b"I don't remember")])),
                ('bike_lights', models.CharField(blank=True, max_length=200, null=True, verbose_name=b'Were you using bike lights?', choices=[(b'NL', b'No Lights'), (b'FB', b'Front and back lights'), (b'F', b'Front lights only'), (b'B', b'Back lights only'), (b"Don't remember", b"I don't remember")])),
                ('terrain', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What was the terrain like?', choices=[(b'Uphill', b'Uphill'), (b'Downhill', b'Downhill'), (b'Flat', b'Flat'), (b"Don't remember", b"I don't remember")])),
                ('direction', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What direction were you heading?', choices=[(b'N', b'N'), (b'NE', b'NE'), (b'E', b'E'), (b'SE', b'SE'), (b'S', b'S'), (b'SW', b'SW'), (b'W', b'W'), (b'NW', b'NW'), (b"I don't know", b"I don't know")])),
                ('turning', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'How were you moving?', choices=[(b'Heading straight', b'Heading straight'), (b'Turning left', b'Turning left'), (b'Turning right', b'Turning right'), (b"I don't remember", b"I don't remember")])),
                ('weather', models.CharField(max_length=100, null=True, verbose_name=b'What was the weather like?', blank=True)),
            ],
            options={
            },
            bases=('mapApp.point',),
        ),
        migrations.CreateModel(
            name='Hazard',
            fields=[
                ('point', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='mapApp.Point')),
                ('hazard_type', models.CharField(max_length=150, verbose_name=b'What type of hazard was it?', choices=[(b'Infrastructure', ((b'Curb', b'Curb'), (b'Island', b'Island'), (b'Train track', b'Train track'), (b'Pothole', b'Pothole'), (b'Road surface', b'Road surface'), (b'Poor signage', b'Poor signage'), (b'Speed limits', b'Speed limits'), (b'Other infrastructure', b'Other infrastructure'))), (b'Other', ((b'Poor visibility', b'Poor visibility'), (b'Parked car', b'Parked car'), (b'Traffic flow', b'Traffic flow'), (b'Driver behaviour', b'Driver behaviour'), (b'Cyclist behaviour', b'Cyclist behaviour'), (b'Pedestrian behaviour', b'Pedestrian behaviour'), (b'Congestion', b'Congestion'), (b'Broken glass', b'Broken glass on road'), (b'Other', b'Other (Please describe)')))])),
                ('regular_cyclist', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Do you bike at least once a week?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
            ],
            options={
            },
            bases=('mapApp.point',),
        ),
        migrations.CreateModel(
            name='Theft',
            fields=[
                ('point', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='mapApp.Point')),
                ('theft_type', models.CharField(max_length=100, verbose_name=b'What was stolen?', choices=[(b'Bike (value < $1000)', b'Bike (value < $1000)'), (b'Bike (value >= $1000)', b'Bike (value >= $1000)'), (b'Major bike component', b'Major bike component (e.g. tire, seat, handlebars, etc.)'), (b'Minor bike component', b'Minor bike component (e.g. lights, topbar padding, bell, etc.)')])),
                ('how_locked', models.CharField(max_length=100, verbose_name=b'Did you have your bike locked?', choices=[(b'Yes', ((b'Frame locked', b'Frame locked'), (b'Frame and tire locked', b'Frame and tire locked'), (b'Frame and both tires locked', b'Frame and both tires locked'), (b'Tire(s) locked', b'Tire(s) locked'))), (b'No', ((b'Not locked', b'Not locked'),))])),
                ('lock', models.CharField(max_length=100, verbose_name=b'What kind of lock were you using?', choices=[(b'U-Lock', b'U-Lock'), (b'Cable lock', b'Cable lock'), (b'U-Lock and cable', b'U-Lock and cable'), (b'Padlock', b'Padlock'), (b'NA', b'Not locked')])),
                ('locked_to', models.CharField(max_length=100, verbose_name=b'Where did you leave your bike?', choices=[(b'Outdoor bike rack', b'At an outdoor bike rack'), (b'Indoor bike rack', b'At an indoor bike rack (e.g. parking garage, bike room)'), (b'Bike locker', b'Inside a bike locker'), (b'Street sign', b'Against street sign'), (b'Fence/railing', b'Against a fence or railing'), (b'Bench', b'Against a public bench'), (b'Indoors/lobby', b'Inside a building/lobby'), (b'Other', b'Other (please describe)')])),
                ('lighting', models.CharField(max_length=100, verbose_name=b'Which describes the lighting conditions where and when the theft occurred?', choices=[(b'Good', b'Well lit (e.g. bright daylight)'), (b'Moderate', b'Moderately well lit (e.g. streetlights, parking garage)'), (b'Poor', b'Poorly lit (e.g. night, unlit alleyway)'), (b"I don't know", b"I don't know")])),
                ('traffic', models.CharField(max_length=100, verbose_name=b'Which best describes the traffic in the area where the theft occurred?', choices=[(b'Very High', b'Very heavy (pedestrians passing by in a nearly constant stream)'), (b'High', b'Heavy (pedestrians passing by regularly)'), (b'Medium', b'Moderate (irregular pedestrian with busy vehicle traffic)'), (b'Low', b'Light (irregular pedestrian with light to moderate vehicle traffic)'), (b'Very Low', b'Very light (little pedestrian and vehicle traffic)'), (b"I don't know", b"I don't know")])),
                ('police_report', models.NullBooleanField(verbose_name=b'Did you file a report with the police?', choices=[(True, b'Yes'), (False, b'No')])),
                ('police_report_num', models.CharField(max_length=100, null=True, verbose_name=b'If you filed a police report, what is the report number?', blank=True)),
                ('insurance_claim', models.NullBooleanField(verbose_name=b'Did you file an insurance claim?', choices=[(True, b'Yes'), (False, b'No')])),
                ('insurance_claim_num', models.CharField(max_length=100, null=True, verbose_name=b'If you filed an insurance claim, what is the claim number?', blank=True)),
                ('regular_cyclist', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Do you bike at least once a week?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
            ],
            options={
            },
            bases=('mapApp.point',),
        ),
        migrations.CreateModel(
            name='TheftNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action', models.IntegerField(default=4, choices=[(0, 'Incident'), (1, 'Near miss'), (2, 'Hazard'), (3, 'Theft'), (4, 'Undefined')])),
                ('is_read', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
                ('point', models.ForeignKey(related_name=b'theftNotification', to='mapApp.Theft')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
                'verbose_name': 'alert notification',
                'verbose_name_plural': 'alert notifications',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='theftnotification',
            unique_together=set([('user', 'point')]),
        ),
        migrations.AddField(
            model_name='incidentnotification',
            name='point',
            field=models.ForeignKey(related_name=b'incidentNotification', to='mapApp.Incident'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incidentnotification',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='incidentnotification',
            unique_together=set([('user', 'point')]),
        ),
        migrations.AddField(
            model_name='hazardnotification',
            name='point',
            field=models.ForeignKey(related_name=b'hazardNotification', to='mapApp.Hazard'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazardnotification',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='hazardnotification',
            unique_together=set([('user', 'point')]),
        ),
    ]
