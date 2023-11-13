from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from v1.db.master.school import School

from v1.db.models import SchoolLetterType
from v1.base.configs import cRequest
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

from django.db import transaction, IntegrityError


class AddSchoolLetterType(PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_schoollettertype',)
	form_class = SchoolLetterTypeForm
	template_name = 'admin/school/letter/type/add.html'
	

	def __init__(self):
		super().__init__()

	def get(self, request, *args, **kwargs):
		school_id = kwargs.get( "pk" )
		school = get_object_or_404(School, pk=school_id)
		CHECK_USER_PERMISSION(self.request, school)
		return super().get(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('web:deatil_school' , kwargs={ "pk" : self.object.ref_school.pk })

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add School Letter Type"
		context['school'] = self.kwargs.get( "pk" )
		return context
	

	def form_valid(self, form, **kwargs):
		context = self.get_context_data()
		school_id = context.get('school')
		obj = form.save(commit=False)
		try:
			school = get_object_or_404(School, pk=school_id)
			obj.ref_school = school
			obj.save()
			messages.success(self.request, 'Successfully Added.')
		except IntegrityError:
			error = "This letter type already exist"
			form.add_error(None, error)
			return super().form_invalid(form)

		return super().form_valid(form)

# class ListSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, ListView):
# 	permission_required = ('db.add_schoollettertype',)
# 	model = SchoolExamType
# 	context_object_name = 'records'
# 	template_name = 'admin/master/school/exam_type/list.html'


class DeleteSchoolLetterType(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_schoollettertype',)
	model = SchoolLetterType
	template_name = 'admin/school/letter/type/delete.html'
	context_object_name = 'record'
	pk_url_kwarg = 'pk'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:deatil_school' , kwargs={ "pk" : self.object.ref_school.pk })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_school)
		context = super().get_context_data(**kwargs)
		context['page'] = 'Delete School Letter Type'
		context['content'] = 'Are you sure you want to delete ?'

		# cRequest.params[ "school_id" ] = context.get( "record" ).ref_school.id

		return context


class EditSchoolLetterType(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoollettertype',)
	model = SchoolLetterType
	form_class = SchoolLetterTypeForm
	template_name = 'admin/school/letter/type/edit.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:deatil_school' , kwargs={ "pk" : self.object.ref_school.pk })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_school)
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edit School Letter Type'		
		context['school']= self.object.ref_school.pk
		return context

	def form_valid(self, form):
		try:
			obj = form.save(commit=False)
			obj.user = self.request.user
			messages.success(self.request, 'Successfully Update.')
		except IntegrityError:
			error = "This letter type already exist"
			form.add_error(None, error)

			return super().form_invalid(form)
		
		return super().form_valid(form)