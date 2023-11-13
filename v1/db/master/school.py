from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from ..organization import Organization
from .city import City, Country
from ..other import Currency


class School(BaseModel, models.Model):
    ref_organization = models.ForeignKey(Organization, blank=True, null=True,
                                         related_name="rel_ref_organization_organization", on_delete=models.CASCADE)
    school_name = models.CharField(max_length=200)
    ref_country = models.ForeignKey(
        Country, blank=True, null=True, related_name="rel_ref_country_school", on_delete=models.CASCADE)
    ref_city = models.ForeignKey(
        City, blank=True, null=True, related_name="city_info", on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True, null=True)
    ref_currency = models.ForeignKey(
        Currency, blank=True, null=True, related_name="rel_ref_currency_school", on_delete=models.DO_NOTHING)
    postal_code = models.CharField(
        verbose_name='Postal Code', max_length=6, blank=True, null=True)
    address = models.TextField(
        max_length=255, verbose_name='Address', blank=True, null=True)

    Meta = BaseModelMeta(attr={"db_table": "school"}, app_name='db')

    def __str__(self):
        return '%s' % self.school_name

    @property
    def school_address(self):
        return f'{self.address}, {self.ref_city} - {self.postal_code}, {self.ref_country}, '


class DynamicSchoolApplicationFormField(BaseModel, models.Model):
    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_school_application_form", on_delete=models.CASCADE)
    label = models.CharField(max_length=250)
    name = models.CharField(max_length=250, unique=True)
    type = models.CharField(max_length=10, default="text")
    attributes = jsonfield.JSONField(null=True, blank=True)

    Meta = BaseModelMeta(
        attr={"db_table": "dynamic_school_application_form_field"}, app_name='db')
