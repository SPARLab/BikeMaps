# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0005_auto_20150819_1829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weather',
            options={'verbose_name': 'Weather', 'verbose_name_plural': 'Weather'},
        ),
        migrations.AlterField(
            model_name='weather',
            name='black_ice_risk',
            field=models.BooleanField(verbose_name=b'Black ice risk present'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='dawn',
            field=models.BooleanField(verbose_name=b'The accident occurred at dawn'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='dusk',
            field=models.BooleanField(verbose_name=b'The accident occurred at dusk'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='precip_mmh',
            field=models.FloatField(verbose_name=b'Precipitation intensity (mm/h)'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='precip_prob',
            field=models.FloatField(verbose_name=b'Precipitation probability'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='summary',
            field=models.CharField(max_length=250, verbose_name=b'Summary'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='sunrise_time',
            field=models.DateTimeField(verbose_name=b'Sunrise time'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='sunset_time',
            field=models.DateTimeField(verbose_name=b'Sunset time'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='temperature_c',
            field=models.FloatField(verbose_name=b'Temperature (C)'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='visibility_km',
            field=models.FloatField(verbose_name=b'Visibility (km)'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_dir_deg',
            field=models.FloatField(verbose_name=b'Wind origin (deg)'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_dir_str',
            field=models.CharField(max_length=5, verbose_name=b'Wind origin'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='windspeed_kmh',
            field=models.FloatField(verbose_name=b'Wind speed (km/h)'),
        ),
    ]
