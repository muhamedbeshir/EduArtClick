from datetime import date, timedelta
from typing import Any, Dict
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from v1.db.master.school import School
from v1.db.master.school_course import SchoolCourse
from v1.db.school.school_setting import SchoolSetting
from v1.db.user.profile import SchoolStudentUserProfile
from v1.web.utils import CHECK_USER_PERMISSION
from v1.web.views.admin.master.school.sslue import SelectiveStudentExam
from v1.base.configs import cRequest
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction

from v1.web.views.admin.master.school.sslue.forms import SelectiveStudentExamForm


class AddSelectiveSchoolExam(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_selectivestudentexam',)
    template_name = 'admin/school/sslue/add.html'
    model = SelectiveStudentExam
    form_class = SelectiveStudentExamForm

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get( "pk" )
        self.course = get_object_or_404(SchoolCourse, pk=course_id)
        CHECK_USER_PERMISSION(self.request, self.course.ref_school)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('web:details_school_course', kwargs={'pk': self.object.ref_course.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Assign Student Exam"
        context['course'] = self.course
        context['school'] = self.course.ref_school
        return context
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['course_id'] = self.kwargs.get( "pk" )
        return kwargs
    
    def form_valid(self, form):
        selected_students = self.request.POST.getlist('selected_student', None)

        school_id = cRequest.params[ "school_id" ]
        cRequest.params[ "school_id" ] = school_id
        
        school = get_object_or_404(School, pk=school_id)
        students = SchoolStudentUserProfile.objects.filter(id__in=selected_students)

        try:
            with transaction.atomic():
                obj = form.save(commit=False)
                obj.ref_school = school
                obj.save()
                obj.ref_student.set(students)
                obj.save()
                messages.success(self.request, 'Successfully Added.')
                return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'You can not add more than one'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class DeleteSelectiveSchoolExam(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_selectivestudentexam',)
    model = SelectiveStudentExam
    template_name = 'admin/school/setting/school_setting_delete.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('web:details_school_course', kwargs={'pk': self.object.ref_course.pk})

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete School Exam'
        context['content'] = 'Are you sure you want to delete ?'
        return context