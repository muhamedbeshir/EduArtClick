from django.db import models

from os import path

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


from v1.base.models import BaseModel, BaseModelMeta
from django.db import models


class UserContact(BaseModel, models.Model):
	ref_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rel_ref_user_user_contact")
	home_phone = models.CharField(max_length=45)
	office_phone = models.CharField(max_length=45, blank=True, null=True)
	personal_email = models.EmailField(max_length=100, blank=True, null=True)
	work_email = models.EmailField(max_length=100, blank=True, null=True)
	emergency_name = models.CharField(max_length=40, blank=True, null=True)
	emergency_phone = models.CharField(max_length=40, blank=True, null=True)

	Meta = BaseModelMeta( attr={"db_table": "user_contact"}, app_name='db' )


class ContactUs(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	email = models.CharField(max_length=255, blank=True, null=True)
	subject = models.CharField(max_length=255, blank=True, null=True)
	message = models.TextField(blank=True, null=True)
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'nqraa_contactus'

	def __str__(self):
		return '%s' % (self.name or '')
