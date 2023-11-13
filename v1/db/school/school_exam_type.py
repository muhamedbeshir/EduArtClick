from django.db import models

from v1.base.models import BaseModel, BaseModelMeta

class SchoolExamType(BaseModel, models.Model):
	name = models.CharField(max_length=200, unique=True)
	Meta = BaseModelMeta( attr={"db_table": "school_exam_type"}, app_name='db' )

	def __str__(self):
		return '%s' % self.name