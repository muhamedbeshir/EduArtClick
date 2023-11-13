from django.db import models

from os import path

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


from v1.base.models import BaseModel, BaseModelMeta
from django.db import models

from .profile import TeacherUserProfile
from django.core.validators import RegexValidator


character_validators = RegexValidator(r'^[a-zA-Z]+', 'Should start with characters.')


class CertificateTeacher(BaseModel, models.Model):
	ref_teacher_user_profile = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, related_name="rel_ref_teacher_user_profile_certificate_teacher")
	name = models.CharField(max_length=200)
	code = models.CharField(max_length=200)
	date = models.DateField()

	Meta = BaseModelMeta( attr={"db_table": "certificate_teacher", "unique_together": ("ref_teacher_user_profile", "code",)}, app_name='db' )