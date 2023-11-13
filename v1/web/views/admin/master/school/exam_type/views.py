from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse

from v1.db.models import SchoolExamType

from .forms import *

from django.db import transaction, IntegrityError


class AddSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_schoolexamtype')
	form_class = SchoolExamTypeForm
	template_name = 'admin/master/school/exam_type/add.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_type_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add School Exam Type"
		return context
	
	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(__class__, self).form_valid(form)


class ListSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('db.view_schoolexamtype')
	model = SchoolExamType
	context_object_name = 'records'
	template_name = 'admin/master/school/exam_type/list.html'


class DeleteSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_schoolexamtype')
	model = SchoolExamType
	template_name = 'admin/master/school/exam_type/delete.html'
	context_object_name = 'record'
	pk_url_kwarg = 'pk'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_type_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page'] = 'Delete School Exam Type'
		context['content'] = 'Are you sure you want to delete ?'
		return context


class EditSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolexamtype')
	model = SchoolExamType
	form_class = SchoolExamTypeForm
	template_name = 'admin/master/school/exam_type/add.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_type_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['title'] = 'Edit School Exam Type'
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(__class__, self).form_valid(form)
