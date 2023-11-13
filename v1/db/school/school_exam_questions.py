from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school_exam_category import SchoolExamCategory

class SchoolExamQuestions(BaseModel, models.Model):
	ref_exam_category = models.ForeignKey( SchoolExamCategory , related_name="rel_school_exam_questions_school_exam_category" , on_delete=models.CASCADE )

	question = models.CharField(max_length=1024)
	
	answer = models.CharField(max_length=255)
	option1 = models.CharField(max_length=255)
	option2 = models.CharField(max_length=255)
	option3 = models.CharField(max_length=255)

	score = models.IntegerField()

	Meta = BaseModelMeta( attr={"db_table": "school_exam_questions"}, app_name='db' )