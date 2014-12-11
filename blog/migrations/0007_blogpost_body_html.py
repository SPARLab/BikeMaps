# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogpost_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='body_html',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
