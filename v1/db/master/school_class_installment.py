from django.db import models

from v1.base.models import BaseModel
from v1.db.master.school_class import SchoolClass


class SchoolClassInstallment(BaseModel, models.Model):

    PER_WEEK = 'Per Week'
    PER_MONTH = 'Per Month'
    THREE_TIMES = 'Three Times'

    INSTALLMENT_TYPE_CHOICES = (
        (PER_WEEK, PER_WEEK),
        (PER_MONTH, PER_MONTH),
        (THREE_TIMES, THREE_TIMES)
    )

    ref_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        verbose_name='Installment Type',
        max_length=11,
        choices=INSTALLMENT_TYPE_CHOICES,
        default=PER_WEEK
    )

    charges = models.DecimalField(
        verbose_name='Extra Chargers',
        max_digits=5,
        decimal_places=2,
        default=0.0,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "nqraa_school_class_installment"
        unique_together = ('ref_class', 'type',)

    def __str__(self):
        return f'{self.charges}'

    @property
    def type_str(self):
        return self.type.lower().replace(' ', '_')


class SchoolClassInstallmentDetails(BaseModel, models.Model):

    ref_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )

    installment = models.CharField(
        max_length=50,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField(
        auto_now_add=False
    )

    class Meta:
        db_table = "nqraa_school_class_installment_details"
        unique_together = ('ref_class', 'installment', 'payment_date')

    def __str__(self):
        return self.installment
