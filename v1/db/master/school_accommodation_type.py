from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school import School

class SchoolAccommodationType(BaseModel, models.Model):
	ref_school = models.ForeignKey( School , related_name="rel_ref_school_school_accommodation_type" , on_delete=models.CASCADE )
	accommodation_type_name = models.CharField(max_length=45)

	Meta = BaseModelMeta( attr={"db_table": "school_accommodation_type"}, app_name='db' )

	def __str__(self):
		return '%s' % self.accommodation_type_name


