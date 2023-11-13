from sqlite3 import DatabaseError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse

from django.forms import formset_factory
from django.forms import modelformset_factory

from django.db import transaction, IntegrityError

from v1.base.configs import cRequest
from v1.db.master.school_class import SchoolClass
from v1.db.master.school_course import SchoolCourse
from v1.db.models import SchoolExamQuestions, Application, SchoolExamAnswers, SchoolExamResult
from v1.db.school.school_exam import SchoolExam
from v1.db.school.school_sslue import SelectiveStudentExam
from v1.db.user.profile import SchoolStudentUserProfile
from v1.db.user.student_profile_has_course import StudentProfileHasCourse
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *
from v1.base.configs import cRequest
from django.utils import timezone


class StartSchoolExam(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('db.view_schoolexamquestions')
    form_class = SchoolExamQuestionsForm
    template_name = 'admin/school/exam/start/list.html'

    context_object_name = 'questions'
    exam = {}
    is_exam_completed = False
    answers = list()

    def get(self, request, *args, **kwargs):
        app_id = kwargs.get('app_id')

        cRequest.params["app_id"] = app_id
        app_query = Application.objects.filter(id=app_id, user=request.user)
        if app_query.exists():
            application = app_query.get()
            cRequest.params["application"] = application
            course = get_object_or_404(
                SchoolClass, pk=application.ap_course_class)

            # course = application.ref_school.rel_ref_school_school_course.first()
            cRequest.params["course_id"] = course.id

            # course.ref_course.rel_school_exam_school_course.first()
            self.exam = SchoolExam.objects.filter(ref_course=course.id).first()
            print(self.exam)
            # self.exam = course.ref_course.rel_school_exam_school_course.first()
            cRequest.params["exam"] = self.exam

            answers_query = SchoolExamAnswers.objects.filter(
                ref_application=application, ref_exam=self.exam, ref_student=request.user.studentuserprofile)
            if answers_query.exists():
                self.is_exam_completed = True

                self.answers = SchoolExamAnswers.objects.filter(
                    ref_application=application, ref_exam=self.exam, ref_student=request.user.studentuserprofile).all()
        else:
            raise Http404

        return super(__class__, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req_data = request.POST
        data = list()
        _score = 0
        if cRequest.params.get("questions"):
            for record in cRequest.params["questions"]:
                score = record.score if req_data.get(
                    str(record.id)) == record.answer else 0
                _score += score
                data.append({"ref_question": record, "answer": req_data.get(
                    str(record.id)), "score": score})

            student = request.user.studentuserprofile
            for question in data:
                _record = {
                    "answer": question.get("answer"),
                    "score": question.get("score"),
                    "ref_question": question.get("ref_question"),
                    "ref_student": student,
                    "ref_exam": cRequest.params["exam"],
                    "ref_application": cRequest.params["application"],
                }
                record = SchoolExamAnswers(**_record)

                record.save()

            _exam_result = {
                "score": _score,
                "ref_student": student,
                "ref_exam": cRequest.params["exam"],
                "ref_application": cRequest.params["application"],
            }

            SchoolExamResult(**_exam_result).save()

        return redirect('web:application_list')

    def get_queryset(self):
        queryset = SchoolExamQuestions.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(__class__, self).get_context_data(*args, **kwargs)
        total_questions = self.exam.total_questions if self.exam else 0
        print('=>', total_questions)

        questions = SchoolExamQuestions.objects.filter(
            ref_exam_category__ref_exam__ref_course=cRequest.params["course_id"], ref_exam_category__ref_exam__ref_exam_type__name='Initial').order_by("?")[:total_questions]
        print(questions)
        cRequest.params["questions"] = context['records'] = questions
        if not len(questions) == total_questions:
            cRequest.params["questions"] = context['records'] = []

        context["is_exam_completed"] = self.is_exam_completed
        context["answers"] = self.answers
        context["duration"] = (self.exam.duration)*60 if self.exam else 360

        return context


class SchoolExamList(LoginRequiredMixin, ListView):
    template_name = 'admin/school/exam/list.html'
    model = SchoolExam
    context_object_name = 'exam_list'

    def get_queryset(self):
        student = SchoolStudentUserProfile.objects.get(
            ref_user=self.request.user)
        school = student.ref_school

        student_course = StudentProfileHasCourse.objects.filter(
            ref_student=student, status=True).values('ref_course')
        course_ids = [s_course['ref_course'] for s_course in student_course]
        
        # For level-up exam for selective students
        school_students = SchoolStudentUserProfile.objects.filter(ref_school=school, ref_user=self.request.user)
        selective_student_queryset = SelectiveStudentExam.objects.filter(ref_school=school, ref_student__in=school_students)

        exam_ids = [_s.ref_exam.pk for _s in selective_student_queryset]

        queryset1 = SchoolExam.objects.filter(pk__in=exam_ids)
        
        queryset = SchoolExam.objects.filter(
            ref_course__id__in=course_ids, ref_exam_type__name__in=('Intermediate', 'Final'))
        
        queryset2 = queryset | queryset1

        return queryset2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Exam List'
        return context


class StartExam(LoginRequiredMixin, CreateView):
    form_class = SchoolExamQuestionsForm
    model = SchoolExamQuestions
    template_name = 'admin/school/exam/start/student.html'
    exam = None
    is_exam_completed = False
    answers = list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        school_student = SchoolStudentUserProfile.objects.get(ref_user=user)
        student_level = school_student.ref_course_level

        exam_id = self.kwargs.get('pk', None)
        # self.exam = SchoolExam.objects.get(id=exam_id)
        self.exam = get_object_or_404(SchoolExam, id=exam_id)

        if self.exam.exam_date == timezone.now().date():
            # Checking Level Up Exam
            if (self.exam.ref_exam_type.name == 'Level Up'):
                # If Student current level at Level 5 then questions come from Level 6
                # If student current level at Level 7 means last level then questions come from Level 7
                question_level = int(str(student_level.name)[-1]) + 1
                if question_level > 7:
                    question_level -= 1

                queryset = SchoolExamQuestions.objects.filter(
                    ref_exam_category__ref_exam=self.exam, ref_exam_category__name=f'Level {question_level}').order_by('?')[0:self.exam.total_questions]
            else:
                queryset = SchoolExamQuestions.objects.filter(
                    ref_exam_category__ref_exam=self.exam).order_by('?')[0:self.exam.total_questions]

            answers_query = SchoolExamAnswers.objects.filter(
                ref_exam=self.exam, ref_school_student__ref_user=self.request.user)
            if answers_query.exists():
                self.is_exam_completed = True

                self.answers = SchoolExamAnswers.objects.filter(
                    ref_exam=self.exam, ref_school_student__ref_user=self.request.user).all()

            cRequest.params["exam"] = self.exam
            cRequest.params["questions"] = context['questions'] = queryset

        context['title'] = 'Start Student Exam'
        context['is_exam_completed'] = self.is_exam_completed
        context["duration"] = self.exam.duration*60
        context["answers"] = self.answers
        return context

    def post(self, request, *args, **kwargs):
        req_data = request.POST
        data = list()
        _score = 0
        if cRequest.params.get("questions"):
            for record in cRequest.params["questions"]:
                score = record.score if req_data.get(
                    str(record.id)) == record.answer else 0
                _score += score
                data.append({"ref_question": record, "answer": req_data.get(
                    str(record.id)), "score": score})

            student = SchoolStudentUserProfile.objects.get(
                ref_user=self.request.user)
            print(student)
            for question in data:
                _record = {
                    "answer": question.get("answer"),
                    "score": question.get("score"),
                    "ref_question": question.get("ref_question"),
                    "ref_school_student": student,
                    "ref_exam": cRequest.params["exam"],
                    "ref_application": None,
                }
                record = SchoolExamAnswers(**_record)

                record.save()

            _exam_result = {
                "score": _score,
                "ref_school_student": student,
                "ref_exam": cRequest.params["exam"],
                "ref_application": None,
            }

            SchoolExamResult(**_exam_result).save()

        return redirect('web:school_student_dashboard')
