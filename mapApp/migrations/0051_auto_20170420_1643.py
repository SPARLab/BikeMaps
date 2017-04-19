# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0050_auto_20170420_1638'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TakeInFile',
            new_name='ShapefilesForHazardMessages',
        ),
    ]
