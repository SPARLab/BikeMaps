# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0049_auto_20170420_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='cpgFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='dbfFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='prjFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='sbnFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='sbxFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='shpFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='shpXMLFile',
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='shxFile',
        ),
    ]
