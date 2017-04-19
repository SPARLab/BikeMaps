# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0022_auto_20170419_1721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hazardmessagedistricts',
            old_name='shapeFile',
            new_name='shpFile',
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='shxFile',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='hazardmessagedistricts',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True),
        ),
    ]
