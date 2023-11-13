from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from v1.base.configs import cRequest
from v1.db.models import SchoolExamResult

from v1.base.configs import cRequest
from v1.db.school.school_exam import SchoolExam
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *


class UpdateSchoolExamResult(LoginRequiredMixin, UpdateView):
    model = SchoolExamResult
    form_class = SchoolExamResultForm
    template_name = 'admin/school/exam/result/edit.html'
    context_object_name = "record"

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:school_exam_details', kwargs={"pk": cRequest.params["exam_id"]})

    def get_context_data(self, **kwargs):
        user = self.request.user
        CHECK_USER_PERMISSION(self.request, self.object.ref_exam.ref_course.ref_school)
        context = super().get_context_data(**kwargs)

        cRequest.params["exam_id"] = context["record"].ref_exam.id

        if user.groups.filter(name='teacher').exists():
            exam_query = SchoolExam.objects.filter(id=self.object.ref_exam.id,ref_course__ref_teacher_name=user)
            if not exam_query.exists():
                raise PermissionDenied()

        context['title'] = ''
        context['exam_id'] = cRequest.params["exam_id"]

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        if obj.ref_exam.ref_exam_type.name == 'Initial':
            obj.ref_application.ap_level = obj.ref_course_level.name
            obj.ref_application.save()
        else:
            obj.ref_school_student.ref_course_level = obj.ref_course_level
            obj.ref_school_student.save()

        messages.success(self.request, 'Successfully Update.')
        return super(__class__, self).form_valid(form)
