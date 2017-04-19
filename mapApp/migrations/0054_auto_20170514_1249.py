# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0053_hazardmessagedistricts_regionname'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShapefilesForHazardMessages',
            new_name='ShapefilesForHazardMessage',
        ),
    ]
