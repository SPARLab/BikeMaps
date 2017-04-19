# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0025_auto_20170420_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='takeinfile',
            name='districtName',
        ),
        migrations.RemoveField(
            model_name='takeinfile',
            name='shpFile',
        ),
        migrations.RemoveField(
            model_name='takeinfile',
            name='shxFile',
        ),
    ]
