# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0016_hazardmessagedistricts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HazardMessageDistricts',
        ),
    ]
