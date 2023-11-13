from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school import School


class SchoolSchedule(BaseModel, models.Model):
    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_school_schedule", on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    Meta = BaseModelMeta(attr={"db_table": "school_schedule", "unique_together": (
        "ref_school", "start_time", "end_time")}, app_name='db')

    def __str__(self):
        return f'{self.start_time.strftime("%I:%M %p")} - {self.end_time.strftime("%I:%M %p")}'

    @property
    def get_schedule(self):
        return f'{self.start_time} - {self.end_time}'
