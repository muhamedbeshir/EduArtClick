from django.db import models

from v1.base.models.model import BaseModel, BaseModelMeta
from v1.db.master.school import School
from django.utils.html import format_html

from v1.db.master.school_course import SchoolCourse
from v1.db.master.school_service import SchoolService
from v1.db.user.profile import TeacherUserProfile


class SchoolPayroll(BaseModel, models.Model):

    ref_school = models.ForeignKey( School , related_name="rel_ref_school_school_payroll" , on_delete=models.CASCADE )

    ref_school_teacher = models.ForeignKey( TeacherUserProfile , related_name="rel_ref_school_service_payroll" , on_delete=models.DO_NOTHING, null=True, blank=True )

    code = models.CharField(verbose_name='Payroll Code', max_length=32)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    payroll_date = models.DateField(
        verbose_name='Payroll Date',
    )

    receipt = models.ImageField(
        verbose_name='Payroll Receipt',
        upload_to=f'school/receipt/payroll/%Y-%m-%d/',
        blank=True,
        null=True,
    )

    Meta = BaseModelMeta( 
        attr={
            "db_table": "school_payroll",
            "unique_together": ('ref_school', 'ref_school_teacher', 'payroll_date')
        }, 
        app_name='db'
    )

    def __str__(self) -> str:
        return self.code