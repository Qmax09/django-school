from django.apps import AppConfig


class CorecodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.corecode' 

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError
        try:
            User = get_user_model()
            admin, created = User.objects.get_or_create(username='admin')
            admin.email = 'admin@example.com'
            admin.set_password('admin1234')
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            print('✅ Superuser created or updated')
        except (OperationalError, ProgrammingError):
            print('❌ Could not create superuser (db not ready)')



