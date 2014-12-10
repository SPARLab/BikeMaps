# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20141205_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default=datetime.date(2014, 12, 5), unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=datetime.date(2014, 12, 5), unique=True),
            preserve_default=False,
        ),
    ]
