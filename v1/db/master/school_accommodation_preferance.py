from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school_accommodation_service import SchoolAccommodationService

class SchoolAccommodationPreferance(BaseModel, models.Model):
	ref_accommodation = models.ForeignKey( SchoolAccommodationService , related_name="rel_ref_accommodation_school_accommodation_preferance" , on_delete=models.CASCADE )
	name = models.CharField(max_length=45)

	Meta = BaseModelMeta( attr={"db_table": "school_accommodation_preferance"}, app_name='db' )