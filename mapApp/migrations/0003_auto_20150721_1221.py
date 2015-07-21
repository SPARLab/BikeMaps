# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0002_auto_20150720_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='hazard_category',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Please select the category of hazard you are reporting:', choices=[(b'infrastructure', 'Infrastructure'), (b'environmental', 'Environmental'), (b'human behaviour', 'Human Behaviour')]),
        ),
    ]
