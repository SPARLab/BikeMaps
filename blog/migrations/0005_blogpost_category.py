# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20141205_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(related_name=b'categoryPost', blank=True, to='blog.Category', null=True),
            preserve_default=True,
        ),
    ]
