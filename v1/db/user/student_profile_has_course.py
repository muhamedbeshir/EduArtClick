from django.db import models

from os import path

from django.utils import timezone

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta


from v1.base.models import BaseModel, BaseModelMeta
from django.db import models

from v1.db.master.school_class import SchoolClass

from .profile import SchoolStudentUserProfile
from ..master import SchoolCourse


class StudentProfileHasCourse(BaseModel, models.Model):
    ref_student = models.ForeignKey(SchoolStudentUserProfile, on_delete=models.CASCADE,
                                    related_name="rel_ref_student_student_profile_has_course", blank=True, null=True)
    ref_course = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name="rel_ref_course_student_profile_has_course")
    study_period = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    installments = models.JSONField(default=list, null=True, blank=True)

    Meta = BaseModelMeta(
        attr={"db_table": "student_profile_has_course"}, app_name='db')

    def __str__(self) -> str:
        return self.ref_student.__str__()
