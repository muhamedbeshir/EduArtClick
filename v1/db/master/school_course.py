from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school import School



class SchoolCourse(BaseModel, models.Model):

	ref_school = models.ForeignKey( School , related_name="rel_ref_school_school_course" , on_delete=models.CASCADE )
	title = models.CharField(max_length=200)
	
	class Meta:
		db_table = "nqraa_school_course"
		unique_together = ('ref_school', 'title',)

	def __str__(self):
		return self.title