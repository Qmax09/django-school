from django.contrib import admin
from .models import Staff

class StaffAdmin(admin.ModelAdmin):
    filter_horizontal = ("subjects",)  # Должно разрешить выбор нескольких предметов

admin.site.register(Staff, StaffAdmin)
