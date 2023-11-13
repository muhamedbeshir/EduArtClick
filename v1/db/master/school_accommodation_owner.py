from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school import School
from .school_accommodation_type import SchoolAccommodationType


class SchoolAccommodationOwner(BaseModel, models.Model):

	HOST_FAMILY = 0
	RESIDENT = 1
	HOTEL_OR_HOSTEL = 2
	ACCOMMODATION_TYPE = (
		(HOST_FAMILY, 'Host family'),
		(RESIDENT, 'Resident'),
		(HOTEL_OR_HOSTEL, 'Hotel/Hostel'),
	)
	ref_school = models.ForeignKey( School , related_name="rel_ref_school_accommodation_owner" , on_delete=models.CASCADE )
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	company_name = models.CharField(max_length=200, blank=True, null=True)
	address = models.TextField(blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True)
	postal_code = models.CharField(max_length=50, blank=True, null=True)
	email = models.CharField(max_length=200, blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	
	notes = models.TextField(blank=True, null=True)
	capacity = models.IntegerField(blank=True, null=True)
	accommodation_type = models.IntegerField(choices=ACCOMMODATION_TYPE, default=0)

	Meta = BaseModelMeta( attr={"db_table": "school_accommodation_owner"}, app_name='db' )

	def __str__(self):
		return '%s' % self.id

	@property
	def accommodation_type_title(self):
		res = ""
		for accommodation_type in self.ACCOMMODATION_TYPE:
			if accommodation_type[0] == self.accommodation_type:
				res = accommodation_type[1]
		return res

		