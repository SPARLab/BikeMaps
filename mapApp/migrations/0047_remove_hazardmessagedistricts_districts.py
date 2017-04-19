# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0046_hazardmessagedistricts_districts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='districts',
        ),
    ]
