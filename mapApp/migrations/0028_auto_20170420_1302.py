# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0027_auto_20170420_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazardmessagedistricts',
            name='districtName',
            field=models.CharField(max_length=250, null=True, verbose_name=b'District Name'),
        ),
    ]
