from django.db import migrations

def add_academic_session(apps, schema_editor):
    AcademicSession = apps.get_model("corecode", "AcademicSession")
    AcademicSession.objects.create(name="2024/2025", current=True)

class Migration(migrations.Migration):
    dependencies = [
        ("corecode", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_academic_session),
    ]
