from django.db import models

from v1.base.models.model import BaseModel, BaseModelMeta
from v1.db.master.school import School
from v1.db.master.school_course import SchoolCourse


class SchoolCourseDiscount(BaseModel, models.Model):   
    ref_school = models.ForeignKey( School , related_name="rel_ref_school_school_discount" , on_delete=models.CASCADE )
    ref_course = models.ForeignKey( SchoolCourse , related_name="rel_ref_school_school_course_discount" , on_delete=models.SET_NULL, null=True, blank=True )
    coupon_code = models.CharField(max_length=255, verbose_name='Coupon Code')
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    valid_from = models.DateField()
    valid_upto = models.DateField()
    is_active = models.BooleanField(default=False, null=True, blank=True, verbose_name='Is Active')

    Meta = BaseModelMeta( 
        attr={
            "db_table": "school_course_discount", 
            "unique_together": ("ref_school", "coupon_code")
        }, 
        app_name='db'
    )

    def __str__(self):
        return str(self.coupon_code).upper()