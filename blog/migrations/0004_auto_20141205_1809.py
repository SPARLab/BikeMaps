# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date'),
        ),
    ]
