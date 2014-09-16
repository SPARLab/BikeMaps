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
            name='Hazard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date reported')),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name=b'Location')),
                ('hazard_date', models.DateTimeField(verbose_name=b'When did you notice the hazard?')),
                ('hazard', models.CharField(max_length=150, verbose_name=b'What type of hazard was it?', choices=[(b'Infrastructure', ((b'Curb', b'Curb'), (b'Island', b'Island'), (b'Train track', b'Train track'), (b'Pothole', b'Pothole'), (b'Road surface', b'Road surface'), (b'Poor signage', b'Poor signage'), (b'Speed limits', b'Speed limits'), (b'Other infrastructure', b'Other infrastructure'))), (b'Other', ((b'Poor visibility', b'Poor visibility'), (b'Parked car', b'Parked car'), (b'Traffic flow', b'Traffic flow'), (b'Driver behaviour', b'Driver behaviour'), (b'Pedestrian behaviour', b'Pedestrian behaviour'), (b'Congestion', b'Congestion'), (b'Broken glass', b'Broken glass on road'), (b'Other', b'Other (Please describe)')))])),
                ('age', models.CharField(blank=True, max_length=15, null=True, verbose_name=b'Please tell us which age category you fit into', choices=[(b'<19', b'19 or under'), (b'19-29', b'19 - 29'), (b'30-39', b'30 - 39'), (b'40-49', b'40 - 49'), (b'50-59', b'50 - 59'), (b'60-69', b'60 - 69'), (b'>70', b'70 or over')])),
                ('sex', models.CharField(blank=True, max_length=10, null=True, verbose_name=b'Please select your sex', choices=[(b'M', b'Male'), (b'F', b'Female'), (b'Other', b'Other')])),
                ('regular_cyclist', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Do you bike at least once a week?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('hazard_detail', models.TextField(max_length=300, null=True, verbose_name=b'Please give a brief description of the hazard', blank=True)),
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
                ('point', models.ForeignKey(related_name=b'+', to='mapApp.Hazard')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date reported')),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name=b'Location')),
                ('incident_date', models.DateTimeField(verbose_name=b'When was the incident?')),
                ('incident', models.CharField(max_length=150, verbose_name=b'What type of incident was it?', choices=[(b'Collision', ((b'Collision with stationary object or vehicle', b'Collision with a stationary object or vehicle'), (b'Collision with moving object or vehicle', b'Collision with a moving object or vehicle'))), (b'Near miss', ((b'Near collision with stationary object or vehicle', b'Near miss with a stationary object or vehicle'), (b'Near collision with moving object or vehicle', b'Near miss with a moving object or vehicle'))), (b'Fall', ((b'Fall', b'Lost control and fell'),))])),
                ('incident_with', models.CharField(max_length=100, verbose_name=b'What sort of object did you collide or nearly collide with?', choices=[(b'Vehicle', ((b'Vehicle, head on', b'Head on'), (b'Vehicle, side', b'Side impact'), (b'Vehicle, angle', b'Angle impact'), (b'Vehicle, rear end', b'Rear end'), (b'Vehicle, open door', b'Open vehicle door'))), (b'Person/animal', ((b'Another cyclist', b'Another cyclist'), (b'Pedestrian', b'Pedestrian'), (b'Animal', b'Animal'))), (b'Infrastructure', ((b'Curb', b'Curb'), (b'Train Tracks', b'Train Tracks'), (b'Pothole', b'Pothole'), (b'Lane divider', b'Lane divider'), (b'Sign/Post', b'Sign/Post'), (b'Roadway', b'Roadway'))), (b'Other', b'Other (please describe)')])),
                ('injury', models.CharField(max_length=50, verbose_name=b'Were you injured?', choices=[(b'Yes', ((b'Injury, no treatment', b'Medical treatment not required'), (b'Injury, saw family doctor', b'Saw a family doctor'), (b'Injury, hospital emergency visit', b'Visited the hospital emergency dept.'), (b'Injury, hospitalized', b'Overnight stay in hospital'))), (b'No', ((b'No injury', b'No injury'),))])),
                ('trip_purpose', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What was the purpose of your trip?', choices=[(b'Commute', b'To/from work or school'), (b'Exercise or recreation', b'Exercise or recreation'), (b'Social reason', b'Social reason (e.g., movies, visit friends)'), (b'Personal business', b'Personal business'), (b'During work', b'During work')])),
                ('age', models.CharField(blank=True, max_length=15, null=True, verbose_name=b'Please tell us which age category you fit into', choices=[(b'<19', b'19 or under'), (b'19-29', b'19 - 29'), (b'30-39', b'30 - 39'), (b'40-49', b'40 - 49'), (b'50-59', b'50 - 59'), (b'60-69', b'60 - 69'), (b'>70', b'70 or over')])),
                ('sex', models.CharField(blank=True, max_length=10, null=True, verbose_name=b'Please select your sex', choices=[(b'M', b'Male'), (b'F', b'Female'), (b'Other', b'Other')])),
                ('regular_cyclist', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Do you bike at least once a week?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('helmet', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Were you wearing a helmet?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('intoxicated', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Were you intoxicated?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('road_conditions', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What were the road conditions?', choices=[(b'Dry', b'Dry'), (b'Wet', b'Wet'), (b'Loose sand, gravel, or dirt', b'Loose sand, gravel, or dirt'), (b'Icy', b'Icy'), (b'Snowy', b'Snowy'), (b"Don't remember", b"I don't remember")])),
                ('sightlines', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'How were the sight lines?', choices=[(b'No obstructions', b'No obstructions'), (b'View obstructed', b'View obstructed'), (b'Glare or reflection', b'Glare or reflection'), (b'Obstruction on road', b'Obstruction on road'), (b"Don't Remember", b"Don't Remember")])),
                ('cars_on_roadside', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Were there cars parked on the roadside', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('riding_on', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Where were you riding your bike?', choices=[(b'Busy street', ((b'Busy street bike lane', b'On a painted bike lane'), (b'Busy street, no bike facilities', b'On road with no bike facilities'))), (b'Quiet street', ((b'Quiet street bike lane', b'On a painted bike lane'), (b'Quiet street, no bike facilities', b'On road with no bike facilities'))), (b'Not on the street', ((b'Cycle track', b'On a physically separated bike lane (cycle track)'), (b'Mixed use trail', b'On a mixed use trail'), (b'Sidewalk', b'On the sidewalk'))), (b"Don't remember", b"I don't remember")])),
                ('bike_lights', models.CharField(blank=True, max_length=200, null=True, verbose_name=b'Were you using bike lights?', choices=[(b'NL', b'No Lights'), (b'FB', b'Front and back lights'), (b'F', b'Front lights only'), (b'B', b'Back lights only'), (b"Don't remember", b"I don't remember")])),
                ('terrain', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What was the terrain like?', choices=[(b'Uphill', b'Uphill'), (b'Downhill', b'Downhill'), (b'Flat', b'Flat'), (b"Don't remember", b"I don't remember")])),
                ('incident_detail', models.TextField(max_length=300, null=True, verbose_name=b'Please give a brief description of the incident', blank=True)),
                ('weather', models.CharField(max_length=100, null=True, verbose_name=b'What was the weather like?', blank=True)),
            ],
            options={
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
                ('point', models.ForeignKey(related_name=b'+', to='mapApp.Incident')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Theft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date reported')),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name=b'Location')),
                ('theft_date', models.DateTimeField(verbose_name=b'When did notice that you had been robbed?')),
                ('theft', models.CharField(max_length=100, verbose_name=b'What was stolen?', choices=[(b'Bike (value < $1000)', b'Bike (value < $1000)'), (b'Bike (value >= $1000)', b'Bike (value >= $1000)'), (b'Major bike component', b'Major bike component (e.g. tire, seat, handlebars, etc.)'), (b'Minor bike component', b'Minor bike component (e.g. lights, topbar padding, bell, etc.)')])),
                ('how_locked', models.CharField(max_length=100, verbose_name=b'Did you have your bike locked?', choices=[(b'Yes', ((b'Frame locked', b'Frame locked'), (b'Frame and tire locked', b'Frame and tire locked'), (b'Frame and both tires locked', b'Frame and both tires locked'), (b'Tire(s) locked', b'Tire(s) locked'))), (b'No', ((b'Not locked', b'Not locked'),))])),
                ('lock', models.CharField(max_length=100, verbose_name=b'What kind of lock were you using?', choices=[(b'U-Lock', b'U-Lock'), (b'Cable lock', b'Cable lock'), (b'U-Lock and cable', b'U-Lock and cable'), (b'Padlock', b'Padlock'), (b'NA', b'Not locked')])),
                ('locked_to', models.CharField(max_length=100, verbose_name=b'Where did you leave your bike?', choices=[(b'Outdoor bike rack', b'At an outdoor bike rack'), (b'Indoor bike rack', b'At an indoor bike rack (e.g. parking garage, bike room)'), (b'Bike locker', b'Inside a bike locker'), (b'Street sign', b'Against street sign'), (b'Fence/railing', b'Against a fence or railing'), (b'Bench', b'Against a public bench'), (b'Indoors/lobby', b'Inside a building/lobby'), (b'Other', b'Other (please describe)')])),
                ('lighting', models.CharField(max_length=100, verbose_name=b'Which describes the lighting conditions where and when the theft occurred?', choices=[(b'Good', b'Well lit (e.g. bright daylight)'), (b'Moderate', b'Moderately well lit (e.g. streetlights, parking garage)'), (b'Poor', b'Poorly lit (e.g. night, unlit alleyway)'), (b"I don't know", b"I don't know")])),
                ('traffic', models.CharField(max_length=100, verbose_name=b'Which best describes the traffic in the area where the theft occurred?', choices=[(b'Very High', b'Very heavy (pedestrians passing by in a nearly constant stream)'), (b'High', b'Heavy (pedestrians passing by regularly)'), (b'Medium', b'Moderate (irregular pedestrian with busy vehicle traffic)'), (b'Low', b'Light (irregular pedestrian with light to moderate vehicle traffic)'), (b'Very Low', b'Very light (little pedestrian and vehicle traffic)'), (b"I don't know", b"I don't know")])),
                ('police_report', models.NullBooleanField(verbose_name=b'Did you file a report with the police?', choices=[(True, b'Yes'), (False, b'No')])),
                ('insurance_claim', models.NullBooleanField(verbose_name=b'Did you file an insurance claim?', choices=[(True, b'Yes'), (False, b'No')])),
                ('regular_cyclist', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Do you bike at least once a week?', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b"I don't know", b"I don't know")])),
                ('theft_detail', models.TextField(max_length=300, null=True, verbose_name=b'Please give a brief description about what happened.', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TheftNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action', models.IntegerField(default=4, choices=[(0, 'Incident'), (1, 'Near miss'), (2, 'Hazard'), (3, 'Theft'), (4, 'Undefined')])),
                ('is_read', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
                ('point', models.ForeignKey(related_name=b'+', to='mapApp.Theft')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
