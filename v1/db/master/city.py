from django.db import models

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from django.core.validators import RegexValidator


from .country import Country

character_validators = RegexValidator(r'^[a-zA-Z]+', 'Should start with characters.')

class City(BaseModel, models.Model):
	ref_country = models.ForeignKey( Country , blank=True, null=True, related_name="country_info" , on_delete=models.CASCADE )
	city_name = models.CharField(max_length=200, unique=True, validators=[character_validators])

	Meta = BaseModelMeta( attr={"db_table": "city"}, app_name='db' )

	def __str__(self):
		return '%s' % self.city_name
