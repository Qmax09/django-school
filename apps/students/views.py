from registration.decorators import role_required

import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, get_object_or_404
from .models import Student
from simple_history.utils import update_change_reason
from django.utils.decorators import method_decorator

from apps.finance.models import Invoice
from .models import Student, StudentBulkUpload

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(student=self.object)
        return context

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = "__all__"
    success_message = "New student successfully added."

    def get_form(self):
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        form = super().get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form

    def form_valid(self, form):
        student = form.save(commit=False)
        student.save()
        update_change_reason(student, "Student updated via form")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('student-detail', kwargs={'pk': self.object.pk})

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "registration_number",
            "surname",
            "firstname",
            "other_names",
            "gender",
            "parent_number",
            "address",
            "current_class",
        ])

        return response

@role_required(['admin', 'teacher'])
def student_history(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    history = student.history.all()
    return render(request, "students/student_history.html", {"student": student, "history": history})


