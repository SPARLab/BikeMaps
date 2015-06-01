# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='comment_count',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_administrator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_moderator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_ip',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_seen',
        ),
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='user',
            name='timezone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='topic_count',
        ),
    ]
