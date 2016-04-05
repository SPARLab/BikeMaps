# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0009_auto_20160113_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='impact',
            field=models.CharField(max_length=50, null=True, verbose_name='How did this incident impact your bicycling?', choices=[(b'None', 'No impact'), (b'More careful', "I'm now more careful about where/when I ride"), (b'Bike less', 'I bike less'), (b'More careful and bike less', "I'm now more careful about where/when I ride AND I bike less"), (b'Stopped biking', "I haven't biked since"), (b'Too soon', 'Too soon to say')]),
        ),
    ]
