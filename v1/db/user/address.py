from django.db import models

from os import path

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


from v1.base.models import BaseModel, BaseModelMeta
from django.db import models
from django.core.validators import RegexValidator


character_validators = RegexValidator(r'^[a-zA-Z]+', 'Should start with characters.')


class UserAddress(BaseModel, models.Model):
	ref_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rel_ref_user_user_address")
	street_1 = models.CharField(max_length=100)
	street_2 = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100, blank=True, null=True)
	code = models.CharField(max_length=40, blank=True, null=True)

	Meta = BaseModelMeta( attr={"db_table": "user_address"}, app_name='db' )