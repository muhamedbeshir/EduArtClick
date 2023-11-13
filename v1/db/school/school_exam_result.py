from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.application.application import Application
from v1.db.master.school_course_level import SchoolCourseLevel

from .school_exam_answers import SchoolExamAnswers
from .school_exam import SchoolExam
from ..user.profile import SchoolStudentUserProfile, StudentUserProfile, TeacherUserProfile


class SchoolExamResult(BaseModel, models.Model):
    ref_exam = models.ForeignKey(
        SchoolExam, related_name="rel_exam_student_answers_exam", on_delete=models.CASCADE)
    ref_student = models.ForeignKey(
        StudentUserProfile, related_name="rel_exam_student_answers_student", null=True, on_delete=models.CASCADE)
    ref_application = models.ForeignKey(
        Application, related_name="rel_exam_student_answers_application", null=True, on_delete=models.CASCADE)
    ref_course_level = models.ForeignKey(
        SchoolCourseLevel, related_name="rel_exam_student_answers_course_level", null=True, on_delete=models.CASCADE)
    ref_school_student = models.ForeignKey(
        SchoolStudentUserProfile, related_name="rel_exam_school_student_answers_student", null=True, on_delete=models.CASCADE)

    remarks = models.CharField(max_length=1024, null=True, blank=True)
    score = models.IntegerField(default=0)

    Meta = BaseModelMeta(
        attr={"db_table": "school_exam_results"}, app_name='db')
