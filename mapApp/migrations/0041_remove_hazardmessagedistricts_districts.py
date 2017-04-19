# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0040_auto_20170420_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='districts',
        ),
    ]
