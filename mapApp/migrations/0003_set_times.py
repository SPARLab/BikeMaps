# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def set_times(apps, schema_editor):
    Point = apps.get_model("mapApp", "Point")
    for p in Point.objects.all():
        p.time = p.date.time()
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0002_point_time'),
    ]

    operations = [
        migrations.RunPython(set_times)
    ]
