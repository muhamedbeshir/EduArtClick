from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school_accommodation_owner import SchoolAccommodationOwner
from django.core.validators import RegexValidator


character_validators = RegexValidator(r'^[a-zA-Z]+', 'Should start with characters.')


class SchoolAccommodationAccBank(BaseModel, models.Model):
	ref_accommodation = models.ForeignKey( SchoolAccommodationOwner , related_name="rel_ref_accommodation_owener_school_accommodation_acc_bank" , on_delete=models.CASCADE )
	acc_bank = models.CharField(max_length=200)
	acc_holder = models.CharField(max_length=45)
	acc_no = models.CharField(max_length=45, unique=True)
	bank_sort_code = models.CharField(max_length=45, blank=True, null=True)

	Meta = BaseModelMeta( attr={"db_table": "school_accommodation_acc_bank"}, app_name='db' )

