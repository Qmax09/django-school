from django.utils.decorators import method_decorator
from registration.decorators import role_required
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from ..staffs.models import Staff
from django.forms import modelformset_factory

from django.views.decorators.csrf import csrf_exempt
from django.db import connection


from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    StudentClassForm,
    SubjectForm,
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
)

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if not obj.current:
            terms = AcademicSession.objects.filter(current=True).exclude(name=obj.name).exists()
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("session-list")
        return super().form_valid(form)

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    template_name = "corecode/term_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "New term successfully added"

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if not obj.current:
            terms = AcademicTerm.objects.filter(current=True).exclude(name=obj.name).exists()
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("term")
        return super().form_valid(form)

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy("terms")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current:
            messages.warning(request, "Cannot delete term as it is set to current")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class ClassListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentClass
    template_name = "corecode/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        context["teachers"] = Staff.objects.all()
        return context

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "New class successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        return context

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    fields = ["name", "teachers"]
    success_url = reverse_lazy("classes")
    success_message = "Class successfully updated."
    template_name = "corecode/mgt_form.html"

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentClass
    success_url = reverse_lazy("classes")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The class {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "New subject successfully added"

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = ["name"]
    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated."
    template_name = "corecode/mgt_form.html"

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("subjects")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The subject {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super().delete(request, *args, **kwargs)

@method_decorator(role_required(['admin', 'teacher']), name='dispatch')
class CurrentSessionAndTermView(LoginRequiredMixin, View):
    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={
            "current_session": AcademicSession.objects.filter(current=True).first(),
            "current_term": AcademicTerm.objects.filter(current=True).first(),
        })
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]
            AcademicSession.objects.update(current=False)
            AcademicTerm.objects.update(current=False)
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicTerm.objects.filter(name=term).update(current=True)
        return render(request, self.template_name, {"form": form})

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

class CorecodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.corecode'

    def ready(self):
        try:
            User = get_user_model()
            admin, created = User.objects.get_or_create(username="admin")
            admin.email = "admin@example.com"
            admin.set_password("admin1234")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            print("✅ Superuser 'admin' created or updated.")
        except (OperationalError, ProgrammingError):
            pass



