# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0014_auto_20170418_1856'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HazardMessageDistricts',
        ),
    ]
