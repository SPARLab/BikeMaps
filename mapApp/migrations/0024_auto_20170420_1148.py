# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0023_auto_20170419_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='takeinfile',
            old_name='file',
            new_name='shpFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='shpFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='shxFile',
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='shxFile',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
