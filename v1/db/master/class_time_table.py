from django.db import models
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.master.school import School
from v1.db.master.school_class import SchoolClass
from v1.db.master.school_course import SchoolCourse


class ClassTimeTable(BaseModel, models.Model):

    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_school_time_table", on_delete=models.CASCADE)
    ref_course = models.ForeignKey(
        SchoolCourse, related_name="rel_ref_course_school_time_table", on_delete=models.CASCADE)
    ref_class = models.ForeignKey(
        SchoolClass, related_name="rel_ref_class_school_time_table", on_delete=models.CASCADE, null=True)

    class_date = models.DateField(verbose_name='Class Date', null=True)
    start_time = models.TimeField(verbose_name='Start Time')
    end_time = models.TimeField(verbose_name='End Time')

    Meta = BaseModelMeta(
        attr={
            "db_table": "class_time_table",
            "unique_together": ("ref_school", "ref_course", "ref_class", "class_date")
        }, app_name='db')

    def __str__(self):
        return f'{self.ref_class}, {self.class_date} - {self.start_time} - {self.end_time}'
