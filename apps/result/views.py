from registration.decorators import role_required
from django.utils.decorators import method_decorator
from utils.telegram import send_message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View
from .models import AcademicTerm
from ..students.models import Student
from .forms import CreateResults, EditResults
from .models import Result

@login_required
@role_required(['admin', 'teacher'])
def create_result(request):
    students = Student.objects.all()
    if request.method == "POST":
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                subjects = form.cleaned_data["subjects"]
                session = form.cleaned_data["session"]
                term = form.cleaned_data["term"]
                students = request.POST["students"]
                results = []
                for student in students.split(","):
                    stu = Student.objects.get(pk=student)
                    if stu.current_class:
                        for subject in subjects:
                            check = Result.objects.filter(
                                session=session,
                                term=term,
                                current_class=stu.current_class,
                                subject=subject,
                                student=stu,
                            ).first()
                            if not check:
                                results.append(
                                    Result(
                                        session=session,
                                        term=term,
                                        current_class=stu.current_class,
                                        subject=subject,
                                        student=stu,
                                    )
                                )
                Result.objects.bulk_create(results)
                
                student_names = ", ".join(set([f"{r.student.firstname} {r.student.surname}" for r in results]))
                subject_names = ", ".join(set([r.subject.name for r in results]))
                class_name = results[0].current_class.name if results else "Unknown class"
                
                message = (
                    f"📢 *New Grades Submitted!*\n\n"
                    f"👩‍🏫 Teacher: *{request.user.get_full_name() or request.user.username}*\n"
                    f"👨‍🎓 Students: *{student_names}*\n"
                    f"📘 Subjects: *{subject_names}*\n"
                    f"🏫 Class: *{class_name}*\n"
                    f"📅 Session: *{session}* | Term: *{term}*\n"
                )
                
                send_message(message)
                

                

                return redirect("edit-results")

        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "term": request.current_term,
                }
            )
            studentlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didn't select any student.")
    return render(request, "result/create_result.html", {"students": students})

@login_required
@role_required(['admin', 'teacher'])
def edit_results(request):
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        form = EditResults(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})

@method_decorator(role_required(['admin', 'teacher', 'student']), name='dispatch')
class ResultListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        results = Result.objects.filter(
            session=request.current_session,
            term=AcademicTerm.objects.filter(current=True).first()
        )
        bulk = {}

        for result in results:
            test_total = 0
            exam_total = 0
            subjects = []
            for subject in results:
                if subject.student == result.student:
                    subjects.append(subject)
                    test_total += subject.test_score
                    exam_total += subject.exam_score

            bulk[result.student.id] = {
                "student": result.student,
                "subjects": subjects,
                "test_total": test_total,
                "exam_total": exam_total,
                "total_total": test_total + exam_total,
            }

        context = {"results": bulk}
        return render(request, "result/all_results.html", context)


