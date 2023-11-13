from django.db import models

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta




class WeekDayList(BaseModel, models.Model):
	name = models.CharField(max_length=100)
	short_name = models.CharField(max_length=100)
	

	Meta = BaseModelMeta( attr={"db_table": "weekdaylist"}, app_name='db' )

	def __str__(self):
		return '%s' % self.name