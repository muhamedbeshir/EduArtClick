from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school_schedule import SchoolSchedule
from .school_course import SchoolCourse
from .school_room import SchoolRoom


class ScheduleHasCourse(BaseModel, models.Model):
	ref_schedule = models.ForeignKey( SchoolSchedule , related_name="rel_ref_schedule_schedule_has_course" , on_delete=models.CASCADE )
	ref_course = models.ForeignKey(SchoolCourse, related_name="rel_ref_course_schedule_has_course" , on_delete=models.CASCADE )
	ref_room = models.ForeignKey(SchoolRoom, related_name="rel_ref_room_schedule_has_course" , on_delete=models.CASCADE )

	Meta = BaseModelMeta( attr={"db_table": "schedule_has_course"}, app_name='db' )