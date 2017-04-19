# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0045_auto_20170420_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='districts',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True),
        ),
    ]
