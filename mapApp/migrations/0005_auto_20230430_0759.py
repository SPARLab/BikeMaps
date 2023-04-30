# Generated by Django 3.1.7 on 2023-04-30 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0004_auto_20230422_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='gender_additional',
            field=models.TextField(blank=True, default='', max_length=100, null=True, verbose_name="If you selected 'another option', optionally describe here:"),
        ),
        migrations.AlterField(
            model_name='point',
            name='gender',
            field=models.ManyToManyField(blank=True, null=True, to='mapApp.Gender'),
        ),
    ]
