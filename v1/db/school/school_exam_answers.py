from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.application.application import Application

from .school_exam_questions import SchoolExamQuestions
from .school_exam import SchoolExam
from ..user.profile import SchoolStudentUserProfile, StudentUserProfile


class SchoolExamAnswers(BaseModel, models.Model):
    ref_question = models.ForeignKey(
        SchoolExamQuestions, related_name="rel_exam_answersheet_exam_question", on_delete=models.CASCADE)
    ref_exam = models.ForeignKey(
        SchoolExam, related_name="rel_exam_answersheet_exam", on_delete=models.CASCADE)
    ref_student = models.ForeignKey(
        StudentUserProfile, related_name="rel_exam_answersheet_student", null=True, on_delete=models.CASCADE)
    ref_application = models.ForeignKey(
        Application, related_name="rel_exam_answersheet_application", null=True, on_delete=models.CASCADE)
    ref_school_student = models.ForeignKey(
        SchoolStudentUserProfile, related_name="rel_exam_answersheet_school_student", null=True, on_delete=models.CASCADE)

    answer = models.CharField(max_length=200, null=True, blank=True)
    score = models.IntegerField(default=0)

    Meta = BaseModelMeta(
        attr={"db_table": "school_exam_answers"}, app_name='db')
