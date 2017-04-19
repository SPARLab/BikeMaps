# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0011_auto_20170418_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='HazardMessageDistricts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('districtName', models.CharField(max_length=250, verbose_name=b'District Name')),
            ],
        ),
    ]
