from django.db import models
import math
from os import path

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


from v1.base.models import BaseModel, BaseModelMeta
from django.db import models

from .profile import SchoolStudentUserProfile
from ..master import SchoolAccommodationService


class StudentProfileHasAccommodation(BaseModel, models.Model):
    ref_student = models.ForeignKey(SchoolStudentUserProfile, on_delete=models.CASCADE,
                                    related_name="rel_ref_student_student_profile_has_accommodation")
    ref_accommodation_room = models.ForeignKey(
        SchoolAccommodationService, on_delete=models.CASCADE, related_name="rel_ref_accommodation_room_student_profile_has_accommodation")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    payment = models.BooleanField(default=False)

    Meta = BaseModelMeta(
        attr={"db_table": "student_profile_has_accommodation"}, app_name='db')

    @property
    def calculate_weeks(self):
        start_date = self.start_date
        end_date = self.end_date
        days = (end_date - start_date).days
        weeks = math.ceil(days/7)
        return weeks

    @property
    def calculate_amount(self):
        start_date = self.start_date
        end_date = self.end_date
        days = (end_date - start_date).days
        weeks = math.ceil(days/7)
        amount = self.ref_accommodation_room.price * weeks
        return amount
