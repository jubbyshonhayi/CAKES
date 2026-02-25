from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import StudentForm
from .models import Student


class SchoolUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_school_user and user.school.status == 'active'

    def handle_no_permission(self):
        raise Http404('Not found')


class SchoolScopedStudentMixin(LoginRequiredMixin, SchoolUserRequiredMixin):
    model = Student

    def get_queryset(self):
        return Student.objects.for_user(self.request.user).select_related('school')


class StudentListView(SchoolScopedStudentMixin, ListView):
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 25


class StudentDetailView(SchoolScopedStudentMixin, DetailView):
    template_name = 'students/student_detail.html'


class StudentCreateView(SchoolScopedStudentMixin, CreateView):
    template_name = 'students/student_form.html'
    form_class = StudentForm
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)


class StudentUpdateView(SchoolScopedStudentMixin, UpdateView):
    template_name = 'students/student_form.html'
    form_class = StudentForm
    success_url = reverse_lazy('student-list')


class StudentDeleteView(SchoolScopedStudentMixin, DeleteView):
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')
