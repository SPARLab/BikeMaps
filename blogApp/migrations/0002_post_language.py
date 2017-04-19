# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='language',
            field=models.CharField(default=b'en', max_length=50, verbose_name='Language', choices=[(b'en', 'English'), (b'fr', 'French')]),
        ),
    ]
