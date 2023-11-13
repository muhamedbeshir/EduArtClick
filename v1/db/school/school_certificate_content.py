import imp
from django.db import models

from v1.base.models import BaseModel, BaseModelMeta
from v1.db.master.school import School
from v1.db.master.school_class import SchoolClass
from ..master import SchoolCourse

from v1.base.configs import cRequest
from django.core.validators import RegexValidator


character_validators = RegexValidator(
    r'^[a-zA-Z]+', 'Should start with characters.')


class SchoolCertificateContent(BaseModel, models.Model):
    ref_course = models.ForeignKey(
        SchoolClass, related_name="rel_school_course_school_certificate", on_delete=models.CASCADE)

    code = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)

    Meta = BaseModelMeta(
        attr={"db_table": "school_certificate_content"}, app_name='db')

    def __str__(self):
        return '%s' % self.code
