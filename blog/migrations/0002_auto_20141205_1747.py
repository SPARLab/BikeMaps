# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
    ]
