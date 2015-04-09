# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141205_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='post_date',
            field=models.DateTimeField(default=True, auto_now_add=True),
            preserve_default=False,
        ),
    ]
