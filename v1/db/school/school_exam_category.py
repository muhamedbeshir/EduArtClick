from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from v1.base.configs import cRequest
from .school_exam import SchoolExam
from django.core.validators import RegexValidator


character_validators = RegexValidator(r'^[a-zA-Z]+', 'Should start with characters.')


class SchoolExamCategory(BaseModel, models.Model):
	ref_exam = models.ForeignKey( SchoolExam , related_name="rel_school_exam_category_school_exam" , on_delete=models.CASCADE )

	name = models.CharField(max_length=200)

	Meta = BaseModelMeta( attr={"db_table": "school_exam_category"}, app_name='db' )

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if cRequest.params[ "ref_exam_id" ]:
			self.ref_exam_id = cRequest.params[ "ref_exam_id" ]
		return super().save(force_insert, force_update, using, update_fields)
	
	def __str__(self):
		return self.name