from django.db import migrations

def add_initial_term(apps, schema_editor):
    AcademicTerm = apps.get_model("corecode", "AcademicTerm")
    AcademicTerm.objects.create(name="1st Term", current=True)

class Migration(migrations.Migration):

    dependencies = [
        ("corecode", "0003_merge_0002_add_initial_session_0002_initial"),  
    ]

    operations = [
        migrations.RunPython(add_initial_term),
    ]
