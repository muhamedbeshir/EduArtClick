from typing import Any, Dict
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail , EmailMessage
from django.http import HttpResponse
from v1.base.configs import cRequest
from v1.db.master.school import School

from v1.db.models import SchoolCertificateContent
from v1.db.school.school_certificate import SchoolCertificate
from v1.db.user.profile import SchoolStudentUserProfile
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

import os
import pdfkit
from datetime import date

class AddSchoolCertificateContent(PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_schoolcertificate',)
	form_class = SchoolCertificateContentForm
	template_name = 'admin/school/certificate/content/add.html'

	def get_success_url(self):
		return reverse('web:details_school_course' , kwargs={ "pk": self.object.ref_course.ref_course.pk })

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add School Certificate"
		course_id = self.kwargs.get( "pk" )
		course = get_object_or_404(SchoolCourse, pk=course_id)
		context['course'] = course
		CHECK_USER_PERMISSION(self.request, course.ref_school)
		return context
	
	def get_form_kwargs(self) -> Dict[str, Any]:
		kwargs = super().get_form_kwargs()
		kwargs.update(self.kwargs)
		return kwargs
	
	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(__class__, self).form_valid(form)


class EditSchoolCertificateContent(PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolcertificate',)
	model = SchoolCertificateContent
	form_class = SchoolCertificateContentForm
	template_name = 'admin/school/certificate/content/edit.html'


	def get_success_url(self):
		return reverse('web:details_school_course' , kwargs={ "pk": self.object.ref_course.ref_course.pk })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_course.ref_school)
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edit School Certificate'
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(__class__, self).form_valid(form)


class DeleteSchoolCertificateContent(PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_schoolcertificate',)
	model = SchoolCertificateContent
	template_name = 'admin/school/certificate/content/delete.html'
	context_object_name = 'record'
	pk_url_kwarg = 'pk'

	def get_success_url(self):
		return reverse('web:details_school_course' , kwargs={ "pk": self.object.ref_course.ref_course.pk })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_course.ref_school)
		context = super().get_context_data(**kwargs)
		context['page'] = 'Delete School Certificate'
		context['content'] = 'Are you sure you want to delete ?'
		return context

class ViewSchoolCertificateContent(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolcertificate',)
	model = SchoolCertificateContent
	form_class = SchoolCertificateContentFormView
	template_name = 'admin/school/certificate/content/view.html'

	def __init__(self):
		super().__init__()

	def get(self, request, *args, **kwargs):
		query = SchoolCertificateContent.objects.filter( id=kwargs["pk"] )
		if query.exists():
			obj = query.get()
			cRequest.params[ "school_id" ] = obj.ref_course.ref_school.id
		return super().get(request, *args, **kwargs)
	
	def get_success_url(self):
		return reverse('web:details_school_course' , kwargs={ "pk": self.object.ref_course.ref_course.pk })

	def get_context_data(self, **kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_course.ref_school)
		context = super().get_context_data(**kwargs)
		context['title'] = 'View School Certificate'
		try:
			students = context.get( "object" ).ref_course.ref_school.rel_school_student_user_profile_ref_school_school.all()
		except:
			students = []
		
		context['school']= cRequest.params[ "school_id" ]
		context[ "students" ] = students
		
		return context
	
	def post(self, request, *args, **kwargs):
		
		if request.POST and request.POST.get( "student" ):
			student_id = request.POST.get( "student" )
			students = []
			query = SchoolCertificateContent.objects.filter( id = kwargs.get( "pk" ) )
			
			if( query.exists() ):
				obj = query.get()
				if( student_id == '-1' ):
					students = obj.ref_course.ref_school.rel_school_student_user_profile_ref_school_school.all()
				else:
					students = SchoolStudentUserProfile.objects.filter( id = student_id ).all()
			
			if( students ):
				for student in students:
					try:
						substitutions = { 
							"course_title" : obj.ref_course.title , 
							"name" : student.name , 
							"score" : "10" , 
							"date" : date.today() ,
							"teacher" : str(obj.ref_course.ref_teacher_name.teacheruserprofile)
						}
						
						certificate_content = obj.content.format(**substitutions) 

						obj_cert = SchoolCertificate()
						obj_cert.ref_cert = obj
						obj_cert.content = certificate_content
						obj_cert.submit_date = date.today()
						obj_cert.ref_submit_by = obj.ref_course.ref_teacher_name
						obj_cert.ref_student = student
						obj_cert.save()

						pdfkit.from_string(certificate_content, 'certificate.pdf')
		
						email = EmailMessage(
							'School Certificate', 'Please find the Certificate as attached.', settings.EMAIL_HOST_USER, [student.email])
						email.attach_file('certificate.pdf')
						email.send()
						
						os.remove('certificate.pdf')
					except BadHeaderError:
						return HttpResponse('Invalid header found.')

		return super().post(request, *args, **kwargs)

