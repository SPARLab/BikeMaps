
from django.db import migrations, models
from mapApp.models import Gender, Point

def move_sex_to_gender(apps, schema_editor):
    gender_f = Gender.objects.get(value='F')
    gender_m = Gender.objects.get(value='M')
    gender_o = Gender.objects.get(value='O')

    for point in Point.objects.filter(sex='F'):
        point.gender.add(gender_f)
    for point in Point.objects.filter(sex='M'):
        point.gender.add(gender_m)
    for point in Point.objects.filter(sex='O'):
        point.gender.add(gender_o)

class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0005_add_gender_options'),
    ]

    operations = [
        migrations.RunPython(move_sex_to_gender)
    ]
