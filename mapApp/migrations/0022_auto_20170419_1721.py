# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0021_hazardmessagedistricts_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hazardmessagedistricts',
            old_name='file',
            new_name='shapeFile',
        ),
    ]
