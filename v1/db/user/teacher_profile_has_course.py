from django.db import models

from os import path

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


from v1.base.models import BaseModel, BaseModelMeta
from django.db import models

from .profile import TeacherUserProfile
from ..master import SchoolCourse


class TeacherProfileHasCourse(BaseModel, models.Model):
	ref_teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, related_name="rel_ref_teacher_teacher_profile_has_course")
	ref_course = models.ForeignKey(SchoolCourse, on_delete=models.CASCADE, related_name="rel_ref_course_teacher_profile_has_course")
	
	Meta = BaseModelMeta( attr={"db_table": "teacher_profile_has_course"}, app_name='db' )