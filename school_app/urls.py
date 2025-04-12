from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from registration.views import register_view


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("apps.corecode.urls")),
    path("student/", include("apps.students.urls")),
    path("staff/", include("apps.staffs.urls")),
    path("finance/", include("apps.finance.urls")),
    path("result/", include("apps.result.urls")),
    path('admin/', admin.site.urls),
    path("", register_view, name="register"),
    path("register/", register_view, name="register"),
    path("schedule/", include("schedule.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
