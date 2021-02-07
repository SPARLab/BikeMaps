# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0003_auto_20150721_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrativearea',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='users', blank=True),
        ),
        migrations.AlterField(
            model_name='alertarea',
            name='email',
            field=models.EmailField(max_length=254, verbose_name=b'Current email'),
        ),
    ]
