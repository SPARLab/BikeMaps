# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0034_auto_20170420_1344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hazardmessagedistricts',
            old_name='geom',
            new_name='districts',
        ),
    ]
