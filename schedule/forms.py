from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["school_class", "subject", "teacher", "day_of_week", "time_slot", "room"]

    def clean(self):
        cleaned_data = super().clean()
        school_class = cleaned_data.get("school_class")
        teacher = cleaned_data.get("teacher")
        day_of_week = cleaned_data.get("day_of_week")
        time_slot = cleaned_data.get("time_slot")

        if not teacher or not day_of_week or not time_slot:
            return cleaned_data  

       
        teacher_conflict = Schedule.objects.filter(
            teacher=teacher,
            day_of_week=day_of_week,
            time_slot=time_slot
        )

        
        if self.instance.pk:
            teacher_conflict = teacher_conflict.exclude(pk=self.instance.pk)

        if teacher_conflict.exists():
            raise forms.ValidationError("This teacher is already assigned to another class at this time.")

        return cleaned_data
