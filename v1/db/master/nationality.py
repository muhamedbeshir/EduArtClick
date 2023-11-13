from django.db import models

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta



class Nationality(BaseModel, models.Model):
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=10, blank=True, null=True)

	Meta = BaseModelMeta( attr={"db_table": "nationality"}, app_name='db' )

	def __str__(self):
		return '%s' % self.name