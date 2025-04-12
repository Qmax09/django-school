from registration.decorators import role_required
from django.utils.decorators import method_decorator

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django import forms
from .forms import StaffForm
from .models import Staff
from django.contrib import messages

@method_decorator(role_required(['admin']), name='dispatch')
class StaffListView(ListView):
    model = Staff
@method_decorator(role_required(['admin']), name='dispatch')
class StaffDetailView(DetailView):
    model = Staff
    template_name = "staffs/staff_detail.html"

@method_decorator(role_required(['admin']), name='dispatch')
class StaffCreateView(SuccessMessageMixin, CreateView):
    model = Staff
    form_class = StaffForm
    success_message = "New staff successfully added"
    success_url = reverse_lazy("staff-list")

    def get_form(self):
        form = super().get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["subjects"].widget = widgets.CheckboxSelectMultiple() 
        return form
    
@method_decorator(role_required(['admin']), name='dispatch')
class StaffUpdateView(SuccessMessageMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    success_message = "Record successfully updated."
    success_url = reverse_lazy("staff-list")

    def get_form(self):
        form = super().get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["subjects"].widget = widgets.CheckboxSelectMultiple() 
        return form

@method_decorator(role_required(['admin']), name='dispatch')
class StaffDeleteView(DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")

@role_required(['admin'])
def add_staff(request):
    if request.method == "POST":
        form = StaffForm()
        if form.is_valid():
            form.save()
            messages.success(request, "Новый сотрудник успешно добавлен!")
            return redirect("staff-list")
        else:
            messages.error(request, "Ошибка в заполнении формы.")
    else:
        form = StaffForm()

    return render(request, "staffs/staff_form.html", {"form": form})
