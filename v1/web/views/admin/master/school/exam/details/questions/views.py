from sqlite3 import DatabaseError
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.forms import modelformset_factory

from django.db import transaction, IntegrityError

from v1.base.configs import cRequest
from v1.db.models import SchoolExamQuestions
from v1.db.school.school_exam import SchoolExam
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

class AddSchoolExamQuestion(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_schoolexamquestions',)
	form_class = SchoolExamQuestionsForm
	template_name = 'admin/school/exam/questions/add.html'
	ref_exam_id = ""

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_details',kwargs = { "pk" :cRequest.params["ref_exam_id"] })

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add Exam Questions"
		context['ref_exam_id'] = cRequest.params["ref_exam_id"]
		context['formset'] = ExamQuestionsFormset(queryset=SchoolExamQuestions.objects.none() , prefix="questions")		
		
		return context

	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(__class__, self).form_valid(form)

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			formset = ExamQuestionsFormset(data=request.POST or None, prefix="questions")
			print( "data" , request.POST )
			if formset.is_valid():
				for form in formset:
					try:
						with transaction.atomic():
							if form.is_valid():
								question = form.save(commit=True)
								question.save()
					except IntegrityError as e:
						raise IntegrityError(e)

		return redirect('web:school_exam_details',pk = cRequest.params["ref_exam_id"])

	
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

class DeleteSchoolExamQuestion(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_schoolexamquestions',)
	model = SchoolExamQuestions
	template_name = 'admin/school/exam/questions/delete.html'
	context_object_name = 'record'
	pk_url_kwarg = 'pk'
	ref_exam_id = ""

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school_exam_details',kwargs={ "pk" : cRequest.params["ref_exam_id"]})

	def get_context_data(self, **kwargs):
		user = self.request.user
		context = super().get_context_data(**kwargs)
		CHECK_USER_PERMISSION(self.request, self.object.ref_exam_category.ref_exam.ref_course.ref_school)
		cRequest.params["ref_exam_id"] = context.get("record").ref_exam_category.ref_exam.id;
		context[ 'ref_exam_id' ] = cRequest.params["ref_exam_id"]

		if user.groups.filter(name='teacher').exists():
			exam_query = SchoolExam.objects.filter(id=self.object.ref_exam_category.ref_exam.id,ref_course__ref_teacher_name=user)
			if not exam_query.exists():
				raise PermissionDenied()

		context['page'] = 'Delete'
		context['content'] = 'Are you sure you want to delete ?'
		return context

class ViewSchoolExamQuestion(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolexamquestions',)
	model = SchoolExamQuestions
	form_class = SchoolExamQuestionsFormView
	template_name = 'admin/school/exam/questions/view.html'

	def __init__(self):
		super().__init__()
		
	def get_context_data(self, **kwargs):
		user = self.request.user
		context = super().get_context_data(**kwargs)
		CHECK_USER_PERMISSION(self.request, self.object.ref_exam_category.ref_exam.ref_course.ref_school)
		cRequest.params["ref_exam_id"] = context.get("object").ref_exam_category.ref_exam.id

		context['title'] = 'View Exam Questions'
		context['ref_exam_id'] = cRequest.params["ref_exam_id"]
		#context['event'] = event

		if user.groups.filter(name='teacher').exists():
			exam_query = SchoolExam.objects.filter(id=self.object.ref_exam_category.ref_exam.id,ref_course__ref_teacher_name=user)
			if not exam_query.exists():
				raise PermissionDenied()
		
		return context

class EditSchoolExamType(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_schoolexamquestions',)
	model = SchoolExamQuestions
	form_class = SchoolExamQuestionsForm
	template_name = 'admin/master/school/exam_type/add.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:school/application_detail')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		cRequest.params["ref_exam_id"] = context.get("object").ref_exam_category.ref_exam.id

		context['title'] = 'Edit Exam Questions'
		context['ref_exam_id'] = cRequest.params["ref_exam_id"]
		#context['event'] = event
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(__class__, self).form_valid(form)
