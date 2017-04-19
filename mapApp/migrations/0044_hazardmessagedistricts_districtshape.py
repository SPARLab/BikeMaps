# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0043_remove_hazardmessagedistricts_districts'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='districtShape',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True),
        ),
    ]
