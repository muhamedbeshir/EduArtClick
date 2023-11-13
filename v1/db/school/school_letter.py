import imp
from django.db import models

from v1.base.models import BaseModel, BaseModelMeta
from .school_letter_type import SchoolLetterType

from v1.base.configs import cRequest

class SchoolLetter(BaseModel, models.Model):
	ref_type = models.ForeignKey( SchoolLetterType , related_name="rel_letter_ref_school_letter" , on_delete=models.CASCADE )
	
	content = models.TextField(blank=True,null=True)
	is_default = models.BooleanField(default=False,blank=True,null=True)

	Meta = BaseModelMeta( attr={"db_table": "school_letter"}, app_name='db' )

	def __str__(self):
		return '%s' % self.id