from django.urls import path
from .views import class_schedule, create_schedule, edit_schedule, delete_schedule

urlpatterns = [
    path("", class_schedule, name="schedule"),
    path("create/", create_schedule, name="create_schedule"),
    path("edit/<int:schedule_id>/", edit_schedule, name="edit_schedule"),
    path("delete/<int:schedule_id>/", delete_schedule, name="delete_schedule"),
]