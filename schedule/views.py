from registration.decorators import role_required
from .models import Schedule
from .forms import ScheduleForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect

@role_required(['admin', 'teacher', 'student'])
def class_schedule(request):
    schedules = Schedule.objects.all().order_by("day_of_week", "time_slot")
    return render(request, "schedule/class_schedule.html", {"schedules": schedules})

@role_required(['admin', 'teacher', 'student'])
def student_schedule(request, student_id):
    student = Student.objects.get(id=student_id)
    schedules = Schedule.objects.filter(school_class=student.current_class)
    return render(request, "schedule/student_schedule.html", {"student": student, "schedules": schedules})

@role_required(['admin', 'teacher', ])
def teacher_schedule(request, teacher_id):
    teacher = Staff.objects.get(id=teacher_id)
    schedules = Schedule.objects.filter(teacher=teacher)
    return render(request, "schedule/teacher_schedule.html", {"teacher": teacher, "schedules": schedules})

@role_required(['admin', 'teacher'])
def create_schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            day_of_week = form.cleaned_data['day_of_week']
            time_slot = form.cleaned_data['time_slot']
            teacher = form.cleaned_data['teacher']
            school_class = form.cleaned_data['school_class']

            existing_schedule = Schedule.objects.filter(
                day_of_week=day_of_week,
                time_slot=time_slot,
                teacher=teacher,
                school_class=school_class
            ).exists()

            if existing_schedule:
                form.add_error(None, "Это расписание уже существует!")
                return render(request, "schedule/create_schedule.html", {"form": form})

            form.save()
            return redirect("schedule")
    else:
        form = ScheduleForm()

    return render(request, "schedule/create_schedule.html", {"form": form})

@role_required(['admin', 'teacher'])
def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect("schedule")
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, "schedule/edit_schedule.html", {"form": form})

@role_required(['admin', 'teacher'])
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == "POST":
        schedule.delete()
        return redirect("schedule")
    return render(request, "schedule/delete_schedule.html", {"schedule": schedule})
