# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20141205_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=models.TextField(),
        ),
    ]
