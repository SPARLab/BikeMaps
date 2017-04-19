# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0020_auto_20170419_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
