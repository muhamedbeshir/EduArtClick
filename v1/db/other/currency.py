from django.db import models

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta




class Currency(BaseModel, models.Model):
	title = models.CharField(max_length=100)
	currency_short = models.CharField(max_length=10, unique=True)
	currency_symbol = models.CharField(max_length=10, unique=True, blank=True, null=True) 

	Meta = BaseModelMeta( attr={"db_table": "currency"}, app_name='db' )

	def __str__(self):
		return '%s' % self.title