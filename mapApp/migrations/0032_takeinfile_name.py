# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0031_auto_20170420_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='takeinfile',
            name='name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'District Name'),
        ),
    ]
