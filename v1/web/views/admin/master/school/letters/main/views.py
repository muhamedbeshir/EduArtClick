from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from v1.db.master.school import School

from v1.db.models import SchoolLetterType , SchoolStudentUserProfile, SchoolLetterSend
from v1.base.configs import cRequest
from v1.db.user.profile import StudentUserProfile
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

from django.db import transaction, IntegrityError


class AddSchoolLetter(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_schoolletter',)
	form_class = SchoolLetterForm
	template_name = 'admin/school/letter/main/add.html'

	def __init__(self):
		super().__init__()

	def get(self, request, *args, **kwargs):
		cRequest.params[ "school_id" ] = kwargs.get( "school_id" )
		school_id= kwargs.get( "school_id" )
		school = get_object_or_404(School, pk=school_id)
		CHECK_USER_PERMISSION(self.request, school)
		return super().get(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('web:deatil_school' , kwargs={ "pk" :cRequest.params[ "school_id" ] })

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add School Letter"
		context['school']= cRequest.params[ "school_id" ]
		return context
	
	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(__class__, self).form_valid(form)

class DeleteSchoolLetter(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_schoolletter',)
	model = SchoolLetter
	template_name = 'admin/school/letter/main/delete.html'
	context_object_name = 'record'
	pk_url_kwarg = 'pk'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:deatil_school' , kwargs={ "pk" :cRequest.params[ "school_id" ] })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_type.ref_school)
		context = super().get_context_data(**kwargs)
		context['page'] = 'Delete School Letter'
		context['content'] = 'Are you sure you want to delete ?'

		cRequest.params[ "school_id" ] = context.get( "object" ).ref_type.ref_school.id

		return context


class EditSchoolLetter(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolletter',)
	model = SchoolLetter
	form_class = SchoolLetterForm
	template_name = 'admin/school/letter/main/edit.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:deatil_school' , kwargs={ "pk" :cRequest.params[ "school_id" ] })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_type.ref_school)
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edit School Letter'

		cRequest.params[ "school_id" ] = context.get( "object" ).ref_type.ref_school.id

		context['school']= cRequest.params[ "school_id" ]
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(__class__, self).form_valid(form)


class ViewSchoolLetter(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolletter',)
	model = SchoolLetter
	form_class = SchoolLetterFormView
	template_name = 'admin/school/letter/main/view.html'

	def __init__(self):
		super().__init__()

	def get_user(self):
		return self.request.user

	def get_success_url(self):
		return reverse('web:deatil_school' , kwargs={ "pk" :cRequest.params[ "school_id" ] })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_type.ref_school)
		context = super().get_context_data(**kwargs)
		cRequest.params[ "school_id" ] = context.get( "object" ).ref_type.ref_school.id

		context['title'] = 'View School Letter'

		try:
			students = context.get( "object" ).ref_type.ref_school.rel_school_student_user_profile_ref_school_school.all()
		except:
			students = []
		
		context['school']= cRequest.params[ "school_id" ]
		context[ "students" ] = students
		
		return context
	
	def post(self, request, *args, **kwargs):
		if request.POST and request.POST.get( "student" ):
			student_id = request.POST.get( "student" )
			user=self.get_user()
			students = []
			obj = SchoolLetter.objects.filter( id = kwargs.get( "pk" ) )
			
			if( obj.exists() ):
				obj_letter = obj.get()
				if( student_id == '-1' ):
					students = obj_letter.ref_type.ref_school.rel_school_student_user_profile_ref_school_school.all()
				else:
					students = SchoolStudentUserProfile.objects.filter( id = student_id ).all()
			
			if( students ):
				for student in students:
					try:
						obj_lett = SchoolLetterSend()
						obj_lett.ref_letter = obj_letter
						obj_lett.content = obj_letter.content
						obj_lett.ref_submit_by = user
						obj_lett.ref_student = student
						obj_lett.save()
						send_mail( "School Letter" , obj_letter.content, settings.EMAIL_HOST_USER, [student.email], fail_silently=False)
						print("Successfully send mail")
					except BadHeaderError:
						return HttpResponse('Invalid header found.')

		return super().post(request, *args, **kwargs)


