# ref_application = models.ForeignKey(
#         Application, related_name="ref_application_token", on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import User
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.master.school_accommodation_service import SchoolAccommodationService
from v1.db.master.school_service import SchoolService
from v1.db.user.profile import SchoolStudentUserProfile
from v1.db.user.student_profile_has_accommodation import StudentProfileHasAccommodation
from v1.db.user.student_profile_has_service import StudentProfileHasService
from ..application import Application


class Transaction(BaseModel, models.Model):

    FAILED = 0
    SUCCESS = 1
    PAYMENT_STATUS = (
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    )

    payment_id = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=PAYMENT_STATUS, default=FAILED)
    currency = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(max_length=200)
    application = models.ForeignKey(
        Application, related_name="application_transaction", on_delete=models.DO_NOTHING, null=True)
    ref_school_service = models.ForeignKey(
        StudentProfileHasService, related_name="school_service_transaction", on_delete=models.DO_NOTHING, null=True)
    ref_school_accommodation_service = models.ForeignKey(
        StudentProfileHasAccommodation, related_name="school_accommodation_service_transaction", on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(
        User, related_name="user_transaction", on_delete=models.DO_NOTHING, null=True)

    Meta = BaseModelMeta(attr={"db_table": "transaction"}, app_name='db')

    def __str__(self) -> str:
        return self.payment_id

    @property
    def payment_status_title(self):
        res = ""
        for status in self.PAYMENT_STATUS:
            if status[0] == self.status:
                res = status[1]
        return res
