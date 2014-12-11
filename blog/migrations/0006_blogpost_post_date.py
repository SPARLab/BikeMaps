# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_blogpost_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 5, 18, 15, 26, 847995), auto_now_add=True),
            preserve_default=False,
        ),
    ]
