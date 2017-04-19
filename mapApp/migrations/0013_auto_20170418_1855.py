# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0012_hazardmessagedistricts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Districts',
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(default=1, srid=4326),
            preserve_default=False,
        ),
    ]
