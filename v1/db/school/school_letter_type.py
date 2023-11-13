import imp
from django.db import models

from v1.base.models import BaseModel, BaseModelMeta
from ..master.school import School

from v1.base.configs import cRequest
from django.core.validators import RegexValidator


character_validators = RegexValidator(r'^[a-zA-Z]+', 'Should start with characters.')

class SchoolLetterType(BaseModel, models.Model):
	ref_school = models.ForeignKey( School , related_name="rel_letter_type_rel_school" , on_delete=models.CASCADE )
	name = models.CharField(max_length=200)
	
	Meta = BaseModelMeta( attr={"db_table": "school_letter_type", "unique_together": ("ref_school", "name")}, app_name='db' )

	def __str__(self):
		return '%s' % self.name
	
	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if cRequest.params.get( "school_id" ):
			self.ref_school_id = cRequest.params.get( "school_id" )
		
		return super().save(force_insert, force_update, using, update_fields)