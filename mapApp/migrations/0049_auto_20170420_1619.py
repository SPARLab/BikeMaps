# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0048_auto_20170420_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='cpgFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='dbfFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='prjFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='sbnFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='sbxFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='shpFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='shpXMLFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='hazardmessagedistricts',
            name='shxFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
    ]
