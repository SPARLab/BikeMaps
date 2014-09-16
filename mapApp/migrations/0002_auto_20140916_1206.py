# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='direction',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'What direction were you heading?', choices=[(b'N', b'N'), (b'NE', b'NE'), (b'E', b'E'), (b'SE', b'SE'), (b'S', b'S'), (b'SW', b'SW'), (b'W', b'W'), (b'NW', b'NW'), (b"I don't know", b"I don't know")]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='turning',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'How were you moving?', choices=[(b'Heading straight', b'Heading straight'), (b'Turning left', b'Turning left'), (b'Turning right', b'Turning right'), (b"I don't remember", b"I don't remember")]),
            preserve_default=True,
        ),
    ]
