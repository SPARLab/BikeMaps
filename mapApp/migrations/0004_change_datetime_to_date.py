# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0003_set_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='date',
            field=models.DateField(default=None, verbose_name=b'When was the incident?'),
        ),
    ]
