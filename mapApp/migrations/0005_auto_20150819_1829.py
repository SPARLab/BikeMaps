# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0004_auto_20150806_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('incident', models.OneToOneField(primary_key=True, serialize=False, to='mapApp.Incident')),
                ('temperature_c', models.FloatField()),
                ('visibility_km', models.FloatField()),
                ('windspeed_kmh', models.FloatField()),
                ('precip_mmh', models.FloatField()),
                ('precip_prob', models.FloatField()),
                ('sunrise_time', models.DateTimeField()),
                ('sunset_time', models.DateTimeField()),
                ('dawn', models.BooleanField()),
                ('dusk', models.BooleanField()),
                ('wind_dir_deg', models.FloatField()),
                ('wind_dir_str', models.CharField(max_length=5)),
                ('black_ice_risk', models.BooleanField()),
                ('summary', models.CharField(max_length=250)),
            ],
        ),
        migrations.RemoveField(
            model_name='incident',
            name='weather',
        ),
    ]
