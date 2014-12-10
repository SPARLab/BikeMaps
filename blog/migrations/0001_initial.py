# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=75)),
                ('body', models.CharField(max_length=3000)),
                ('slug', models.SlugField(max_length=100)),
                ('is_removed', models.BooleanField(default=False)),
                ('is_private', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=75)),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('is_private', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, to='blog.Category', null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
    ]
