# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0030_auto_20170420_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='takeinfile',
            name='geom',
        ),
        migrations.RemoveField(
            model_name='takeinfile',
            name='name',
        ),
    ]
