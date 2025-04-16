from django.http import HttpResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def force_migrate(request):
    try:
        call_command("migrate")
        return HttpResponse("✅ Migrations applied.")
    except Exception as e:
        return HttpResponse(f"❌ Migration error: {str(e)}", status=500)
