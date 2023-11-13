
from django.db import migrations, models
from mapApp.models import Gender

gender_options = [
    ['F', 'Woman'],
    ['M', 'Man'],
    ['NBY', 'Non-binary'],
    ['GNC', 'Genderfluid or Gender nonconforming'],
    ['TS', 'Two-Spirit'],
    ['T', 'Transgender'],
    ['A', 'Agender'],
    ['P', 'Prefer not to say'],
    ['O', 'Another option not listed here'],
]

def populate_gender_options(apps, schema_editor):
    for opt in gender_options:
        g = Gender(value=opt[0], label=opt[1])
        g.save()

def remove_gender_options(apps, schema_editor):
    for opt in gender_options:
        try:
            Gender.objects.get(value=opt[0]).delete()
        # Allow migration to roll back if option has already been deleted
        except Gender.DoesNotExist:
            pass

class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0004_add_gender_fields'),
    ]

    operations = [
        migrations.RunPython(populate_gender_options, remove_gender_options)
    ]