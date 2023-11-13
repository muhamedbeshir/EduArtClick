from django.db import models
from django.contrib.auth.models import User
from v1.base.models import BaseModel
from v1.db.master.school_class import SchoolClass
from v1.db.master.school_room import SchoolRoom
from v1.db.master.school_schedule import SchoolSchedule


class ClassClassroom(BaseModel, models.Model):

    ref_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )

    ref_schedule = models.ForeignKey(
        SchoolSchedule,
        on_delete=models.CASCADE
    )

    ref_teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    ref_room = models.ForeignKey(
        SchoolRoom,
        on_delete=models.CASCADE
    )

    class_date = models.DateField(
        verbose_name='Class Date',
    )

    note = models.TextField(
        verbose_name='Note',
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "nqraa_class_classroom"
        unique_together = ('ref_class', 'class_date',)

    def __str__(self):
        return f'{self.class_date}'

    @property
    def teacher_fullname(self):
        try:
            fullname = self.ref_teacher.first_name+" "+self.ref_teacher.last_name
            return fullname.title()
        except:
            return ""