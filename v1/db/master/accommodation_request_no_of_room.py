from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school_accommodation_service import SchoolAccommodationService

class AccommodationRequestNoOfRoom(BaseModel, models.Model):
	ref_accommodation = models.ForeignKey( SchoolAccommodationService , related_name="rel_ref_accommodation_accommodation_request_no_of_room" , on_delete=models.CASCADE )
	title = models.CharField(max_length=100)
	code = models.IntegerField(default=1)

	Meta = BaseModelMeta( attr={"db_table": "accommodation_request_no_of_room"}, app_name='db' )




