# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mapApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date created')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('description', models.CharField(max_length=200)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='users', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hazard',
            name='expires_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='hazard_category',
            field=models.CharField(default='infrastructure', max_length=100, verbose_name='Please select the category of hazard you are reporting:', choices=[(b'infrastructure', 'Infrastructure'), (b'environmental', 'Environmental'), (b'human behaviour', 'Human Behaviour')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hazard',
            name='hazard_fixed',
            field=models.BooleanField(default=False, verbose_name='Has this been fixed?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='hazard_fixed_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazard',
            name='i_type',
            field=models.CharField(max_length=150, verbose_name='What type of hazard was it?', choices=[('Infrastructure', ((b'Curb', 'Curb'), (b'Island', 'Island'), (b'Train track', 'Train track'), (b'Pothole', 'Pothole'), (b'Road surface', 'Road surface'), (b'Poor signage', 'Poor signage'), (b'Speed limits', 'Speed limits'), (b'Other infrastructure', 'Other (Please describe)'))), ('Environmental', ((b'Poor visibility', 'Poor visibility'), (b'Broken glass', 'Broken glass on road'), (b'Wet leaves', 'Wet leaves on road'), (b'Other', 'Other (Please describe)'))), ('Human Behaviour', ((b'Poor visibility', 'Poor visibility'), (b'Parked car', 'Parked car'), (b'Traffic flow', 'Traffic flow'), (b'Driver behaviour', 'Driver behaviour'), (b'Cyclist behaviour', 'Cyclist behaviour'), (b'Pedestrian behaviour', 'Pedestrian behaviour'), (b'Congestion', 'Congestion'), (b'Other', 'Other (Please describe)')))]),
        ),
    ]
