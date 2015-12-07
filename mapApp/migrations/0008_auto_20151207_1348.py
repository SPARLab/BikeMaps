# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0007_auto_20150820_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='i_type',
            field=models.CharField(max_length=150, verbose_name='What type of hazard was it?', choices=[('Infrastructure', ((b'Curb', 'Curb'), (b'Island', 'Island'), (b'Train track', 'Train track'), (b'Pothole', 'Pothole'), (b'Road surface', 'Road surface'), (b'Poor signage', 'Poor signage'), (b'Speed limits', 'Speed limits'), (b'Other infrastructure', 'Other (Please describe)'))), ('Environmental', ((b'Icy/Snowy', 'Icy/Snowy'), (b'Poor visibility', 'Poor visibility'), (b'Broken glass', 'Broken glass on road'), (b'Wet leaves', 'Wet leaves on road'), (b'Other', 'Other (Please describe)'))), ('Human Behaviour', ((b'Poor visibility', 'Poor visibility'), (b'Parked car', 'Parked car'), (b'Traffic flow', 'Traffic flow'), (b'Driver behaviour', 'Driver behaviour'), (b'Cyclist behaviour', 'Cyclist behaviour'), (b'Pedestrian behaviour', 'Pedestrian behaviour'), (b'Congestion', 'Congestion'), (b'Other', 'Other (Please describe)')))]),
        ),
    ]
