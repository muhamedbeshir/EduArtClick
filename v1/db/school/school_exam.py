from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.master.school_class import SchoolClass

from ..master import SchoolCourse
from .school_exam_type import SchoolExamType
from ..user.profile import TeacherUserProfile
from django.core.validators import RegexValidator


character_validators = RegexValidator(
    r'^[a-zA-Z]+', 'Should start with characters.')


class SchoolExam(BaseModel, models.Model):
    ref_exam_type = models.ForeignKey(
        SchoolExamType, related_name="rel_school_exam_school_exam_type", on_delete=models.CASCADE)
    ref_course = models.ForeignKey(
        SchoolClass, related_name="rel_school_exam_school_course", on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    code = models.CharField(max_length=200)

    duration = models.IntegerField()
    score = models.IntegerField()
    total_questions = models.IntegerField()
    exam_date = models.DateField(verbose_name='Exam Date', null=True)

    Meta = BaseModelMeta(attr={"db_table": "school_exam"}, app_name='db')

    
    def __str__(self) -> str:
        return self.title
