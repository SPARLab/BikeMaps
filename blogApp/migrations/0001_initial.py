# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date created')),
                ('title', models.CharField(max_length=100, verbose_name=b'Title')),
                ('description', models.CharField(max_length=300, verbose_name=b'Description')),
                ('post_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Date posted')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name=b'Slug', blank=True)),
                ('published', models.BooleanField(default=False, verbose_name=b'Published')),
                ('content', models.TextField(verbose_name=b'Content', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
