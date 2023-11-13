from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from v1.base.configs import cRequest
from v1.db.models import SchoolExamCategory
from v1.db.school.school_exam import SchoolExam
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

class AddSchoolExamCategory(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_schoolexamcategory',)
	form_class = SchoolExamCategoryForm
	template_name = 'admin/school/exam/category/add.html'
	ref_exam_id = ""

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_details',kwargs = { "pk" :cRequest.params["ref_exam_id"] })

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add School Exam Category"
		context['ref_exam_id'] = cRequest.params["ref_exam_id"]
		return context

	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(__class__, self).form_valid(form)
	
	def get(self, request, *args, **kwargs):
		user = self.request.user
		exam_id = kwargs.get( "ref_exam_id" )
		cRequest.params["ref_exam_id"]  = kwargs.get( "ref_exam_id" )
		exam = get_object_or_404(SchoolExam, pk=exam_id)
		CHECK_USER_PERMISSION(self.request, exam.ref_course.ref_school)
		
		if user.groups.filter(name='teacher').exists():
			exam_query = SchoolExam.objects.filter(id=exam_id,ref_course__ref_teacher_name=user)
			if not exam_query.exists():
				raise PermissionDenied()
			
		return super().get(request, *args, **kwargs)


class ListSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('db.view_schoolexamcategory',)
	model = SchoolExamCategory
	context_object_name = 'records'
	template_name = 'admin/master/school/exam_type/list.html'


class DeleteSchoolExamCategory(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_schoolexamcategory',)
	model = SchoolExamCategory
	template_name = 'admin/school/exam/category/delete.html'
	context_object_name = 'record'
	pk_url_kwarg = 'pk'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_details',kwargs={ "pk" : cRequest.params["ref_exam_id"]})

	def get_context_data(self, **kwargs):
		user = self.request.user
		CHECK_USER_PERMISSION(self.request, self.object.ref_exam.ref_course.ref_school)
		context = super().get_context_data(**kwargs)
		
		cRequest.params["ref_exam_id"] = context.get("record").ref_exam.id
		context[ 'ref_exam_id' ] = cRequest.params["ref_exam_id"]
		exam_id = cRequest.params["ref_exam_id"]

		if user.groups.filter(name='teacher').exists():
			exam_query = SchoolExam.objects.filter(id=exam_id,ref_course__ref_teacher_name=user)
			if not exam_query.exists():
				raise PermissionDenied()
		
		context['title'] = 'Delete School Exam Category'
		context['page'] = 'Delete'
		context['content'] = 'Are you sure you want to delete ?'
		return context


class EditSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolexamcategory',)
	model = SchoolExamCategory
	form_class = SchoolExamCategoryForm
	template_name = 'admin/master/school/exam_type/add.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_details',kwargs = { "pk" :cRequest.params["ref_exam_id"] })
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['title'] = 'Edit School Exam Category'
		context['ref_exam_id'] = cRequest.params["ref_exam_id"]
		#context['event'] = event
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(__class__, self).form_valid(form)
