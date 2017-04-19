# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0028_auto_20170420_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='takeinfile',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(default=[1, 1], srid=4326),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'District Name'),
        ),
    ]
