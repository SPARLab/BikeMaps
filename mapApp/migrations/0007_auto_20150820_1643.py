# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0006_auto_20150820_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weather',
            old_name='precip_mmh',
            new_name='precip_intensity',
        ),
        migrations.RenameField(
            model_name='weather',
            old_name='precip_prob',
            new_name='precip_probability',
        ),
        migrations.RenameField(
            model_name='weather',
            old_name='temperature_c',
            new_name='temperature',
        ),
        migrations.RenameField(
            model_name='weather',
            old_name='wind_dir_deg',
            new_name='wind_bearing',
        ),
        migrations.RenameField(
            model_name='weather',
            old_name='wind_dir_str',
            new_name='wind_bearing_str',
        ),
        migrations.RenameField(
            model_name='weather',
            old_name='windspeed_kmh',
            new_name='wind_speed',
        ),
        migrations.AddField(
            model_name='weather',
            name='precip_type',
            field=models.CharField(default='', max_length=50, verbose_name=b'Type of precipitation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_bearing',
            field=models.FloatField(verbose_name=b'Wind bearing (deg)'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_bearing_str',
            field=models.CharField(max_length=5, verbose_name=b'Wind bearing'),
        ),
    ]
