from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.master.school_class import SchoolClass

from .school_course import SchoolCourse


class SchoolCoursePrice(BaseModel, models.Model):
    ref_school_course = models.ForeignKey(
        SchoolClass, related_name="rel_ref_school_course_school_course_price", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_weak = models.IntegerField(blank=True, null=True)
    min_weak = models.IntegerField()

    Meta = BaseModelMeta(
        attr={"db_table": "school_course_price"}, app_name='db')
