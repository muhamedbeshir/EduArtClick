from django.db import models
import jsonfield

from django.utils import timezone

from django.utils.text import slugify

from django.contrib.auth.models import User

from v1.base import configs
from v1.base.models import BaseModel, BaseModelMeta

from .school import School
from .school_accommodation_type import SchoolAccommodationType
from .school_accommodation_owner import SchoolAccommodationOwner
from django.core.validators import RegexValidator


character_validators = RegexValidator(
    r'^[a-zA-Z]+', 'Should start with characters.')


class SchoolAccommodationService(BaseModel, models.Model):

    SINGLE_ROOM = 0
    DOUBLE_ROOM = 1

    ROOM_TYPE = (
        (SINGLE_ROOM, 'Single Room'),
        (DOUBLE_ROOM, 'Double Room')
    )

    ref_school = models.ForeignKey(
        School, related_name="rel_ref_school_accommodation_service", on_delete=models.CASCADE)
    accommodation_title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,)
    code = models.IntegerField()
    room_type = models.IntegerField(choices=ROOM_TYPE, default=0)
    # address = models.TextField(blank=True, null=True)
    # city = models.CharField(max_length=100, blank=True, null=True)
    # country = models.CharField(max_length=100, blank=True, null=True)
    # postal_code = models.CharField(max_length=50, blank=True, null=True)
    # distance_from_school = models.CharField(max_length=50, blank=True, null=True)
    # latitude = models.DecimalField(max_digits=20, decimal_places=16,blank=True , null=True)
    # longitude = models.DecimalField(max_digits=20, decimal_places=16,blank=True , null=True)
    notes = models.TextField(blank=True, null=True)
    # room_no = models.CharField(max_length=50, blank=True, null=True)
    ref_accommodation_owner = models.ForeignKey(
        SchoolAccommodationOwner, related_name="rel_ref_accommodation_type_school_accommodation_owner", on_delete=models.CASCADE, blank=True, null=True)

    Meta = BaseModelMeta(
        attr={"db_table": "school_accommodation_service"}, app_name='db')

    def __str__(self):
        return '%s' % self.accommodation_title

    @property
    def room_type_str(self):
        if self.room_type == 0:
            return 'Single Room'
        elif self.room_type == 1:
            return 'Double Room'
