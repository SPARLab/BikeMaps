# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0052_auto_20170513_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='regionName',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Region Name'),
        ),
    ]
