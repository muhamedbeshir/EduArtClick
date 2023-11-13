from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.master.school_course import SchoolCourse
from v1.db.master.school_course_type import SchoolCourseType

from .school import School
from .school_course_level import SchoolCourseLevel
from .school_room import SchoolRoom
from .school_schedule import SchoolSchedule
from ..other import WeekDayList


class SchoolClass(BaseModel, models.Model):
    # CONTINUE = 0
    # START = 1
    # COURSE_TYPE = (
    #     (CONTINUE, 'Continue'),
    #     (START, 'Start'),
    # )

    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_school_class", on_delete=models.CASCADE)
    ref_course = models.ForeignKey(
        SchoolCourse, related_name="rel_ref_school_course_class", on_delete=models.CASCADE)
    ref_teacher_name = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    ref_level = models.ForeignKey(
        SchoolCourseLevel, related_name="rel_ref_level_school_course_level", on_delete=models.CASCADE, blank=True, null=True)
    ref_type_of_course = models.ForeignKey(
        SchoolCourseType, related_name="rel_ref_level_school_course_type", on_delete=models.CASCADE, blank=True, null=True)
    ref_room = models.ForeignKey(
        SchoolRoom, related_name="ref_room_school_course", on_delete=models.CASCADE, blank=True, null=True)
    ref_schedule = models.ForeignKey(
        SchoolSchedule, related_name="ref_schedule_school_course", on_delete=models.CASCADE, blank=True, null=True)
    ref_day = models.ManyToManyField(WeekDayList, blank=True)

    title = models.CharField(max_length=200)
    maximum = models.IntegerField(blank=True, null=True)
    minimum = models.IntegerField(blank=True, null=True)
    summar_start = models.DateField(blank=True, null=True)
    summar_end = models.DateField(blank=True, null=True)
    start_day = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True)
    document = models.FileField(
        upload_to="course/document/%Y-%m-%d", null=True, blank=True)

    # started_time = models.TimeField(blank=True, null=True)
    # end_time = models.TimeField(blank=True, null=True)
    # type_of_course = models.IntegerField(
    #     choices=COURSE_TYPE, blank=True, null=True)

    class Meta:
        db_table = "nqraa_school_class"
        # unique_together = ('ref_school', 'ref_teacher_name',
        #                    'ref_schedule', 'ref_room')

    @property
    def teacher_fullname(self):
        try:
            user = User.objects.get(id=self.ref_teacher_name.id)
            fullname = user.first_name+" "+user.last_name
            return fullname.title()
        except:
            return ""

    @property
    def ref_day_list(self):
        x = ", ".join([str(p) for p in self.ref_day.all()])
        return x
    
    @property
    def days_list(self):
        days = [day.name for day in self.ref_day.all()]
        return days

    def __str__(self):
        return self.title

    # @property
    # def type_of_course_str(self):
    #     if self.type_of_course == 0:
    #         return 'Continue'
    #     return 'Start'

    @property
    def study_period(self):
        study_days = (self.summar_end - self.summar_start).days
        study_weeks = int(study_days/7)
        if not study_weeks % 7 == 0:
            study_weeks += 1
        return study_weeks
    
    @property
    def datetimepicuresdays(self):
        class_days = []

        for day_ in self.ref_day_list.split(", "):
            if day_ == 'Sunday':
                class_days.append(0)
            elif day_ == 'Monday':
                class_days.append(1)
            elif day_ == 'Tuesday':
                class_days.append(2)
            elif day_ == 'Wednesday':
                class_days.append(3)
            elif day_ == 'Thursday':
                class_days.append(4)
            elif day_ == 'Friday':
                class_days.append(5)
            elif day_ == 'Saturday':
                class_days.append(6)
        return class_days
