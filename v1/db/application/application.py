from django.db import models

import os
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta
from v1.db.school.school_course_discount import SchoolCourseDiscount
from v1.db.school.school_sponsor import SchoolSponsor
from ..organization import Organization
from ..master import School, Nationality
from ..user import TeacherUserProfile

import re

import datetime

from google_currency import convert
import ast


def increment_application_code():
    last_application = Application.objects.all().order_by('id').last()
    print(last_application)
    if not last_application:
        return 'APP-0001'

    return 'APP-' + str(int(re.sub('\D', '', last_application.ap_code)) + 1).zfill(4)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'Unsupported file extension. Only pdf file support.')


def current_year():
    return datetime.date.today().year


class Application(BaseModel, models.Model):

    PENDING = 0
    ACCEPTED = 1
    RENEW = 2
    REJECTED = 3

    APPLICATION_STATUS = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (RENEW, 'Renew'),
        (REJECTED, 'Rejected'),
    )

    PAYMENT_PENDING = 0
    PAYMENT_DONE = 1
    PAYMENT_INSTALLMENT = 2

    APPLICATION_PAYMENT_STATUS = (
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_DONE, 'Done'),
        (PAYMENT_INSTALLMENT, 'Installment'),
    )

    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    ap_country = models.CharField(max_length=200)
    ap_city = models.CharField(max_length=200)
    ap_school = models.CharField(max_length=500)
    ap_school_email = models.EmailField(max_length=300, blank=True, null=True)
    ap_course_name = models.CharField(max_length=500)
    ap_course_class = models.PositiveSmallIntegerField(blank=True, null=True)
    ap_study_period = models.IntegerField()
    ap_start_date = models.DateField()
    ap_end_date = models.DateField()

    ap_currency = models.CharField(max_length=10)
    ref_ap_coupon = models.ForeignKey(SchoolCourseDiscount, on_delete=models.DO_NOTHING,
                                      related_name="rel_ref_ap_coupon_application", null=True, blank=True)
    ap_course_discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    ap_course_price_total = models.DecimalField(
        max_digits=10, decimal_places=2)
    ap_sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    ap_grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    ap_first_name = models.CharField(max_length=100)
    ap_last_name = models.CharField(max_length=100)
    ap_gender = models.IntegerField(choices=GENDER_CHOICES)
    ap_date_of_birth = models.DateField()
    home_address = models.TextField(blank=True, null=True)
    post_code = models.CharField(max_length=50, blank=True)
    ref_ap_nationality = models.ForeignKey(
        Nationality, related_name="rel_ref_nationality", on_delete=models.DO_NOTHING, blank=True)
    ap_email = models.EmailField(max_length=300)
    ap_phone = models.CharField(max_length=20, blank=True)
    first_language = models.CharField(max_length=50, blank=True)
    ap_religion = models.CharField(max_length=50, blank=True, null=True)
    ap_passport_number = models.CharField(
        max_length=100, blank=True, null=True)
    ap_passport_expiry_date = models.DateField(blank=True, null=True)

    ap_json_data = models.TextField(blank=True, null=True)
    html_invoice = models.TextField(blank=True, null=True)
    ap_service_json_data = models.TextField(blank=True, null=True)

    ap_status = models.IntegerField(choices=APPLICATION_STATUS, default=0)
    ap_payment_status = models.IntegerField(
        choices=APPLICATION_PAYMENT_STATUS, default=0)
    ap_code = models.CharField(
        max_length=500, default=increment_application_code, null=True, blank=True)
    year = models.IntegerField(default=current_year, blank=True, null=True)

    user = models.ForeignKey(
        User, related_name="user_application", on_delete=models.DO_NOTHING, blank=True)
    ref_organization = models.ForeignKey(
        Organization, related_name="rel_ref_organization_application", on_delete=models.DO_NOTHING, blank=True, null=True)
    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_application", on_delete=models.DO_NOTHING, blank=True, null=True)
    ref_sponsor = models.ForeignKey(
        SchoolSponsor, on_delete=models.CASCADE, null=True, blank=True
    )

    document_file = models.FileField(
        upload_to="documents/%Y/%m/%d", validators=[validate_file_extension])
    sponsor_document_file = models.FileField(
        upload_to="sponsor/documents/%Y/%m/%d", validators=[validate_file_extension], null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    ap_level = models.CharField(max_length=200)

    payment_in_installment = models.BooleanField(
        verbose_name='Payment In Installment',
        default=False
    )

    installment_sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)

    installments = models.JSONField(default=list, null=True, blank=True)

    Meta = BaseModelMeta(attr={"db_table": "application"}, app_name='db')

    ap_approved_file = models.FileField(
        upload_to="application/approved/%Y-%m-%d", validators=[validate_file_extension])
    ap_reject_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.ap_code

    @property
    def ap_status_title(self):
        res = ""
        for ap_status in self.APPLICATION_STATUS:
            if ap_status[0] == self.ap_status:
                res = ap_status[1]
        return res

    @property
    def ap_payment_status_title(self):
        res = ""
        for ap_payment_status in self.APPLICATION_PAYMENT_STATUS:
            if ap_payment_status[0] == self.ap_payment_status:
                res = ap_payment_status[1]
        return res

    @property
    def ap_gender_title(self):
        res = ""
        for ap_gender in self.GENDER_CHOICES:
            if ap_gender[0] == self.ap_gender:
                res = ap_gender[1]
        return res

    '''@property
	def convert_currency(self):
		cr = self.ap_currency
		print(cr)
		amount = self.ap_grand_total
		print(amount)
		print(type(convert("gbp", 'SAR', float(amount))))

		return convert("gbp", 'SAR', float(amount)) '''


class ApplicationService(BaseModel, models.Model):
    ref_application = models.ForeignKey(
        Application, related_name="rel_ref_application_application_service", on_delete=models.CASCADE)
    ap_service_name = models.CharField(max_length=500, blank=True, null=True)
    ap_service_type = models.CharField(max_length=500, blank=True, null=True)
    ap_service_price_total = models.FloatField(
        max_length=500, blank=True, null=True)
    Meta = BaseModelMeta(
        attr={"db_table": "application_service"}, app_name='db')


class ApplicationToken(BaseModel, models.Model):
    ref_application = models.ForeignKey(
        Application, related_name="ref_application_token", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)

    Meta = BaseModelMeta(
        attr={"db_table": "application_token"}, app_name='db')
