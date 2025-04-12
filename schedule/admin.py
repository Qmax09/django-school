from django.contrib import admin
from .models import Room, TimeSlot, Schedule

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number",)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time")

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("school_class", "subject", "teacher", "day_of_week", "time_slot", "room")
    list_filter = ("school_class", "teacher", "day_of_week")


