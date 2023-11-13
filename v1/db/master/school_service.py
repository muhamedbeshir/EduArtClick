from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school import School


character_validators = RegexValidator(
    r'^[a-zA-Z]+', 'Service name should start with characters.')


class SchoolService(BaseModel, models.Model):
    PER_WEEK = 1
    ONE_TIME = 2
    SERVICE_TYPE_CHOICES = (
        (PER_WEEK, 'Per Week'),
        (ONE_TIME, 'One Time')
    )

    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_service", on_delete=models.CASCADE)
    service_type = models.IntegerField(choices=SERVICE_TYPE_CHOICES)
    service_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    Meta = BaseModelMeta(attr={"db_table": "school_service", "unique_together": (
        "ref_school", "service_type", "service_name")}, app_name='db')

    def __str__(self):
        return '%s' % self.service_name

    @property
    def service_type_title(self):
        res = ""
        for service_type in self.SERVICE_TYPE_CHOICES:
            if service_type[0] == self.service_type:
                res = service_type[1]
        return res
