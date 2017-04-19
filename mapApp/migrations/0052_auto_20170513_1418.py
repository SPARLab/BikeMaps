# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0051_auto_20170420_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shapefilesforhazardmessages',
            name='cpgFile',
        ),
        migrations.RemoveField(
            model_name='shapefilesforhazardmessages',
            name='sbnFile',
        ),
        migrations.RemoveField(
            model_name='shapefilesforhazardmessages',
            name='sbxFile',
        ),
        migrations.RemoveField(
            model_name='shapefilesforhazardmessages',
            name='shpXMLFile',
        ),
    ]
