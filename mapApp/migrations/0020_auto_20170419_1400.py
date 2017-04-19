# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0019_hazardmessagedistricts_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='TakeInFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('districtName', models.CharField(max_length=250, verbose_name=b'District Name')),
                ('file', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='hazardmessagedistricts',
            name='file',
        ),
    ]
