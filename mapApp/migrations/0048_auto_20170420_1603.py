# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0047_remove_hazardmessagedistricts_districts'),
    ]

    operations = [
        migrations.AddField(
            model_name='takeinfile',
            name='cpgFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='dbfFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='prjFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='sbnFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='sbxFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='shpFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='shpXMLFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='takeinfile',
            name='shxFile',
            field=models.FileField(null=True, upload_to=b''),
        ),
    ]
