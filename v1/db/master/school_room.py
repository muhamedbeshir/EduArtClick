from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school import School

character_validators = RegexValidator(r'^[a-zA-Z]+', 'Should start with characters.')

class SchoolRoom(BaseModel, models.Model):
	ref_school = models.ForeignKey( School , related_name="rel_ref_school_school_room" , on_delete=models.CASCADE )
	name = models.CharField(max_length=45)
	capacity = models.SmallIntegerField()
	minimum = models.SmallIntegerField()

	Meta = BaseModelMeta( attr={"db_table": "school_room", "unique_together": ("ref_school", "name")}, app_name='db' )

	def __str__(self):
		return '%s' % self.name

