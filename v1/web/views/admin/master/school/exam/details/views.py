from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.core.exceptions import PermissionDenied

from v1.db.models import *
from v1.web.utils import CHECK_USER_PERMISSION

class SchoolExamDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	permission_required = ('db.view_schoolexam',)
	model = SchoolExam
	context_object_name = 'exam'
	template_name = 'admin/school/exam/details.html'

	def get_user(self):
		return self.request.user

	def get_context_data(self,**kwargs):
		CHECK_USER_PERMISSION(self.request, self.object.ref_course.ref_school)
		user=self.get_user()
		
		if user.groups.filter(name='school').exists():
			exam_id = self.kwargs.get('pk', None)
			exam_query = SchoolExam.objects.filter(id=exam_id,ref_course__ref_school=user.organizationuserprofile.ref_school)
			if exam_query.exists():
				exam = exam_query.get()
				context = super(__class__,self).get_context_data(**kwargs)
				context["exam"] = exam
				context['categories'] = SchoolExamCategory.objects.filter(ref_exam=exam).order_by("id")
				context['questions'] = SchoolExamQuestions.objects.filter(ref_exam_category__ref_exam=exam).order_by("id")
				context['answers'] = SchoolExamResult.objects.filter(ref_exam=exam).order_by("id")
				return context
		
		elif user.groups.filter(name='teacher').exists():
			exam_id = self.kwargs.get('pk', None)
			exam_query = SchoolExam.objects.filter(id=exam_id,ref_course__ref_teacher_name=user)
			if exam_query.exists():
				exam = exam_query.get()
				context = super(__class__,self).get_context_data(**kwargs)
				context["exam"] = exam
				context['categories'] = SchoolExamCategory.objects.filter(ref_exam=exam).order_by("id")
				context['questions'] = SchoolExamQuestions.objects.filter(ref_exam_category__ref_exam=exam).order_by("id")
				context['answers'] = SchoolExamResult.objects.filter(ref_exam=exam).order_by("id")
				return context

		elif user.groups.filter(name='admin').exists() or user.is_superuser:
			exam_id = self.kwargs.get('pk', None)
			exam_query = SchoolExam.objects.filter(id=exam_id)
			if exam_query.exists():
				exam = exam_query.get()
				context = super(__class__,self).get_context_data(**kwargs)
				context["exam"] = exam
				context['categories'] = SchoolExamCategory.objects.filter(ref_exam=exam).order_by("id")
				context['questions'] = SchoolExamQuestions.objects.filter(ref_exam_category__ref_exam=exam).order_by("id")
				context['answers'] = SchoolExamResult.objects.filter(ref_exam=exam).order_by("id")
				return context
		
		#context = super(SchoolExam,self).get_context_data(**kwargs)
		raise PermissionDenied()
		context = {}
		context["permission"] = "permission"
		return context
		
		