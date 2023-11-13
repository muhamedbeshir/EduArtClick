from django.db import models

from v1.base.models.model import BaseModel, BaseModelMeta
from v1.db.master.school import School
from django.utils.html import format_html

from v1.db.master.school_course import SchoolCourse
from v1.db.master.school_service import SchoolService
from v1.db.user.profile import TeacherUserProfile


class SchoolExpense(BaseModel, models.Model):

    EXPENSE_INTERNAL = 'Internal'
    EXPENSE_EXTERNAL = 'External'
    EXPENSES_CHOICES = (
        (EXPENSE_INTERNAL, EXPENSE_INTERNAL),
        (EXPENSE_EXTERNAL, EXPENSE_EXTERNAL),
    )

    INTERNAL_EXPENSES_ACCOMMODATION = 'Select'
    INTERNAL_EXPENSES_COURSE = 'Course'
    INTERNAL_EXPENSES_SERVICE = 'Service'
    # INTERNAL_EXPENSES_TEACHER = 'Teacher'
    INTERNAL_EXPENSES_OTHER = 'Other'

    INTERNAL_EXPENSES_CHOICES = (
        (INTERNAL_EXPENSES_ACCOMMODATION, INTERNAL_EXPENSES_ACCOMMODATION),
        (INTERNAL_EXPENSES_COURSE, INTERNAL_EXPENSES_COURSE),
        (INTERNAL_EXPENSES_SERVICE, INTERNAL_EXPENSES_SERVICE),
        # (INTERNAL_EXPENSES_TEACHER, INTERNAL_EXPENSES_TEACHER),
        (INTERNAL_EXPENSES_OTHER, INTERNAL_EXPENSES_OTHER),
    )

    ref_school = models.ForeignKey( School , related_name="rel_ref_school_school_expense" , on_delete=models.CASCADE )
    expense_type = models.CharField(max_length=20, choices=EXPENSES_CHOICES, default=EXPENSE_INTERNAL)
    internal_expense_type = models.CharField(max_length=50, choices=INTERNAL_EXPENSES_CHOICES, default=INTERNAL_EXPENSES_OTHER, null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Name', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    expense_date = models.DateField(
        verbose_name='Expense Date',
    )

    receipt = models.ImageField(
        verbose_name='Expenses Receipt',
        upload_to=f'school/receipt/%Y-%m-%d/',
        blank=True,
        null=True,
    )

    ref_school_course = models.ForeignKey( SchoolCourse , related_name="rel_ref_school_course_expense" , on_delete=models.DO_NOTHING, null=True, blank=True )
    ref_school_service = models.ForeignKey( SchoolService , related_name="rel_ref_school_service_expense" , on_delete=models.DO_NOTHING, null=True, blank=True )
    # ref_school_teacher = models.ForeignKey( TeacherUserProfile , related_name="rel_ref_school_service_expense" , on_delete=models.DO_NOTHING, null=True, blank=True )

    Meta = BaseModelMeta( 
        attr={
            "db_table": "school_expense",
            # "unique_together": ('ref_school', 'name', 'expense_type', 'expense_date',)
        }, 
        app_name='db'
    )

    def __str__(self) -> str:
        return str(self.name).title()