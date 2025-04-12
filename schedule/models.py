from django.db import models
from apps.staffs.models import Staff
from apps.corecode.models import StudentClass, Subject


DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
]

class Room(models.Model):
    
    number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Room {self.number}"

class TimeSlot(models.Model):
    
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class Schedule(models.Model):
    
    school_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"{self.school_class} - {self.subject} ({self.day_of_week} {self.time_slot})"

