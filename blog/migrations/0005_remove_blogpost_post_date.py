# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20141205_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='post_date',
        ),
    ]
