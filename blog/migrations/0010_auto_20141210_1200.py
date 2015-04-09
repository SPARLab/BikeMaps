# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='body_html',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='post_date',
            field=models.DateTimeField(default=datetime.date(2014, 12, 10), auto_now_add=True),
            preserve_default=False,
        ),
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
