# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogpost_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=models.TextField(null=True, blank=True),
        ),
    ]
